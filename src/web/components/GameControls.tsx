import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import './GameControls.css';

interface GameControlsProps {
  onNewGame: () => void;
  onUndo: () => void;
  onRedo: () => void;
  onPause: () => void;
  onResign: () => void;
  onOfferDraw: () => void;
  onAnalyze: () => void;
  onSettings: () => void;
  canUndo: boolean;
  canRedo: boolean;
  isPaused: boolean;
  isGameOver: boolean;
  currentPlayer: 'white' | 'black';
  timeWhite?: number;
  timeBlack?: number;
  moveCount: number;
}

interface Timer {
  minutes: number;
  seconds: number;
}

export const GameControls: React.FC<GameControlsProps> = ({
  onNewGame,
  onUndo,
  onRedo,
  onPause,
  onResign,
  onOfferDraw,
  onAnalyze,
  onSettings,
  canUndo,
  canRedo,
  isPaused,
  isGameOver,
  currentPlayer,
  timeWhite = 900, // 15 minutos em segundos
  timeBlack = 900,
  moveCount
}) => {
  const [whiteTime, setWhiteTime] = useState(timeWhite);
  const [blackTime, setBlackTime] = useState(timeBlack);
  const [showConfirmDialog, setShowConfirmDialog] = useState<string | null>(null);
  const [isAnalysisMode, setIsAnalysisMode] = useState(false);

  // Atualizar relógio
  useEffect(() => {
    if (!isPaused && !isGameOver) {
      const interval = setInterval(() => {
        if (currentPlayer === 'white') {
          setWhiteTime(prev => Math.max(0, prev - 1));
        } else {
          setBlackTime(prev => Math.max(0, prev - 1));
        }
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [currentPlayer, isPaused, isGameOver]);

  // Formatar tempo
  const formatTime = (seconds: number): Timer => {
    return {
      minutes: Math.floor(seconds / 60),
      seconds: seconds % 60
    };
  };

  // Lidar com confirmações
  const handleConfirm = (action: string) => {
    setShowConfirmDialog(action);
  };

  const executeAction = (action: string) => {
    switch (action) {
      case 'newGame':
        onNewGame();
        setWhiteTime(timeWhite);
        setBlackTime(timeBlack);
        break;
      case 'resign':
        onResign();
        break;
      case 'draw':
        onOfferDraw();
        break;
    }
    setShowConfirmDialog(null);
  };

  const toggleAnalysis = () => {
    setIsAnalysisMode(!isAnalysisMode);
    onAnalyze();
  };

  const whiteTimer = formatTime(whiteTime);
  const blackTimer = formatTime(blackTime);

  return (
    <div className="game-controls">
      {/* Relógios */}
      <div className="time-controls">
        <motion.div 
          className={`timer ${currentPlayer === 'black' ? 'active' : ''}`}
          animate={{ scale: currentPlayer === 'black' ? 1.05 : 1 }}
        >
          <div className="player-label">
            <span className="player-icon">♚</span>
            <span>Pretas</span>
          </div>
          <div className="time-display">
            {String(blackTimer.minutes).padStart(2, '0')}:
            {String(blackTimer.seconds).padStart(2, '0')}
          </div>
        </motion.div>

        <div className="move-counter">
          <div className="move-label">Movimento</div>
          <div className="move-number">{moveCount}</div>
        </div>

        <motion.div 
          className={`timer ${currentPlayer === 'white' ? 'active' : ''}`}
          animate={{ scale: currentPlayer === 'white' ? 1.05 : 1 }}
        >
          <div className="player-label">
            <span className="player-icon">♔</span>
            <span>Brancas</span>
          </div>
          <div className="time-display">
            {String(whiteTimer.minutes).padStart(2, '0')}:
            {String(whiteTimer.seconds).padStart(2, '0')}
          </div>
        </motion.div>
      </div>

      {/* Controles principais */}
      <div className="main-controls">
        <div className="control-group">
          <motion.button
            className="control-button primary"
            onClick={() => handleConfirm('newGame')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={!isGameOver && moveCount > 0}
          >
            <span className="button-icon">🔄</span>
            <span className="button-text">Novo Jogo</span>
          </motion.button>

          <motion.button
            className="control-button"
            onClick={onPause}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={isGameOver}
          >
            <span className="button-icon">{isPaused ? '▶️' : '⏸️'}</span>
            <span className="button-text">{isPaused ? 'Continuar' : 'Pausar'}</span>
          </motion.button>
        </div>

        <div className="control-group">
          <motion.button
            className="control-button"
            onClick={onUndo}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={!canUndo || isGameOver}
            title="Desfazer movimento"
          >
            <span className="button-icon">↩️</span>
          </motion.button>

          <motion.button
            className="control-button"
            onClick={onRedo}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={!canRedo || isGameOver}
            title="Refazer movimento"
          >
            <span className="button-icon">↪️</span>
          </motion.button>
        </div>

        <div className="control-group">
          <motion.button
            className="control-button danger"
            onClick={() => handleConfirm('resign')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={isGameOver}
          >
            <span className="button-icon">🏳️</span>
            <span className="button-text">Desistir</span>
          </motion.button>

          <motion.button
            className="control-button"
            onClick={() => handleConfirm('draw')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={isGameOver || moveCount < 10}
          >
            <span className="button-icon">🤝</span>
            <span className="button-text">Empate</span>
          </motion.button>
        </div>
      </div>

      {/* Controles secundários */}
      <div className="secondary-controls">
        <motion.button
          className={`control-button ${isAnalysisMode ? 'active' : ''}`}
          onClick={toggleAnalysis}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <span className="button-icon">🔍</span>
          <span className="button-text">Análise</span>
        </motion.button>

        <motion.button
          className="control-button"
          onClick={onSettings}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <span className="button-icon">⚙️</span>
          <span className="button-text">Configurações</span>
        </motion.button>
      </div>

      {/* Diálogo de confirmação */}
      {showConfirmDialog && (
        <motion.div 
          className="confirm-dialog-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setShowConfirmDialog(null)}
        >
          <motion.div 
            className="confirm-dialog"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3>
              {showConfirmDialog === 'newGame' && 'Iniciar novo jogo?'}
              {showConfirmDialog === 'resign' && 'Desistir da partida?'}
              {showConfirmDialog === 'draw' && 'Oferecer empate?'}
            </h3>
            <p>
              {showConfirmDialog === 'newGame' && 'O progresso atual será perdido.'}
              {showConfirmDialog === 'resign' && 'Você perderá a partida.'}
              {showConfirmDialog === 'draw' && 'Seu oponente pode aceitar ou recusar.'}
            </p>
            <div className="dialog-buttons">
              <button 
                className="dialog-button cancel"
                onClick={() => setShowConfirmDialog(null)}
              >
                Cancelar
              </button>
              <button 
                className="dialog-button confirm"
                onClick={() => executeAction(showConfirmDialog)}
              >
                Confirmar
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Indicador de análise */}
      {isAnalysisMode && (
        <motion.div 
          className="analysis-indicator"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
        >
          <div className="analysis-icon">🧠</div>
          <div className="analysis-text">Modo Análise Ativo</div>
        </motion.div>
      )}
    </div>
  );
};

export default GameControls;
