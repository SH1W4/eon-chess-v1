#!/usr/bin/env python3
"""
🌐 Chess Effects API - API Python para Integração com Frontend
Interface REST para o motor de efeitos visuais avançados

Funcionalidades:
- API REST para análise de posições
- Geração de efeitos visuais sob demanda
- Streaming de animações em tempo real
- Integração com base de dados Pro
- Cache inteligente de efeitos

@author AEON CHESS Team
@version 1.0.0
@date Janeiro 2025
"""

from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import json
import time
import threading
from pathlib import Path
import base64
import io
from typing import Dict, List, Any, Optional
import logging
import asyncio
import queue

# Importar nosso motor de efeitos
from chess_visual_effects_engine import ChessEffectsEngine, ChessPattern

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permitir CORS para integração com frontend

class ChessEffectsAPI:
    """API para integração do motor de efeitos visuais"""
    
    def __init__(self):
        self.effects_engine = ChessEffectsEngine()
        self.effects_cache = {}  # Cache de efeitos gerados
        self.animation_queue = queue.Queue()  # Fila de animações
        self.is_processing = False
        
        # Iniciar worker de processamento
        self.start_processing_worker()
    
    def start_processing_worker(self):
        """Iniciar worker para processar animações em background"""
        def worker():
            while True:
                try:
                    if not self.animation_queue.empty():
                        task = self.animation_queue.get()
                        self.process_animation_task(task)
                        self.animation_queue.task_done()
                    else:
                        time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Erro no worker de processamento: {e}")
                    time.sleep(1)
        
        worker_thread = threading.Thread(target=worker, daemon=True)
        worker_thread.start()
    
    def process_animation_task(self, task: Dict[str, Any]):
        """Processar tarefa de animação"""
        try:
            fen = task['fen']
            effect_type = task.get('effect_type', 'auto')
            callback_url = task.get('callback_url')
            
            logger.info(f"Processando animação para FEN: {fen[:50]}...")
            
            # Analisar posição
            patterns = self.effects_engine.analyze_position(fen)
            
            if patterns:
                # Gerar efeitos visuais
                frames = self.effects_engine.generate_visual_effects(patterns)
                
                # Salvar frames
                output_path = f"output/effects_{int(time.time())}"
                self.effects_engine.save_animation_frames(frames, output_path)
                
                # Armazenar no cache
                cache_key = f"{fen}_{effect_type}"
                self.effects_cache[cache_key] = {
                    'frames_path': output_path,
                    'frame_count': len(frames),
                    'patterns': [p.__dict__ for p in patterns],
                    'timestamp': time.time()
                }
                
                logger.info(f"Animação gerada: {len(frames)} frames salvos em {output_path}")
                
                # Notificar frontend se callback fornecido
                if callback_url:
                    self.notify_frontend(callback_url, cache_key)
            else:
                logger.info("Nenhum padrão tático encontrado")
                
        except Exception as e:
            logger.error(f"Erro ao processar animação: {e}")
    
    def notify_frontend(self, callback_url: str, cache_key: str):
        """Notificar frontend sobre conclusão da animação"""
        try:
            # Aqui você implementaria a notificação real
            # Por exemplo, WebSocket, Server-Sent Events, ou HTTP callback
            logger.info(f"Notificando frontend em {callback_url} sobre {cache_key}")
        except Exception as e:
            logger.error(f"Erro ao notificar frontend: {e}")

# Instanciar API
api = ChessEffectsAPI()

@app.route('/health', methods=['GET'])
def health_check():
    """Verificar saúde da API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '2.0.0',
        'engine_status': api.effects_engine.get_animation_status()
    })

@app.route('/analyze', methods=['POST'])
def analyze_position():
    """Analisar posição de xadrez e identificar padrões"""
    try:
        data = request.get_json()
        fen = data.get('fen')
        
        if not fen:
            return jsonify({'error': 'FEN não fornecido'}), 400
        
        logger.info(f"Analisando posição: {fen[:50]}...")
        
        # Analisar posição
        patterns = api.effects_engine.analyze_position(fen)
        
        # Converter para formato JSON
        patterns_data = []
        for pattern in patterns:
            pattern_dict = pattern.__dict__.copy()
            # Converter coordenadas para formato legível
            pattern_dict['squares'] = [
                {'file': chr(97 + sq[0]), 'rank': sq[1] + 1} 
                for sq in pattern.squares
            ]
            patterns_data.append(pattern_dict)
        
        return jsonify({
            'fen': fen,
            'patterns': patterns_data,
            'pattern_count': len(patterns),
            'analysis_timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/effects/generate', methods=['POST'])
def generate_effects():
    """Gerar efeitos visuais para uma posição"""
    try:
        data = request.get_json()
        fen = data.get('fen')
        effect_type = data.get('effect_type', 'auto')
        callback_url = data.get('callback_url')
        
        if not fen:
            return jsonify({'error': 'FEN não fornecido'}), 400
        
        # Verificar cache primeiro
        cache_key = f"{fen}_{effect_type}"
        if cache_key in api.effects_cache:
            cached = api.effects_cache[cache_key]
            if time.time() - cached['timestamp'] < 3600:  # Cache válido por 1 hora
                return jsonify({
                    'status': 'cached',
                    'cache_key': cache_key,
                    'frames_path': cached['frames_path'],
                    'frame_count': cached['frame_count'],
                    'patterns': cached['patterns']
                })
        
        # Adicionar à fila de processamento
        task = {
            'fen': fen,
            'effect_type': effect_type,
            'callback_url': callback_url,
            'timestamp': time.time()
        }
        
        api.animation_queue.put(task)
        
        return jsonify({
            'status': 'queued',
            'task_id': f"task_{int(time.time())}",
            'estimated_time': '5-15 segundos',
            'message': 'Efeitos sendo gerados em background'
        })
        
    except Exception as e:
        logger.error(f"Erro na geração de efeitos: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/effects/status/<task_id>', methods=['GET'])
def get_effects_status(task_id: str):
    """Verificar status da geração de efeitos"""
    try:
        # Aqui você implementaria verificação real do status
        # Por enquanto, retornamos status genérico
        
        return jsonify({
            'task_id': task_id,
            'status': 'processing',
            'progress': '75%',
            'estimated_completion': time.time() + 30
        })
        
    except Exception as e:
        logger.error(f"Erro ao verificar status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/effects/frames/<cache_key>', methods=['GET'])
def get_effects_frames(cache_key: str):
    """Obter frames de efeitos visuais"""
    try:
        if cache_key not in api.effects_cache:
            return jsonify({'error': 'Cache key não encontrada'}), 404
        
        cached = api.effects_cache[cache_key]
        frames_path = cached['frames_path']
        
        # Listar frames disponíveis
        frames_dir = Path(frames_path)
        if not frames_dir.exists():
            return jsonify({'error': 'Diretório de frames não encontrado'}), 404
        
        frames = list(frames_dir.glob('frame_*.png'))
        frames.sort()
        
        return jsonify({
            'cache_key': cache_key,
            'frames_path': frames_path,
            'frame_count': len(frames),
            'frames': [f.name for f in frames],
            'patterns': cached['patterns']
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter frames: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/effects/frame/<cache_key>/<frame_name>', methods=['GET'])
def get_single_frame(cache_key: str, frame_name: str):
    """Obter frame individual"""
    try:
        if cache_key not in api.effects_cache:
            return jsonify({'error': 'Cache key não encontrada'}), 404
        
        cached = api.effects_cache[cache_key]
        frames_path = cached['frames_path']
        
        frame_path = Path(frames_path) / frame_name
        if not frame_path.exists():
            return jsonify({'error': 'Frame não encontrado'}), 404
        
        return send_file(frame_path, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Erro ao obter frame: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/effects/stream/<cache_key>', methods=['GET'])
def stream_effects(cache_key: str):
    """Stream de efeitos visuais em tempo real"""
    try:
        if cache_key not in api.effects_cache:
            return jsonify({'error': 'Cache key não encontrada'}), 404
        
        cached = api.effects_cache[cache_key]
        frames_path = cached['frames_path']
        
        def generate_frames():
            frames_dir = Path(frames_path)
            frames = list(frames_dir.glob('frame_*.png'))
            frames.sort()
            
            for frame_path in frames:
                with open(frame_path, 'rb') as f:
                    frame_data = f.read()
                
                # Enviar frame como base64
                frame_b64 = base64.b64encode(frame_data).decode('utf-8')
                
                yield f"data: {json.dumps({'frame': frame_b64, 'frame_name': frame_path.name})}\n\n"
                time.sleep(0.1)  # 10 FPS
        
        return Response(generate_frames(), mimetype='text/event-stream')
        
    except Exception as e:
        logger.error(f"Erro no stream: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/patterns/database', methods=['GET'])
def get_patterns_database():
    """Obter banco de dados de padrões táticos"""
    try:
        patterns_db = api.effects_engine.analyzer.pattern_database
        
        return jsonify({
            'patterns': patterns_db,
            'total_patterns': len(patterns_db),
            'last_updated': time.time()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter banco de padrões: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Limpar cache de efeitos"""
    try:
        old_size = len(api.effects_cache)
        api.effects_cache.clear()
        
        return jsonify({
            'status': 'success',
            'message': f'Cache limpo: {old_size} entradas removidas',
            'cache_size': 0
        })
        
    except Exception as e:
        logger.error(f"Erro ao limpar cache: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/cache/status', methods=['GET'])
def get_cache_status():
    """Obter status do cache"""
    try:
        cache_size = len(api.effects_cache)
        cache_keys = list(api.effects_cache.keys())
        
        return jsonify({
            'cache_size': cache_size,
            'cache_keys': cache_keys,
            'oldest_entry': min([v['timestamp'] for v in api.effects_cache.values()]) if cache_size > 0 else None,
            'newest_entry': max([v['timestamp'] for v in api.effects_cache.values()]) if cache_size > 0 else None
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter status do cache: {e}")
        return jsonify({'error': str(e)}), 500

# Rotas de demonstração
@app.route('/demo/position', methods=['GET'])
def demo_position():
    """Posição de demonstração"""
    demo_fen = "rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 0 1"
    
    return jsonify({
        'fen': demo_fen,
        'description': 'Posição de demonstração - Abertura Italiana',
        'analysis_url': f'/analyze',
        'effects_url': f'/effects/generate'
    })

@app.route('/demo/effects', methods=['GET'])
def demo_effects():
    """Demonstrar geração de efeitos"""
    demo_fen = "rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 0 1"
    
    # Gerar efeitos para demonstração
    api.animation_queue.put({
        'fen': demo_fen,
        'effect_type': 'demo',
        'timestamp': time.time()
    })
    
    return jsonify({
        'status': 'demo_started',
        'fen': demo_fen,
        'message': 'Efeitos de demonstração sendo gerados',
        'check_status': f'/effects/status/demo_{int(time.time())}'
    })

if __name__ == '__main__':
    print("🌐 Iniciando Chess Effects API...")
    print("📡 Servidor rodando em http://localhost:5000")
    print("🔗 Endpoints disponíveis:")
    print("  - GET  /health - Verificar saúde da API")
    print("  - POST /analyze - Analisar posição")
    print("  - POST /effects/generate - Gerar efeitos visuais")
    print("  - GET  /effects/status/<id> - Verificar status")
    print("  - GET  /effects/frames/<key> - Listar frames")
    print("  - GET  /effects/frame/<key>/<name> - Obter frame")
    print("  - GET  /effects/stream/<key> - Stream de frames")
    print("  - GET  /patterns/database - Banco de padrões")
    print("  - POST /cache/clear - Limpar cache")
    print("  - GET  /cache/status - Status do cache")
    print("  - GET  /demo/position - Posição de demonstração")
    print("  - GET  /demo/effects - Demonstrar efeitos")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
