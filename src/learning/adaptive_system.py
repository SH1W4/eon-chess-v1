"""
Sistema de aprendizado adaptativo para análise de xadrez.
Integra conceitos ARQUIMAX para evolução contínua.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import chess
import chess.engine
import json
import logging
from pathlib import Path

@dataclass
class PositionFeatures:
    """Características extraídas de uma posição."""
    material_balance: float
    piece_activity: float
    king_safety: float
    pawn_structure: float
    center_control: float
    space_advantage: float
    development: float
    initiative: float

@dataclass
class AdaptiveMetrics:
    """Métricas do sistema adaptativo."""
    accuracy: float
    learning_rate: float
    pattern_recognition: float
    adaptation_speed: float
    prediction_confidence: float

class AdaptiveAnalyzer:
    """Analisador adaptativo de xadrez."""
    
    def __init__(self,
                 model_path: Optional[str] = None,
                 stockfish_path: Optional[str] = None,
                 learning_rate: float = 0.01,
                 adaptation_threshold: float = 0.7):
        """
        Inicializa analisador adaptativo.
        
        Args:
            model_path: Caminho para modelo salvo
            stockfish_path: Caminho para Stockfish
            learning_rate: Taxa de aprendizado
            adaptation_threshold: Limiar para adaptação
        """
        self.learning_rate = learning_rate
        self.adaptation_threshold = adaptation_threshold
        self.metrics = AdaptiveMetrics(
            accuracy=0.0,
            learning_rate=learning_rate,
            pattern_recognition=0.0,
            adaptation_speed=0.0,
            prediction_confidence=0.0
        )
        
        # Inicializa modelos
        self.position_model = RandomForestRegressor(n_estimators=100)
        self.pattern_model = RandomForestRegressor(n_estimators=100)
        self.scaler = StandardScaler()
        
        # Inicializa com dados dummy
        dummy_data = np.random.rand(10, 8)  # 8 features
        dummy_scores = np.random.rand(10)  # scores aleatórios
        dummy_patterns = np.random.randint(0, 2, size=(10, 10))  # padrões binários
        
        # Fit inicial dos modelos
        self.scaler.fit(dummy_data)
        self.position_model.fit(dummy_data, dummy_scores)
        self.pattern_model.fit(dummy_data, dummy_patterns.argmax(axis=1))
        
        # Carrega modelo se existir
        if model_path and Path(model_path).exists():
            self._load_model(model_path)
        
        # Inicializa engine
        self.engine = None
        if stockfish_path:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        
        # Cache de posições
        self.position_cache = {}
        
        # Configuração ARQUIMAX
        self.arquimax_config = self._init_arquimax()
    
    def _init_arquimax(self) -> Dict:
        """Inicializa configuração ARQUIMAX."""
        return {
            'capabilities': {
                'pattern_recognition': True,
                'adaptive_learning': True,
                'real_time_analysis': True,
                'strategic_planning': True
            },
            'monitoring': {
                'accuracy_threshold': 0.8,
                'adaptation_rate': 0.1,
                'confidence_minimum': 0.7,
                'pattern_sensitivity': 0.6
            },
            'task_management': {
                'async_execution': True,
                'cache_enabled': True,
                'metrics_collection': True
            }
        }
    
    def analyze_position(self, board: chess.Board) -> Dict:
        """
        Analisa posição com aprendizado adaptativo.
        
        Args:
            board: Posição atual
        
        Returns:
            Análise detalhada
        """
        # Extrai features
        features = self._extract_features(board)
        
        # Verifica cache
        fen = board.fen()
        if fen in self.position_cache:
            cached = self.position_cache[fen]
            self._update_metrics('cache_hit')
            return cached
        
        # Análise básica
        basic_analysis = self._get_basic_analysis(board) if hasattr(self, '_get_basic_analysis') else {}
        
        # Previsão do modelo
        position_score = self._predict_position_score(features)
        patterns = self._identify_patterns(features)
        
        # Integra resultados
        analysis = {
            'score': position_score,
            'features': features.__dict__,
            'patterns': patterns,
            'basic_analysis': basic_analysis,
            'confidence': self.metrics.prediction_confidence
        }
        
        # Atualiza cache
        self.position_cache[fen] = analysis
        
        # Adapta modelo
        if self.engine:
            true_score = self._get_engine_score(board)
            self._adapt_model(features, true_score)
        
        return analysis
    
    def _extract_features(self, board: chess.Board) -> PositionFeatures:
        """Extrai características da posição."""
        return PositionFeatures(
            material_balance=self._calculate_material(board),
            piece_activity=self._calculate_activity(board),
            king_safety=self._calculate_king_safety(board),
            pawn_structure=self._calculate_pawn_structure(board),
            center_control=self._calculate_center_control(board),
            space_advantage=self._calculate_space(board),
            development=self._calculate_development(board),
            initiative=self._calculate_initiative(board)
        )
    
    def _predict_position_score(self, features: PositionFeatures) -> float:
        """Faz previsão da avaliação da posição."""
        feature_vector = np.array([list(features.__dict__.values())])
        feature_vector = self.scaler.transform(feature_vector)
        
        prediction = self.position_model.predict(feature_vector)[0]
        confidence = self._calculate_confidence(prediction)
        
        self.metrics.prediction_confidence = confidence
        return prediction
    
    def _identify_patterns(self, features: PositionFeatures) -> List[str]:
        """Identifica padrões estratégicos."""
        feature_vector = np.array([list(features.__dict__.values())])
        feature_vector = self.scaler.transform(feature_vector)
        
        # Previsão de padrões
        pattern_prediction = int(self.pattern_model.predict(feature_vector)[0])
        
        # Converte para lista de padrões
        patterns = [self._get_pattern_name(pattern_prediction)]
        
        return patterns
    
    def _adapt_model(self, features: PositionFeatures, true_score: float):
        """Adapta modelo com novo exemplo."""
        if self.metrics.prediction_confidence < self.adaptation_threshold:
            feature_vector = np.array([list(features.__dict__.values())])
            
            # Atualiza modelo de posição
            self.position_model.fit(
                feature_vector,
                np.array([true_score])
            )
            
            # Atualiza métricas
            self._update_metrics('model_adapted')
    
    def _calculate_confidence(self, prediction: float) -> float:
        """Calcula confiança da previsão."""
        # Implementar cálculo de confiança
        return 0.8
    
    def _get_engine_score(self, board: chess.Board) -> float:
        """Obtém avaliação da engine."""
        if not self.engine:
            return 0.0
        
        result = self.engine.analyse(
            board,
            chess.engine.Limit(time=0.1)
        )
        
        return result['score'].relative.score() / 100.0
    
    def _update_metrics(self, event: str):
        """Atualiza métricas do sistema."""
        if event == 'cache_hit':
            self.metrics.adaptation_speed += 0.1
        elif event == 'model_adapted':
            self.metrics.learning_rate *= 0.99
            self.metrics.pattern_recognition += 0.05
    
    def get_metrics(self) -> AdaptiveMetrics:
        """Retorna métricas atuais."""
        return self.metrics
    
    def save_model(self, path: str):
        """Salva modelo treinado."""
        model_data = {
            'position_model': self.position_model,
            'pattern_model': self.pattern_model,
            'scaler': self.scaler,
            'metrics': self.metrics.__dict__,
            'arquimax_config': self.arquimax_config
        }
        
        with open(path, 'wb') as f:
            import pickle
            pickle.dump(model_data, f)
    
    def _load_model(self, path: str):
        """Carrega modelo salvo."""
        with open(path, 'rb') as f:
            import pickle
            model_data = pickle.load(f)
            
            self.position_model = model_data['position_model']
            self.pattern_model = model_data['pattern_model']
            self.scaler = model_data['scaler']
            self.metrics = AdaptiveMetrics(**model_data['metrics'])
            self.arquimax_config = model_data['arquimax_config']
    
    # Métodos auxiliares de cálculo
    def _calculate_material(self, board: chess.Board) -> float:
        """Calcula balanço material."""
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }
        
        score = 0
        for piece in chess.PIECE_TYPES:
            score += len(board.pieces(piece, chess.WHITE)) * values.get(piece, 0)
            score -= len(board.pieces(piece, chess.BLACK)) * values.get(piece, 0)
        
        return score
    
    def _calculate_activity(self, board: chess.Board) -> float:
        """Calcula atividade das peças."""
        activity = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                mobility = len(list(board.legal_moves))
                activity += mobility * (1 if piece.color else -1)
        return activity / 100.0
    
    def _calculate_king_safety(self, board: chess.Board) -> float:
        """Calcula segurança dos reis."""
        safety_score = 0.0
        for color in [chess.WHITE, chess.BLACK]:
            king_square = board.king(color)
            protection = len([square for square in board.attacks(king_square) if board.piece_at(square) and board.piece_at(square).color == color])
            safety_score += protection * (1 if color == chess.WHITE else -1)
        return safety_score / 10.0
    
    def _calculate_pawn_structure(self, board: chess.Board) -> float:
        """Avalia estrutura de peões."""
        structure_score = 0.0
        for color in [chess.WHITE, chess.BLACK]:
            pawns = board.pieces(chess.PAWN, color)
            doubled = len([sq for sq in pawns if board.piece_at(sq + 8) or board.piece_at(sq - 8)])
            isolated = len([sq for sq in pawns if not board.piece_at(sq + 1) and not board.piece_at(sq - 1)])
            structure_score -= doubled * 0.5 + isolated * 0.5
        return structure_score
    
    def _calculate_center_control(self, board: chess.Board) -> float:
        """Calcula controle do centro."""
        center_squares = {chess.E4, chess.D4, chess.E5, chess.D5}
        control_score = 0.0
        for square in center_squares:
            attackers = board.attackers(chess.WHITE, square)
            defenders = board.attackers(chess.BLACK, square)
            control_score += (len(attackers) - len(defenders))
        return control_score / 10.0
    
    def _calculate_space(self, board: chess.Board) -> float:
        """Calcula vantagem espacial."""
        space_score = 0.0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    space_score += 1
                else:
                    space_score -= 1
        return space_score / len(chess.SQUARES)
    
    def _calculate_development(self, board: chess.Board) -> float:
        """Calcula desenvolvimento das peças."""
        development_score = 0.0
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for color in [chess.WHITE, chess.BLACK]:
                pieces = board.pieces(piece_type, color)
                initial_rank = 1 if color == chess.WHITE else 8
                developed = sum(1 for square in pieces if chess.square_rank(square) != initial_rank)
                development_score += developed * (1 if color == chess.WHITE else -1)
        return development_score / 20.0
    
    def _calculate_initiative(self, board: chess.Board) -> float:
        """Calcula iniciativa."""
        return len(list(board.legal_moves)) / 100.0
    
    def _get_pattern_name(self, index: int) -> str:
        """Converte índice em nome de padrão."""
        patterns = [
            "fork", "pin", "discovery", "overload",
            "deflection", "interference", "x-ray",
            "zugzwang", "tempo", "prophylaxis"
        ]
        return patterns[index] if index < len(patterns) else "unknown"
