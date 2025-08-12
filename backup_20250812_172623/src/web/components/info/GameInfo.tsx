import React from 'react';
import { ChessMove } from '../../../shared/types/chess';

interface GameInfoProps {
  culturalStyle: string;
  moves: ChessMove[];
  evaluation: number;
  narratives: string[];
  events: Array<{
    type: string;
    description: string;
    timestamp: number;
  }>;
}

export const GameInfo: React.FC<GameInfoProps> = ({
  culturalStyle,
  moves,
  evaluation,
  narratives,
  events,
}) => {
  // Formata a avaliação como string com sinal
  const formatEvaluation = (value: number): string => {
    const absEval = Math.abs(value);
    const sign = value > 0 ? '+' : value < 0 ? '-' : '';
    return `${sign}${absEval.toFixed(1)}`;
  };

  // Formata o movimento para exibição
  const formatMove = (move: ChessMove): string => {
    const pieceSymbols: Record<string, string> = {
      p: '',
      n: 'N',
      b: 'B',
      r: 'R',
      q: 'Q',
      k: 'K',
    };

    const piece = pieceSymbols[move.piece.type] || '';
    const capture = move.captured ? 'x' : '';
    const promotion = move.promotion ? `=${pieceSymbols[move.promotion]}` : '';
    const to = `${String.fromCharCode(97 + move.to.col)}${8 - move.to.row}`;

    return `${piece}${capture}${to}${promotion}`;
  };

  return (
    <div className="flex flex-col gap-4">
      {/* Avaliação */}
      <div 
        data-testid="evaluation-panel"
        className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 shadow-xl p-6"
      >
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">📊</span>
          Avaliação
        </h2>
        <div className="flex items-center justify-between">
          <span className="text-emerald-100">Posição atual:</span>
          <span
            data-testid="evaluation-value"
            data-value={evaluation}
            className={`text-lg font-bold ${
              evaluation > 0
                ? 'text-emerald-400'
                : evaluation < 0
                ? 'text-red-400'
                : 'text-gray-400'
            }`}
          >
            {formatEvaluation(evaluation)}
          </span>
        </div>
      </div>

      {/* Narrativas Culturais */}
      <div 
        data-testid="narratives-panel"
        className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 shadow-xl p-6"
      >
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">📖</span>
          Narrativas
        </h2>
        <div className="space-y-2">
          {narratives.map((narrative, index) => (
            <p 
              key={index} 
              data-testid={`narrative-${index}`}
              className="text-emerald-100 text-sm"
            >
              {narrative}
            </p>
          ))}
        </div>
      </div>

      {/* Histórico de Movimentos */}
      <div
        data-testid="move-history"
        className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 shadow-xl p-6 max-h-48 overflow-y-auto scrollbar-custom"
      >
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">♟️</span>
          Movimentos
        </h2>
        <div className="grid grid-cols-2 gap-2">
          {moves.map((move, index) => (
            <div
              key={index}
              data-testid={`move-history-item-${index}`}
              className={`text-sm ${index % 2 === 0 ? 'text-right' : 'text-left'}`}
            >
              {index % 2 === 0 && (
                <span className="text-emerald-400 mr-2">
                  {Math.floor(index / 2) + 1}.
                </span>
              )}
              <span className="text-emerald-100">{formatMove(move)}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Eventos Culturais */}
      <div
        data-testid="events-panel"
        className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 shadow-xl p-6 max-h-48 overflow-y-auto scrollbar-custom"
      >
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">🎭</span>
          Eventos
        </h2>
        <div className="space-y-2">
          {events.map((event, index) => (
            <div 
              key={index} 
              data-testid={`event-${index}`}
              className="flex items-center gap-2"
            >
              <span className="text-emerald-400 text-xs">
                {new Date(event.timestamp).toLocaleTimeString()}
              </span>
              <span className="text-emerald-100 text-sm">
                {event.description}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Estilo para scrollbars */}
      <style jsx global>{`
        .scrollbar-custom {
          scrollbar-width: thin;
          scrollbar-color: #059669 #065f46;
        }
        .scrollbar-custom::-webkit-scrollbar {
          width: 8px;
        }
        .scrollbar-custom::-webkit-scrollbar-track {
          background: #065f46;
          border-radius: 4px;
        }
        .scrollbar-custom::-webkit-scrollbar-thumb {
          background: #059669;
          border-radius: 4px;
        }
        .scrollbar-custom::-webkit-scrollbar-thumb:hover {
          background: #10b981;
        }
      `}</style>
    </div>
  );
};

export const MemoizedGameInfo = React.memo(GameInfo);
