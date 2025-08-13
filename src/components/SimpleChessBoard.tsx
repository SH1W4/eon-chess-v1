import React, { useState } from 'react';

interface ChessPiece {
  type: 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
  color: 'white' | 'black';
  position: string;
}

const SimpleChessBoard: React.FC = () => {
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const [currentTurn, setCurrentTurn] = useState<'white' | 'black'>('white');
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

  const getPieceAt = (position: string): ChessPiece | null => {
    return pieces.find(piece => piece.position === position) || null;
  };

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

  const handleSquareClick = (position: string) => {
    const piece = getPieceAt(position);
    
    if (selectedPiece) {
      // Executar movimento
      const movingPiece = getPieceAt(selectedPiece);
      if (movingPiece) {
        const newPieces = pieces.map(p => {
          if (p.position === selectedPiece) {
            return { ...p, position };
          }
          if (p.position === position) {
            return null; // Captura
          }
          return p;
        }).filter(Boolean) as ChessPiece[];

        setPieces(newPieces);
        setCurrentTurn(currentTurn === 'white' ? 'black' : 'white');
        console.log(`Movimento: ${selectedPiece} → ${position}`);
      }
      setSelectedPiece(null);
    } else if (piece && piece.color === currentTurn) {
      setSelectedPiece(position);
      console.log(`Peça selecionada: ${piece.type} ${piece.color} em ${position}`);
    }
  };

  const squares = [];
  for (let rank = 7; rank >= 0; rank--) {
    for (let file = 0; file < 8; file++) {
      const position = `${String.fromCharCode(97 + file)}${rank + 1}`;
      const piece = getPieceAt(position);
      const isLightSquare = (file + rank) % 2 === 0;
      const isSelected = selectedPiece === position;

      squares.push(
        <div
          key={position}
          className={`
            relative w-full h-full flex items-center justify-center
            transition-all duration-200 cursor-pointer
            ${isLightSquare ? 'bg-amber-100' : 'bg-amber-800'}
            ${isSelected ? 'ring-4 ring-blue-500' : ''}
            hover:scale-105
          `}
          onClick={() => handleSquareClick(position)}
        >
          {piece && (
            <div className="text-4xl select-none">
              {getPieceSymbol(piece)}
            </div>
          )}
        </div>
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

export default SimpleChessBoard;
