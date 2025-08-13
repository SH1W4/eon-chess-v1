import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';

interface ChessPiece {
  type: 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
  color: 'white' | 'black';
  position: string;
  hasMoved?: boolean;
}

interface ChessBoardProps {
  style?: 'modern' | 'medieval' | 'renaissance' | 'ancient';
  onMove?: (from: string, to: string) => void;
  onPieceSelect?: (piece: ChessPiece) => void;
}

const FunctionalChessBoard: React.FC<ChessBoardProps> = ({
  style = 'modern',
  onMove,
  onPieceSelect
}) => {
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const [validMoves, setValidMoves] = useState<string[]>([]);
  const [currentTurn, setCurrentTurn] = useState<'white' | 'black'>('white');
  const [gameState, setGameState] = useState<'playing' | 'check' | 'checkmate' | 'stalemate'>('playing');

  // Inicializar posição inicial das peças
  const [pieces, setPieces] = useState<ChessPiece[]>([
    // Peças brancas
    { type: 'rook', color: 'white', position: 'a1' },
    { type: 'knight', color: 'white', position: 'b1' },
    { type: 'bishop', color: 'white', position: 'c1' },
    { type: 'queen', color: 'white', position: 'd1' },
    { type: 'king', color: 'white', position: 'e1' },
    { type: 'bishop', color: 'white', position: 'f1' },
    { type: 'knight', color: 'white', position: 'g1' },
    { type: 'rook', color: 'white', position: 'h1' },
    { type: 'pawn', color: 'white', position: 'a2' },
    { type: 'pawn', color: 'white', position: 'b2' },
    { type: 'pawn', color: 'white', position: 'c2' },
    { type: 'pawn', color: 'white', position: 'd2' },
    { type: 'pawn', color: 'white', position: 'e2' },
    { type: 'pawn', color: 'white', position: 'f2' },
    { type: 'pawn', color: 'white', position: 'g2' },
    { type: 'pawn', color: 'white', position: 'h2' },

    // Peças pretas
    { type: 'rook', color: 'black', position: 'a8' },
    { type: 'knight', color: 'black', position: 'b8' },
    { type: 'bishop', color: 'black', position: 'c8' },
    { type: 'queen', color: 'black', position: 'd8' },
    { type: 'king', color: 'black', position: 'e8' },
    { type: 'bishop', color: 'black', position: 'f8' },
    { type: 'knight', color: 'black', position: 'g8' },
    { type: 'rook', color: 'black', position: 'h8' },
    { type: 'pawn', color: 'black', position: 'a7' },
    { type: 'pawn', color: 'black', position: 'b7' },
    { type: 'pawn', color: 'black', position: 'c7' },
    { type: 'pawn', color: 'black', position: 'd7' },
    { type: 'pawn', color: 'black', position: 'e7' },
    { type: 'pawn', color: 'black', position: 'f7' },
    { type: 'pawn', color: 'black', position: 'g7' },
    { type: 'pawn', color: 'black', position: 'h7' },
  ]);

  // Função para obter peça em uma posição
  const getPieceAt = useCallback((position: string): ChessPiece | null => {
    return pieces.find(piece => piece.position === position) || null;
  }, [pieces]);

  // Função para verificar se uma posição está dentro do tabuleiro
  const isValidPosition = (position: string): boolean => {
    const file = position.charCodeAt(0) - 97; // a = 0, b = 1, etc.
    const rank = parseInt(position[1]) - 1;
    return file >= 0 && file <= 7 && rank >= 0 && rank <= 7;
  };

  // Função para calcular movimentos válidos de uma peça
  const calculateValidMoves = useCallback((piece: ChessPiece): string[] => {
    const moves: string[] = [];
    const [file, rank] = [piece.position.charCodeAt(0) - 97, parseInt(piece.position[1]) - 1];

    switch (piece.type) {
      case 'pawn':
        const direction = piece.color === 'white' ? 1 : -1;
        const startRank = piece.color === 'white' ? 1 : 6;
        
        // Movimento simples
        const nextRank = rank + direction;
        if (nextRank >= 0 && nextRank <= 7) {
          const nextPosition = `${String.fromCharCode(97 + file)}${nextRank + 1}`;
          if (!getPieceAt(nextPosition)) {
            moves.push(nextPosition);
            
            // Movimento duplo do início
            if (rank === startRank) {
              const doubleRank = rank + 2 * direction;
              if (doubleRank >= 0 && doubleRank <= 7) {
                const doublePosition = `${String.fromCharCode(97 + file)}${doubleRank + 1}`;
                if (!getPieceAt(doublePosition)) {
                  moves.push(doublePosition);
                }
              }
            }
          }
        }

        // Captura diagonal
        [-1, 1].forEach(fileOffset => {
          const newFile = file + fileOffset;
          const newRank = rank + direction;
          if (newFile >= 0 && newFile <= 7 && newRank >= 0 && newRank <= 7) {
            const capturePosition = `${String.fromCharCode(97 + newFile)}${newRank + 1}`;
            const targetPiece = getPieceAt(capturePosition);
            if (targetPiece && targetPiece.color !== piece.color) {
              moves.push(capturePosition);
            }
          }
        });
        break;

      case 'rook':
        // Movimentos horizontais e verticais
        const rookDirections = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        rookDirections.forEach(([fileOffset, rankOffset]) => {
          for (let i = 1; i <= 7; i++) {
            const newFile = file + fileOffset * i;
            const newRank = rank + rankOffset * i;
            if (newFile >= 0 && newFile <= 7 && newRank >= 0 && newRank <= 7) {
              const position = `${String.fromCharCode(97 + newFile)}${newRank + 1}`;
              const targetPiece = getPieceAt(position);
              if (!targetPiece) {
                moves.push(position);
              } else {
                if (targetPiece.color !== piece.color) {
                  moves.push(position);
                }
                break;
              }
            } else {
              break;
            }
          }
        });
        break;

      case 'knight':
        // Movimentos em L
        const knightMoves = [
          [-2, -1], [-2, 1], [-1, -2], [-1, 2],
          [1, -2], [1, 2], [2, -1], [2, 1]
        ];
        knightMoves.forEach(([fileOffset, rankOffset]) => {
          const newFile = file + fileOffset;
          const newRank = rank + rankOffset;
          if (newFile >= 0 && newFile <= 7 && newRank >= 0 && newRank <= 7) {
            const position = `${String.fromCharCode(97 + newFile)}${newRank + 1}`;
            const targetPiece = getPieceAt(position);
            if (!targetPiece || targetPiece.color !== piece.color) {
              moves.push(position);
            }
          }
        });
        break;

      case 'bishop':
        // Movimentos diagonais
        const bishopDirections = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
        bishopDirections.forEach(([fileOffset, rankOffset]) => {
          for (let i = 1; i <= 7; i++) {
            const newFile = file + fileOffset * i;
            const newRank = rank + rankOffset * i;
            if (newFile >= 0 && newFile <= 7 && newRank >= 0 && newRank <= 7) {
              const position = `${String.fromCharCode(97 + newFile)}${newRank + 1}`;
              const targetPiece = getPieceAt(position);
              if (!targetPiece) {
                moves.push(position);
              } else {
                if (targetPiece.color !== piece.color) {
                  moves.push(position);
                }
                break;
              }
            } else {
              break;
            }
          }
        });
        break;

      case 'queen':
        // Combina movimentos de torre e bispo
        const queenDirections = [
          [0, 1], [0, -1], [1, 0], [-1, 0], // Horizontal e vertical
          [1, 1], [1, -1], [-1, 1], [-1, -1] // Diagonal
        ];
        queenDirections.forEach(([fileOffset, rankOffset]) => {
          for (let i = 1; i <= 7; i++) {
            const newFile = file + fileOffset * i;
            const newRank = rank + rankOffset * i;
            if (newFile >= 0 && newFile <= 7 && newRank >= 0 && newRank <= 7) {
              const position = `${String.fromCharCode(97 + newFile)}${newRank + 1}`;
              const targetPiece = getPieceAt(position);
              if (!targetPiece) {
                moves.push(position);
              } else {
                if (targetPiece.color !== piece.color) {
                  moves.push(position);
                }
                break;
              }
            } else {
              break;
            }
          }
        });
        break;

      case 'king':
        // Movimentos de uma casa em todas as direções
        const kingDirections = [
          [0, 1], [0, -1], [1, 0], [-1, 0],
          [1, 1], [1, -1], [-1, 1], [-1, -1]
        ];
        kingDirections.forEach(([fileOffset, rankOffset]) => {
          const newFile = file + fileOffset;
          const newRank = rank + rankOffset;
          if (newFile >= 0 && newFile <= 7 && newRank >= 0 && newRank <= 7) {
            const position = `${String.fromCharCode(97 + newFile)}${newRank + 1}`;
            const targetPiece = getPieceAt(position);
            if (!targetPiece || targetPiece.color !== piece.color) {
              moves.push(position);
            }
          }
        });
        break;
    }

    return moves;
  }, [getPieceAt]);

  // Função para lidar com clique em uma casa
  const handleSquareClick = useCallback((position: string) => {
    const piece = getPieceAt(position);

    // Se uma peça já está selecionada
    if (selectedPiece) {
      // Se clicou em um movimento válido
      if (validMoves.includes(position)) {
        // Executar o movimento
        const movingPiece = getPieceAt(selectedPiece);
        if (movingPiece) {
          const newPieces = pieces.map(p => {
            if (p.position === selectedPiece) {
              return { ...p, position, hasMoved: true };
            }
            // Remover peça capturada
            if (p.position === position) {
              return null;
            }
            return p;
          }).filter(Boolean) as ChessPiece[];

          setPieces(newPieces);
          setCurrentTurn(currentTurn === 'white' ? 'black' : 'white');
          
          // Callback para movimento
          onMove?.(selectedPiece, position);
        }
      }
      
      // Limpar seleção
      setSelectedPiece(null);
      setValidMoves([]);
    } 
    // Se clicou em uma peça do jogador atual
    else if (piece && piece.color === currentTurn) {
      setSelectedPiece(position);
      const moves = calculateValidMoves(piece);
      setValidMoves(moves);
      onPieceSelect?.(piece);
    }
  }, [selectedPiece, validMoves, pieces, currentTurn, getPieceAt, calculateValidMoves, onMove, onPieceSelect]);

  // Função para obter o símbolo da peça
  const getPieceSymbol = (piece: ChessPiece): string => {
    const symbols = {
      white: {
        king: '♔',
        queen: '♕',
        rook: '♖',
        bishop: '♗',
        knight: '♘',
        pawn: '♙'
      },
      black: {
        king: '♚',
        queen: '♛',
        rook: '♜',
        bishop: '♝',
        knight: '♞',
        pawn: '♟'
      }
    };
    return symbols[piece.color][piece.type];
  };

  // Função para verificar se uma casa deve ser destacada
  const isHighlighted = (position: string): boolean => {
    return selectedPiece === position || validMoves.includes(position);
  };

  // Gerar todas as casas do tabuleiro
  const squares = [];
  for (let rank = 7; rank >= 0; rank--) {
    for (let file = 0; file < 8; file++) {
      const position = `${String.fromCharCode(97 + file)}${rank + 1}`;
      const piece = getPieceAt(position);
      const isLightSquare = (file + rank) % 2 === 0;
      const isHighlightedSquare = isHighlighted(position);

      squares.push(
        <motion.div
          key={position}
          data-testid={`square-${file}-${7-rank}`}
          className={`
            relative w-full h-full flex items-center justify-center
            transition-all duration-200 cursor-pointer
            ${isLightSquare ? 'bg-amber-100' : 'bg-amber-800'}
            ${isHighlightedSquare ? 'ring-4 ring-emerald-400 ring-opacity-70' : ''}
            ${selectedPiece === position ? 'ring-4 ring-blue-500' : ''}
            ${validMoves.includes(position) ? 'ring-2 ring-green-400' : ''}
          `}
          onClick={() => handleSquareClick(position)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {piece && (
            <motion.div
              className="text-4xl select-none"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              {getPieceSymbol(piece)}
            </motion.div>
          )}
        </motion.div>
      );
    }
  }

  return (
    <div className="relative">
      <div 
        className="grid grid-cols-8 rounded-md overflow-hidden border-4 border-emerald-800"
        style={{ width: '280px', height: '280px' }}
      >
        {squares}
      </div>
      
      {/* Indicador de turno */}
      <div className="absolute -top-8 left-0 right-0 text-center">
        <div className={`
          inline-block px-4 py-2 rounded-lg text-white font-bold
          ${currentTurn === 'white' ? 'bg-white text-black' : 'bg-black text-white'}
        `}>
          Vez das {currentTurn === 'white' ? 'Brancas' : 'Pretas'}
        </div>
      </div>
    </div>
  );
};

export default FunctionalChessBoard;
