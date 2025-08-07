import { useState } from 'react';
import Layout from '../components/Layout';
import { MemoizedChessBoard } from '../src/web/components/board/ChessBoard';
import { useGameState } from '../src/web/hooks/useGameState';
import { INITIAL_FEN, TIME_CONTROLS } from '../src/shared/constants/game';
import { ChessPosition, ChessMove } from '../src/shared/types/chess';
import { coordsToAlgebraic } from '../src/shared/utils/chess';

const PlayPage = () => {
  const [orientation, setOrientation] = useState<'white' | 'black'>('white');
  const [culturalStyle, setCulturalStyle] = useState('modern');

  const {
    gameState,
    selectedSquare,
    possibleMoves,
    lastMove,
    pieceAt,
    selectSquare,
    makeMove,
    resetGame,
    undoLastMove,
    isCheck,
    isCheckmate,
    isDraw,
    currentPlayer,
  } = useGameState({
    initialFen: INITIAL_FEN,
    culturalStyle,
    timeControl: TIME_CONTROLS.RAPID,
  });

  // Manipula cliques nas casas do tabuleiro
  const handleSquareClick = (position: ChessPosition) => {
    const piece = pieceAt(position);

    // Se já tem uma peça selecionada, tenta mover
    if (selectedSquare) {
      if (makeMove(selectedSquare, position)) {
        // Movimento realizado com sucesso
        return;
      }
      // Se o movimento falhou, seleciona a nova casa se for uma peça própria
      if (piece && piece.color === currentPlayer) {
        selectSquare(position);
        return;
      }
      // Se não for uma peça própria, limpa a seleção
      selectSquare(null);
      return;
    }

    // Se não tem peça selecionada e clicou em uma peça própria, seleciona
    if (piece && piece.color === currentPlayer) {
      selectSquare(position);
      return;
    }
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {/* Cabeçalho do jogo */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            AEON CHESS
          </h1>
          <p className="text-lg text-gray-600">
            Sistema de Xadrez com Inteligência Cultural
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Coluna da esquerda - Informações do jogo */}
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-bold text-gray-800 mb-4">Configurações</h2>
              <div className="space-y-4">
                <button
                  onClick={() => setOrientation(prev => prev === 'white' ? 'black' : 'white')}
                  className="w-full px-4 py-2 rounded-md text-sm font-medium
                    bg-gray-100 hover:bg-gray-200
                    transition-colors duration-200"
                >
                  Girar Tabuleiro
                </button>

                <button
                  onClick={resetGame}
                  className="w-full px-4 py-2 rounded-md text-sm font-medium
                    bg-blue-600 hover:bg-blue-700 text-white
                    transition-colors duration-200"
                >
                  Novo Jogo
                </button>

                <button
                  onClick={undoLastMove}
                  disabled={gameState.moveHistory.length === 0}
                  className={`w-full px-4 py-2 rounded-md text-sm font-medium
                    transition-colors duration-200
                    ${gameState.moveHistory.length === 0
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                    }`}
                >
                  Desfazer
                </button>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Estilo Cultural
                  </label>
                  <select
                    value={culturalStyle}
                    onChange={(e) => setCulturalStyle(e.target.value)}
                    className="w-full p-2 border rounded-md"
                  >
                    <option value="modern">Moderno</option>
                    <option value="ancient">Antigo</option>
                    <option value="medieval">Medieval</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-bold text-gray-800 mb-4">Status</h2>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Jogador Atual:</span>
                  <span className="font-medium">
                    {currentPlayer === 'white' ? 'Brancas' : 'Pretas'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Movimentos:</span>
                  <span>{gameState.moveHistory.length}</span>
                </div>
                {isCheck && (
                  <div className="text-red-600 font-medium">
                    Xeque!
                  </div>
                )}
                {isCheckmate && (
                  <div className="text-red-600 font-medium">
                    Xeque-mate!
                  </div>
                )}
                {isDraw && (
                  <div className="text-gray-600 font-medium">
                    Empate
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Coluna central - Tabuleiro */}
          <div className="lg:col-span-2">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-full max-w-2xl mx-auto">
                <MemoizedChessBoard
                  orientation={orientation}
                  culturalStyle={culturalStyle}
                  showCoordinates={true}
                  onMove={(from, to) => {
                    makeMove(from, to);
                  }}
                  onGameEnd={(result) => {
                    console.log('Game ended:', result);
                  }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Seção de movimentos */}
        <div className="mt-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Histórico de Movimentos</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="font-medium text-gray-700 mb-2">Brancas</h3>
                <div className="space-y-1 text-sm">
                  {gameState.moveHistory
                    .filter((_, i: number) => i % 2 === 0)
                    .map((move: ChessMove, i: number) => (
                      <div key={i} className="flex justify-between">
                        <span>{i + 1}. {move.piece.type.toUpperCase()}{coordsToAlgebraic(move.to)}</span>
                      </div>
                    ))}
                </div>
              </div>
              <div>
                <h3 className="font-medium text-gray-700 mb-2">Pretas</h3>
                <div className="space-y-1 text-sm">
                  {gameState.moveHistory
                    .filter((_, i: number) => i % 2 === 1)
                    .map((move: ChessMove, i: number) => (
                      <div key={i} className="flex justify-between">
                        <span>{i + 1}... {move.piece.type.toUpperCase()}{coordsToAlgebraic(move.to)}</span>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default PlayPage;
