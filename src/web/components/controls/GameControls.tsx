import React from 'react';
import { theme } from '../../../shared/styles/theme';
import { CULTURAL_STYLES } from '../../../shared/constants/game';

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
    <div className="flex flex-col gap-4 p-4 bg-emerald-800/50 rounded-lg border border-emerald-600">
      <h2 className="text-xl font-bold text-white mb-2">Controles</h2>
      
      {/* Estilo Cultural */}
      <div className="flex flex-col gap-2">
        <label className="text-emerald-100 text-sm">Estilo Cultural</label>
        <select
          value={culturalStyle}
          onChange={(e) => onStyleChange(e.target.value)}
          className="bg-emerald-700 text-white border border-emerald-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
          {Object.entries(CULTURAL_STYLES).map(([key, value]) => (
            <option key={key} value={value}>
              {value.charAt(0).toUpperCase() + value.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Botões de Ação */}
      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={onNewGame}
          className="bg-emerald-600 hover:bg-emerald-500 text-white rounded px-4 py-2 transition-colors"
          style={{
            backgroundImage: theme.culturalConfig[culturalStyle as keyof typeof theme.culturalConfig].buttonPattern,
          }}
        >
          Nova Partida
        </button>
        
        <button
          onClick={onFlipBoard}
          className="bg-emerald-600 hover:bg-emerald-500 text-white rounded px-4 py-2 transition-colors"
          style={{
            backgroundImage: theme.culturalConfig[culturalStyle as keyof typeof theme.culturalConfig].buttonPattern,
          }}
        >
          Inverter Tabuleiro
        </button>

        <button
          onClick={onUndo}
          disabled={!canUndo}
          className={`col-span-2 ${
            canUndo
              ? 'bg-emerald-600 hover:bg-emerald-500'
              : 'bg-emerald-800 cursor-not-allowed'
          } text-white rounded px-4 py-2 transition-colors`}
          style={
            canUndo
              ? {
                  backgroundImage: theme.culturalConfig[culturalStyle as keyof typeof theme.culturalConfig].buttonPattern,
                }
              : undefined
          }
        >
          Desfazer Jogada
        </button>
      </div>

      {/* Status do Jogo */}
      <div className="mt-2 text-center">
        <p className="text-emerald-100">
          {isPlayerTurn ? 'Sua vez de jogar' : 'Aguardando oponente...'}
        </p>
      </div>
    </div>
  );
};

export const MemoizedGameControls = React.memo(GameControls);
