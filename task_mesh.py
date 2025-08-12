#!/usr/bin/env python3
"""
TaskMesh - Sistema de diagnóstico paralelo para debugging de xadrez
Inspirado em arquiteturas distribuídas, mas executando localmente
"""
import os
import sys
import json
import threading
import subprocess
import time
from typing import Dict, List, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import traceback

@dataclass
class Task:
    """Representa uma tarefa de diagnóstico"""
    id: str
    name: str
    command: str
    deps: List[str] = None
    priority: int = 1
    timeout: int = 30
    
    def __post_init__(self):
        if self.deps is None:
            self.deps = []

class TaskResult:
    """Resultado de uma tarefa"""
    def __init__(self, task_id: str, success: bool, output: str = "", error: str = "", duration: float = 0.0):
        self.task_id = task_id
        self.success = success
        self.output = output
        self.error = error
        self.duration = duration
        self.timestamp = time.time()

class Nexus:
    """Orquestrador central de tarefas"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.tasks: Dict[str, Task] = {}
        self.results: Dict[str, TaskResult] = {}
        self.completed = set()
        self.running = set()
        self.failed = set()
        
    def add_task(self, task: Task):
        """Adiciona uma tarefa ao pipeline"""
        self.tasks[task.id] = task
        
    def can_execute(self, task_id: str) -> bool:
        """Verifica se uma tarefa pode ser executada (deps satisfeitas)"""
        task = self.tasks.get(task_id)
        if not task:
            return False
            
        for dep in task.deps:
            if dep not in self.completed:
                return False
        return True
    
    def execute_task(self, task: Task) -> TaskResult:
        """Executa uma tarefa individual"""
        start_time = time.time()
        print(f"🚀 Executando: {task.name} [{task.id}]")
        
        try:
            # Executa o comando
            if task.command.startswith("python"):
                # Replace python with python3
                cmd = task.command.replace("python ", "python3 ", 1)
                result = subprocess.run(
                    cmd.split(), 
                    capture_output=True, 
                    text=True, 
                    timeout=task.timeout,
                    cwd=os.getcwd()
                )
            else:
                result = subprocess.run(
                    task.command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=task.timeout,
                    cwd=os.getcwd()
                )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ {task.name} - Concluído ({duration:.2f}s)")
                return TaskResult(task.id, True, result.stdout, result.stderr, duration)
            else:
                print(f"❌ {task.name} - Falhou ({duration:.2f}s)")
                return TaskResult(task.id, False, result.stdout, result.stderr, duration)
                
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"⏰ {task.name} - Timeout ({duration:.2f}s)")
            return TaskResult(task.id, False, "", f"Timeout após {task.timeout}s", duration)
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 {task.name} - Erro: {str(e)}")
            return TaskResult(task.id, False, "", str(e), duration)
    
    def execute_parallel(self) -> Dict[str, TaskResult]:
        """Executa tarefas em paralelo respeitando dependências"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            
            while len(self.completed) < len(self.tasks):
                # Encontra tarefas prontas para execução
                ready_tasks = []
                for task_id, task in self.tasks.items():
                    if (task_id not in self.completed and 
                        task_id not in self.running and 
                        task_id not in self.failed and
                        self.can_execute(task_id)):
                        ready_tasks.append(task)
                
                # Submete tarefas prontas
                for task in ready_tasks:
                    future = executor.submit(self.execute_task, task)
                    futures[future] = task.id
                    self.running.add(task.id)
                
                # Processa resultados completados
                completed_futures = []
                for future in futures:
                    if future.done():
                        completed_futures.append(future)
                
                for future in completed_futures:
                    task_id = futures[future]
                    result = future.result()
                    self.results[task_id] = result
                    self.running.remove(task_id)
                    
                    if result.success:
                        self.completed.add(task_id)
                    else:
                        self.failed.add(task_id)
                    
                    del futures[future]
                
                # Evita busy wait
                if not completed_futures and not ready_tasks:
                    time.sleep(0.1)
        
        return self.results

class Arkitect:
    """Sistema de análise e geração de correções"""
    
    def __init__(self, nexus: Nexus):
        self.nexus = nexus
        self.diagnostics = {}
        
    def analyze_results(self) -> Dict[str, Any]:
        """Analisa os resultados coletados"""
        analysis = {
            "summary": {
                "total_tasks": len(self.nexus.tasks),
                "completed": len(self.nexus.completed),
                "failed": len(self.nexus.failed)
            },
            "issues": [],
            "recommendations": []
        }
        
        # Analisa falhas
        for task_id in self.nexus.failed:
            result = self.nexus.results[task_id]
            task = self.nexus.tasks[task_id]
            
            issue = {
                "task": task.name,
                "error": result.error,
                "output": result.output
            }
            
            # Análise específica para erros conhecidos
            if "No piece at" in result.output or "Não há peça" in result.output:
                issue["type"] = "piece_not_found"
                issue["analysis"] = "Inconsistência na representação de posições no tabuleiro"
                analysis["recommendations"].append({
                    "priority": "HIGH",
                    "action": "Normalizar formato de chaves no dicionário board.pieces",
                    "details": "Converter todas as chaves para formato string algebraico consistente"
                })
            
            analysis["issues"].append(issue)
        
        return analysis
    
    def generate_fixes(self, analysis: Dict[str, Any]) -> List[str]:
        """Gera scripts de correção baseados na análise"""
        fixes = []
        
        for recommendation in analysis["recommendations"]:
            if "Normalizar formato" in recommendation["action"]:
                fix = """
# Correção para normalização de chaves
def normalize_board_keys(board):
    # Converte todas as chaves para formato string algebraico
    new_pieces = {}
    for pos, piece in board.pieces.items():
        if isinstance(pos, tuple):
            file_char = chr(ord('a') + pos[0])
            rank_char = str(pos[1] + 1)  # Ajuste se necessário
            key = file_char + rank_char
        else:
            key = str(pos)
        new_pieces[key] = piece
        piece.position = Position.from_algebraic(key)
    board.pieces = new_pieces
"""
                fixes.append(fix)
        
        return fixes

def create_diagnostic_tasks() -> List[Task]:
    """Cria tarefas de diagnóstico paralelo"""
    tasks = []
    
    # Criar scripts como arquivos temporários para evitar problemas de escaping
    
    # Tarefa 1: Instrumentação do board
    instrument_script = """
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

# Patch board.py para adicionar logs
try:
    with open('src/core/board/board.py', 'r') as f:
        content = f.read()

    # Adiciona logs na função move_piece
    if 'DEBUG_LOG_MOVE_PIECE' not in content:
        patched = content.replace(
            'def move_piece(self, from_pos, to_pos):',
            '''def move_piece(self, from_pos, to_pos):
        print(f"DEBUG_LOG_MOVE_PIECE: from_pos={from_pos} (type={type(from_pos)}), to_pos={to_pos} (type={type(to_pos)})")
        print(f"DEBUG_LOG_PIECES_KEYS: {list(self.pieces.keys())[:10]}...")
        
        # Tenta diferentes formatos de chave
        piece_found = None
        key_used = None
        for key_format in [from_pos, str(from_pos), tuple(from_pos) if hasattr(from_pos, '__iter__') else None]:
            if key_format and key_format in self.pieces:
                piece_found = self.pieces[key_format]
                key_used = key_format
                break
        
        print(f"DEBUG_LOG_KEY_RESOLUTION: piece_found={piece_found is not None}, key_used={key_used}")'''
        )
        
        with open('src/core/board/board.py', 'w') as f:
            f.write(patched)
        
        print("✅ Board instrumentado")
    else:
        print("⚠️ Board já instrumentado")
except Exception as e:
    print(f"❌ Erro na instrumentação: {e}")
"""
    
    with open('temp_instrument.py', 'w') as f:
        f.write(instrument_script)
    
    tasks.append(Task("instrument_board", "Instrumentar Board", "python3 temp_instrument.py"))
    
    # Tarefa 2: Teste focal h8->g8
    focal_script = """
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

try:
    from src.core.board.board import Board, Position, PieceType, Color, Piece
    from src.core.engine import ChessEngine

    print("=== TESTE FOCAL h8->g8 ===")

    # Cria um board com torre em h8
    board = Board()
    board.setup_board()

    # Verifica se há peça em h8
    h8_piece = board.get_piece("h8")
    print(f"Peça em h8: {h8_piece}")
    print(f"Tipo da peça: {type(h8_piece)}")
    if h8_piece:
        print(f"Cor: {h8_piece.color}")
        print(f"Tipo: {h8_piece.type}")

    # Verifica keys do dicionário pieces
    print(f"Total de peças: {len(board.pieces)}")
    print("Primeiras 10 chaves:")
    for i, key in enumerate(list(board.pieces.keys())[:10]):
        piece = board.pieces[key]
        print(f"  {i+1}. {key} ({type(key).__name__}) -> {piece.type.name} {piece.color.name}")

    # Tenta diferentes formatos para h8
    test_keys = ["h8", "H8", (7, 7), (7, 0)]
    try:
        test_keys.append(Position.from_algebraic("h8"))
    except:
        pass
    
    for test_key in test_keys:
        try:
            found = board.pieces.get(test_key)
            print(f"Teste key {test_key} ({type(test_key).__name__}): {found is not None}")
        except Exception as e:
            print(f"Erro testando {test_key}: {e}")

    # Tenta o movimento
    engine = ChessEngine(board)
    try:
        result = engine.make_move("h8", "g8", Color.BLACK)
        print(f"Resultado do movimento h8->g8: {result}")
    except Exception as e:
        print(f"ERRO no movimento h8->g8: {e}")
        import traceback
        traceback.print_exc()
except Exception as e:
    print(f"❌ Erro no teste focal: {e}")
    import traceback
    traceback.print_exc()
"""
    
    with open('temp_focal.py', 'w') as f:
        f.write(focal_script)
    
    tasks.append(Task("focal_test", "Teste Focal h8->g8", "python3 temp_focal.py", deps=["instrument_board"]))
    
    # Tarefa 3: Teste de integração com logs
    tasks.append(Task(
        "integration_test", 
        "Teste de Integração", 
        "python3 -m pytest tests/test_integration.py::test_complete_game_flow -v -s", 
        deps=["instrument_board"]
    ))
    
    # Tarefa 4: Análise de estrutura do board
    structure_script = """
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

try:
    from src.core.board.board import Board, Position

    print("=== ANÁLISE DE ESTRUTURA ===")

    board = Board()
    board.setup_board()

    # Analisa consistência de Position
    pos_h8 = Position.from_algebraic("h8")
    print(f"Position.from_algebraic('h8'): {pos_h8}")
    print(f"str(pos_h8): {str(pos_h8)}")
    print(f"pos_h8.file: {pos_h8.file}, pos_h8.rank: {pos_h8.rank}")

    # Verifica se __str__ e from_algebraic são inversos
    pos_test = Position.from_algebraic("a1")
    pos_str = str(pos_test)
    pos_back = Position.from_algebraic(pos_str)
    print(f"Teste roundtrip a1: {pos_test} -> {pos_str} -> {pos_back}")
    print(f"Igualdade: {pos_test.file == pos_back.file and pos_test.rank == pos_back.rank}")

    # Testa todas as casas do board inicial
    inconsistencies = []
    for pos, piece in board.pieces.items():
        try:
            pos_str = str(pos)
            pos_from_str = Position.from_algebraic(pos_str)
            if not (pos_from_str.file == piece.position.file and pos_from_str.rank == piece.position.rank):
                inconsistencies.append((pos, pos_str, piece.position))
        except Exception as e:
            inconsistencies.append((pos, f"ERROR: {e}", piece.position))

    print(f"Inconsistências encontradas: {len(inconsistencies)}")
    for inc in inconsistencies[:5]:
        print(f"  {inc}")
except Exception as e:
    print(f"❌ Erro na análise: {e}")
    import traceback
    traceback.print_exc()
"""
    
    with open('temp_structure.py', 'w') as f:
        f.write(structure_script)
    
    tasks.append(Task("structure_analysis", "Análise de Estrutura", "python3 temp_structure.py"))
    
    return tasks

def main():
    """Função principal do TaskMesh"""
    print("🔄 Iniciando TaskMesh - Sistema de Diagnóstico Paralelo")
    print("=" * 60)
    
    # Inicializa o Nexus
    nexus = Nexus(max_workers=3)
    
    # Cria e adiciona tarefas
    tasks = create_diagnostic_tasks()
    for task in tasks:
        nexus.add_task(task)
    
    print(f"📋 {len(tasks)} tarefas adicionadas ao pipeline")
    
    # Executa em paralelo
    start_time = time.time()
    results = nexus.execute_parallel()
    total_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print(f"⏱️  Execução completada em {total_time:.2f}s")
    
    # Análise com Arkitect
    arkitect = Arkitect(nexus)
    analysis = arkitect.analyze_results()
    
    print("\n📊 ANÁLISE DOS RESULTADOS:")
    print("-" * 40)
    print(f"Total de tarefas: {analysis['summary']['total_tasks']}")
    print(f"Completadas: {analysis['summary']['completed']}")
    print(f"Falharam: {analysis['summary']['failed']}")
    
    if analysis['issues']:
        print("\n🚨 PROBLEMAS IDENTIFICADOS:")
        for i, issue in enumerate(analysis['issues'], 1):
            print(f"\n{i}. {issue['task']}")
            if 'type' in issue:
                print(f"   Tipo: {issue['type']}")
            if 'analysis' in issue:
                print(f"   Análise: {issue['analysis']}")
            if issue['error']:
                print(f"   Erro: {issue['error'][:200]}...")
    
    if analysis['recommendations']:
        print("\n💡 RECOMENDAÇÕES:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"\n{i}. [{rec['priority']}] {rec['action']}")
            if 'details' in rec:
                print(f"   {rec['details']}")
    
    # Gera correções
    fixes = arkitect.generate_fixes(analysis)
    if fixes:
        print("\n🔧 CORREÇÕES SUGERIDAS:")
        for i, fix in enumerate(fixes, 1):
            print(f"\nCorreção {i}:")
            print(fix)
    
    # Salva resultados detalhados
    report = {
        "timestamp": time.time(),
        "execution_time": total_time,
        "analysis": analysis,
        "detailed_results": {
            task_id: {
                "success": result.success,
                "output": result.output,
                "error": result.error,
                "duration": result.duration
            }
            for task_id, result in results.items()
        }
    }
    
    with open("taskmesh_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Relatório detalhado salvo em: taskmesh_report.json")
    print("\n🎯 TaskMesh concluído!")
    
    # Cleanup temp files
    import os
    for temp_file in ['temp_instrument.py', 'temp_focal.py', 'temp_structure.py']:
        try:
            os.remove(temp_file)
        except:
            pass

if __name__ == "__main__":
    main()
