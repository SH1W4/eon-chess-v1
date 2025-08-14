import React, { useState, useEffect } from 'react';
import Head from 'next/head';

interface ChessPiece {
  id: string;
  type: 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
  color: 'white' | 'black';
  position: string;
  hasMoved: boolean;
}

const RevolutionChessBoard: React.FC = () => {
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const [currentTurn, setCurrentTurn] = useState<'white' | 'black'>('white');
  const [gameState, setGameState] = useState<'playing' | 'check' | 'checkmate' | 'stalemate'>('playing');
  const [moveCount, setMoveCount] = useState(0);
  const [pieces, setPieces] = useState<ChessPiece[]>([
    // Peças brancas
    { id: 'wr1', type: 'rook', color: 'white', position: 'a1', hasMoved: false },
    { id: 'wn1', type: 'knight', color: 'white', position: 'b1', hasMoved: false },
    { id: 'wb1', type: 'bishop', color: 'white', position: 'c1', hasMoved: false },
    { id: 'wq', type: 'queen', color: 'white', position: 'd1', hasMoved: false },
    { id: 'wk', type: 'king', color: 'white', position: 'e1', hasMoved: false },
    { id: 'wb2', type: 'bishop', color: 'white', position: 'f1', hasMoved: false },
    { id: 'wn2', type: 'knight', color: 'white', position: 'g1', hasMoved: false },
    { id: 'wr2', type: 'rook', color: 'white', position: 'h1', hasMoved: false },
    { id: 'wp1', type: 'pawn', color: 'white', position: 'a2', hasMoved: false },
    { id: 'wp2', type: 'pawn', color: 'white', position: 'b2', hasMoved: false },
    { id: 'wp3', type: 'pawn', color: 'white', position: 'c2', hasMoved: false },
    { id: 'wp4', type: 'pawn', color: 'white', position: 'd2', hasMoved: false },
    { id: 'wp5', type: 'pawn', color: 'white', position: 'e2', hasMoved: false },
    { id: 'wp6', type: 'pawn', color: 'white', position: 'f2', hasMoved: false },
    { id: 'wp7', type: 'pawn', color: 'white', position: 'g2', hasMoved: false },
    { id: 'wp8', type: 'pawn', color: 'white', position: 'h2', hasMoved: false },
    
    // Peças pretas
    { id: 'br1', type: 'rook', color: 'black', position: 'a8', hasMoved: false },
    { id: 'bn1', type: 'knight', color: 'black', position: 'b8', hasMoved: false },
    { id: 'bb1', type: 'bishop', color: 'black', position: 'c8', hasMoved: false },
    { id: 'bq', type: 'queen', color: 'black', position: 'd8', hasMoved: false },
    { id: 'bk', type: 'king', color: 'black', position: 'e8', hasMoved: false },
    { id: 'bb2', type: 'bishop', color: 'black', position: 'f8', hasMoved: false },
    { id: 'bn2', type: 'knight', color: 'black', position: 'g8', hasMoved: false },
    { id: 'br2', type: 'rook', color: 'black', position: 'h8', hasMoved: false },
    { id: 'bp1', type: 'pawn', color: 'black', position: 'a7', hasMoved: false },
    { id: 'bp2', type: 'pawn', color: 'black', position: 'b7', hasMoved: false },
    { id: 'bp3', type: 'pawn', color: 'black', position: 'c7', hasMoved: false },
    { id: 'bp4', type: 'pawn', color: 'black', position: 'd7', hasMoved: false },
    { id: 'bp5', type: 'pawn', color: 'black', position: 'e7', hasMoved: false },
    { id: 'bp6', type: 'pawn', color: 'black', position: 'f7', hasMoved: false },
    { id: 'bp7', type: 'pawn', color: 'black', position: 'g7', hasMoved: false },
    { id: 'bp8', type: 'pawn', color: 'black', position: 'h8', hasMoved: false },
  ]);

  const [hoveredSquare, setHoveredSquare] = useState<string | null>(null);
  const [lastMove, setLastMove] = useState<string | null>(null);

  const getPieceAt = (position: string): ChessPiece | null => {
    return pieces.find(piece => piece.position === position) || null;
  };

  const getPieceSymbol = (piece: ChessPiece): string => {
    const symbols: Record<string, string> = {
      'white-king': '♔', 'white-queen': '♕', 'white-rook': '♖',
      'white-bishop': '♗', 'white-knight': '♘', 'white-pawn': '♙',
      'black-king': '♚', 'black-queen': '♛', 'black-rook': '♜',
      'black-bishop': '♝', 'black-knight': '♞', 'black-pawn': '♟'
    };
    return symbols[`${piece.color}-${piece.type}`] || '?';
  };

  const isValidMove = (piece: ChessPiece, from: string, to: string): boolean => {
    const fromFile = from.charCodeAt(0);
    const fromRank = parseInt(from[1] || '0');
    const toFile = to.charCodeAt(0);
    const toRank = parseInt(to[1] || '0');
    
    const fileDiff = Math.abs(toFile - fromFile);
    const rankDiff = Math.abs(toRank - fromRank);
    
    const targetPiece = getPieceAt(to);
    if (targetPiece && targetPiece.color === piece.color) return false;

    switch (piece.type) {
      case 'pawn':
        const direction = piece.color === 'white' ? 1 : -1;
        const startRank = piece.color === 'white' ? 2 : 7;
        
        // Movimento normal
        if (fileDiff === 0 && toRank === fromRank + direction && !targetPiece) return true;
        
        // Primeiro movimento (2 casas)
        if (fileDiff === 0 && fromRank === startRank && toRank === fromRank + 2 * direction && 
            !targetPiece && !getPieceAt(String.fromCharCode(fromFile) + (fromRank + direction))) return true;
        
        // Captura diagonal
        if (fileDiff === 1 && rankDiff === 1 && targetPiece) return true;
        return false;

      case 'rook':
        return (fileDiff === 0 || rankDiff === 0) && !isPathBlocked(from, to);

      case 'knight':
        return (fileDiff === 2 && rankDiff === 1) || (fileDiff === 1 && rankDiff === 2);

      case 'bishop':
        return fileDiff === rankDiff && !isPathBlocked(from, to);

      case 'queen':
        return ((fileDiff === 0 || rankDiff === 0) || (fileDiff === rankDiff)) && !isPathBlocked(from, to);

      case 'king':
        return fileDiff <= 1 && rankDiff <= 1;

      default:
        return false;
    }
  };

  const isPathBlocked = (from: string, to: string): boolean => {
    const fromFile = from.charCodeAt(0);
    const fromRank = parseInt(from[1] || '0');
    const toFile = to.charCodeAt(0);
    const toRank = parseInt(to[1] || '0');
    
    const fileStep = fromFile === toFile ? 0 : (toFile - fromFile) / Math.abs(toFile - fromFile);
    const rankStep = fromRank === toRank ? 0 : (toRank - fromRank) / Math.abs(toRank - fromRank);
    
    let currentFile = fromFile + fileStep;
    let currentRank = fromRank + rankStep;
    
    while (currentFile !== toFile || currentRank !== toRank) {
      const currentPos = String.fromCharCode(currentFile) + currentRank;
      if (getPieceAt(currentPos)) return true;
      currentFile += fileStep;
      currentRank += rankStep;
    }
    
    return false;
  };

  const handleSquareClick = (position: string) => {
    const piece = getPieceAt(position);
    
    if (selectedPiece) {
      const selectedPieceObj = pieces.find(p => p.id === selectedPiece);
      if (selectedPieceObj && isValidMove(selectedPieceObj, selectedPieceObj.position, position)) {
        // Executar movimento
        const newPieces = pieces.map(p => {
          if (p.id === selectedPiece) {
            return { ...p, position, hasMoved: true };
          }
          if (p.position === position) {
            return { ...p, position: 'captured' };
          }
          return p;
        }).filter(p => p.position !== 'captured');
        
        setPieces(newPieces);
        setLastMove(`${selectedPieceObj.position} → ${position}`);
        setMoveCount(prev => prev + 1);
        setCurrentTurn(prev => prev === 'white' ? 'black' : 'white');
        setSelectedPiece(null);
        
        // Efeito de movimento
        console.log(`🎯 Movimento executado: ${selectedPieceObj.type} ${selectedPieceObj.color} ${selectedPieceObj.position} → ${position}`);
      } else {
        setSelectedPiece(null);
      }
    } else if (piece && piece.color === currentTurn) {
      setSelectedPiece(piece.id);
      console.log(`🎯 Peça selecionada: ${piece.type} ${piece.color} em ${position}`);
    }
  };

  const resetGame = () => {
    setPieces([
      // Peças brancas
      { id: 'wr1', type: 'rook', color: 'white', position: 'a1', hasMoved: false },
      { id: 'wn1', type: 'knight', color: 'white', position: 'b1', hasMoved: false },
      { id: 'wb1', type: 'bishop', color: 'white', position: 'c1', hasMoved: false },
      { id: 'wq', type: 'queen', color: 'white', position: 'd1', hasMoved: false },
      { id: 'wk', type: 'king', color: 'white', position: 'e1', hasMoved: false },
      { id: 'wb2', type: 'bishop', color: 'white', position: 'f1', hasMoved: false },
      { id: 'wn2', type: 'knight', color: 'white', position: 'g1', hasMoved: false },
      { id: 'wr2', type: 'rook', color: 'white', position: 'h1', hasMoved: false },
      { id: 'wp1', type: 'pawn', color: 'white', position: 'a2', hasMoved: false },
      { id: 'wp2', type: 'pawn', color: 'white', position: 'b2', hasMoved: false },
      { id: 'wp3', type: 'pawn', color: 'white', position: 'c2', hasMoved: false },
      { id: 'wp4', type: 'pawn', color: 'white', position: 'd2', hasMoved: false },
      { id: 'wp5', type: 'pawn', color: 'white', position: 'e2', hasMoved: false },
      { id: 'wp6', type: 'pawn', color: 'white', position: 'f2', hasMoved: false },
      { id: 'wp7', type: 'pawn', color: 'white', position: 'g2', hasMoved: false },
      { id: 'wp8', type: 'pawn', color: 'white', position: 'h2', hasMoved: false },
      
      // Peças pretas
      { id: 'br1', type: 'rook', color: 'black', position: 'a8', hasMoved: false },
      { id: 'bn1', type: 'knight', color: 'black', position: 'b8', hasMoved: false },
      { id: 'bb1', type: 'bishop', color: 'black', position: 'c8', hasMoved: false },
      { id: 'bq', type: 'queen', color: 'black', position: 'd8', hasMoved: false },
      { id: 'bk', type: 'king', color: 'black', position: 'e8', hasMoved: false },
      { id: 'bb2', type: 'bishop', color: 'black', position: 'f8', hasMoved: false },
      { id: 'bn2', type: 'knight', color: 'black', position: 'g8', hasMoved: false },
      { id: 'br2', type: 'rook', color: 'black', position: 'h8', hasMoved: false },
      { id: 'bp1', type: 'pawn', color: 'black', position: 'a7', hasMoved: false },
      { id: 'bp2', type: 'pawn', color: 'black', position: 'b7', hasMoved: false },
      { id: 'bp3', type: 'pawn', color: 'black', position: 'c7', hasMoved: false },
      { id: 'bp4', type: 'pawn', color: 'black', position: 'd7', hasMoved: false },
      { id: 'bp5', type: 'pawn', color: 'black', position: 'e7', hasMoved: false },
      { id: 'bp6', type: 'pawn', color: 'black', position: 'f7', hasMoved: false },
      { id: 'bp7', type: 'pawn', color: 'black', position: 'g7', hasMoved: false },
      { id: 'bp8', type: 'pawn', color: 'black', position: 'h8', hasMoved: false },
    ]);
    setSelectedPiece(null);
    setCurrentTurn('white');
    setGameState('playing');
    setMoveCount(0);
    setLastMove(null);
    console.log('🔄 Jogo resetado!');
  };

  const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  const ranks = [8, 7, 6, 5, 4, 3, 2, 1];

  const squares = ranks.flatMap(rank =>
    files.map(file => {
      const position = file + rank;
      const piece = getPieceAt(position);
      const isSelected = selectedPiece && pieces.find(p => p.id === selectedPiece)?.position === position;
      const isHovered = hoveredSquare === position;
      const isLastMove = lastMove && (lastMove.includes(position));
      const isLightSquare = (files.indexOf(file) + rank) % 2 === 0;
      
      return (
        <div
          key={position}
          className={`
            relative w-full h-full flex items-center justify-center cursor-pointer
            transition-all duration-300 ease-out transform
            ${isLightSquare ? 'bg-amber-100' : 'bg-amber-800'}
            ${isSelected ? 'ring-4 ring-blue-500 ring-opacity-80 scale-110 z-10' : ''}
            ${isHovered ? 'ring-2 ring-yellow-400 ring-opacity-60 scale-105' : ''}
            ${isLastMove ? 'ring-2 ring-green-400 ring-opacity-80' : ''}
            hover:scale-105 hover:shadow-lg
          `}
          onClick={() => handleSquareClick(position)}
          onMouseEnter={() => setHoveredSquare(position)}
          onMouseLeave={() => setHoveredSquare(null)}
          data-testid={`square-${position}`}
        >
          {piece && (
            <div
              className={`
                text-4xl md:text-5xl lg:text-6xl font-bold select-none
                transition-all duration-300 ease-out
                ${piece.color === 'white' ? 'text-white drop-shadow-lg' : 'text-gray-900 drop-shadow-lg'}
                ${isSelected ? 'animate-pulse' : ''}
                ${isHovered ? 'scale-110' : ''}
              `}
              style={{
                textShadow: piece.color === 'white' 
                  ? '2px 2px 4px rgba(0,0,0,0.8)' 
                  : '2px 2px 4px rgba(255,255,255,0.8)'
              }}
            >
              {getPieceSymbol(piece)}
            </div>
          )}
          
          {/* Coordenadas */}
          <div className="absolute bottom-1 right-1 text-xs font-mono text-gray-600 opacity-60">
            {position}
          </div>
        </div>
      );
    })
  );

  useEffect(() => {
    console.log('🚀 Revolution Chess Board carregado!');
    console.log('🎯 Estado inicial:', { pieces: pieces.length, currentTurn, gameState });
  }, []);

  return (
    <>
      <Head>
        <title>♟️ Revolution Chess - AEON</title>
        <meta name="description" content="Tabuleiro de xadrez revolucionário com efeitos modernos" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4 md:p-8">
        <div className="max-w-6xl mx-auto">
          {/* Header Revolucionário */}
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 mb-4">
              ♟️ REVOLUTION CHESS
            </h1>
            <p className="text-xl text-cyan-100 mb-6">
              A revolução do xadrez está aqui. Efeitos modernos. Funcionalidade real.
            </p>
            
            {/* Status do Jogo */}
            <div className="flex flex-wrap justify-center gap-4 mb-6">
              <div className="bg-black/30 backdrop-blur-sm rounded-lg px-4 py-2 border border-cyan-500/50">
                <span className="text-cyan-400 font-bold">Turno:</span>
                <span className={`ml-2 font-bold ${currentTurn === 'white' ? 'text-white' : 'text-gray-300'}`}>
                  {currentTurn === 'white' ? '♔ Brancas' : '♚ Pretas'}
                </span>
              </div>
              
              <div className="bg-black/30 backdrop-blur-sm rounded-lg px-4 py-2 border border-purple-500/50">
                <span className="text-purple-400 font-bold">Movimentos:</span>
                <span className="ml-2 text-white font-bold">{moveCount}</span>
              </div>
              
              <div className="bg-black/30 backdrop-blur-sm rounded-lg px-4 py-2 border border-green-500/50">
                <span className="text-green-400 font-bold">Estado:</span>
                <span className="ml-2 text-white font-bold capitalize">{gameState}</span>
              </div>
            </div>

            {/* Último Movimento */}
            {lastMove && (
              <div className="bg-green-500/20 backdrop-blur-sm rounded-lg px-4 py-2 border border-green-500/50 mb-4 animate-pulse">
                <span className="text-green-400 font-bold">Último Movimento:</span>
                <span className="ml-2 text-white font-mono">{lastMove}</span>
              </div>
            )}
          </div>

          {/* Tabuleiro Principal */}
          <div className="flex justify-center mb-8">
            <div 
              className="grid grid-cols-8 rounded-xl overflow-hidden border-4 border-cyan-500/50 shadow-2xl bg-gradient-to-br from-amber-50 to-amber-100"
              style={{ 
                width: 'min(500px, 90vw)', 
                height: 'min(500px, 90vw)',
                maxWidth: '100%',
                maxHeight: '100%'
              }}
              data-testid="revolution-chess-board"
            >
              {squares}
            </div>
          </div>

          {/* Controles */}
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={resetGame}
              className="bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white font-bold py-3 px-6 rounded-lg shadow-lg transform hover:scale-105 transition-all duration-300 border-2 border-red-400/50"
            >
              🔄 Nova Partida
            </button>
            
            <button
              onClick={() => console.log('🎯 Estado atual:', { pieces, currentTurn, gameState, moveCount })}
              className="bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-bold py-3 px-6 rounded-lg shadow-lg transform hover:scale-105 transition-all duration-300 border-2 border-blue-400/50"
            >
              📊 Debug Info
            </button>
          </div>

          {/* Instruções */}
          <div className="mt-8 bg-black/20 backdrop-blur-sm rounded-xl border border-cyan-500/30 p-6">
            <h3 className="text-2xl font-bold text-cyan-400 mb-4 text-center">
              🎯 Como Jogar
            </h3>
            <div className="grid md:grid-cols-2 gap-6 text-cyan-100">
              <div>
                <h4 className="text-lg font-bold text-cyan-300 mb-2">♔ Movimentos Básicos:</h4>
                <ul className="space-y-1 text-sm">
                  <li>• <strong>Peão:</strong> 1 casa para frente, captura na diagonal</li>
                  <li>• <strong>Torre:</strong> Linhas retas (horizontal/vertical)</li>
                  <li>• <strong>Cavalo:</strong> Movimento em L (2+1 casas)</li>
                  <li>• <strong>Bispo:</strong> Diagonais</li>
                  <li>• <strong>Rainha:</strong> Combina torre + bispo</li>
                  <li>• <strong>Rei:</strong> 1 casa em qualquer direção</li>
                </ul>
              </div>
              <div>
                <h4 className="text-lg font-bold text-cyan-300 mb-2">🎮 Controles:</h4>
                <ul className="space-y-1 text-sm">
                  <li>• <strong>Clique</strong> em uma peça para selecionar</li>
                  <li>• <strong>Clique</strong> em uma casa para mover</li>
                  <li>• <strong>Brancas</strong> começam sempre</li>
                  <li>• <strong>Capturas</strong> removem peças adversárias</li>
                  <li>• <strong>Turnos</strong> alternam automaticamente</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default RevolutionChessBoard;
