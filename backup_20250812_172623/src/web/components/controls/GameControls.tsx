import React from 'react';
import { CULTURAL_STYLES } from '../../../shared/constants/game';
import { theme } from '../../../shared/styles/theme';

interface GameControlsProps {
  culturalStyle: string;
  onStyleChange: (style: string) => void;
  onFlipBoard: () => void;
  onNewGame: () => void;
  onUndo: () => void;
  canUndo: boolean;
  isPlayerTurn: boolean;
}

export const GameControls: React.FC<GameControlsProps> = ({
  culturalStyle,
  onStyleChange,
  onFlipBoard,
  onNewGame,
  onUndo,
  canUndo,
  isPlayerTurn,
}) => {
  return (
    <div className="flex flex-col gap-4 p-6 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 shadow-xl">
      <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
        <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">⚙️</span>
        Controles
      </h2>
      
      {/* Estilo Cultural */}
      <div className="flex flex-col gap-2">
        <label className="text-emerald-100 text-sm">Estilo Cultural</label>
        <select
          data-testid="style-select"
          value={culturalStyle}
          onChange={(e) => onStyleChange(e.target.value)}
          className="
            w-full bg-emerald-700/50 text-white 
            border border-emerald-600/50 rounded-lg 
            px-4 py-3 
            focus:outline-none focus:ring-2 focus:ring-emerald-500
            transition-colors
            hover:bg-emerald-700/70
          "
        >
          {Object.entries(CULTURAL_STYLES).map(([key, value]) => (
            <option key={key} value={value} data-testid={`style-${value}`}>
              {value.charAt(0).toUpperCase() + value.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Botões de Ação */}
      <div className="grid grid-cols-2 gap-2">
        <button
          data-testid="new-game-btn"
          onClick={onNewGame}
          className="
            bg-emerald-600/70 hover:bg-emerald-500 
            text-white font-medium
            rounded-lg px-4 py-3 
            transition-all duration-200
            hover:shadow-lg hover:scale-[1.02]
            active:scale-[0.98]
          "
          style={{
            backgroundImage: `url('/images/buttons/${culturalStyle}.png')`
          }}
        >
          Nova Partida
        </button>
        
        <button
          data-testid="flip-board-btn"
          onClick={onFlipBoard}
          className="
            bg-emerald-600/70 hover:bg-emerald-500 
            text-white font-medium
            rounded-lg px-4 py-3 
            transition-all duration-200
            hover:shadow-lg hover:scale-[1.02]
            active:scale-[0.98]
          "
          style={{
            backgroundImage: `url('/images/buttons/${culturalStyle}.png')`
          }}
        >
          Inverter Tabuleiro
        </button>

        <button
          data-testid="undo-btn"
          onClick={onUndo}
          disabled={!canUndo}
          className={`
            col-span-2 
            ${
            canUndo 
              ? 'bg-emerald-600/70 hover:bg-emerald-500 hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]' 
              : 'bg-emerald-800/50 cursor-not-allowed opacity-50'
            }
            text-white font-medium
            rounded-lg px-4 py-3
            transition-all duration-200
          `}
          style={
            canUndo
              ? {
                  backgroundImage: `url('/images/buttons/${culturalStyle}.png')`
                }
              : undefined
          }
        >
          Desfazer Jogada
        </button>
      </div>

      {/* Status do Jogo */}
      <div className="mt-2 text-center">
        <p 
          data-testid="game-status"
          data-state={isPlayerTurn ? "playing" : "waiting"}
          className="text-emerald-100">
          {isPlayerTurn ? 'Sua vez de jogar' : 'Aguardando oponente...'}
        </p>
      </div>
    </div>
  );
};

export const MemoizedGameControls = React.memo(GameControls);
