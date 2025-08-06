import React from 'react';
import { ChessMove } from '../../../shared/types/chess';
import { theme } from '../../../shared/styles/theme';

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
  const formatEvaluation = (eval: number): string => {
    const absEval = Math.abs(eval);
    const sign = eval > 0 ? '+' : eval < 0 ? '-' : '';
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
      <div className="bg-emerald-800/50 rounded-lg border border-emerald-600 p-4">
        <h2 className="text-xl font-bold text-white mb-2">Avaliação</h2>
        <div className="flex items-center justify-between">
          <span className="text-emerald-100">Posição atual:</span>
          <span
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
      <div className="bg-emerald-800/50 rounded-lg border border-emerald-600 p-4">
        <h2 className="text-xl font-bold text-white mb-2">Narrativas</h2>
        <div className="space-y-2">
          {narratives.map((narrative, index) => (
            <p key={index} className="text-emerald-100 text-sm">
              {narrative}
            </p>
          ))}
        </div>
      </div>

      {/* Histórico de Movimentos */}
      <div
        className="bg-emerald-800/50 rounded-lg border border-emerald-600 p-4 max-h-48 overflow-y-auto"
        style={{
          scrollbarWidth: 'thin',
          scrollbarColor: `${theme.colors.emerald[600]} ${theme.colors.emerald[800]}`,
        }}
      >
        <h2 className="text-xl font-bold text-white mb-2">Movimentos</h2>
        <div className="grid grid-cols-2 gap-2">
          {moves.map((move, index) => (
            <div
              key={index}
              className={`text-sm ${
                index % 2 === 0 ? 'text-right' : 'text-left'
              }`}
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
        className="bg-emerald-800/50 rounded-lg border border-emerald-600 p-4 max-h-48 overflow-y-auto"
        style={{
          scrollbarWidth: 'thin',
          scrollbarColor: `${theme.colors.emerald[600]} ${theme.colors.emerald[800]}`,
        }}
      >
        <h2 className="text-xl font-bold text-white mb-2">Eventos</h2>
        <div className="space-y-2">
          {events.map((event, index) => (
            <div key={index} className="flex items-center gap-2">
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
        ::-webkit-scrollbar {
          width: 8px;
        }
        ::-webkit-scrollbar-track {
          background: ${theme.colors.emerald[800]};
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb {
          background: ${theme.colors.emerald[600]};
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: ${theme.colors.emerald[500]};
        }
      `}</style>
    </div>
  );
};

export const MemoizedGameInfo = React.memo(GameInfo);
