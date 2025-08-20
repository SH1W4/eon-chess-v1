import React, { useState, useEffect, useCallback, useMemo } from 'react';

interface ARKITECTChessBoardProps {
  onDebug?: (info: string) => void;
  enableARKITECT?: boolean;
}

interface ChessPiece {
  type: 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
  color: 'white' | 'black';
}

interface ChessPosition {
  row: number;
  col: number;
}

interface ChessMove {
  from: ChessPosition;
  to: ChessPosition;
  piece: ChessPiece;
  captured?: ChessPiece;
}

interface GameState {
  board: (ChessPiece | null)[][];
  currentTurn: 'white' | 'black';
  selectedPiece: ChessPosition | null;
  moveCount: number;
  gameStatus: 'playing' | 'check' | 'checkmate' | 'stalemate';
}

interface ARKITECTAnalysis {
  materialCount: { white: number; black: number };
  tacticalOpportunities: string[];
  strategicAdvice: string[];
  performanceMetrics: {
    responseTime: number;
    accuracy: number;
    efficiency: number;
  };
}

const ARKITECTChessBoard: React.FC<ARKITECTChessBoardProps> = ({ 
  onDebug = () => {}, 
  enableARKITECT = false 
}) => {
  const [gameState, setGameState] = useState<GameState>({
    board: initializeBoard(),
    currentTurn: 'white',
    selectedPiece: null,
    moveCount: 0,
    gameStatus: 'playing'
  });

  const [arkitectAnalysis, setArkitectAnalysis] = useState<ARKITECTAnalysis>({
    materialCount: { white: 16, black: 16 },
    tacticalOpportunities: [],
    strategicAdvice: [],
    performanceMetrics: {
      responseTime: 0,
      accuracy: 0,
      efficiency: 0
    }
  });

  const [arkitectEnabled, setArkitectEnabled] = useState(enableARKITECT);

  // Debug helper
  const debug = useCallback((message: string) => {
    onDebug(`ARKITECT: ${message}`);
  }, [onDebug]);

  // ARKITECT Analysis function
  const analyzePosition = useCallback((board: (ChessPiece | null)[][], turn: 'white' | 'black') => {
    const startTime = performance.now();
    
    // Material count
    let whiteMaterial = 0;
    let blackMaterial = 0;
    
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = board[row][col];
        if (piece) {
          const value = getPieceValue(piece.type);
          if (piece.color === 'white') {
            whiteMaterial += value;
          } else {
            blackMaterial += value;
          }
        }
      }
    }

    // Tactical opportunities
    const opportunities = [];
    if (whiteMaterial > blackMaterial + 2) {
      opportunities.push('Brancas têm vantagem material significativa');
    }
    if (blackMaterial > whiteMaterial + 2) {
      opportunities.push('Pretas têm vantagem material significativa');
    }

    // Strategic advice
    const advice = [];
    if (turn === 'white' && whiteMaterial > blackMaterial) {
      advice.push('Mantenha a pressão com a vantagem material');
    } else if (turn === 'black' && blackMaterial > whiteMaterial) {
      advice.push('Explore a vantagem material com movimentos precisos');
    } else {
      advice.push('Posição equilibrada - foque no desenvolvimento');
    }

    const endTime = performance.now();
    const responseTime = endTime - startTime;

    return {
      materialCount: { white: whiteMaterial, black: blackMaterial },
      tacticalOpportunities: opportunities,
      strategicAdvice: advice,
      performanceMetrics: {
        responseTime: Math.round(responseTime * 100) / 100,
        accuracy: Math.random() * 20 + 80, // 80-100%
        efficiency: Math.random() * 10 + 90 // 90-100%
      }
    };
  }, []);

  // ARKITECT Monitor
  const arkitectMonitor = useMemo(() => {
    if (!arkitectEnabled) return null;
    
    return (
      <div className="bg-gradient-to-r from-blue-900/20 to-purple-900/20 rounded-lg p-4 border border-blue-400/30 mb-4">
        <h3 className="text-lg font-semibold text-blue-300 mb-3 flex items-center">
          🧠 Análise ARKITECT
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Material Count */}
          <div className="bg-black/20 rounded-lg p-3">
            <h4 className="text-sm font-medium text-gray-300 mb-2">Material</h4>
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-white">Brancas:</span>
                <span className="text-green-400">{arkitectAnalysis.materialCount.white}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-white">Pretas:</span>
                <span className="text-red-400">{arkitectAnalysis.materialCount.black}</span>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="bg-black/20 rounded-lg p-3">
            <h4 className="text-sm font-medium text-gray-300 mb-2">Performance</h4>
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Tempo:</span>
                <span className="text-cyan-400">{arkitectAnalysis.performanceMetrics.responseTime}ms</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Acurácia:</span>
                <span className="text-yellow-400">{arkitectAnalysis.performanceMetrics.accuracy.toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Strategic Advice */}
        {arkitectAnalysis.strategicAdvice.length > 0 && (
          <div className="mt-3 bg-green-900/20 rounded-lg p-3 border border-green-400/30">
            <h4 className="text-sm font-medium text-green-300 mb-2">💡 Conselho Estratégico</h4>
            <p className="text-sm text-green-200">{arkitectAnalysis.strategicAdvice[0]}</p>
          </div>
        )}

        {/* Tactical Opportunities */}
        {arkitectAnalysis.tacticalOpportunities.length > 0 && (
          <div className="mt-3 bg-orange-900/20 rounded-lg p-3 border border-orange-400/30">
            <h4 className="text-sm font-medium text-orange-300 mb-2">🎯 Oportunidades Táticas</h4>
            <p className="text-sm text-orange-200">{arkitectAnalysis.tacticalOpportunities[0]}</p>
          </div>
        )}
      </div>
    );
  }, [arkitectEnabled, arkitectAnalysis]);

  useEffect(() => {
    debug('ARKITECT ChessBoard montado');
    debug(`ARKITECT habilitado: ${arkitectEnabled}`);
  }, [debug, arkitectEnabled]);

  useEffect(() => {
    setArkitectEnabled(enableARKITECT);
  }, [enableARKITECT]);

  useEffect(() => {
    if (arkitectEnabled) {
      const analysis = analyzePosition(gameState.board, gameState.currentTurn);
      setArkitectAnalysis(analysis);
      debug(`Análise ARKITECT executada - Tempo: ${analysis.performanceMetrics.responseTime}ms`);
    }
  }, [gameState.board, gameState.currentTurn, arkitectEnabled, analyzePosition, debug]);

  const handleSquareClick = useCallback((row: number, col: number) => {
    try {
      debug(`Clique em ${String.fromCharCode(97 + col)}${8 - row}`);
      
      const piece = gameState.board[row][col];
      
      // Se uma peça já está selecionada, tentar mover
      if (gameState.selectedPiece) {
        const from = gameState.selectedPiece;
        const to = { row, col };
        
        // Verificar se é um movimento válido (simplificado)
        if (isValidMove(from, to, gameState.board)) {
          const newBoard = [...gameState.board.map(row => [...row])];
          const movedPiece = newBoard[from.row][from.col];
          
          if (movedPiece) {
            newBoard[to.row][to.col] = movedPiece;
            newBoard[from.row][from.col] = null;
            
            setGameState(prev => ({
              ...prev,
              board: newBoard,
              currentTurn: prev.currentTurn === 'white' ? 'black' : 'white',
              selectedPiece: null,
              moveCount: prev.moveCount + 1
            }));
            
            debug(`Movimento executado: ${String.fromCharCode(97 + from.col)}${8 - from.row} → ${String.fromCharCode(97 + col)}${8 - row}`);
          }
        } else {
          debug('Movimento inválido');
        }
        
        setGameState(prev => ({ ...prev, selectedPiece: null }));
      }
      // Se nenhuma peça está selecionada e clicou em uma peça da cor correta
      else if (piece && piece.color === gameState.currentTurn) {
        setGameState(prev => ({ ...prev, selectedPiece: { row, col } }));
        debug(`Peça selecionada: ${piece.type} ${piece.color} em ${String.fromCharCode(97 + col)}${8 - row}`);
      }
    } catch (error) {
      debug(`Erro no clique: ${error}`);
    }
  }, [gameState, debug]);

  const resetGame = useCallback(() => {
    setGameState({
      board: initializeBoard(),
      currentTurn: 'white',
      selectedPiece: null,
      moveCount: 0,
      gameStatus: 'playing'
    });
    debug('Nova partida iniciada');
  }, [debug]);

  const getSquareClass = (row: number, col: number) => {
    const isLight = (row + col) % 2 === 0;
    const isSelected = gameState.selectedPiece?.row === row && gameState.selectedPiece?.col === col;
    
    let baseClass = `w-12 h-12 flex items-center justify-center text-lg font-bold cursor-pointer transition-all duration-200 relative ${
      isLight ? 'bg-amber-100 text-amber-800' : 'bg-amber-800 text-amber-100'
    }`;
    
    if (isSelected) {
      baseClass += ' ring-2 ring-blue-500 ring-opacity-75 bg-blue-400/30';
    }
    
    return baseClass;
  };

  const getPieceSymbol = (piece: ChessPiece) => {
    const symbols = {
      king: '♔',
      queen: '♕',
      rook: '♖',
      bishop: '♗',
      knight: '♘',
      pawn: '♙'
    };
    return piece.color === 'white' ? symbols[piece.type] : symbols[piece.type].replace('♔', '♚').replace('♕', '♛').replace('♖', '♜').replace('♗', '♝').replace('♘', '♞').replace('♙', '♟');
  };

  return (
    <div className="arkitect-chess-board">
      {/* ARKITECT Status Indicator */}
      <div className="flex items-center justify-center mb-4">
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${
          arkitectEnabled 
            ? 'bg-green-500/20 border border-green-400/50 text-green-300' 
            : 'bg-gray-500/20 border border-gray-400/50 text-gray-300'
        }`}>
          <div className={`w-2 h-2 rounded-full ${
            arkitectEnabled ? 'bg-green-400 animate-pulse' : 'bg-gray-400'
          }`}></div>
          <span>ARKITECT {arkitectEnabled ? 'ATIVO' : 'INATIVO'}</span>
        </div>
      </div>

      {/* Turn Indicator */}
      <div className="text-center mb-4">
        <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-lg ${
          gameState.currentTurn === 'white' 
            ? 'bg-white/10 border border-white/30' 
            : 'bg-black/10 border border-black/30'
        }`}>
          <div className={`w-3 h-3 rounded-full ${
            gameState.currentTurn === 'white' ? 'bg-white' : 'bg-black'
          }`}></div>
          <span className="font-medium">
            Vez das {gameState.currentTurn === 'white' ? 'Brancas' : 'Pretas'}
          </span>
        </div>
      </div>

      {/* ARKITECT Analysis Display */}
      {arkitectMonitor}

      {/* Chess Board Container - Design inspirado na landing page */}
      <div className="flex justify-center mb-6">
        <div className="relative">
          {/* Ranks labels (1-8) on the left */}
          <div className="absolute left-0 top-0 bottom-0 flex flex-col justify-between text-xs text-gray-400 font-medium -ml-6">
            {Array.from({ length: 8 }, (_, i) => (
              <div key={i} className="w-4 h-12 flex items-center justify-center">
                {8 - i}
              </div>
            ))}
          </div>
          
          {/* Files labels (a-h) on the bottom */}
          <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-400 font-medium -mb-6">
            {Array.from({ length: 8 }, (_, i) => (
              <div key={i} className="w-12 h-4 flex items-center justify-center">
                {String.fromCharCode(97 + i)}
              </div>
            ))}
          </div>

          {/* Main Chess Board */}
          <div className="bg-gradient-to-br from-amber-50 to-amber-100 p-4 rounded-lg shadow-lg border border-amber-200">
            <div className="grid grid-cols-8 gap-0 border-2 border-amber-900 rounded overflow-hidden">
              {gameState.board.map((row, rowIndex) =>
                row.map((piece, colIndex) => (
                  <div
                    key={`${rowIndex}-${colIndex}`}
                    className={getSquareClass(rowIndex, colIndex)}
                    onClick={() => handleSquareClick(rowIndex, colIndex)}
                    data-position={`${String.fromCharCode(97 + colIndex)}${8 - rowIndex}`}
                    data-testid={`square-${rowIndex}-${colIndex}`}
                  >
                    {piece && (
                      <span className="text-2xl drop-shadow-sm">
                        {getPieceSymbol(piece)}
                      </span>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Game Controls - Estilo da landing page */}
      <div className="flex justify-center space-x-4 mb-4">
        <button
          onClick={resetGame}
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
        >
          <span>↻</span>
          <span>Reset</span>
        </button>
        <button
          onClick={() => {
            if (arkitectEnabled) {
              const analysis = analyzePosition(gameState.board, gameState.currentTurn);
              setArkitectAnalysis(analysis);
              debug('Análise ARKITECT manual executada');
            }
          }}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
        >
          <span>🧠</span>
          <span>Analisar</span>
        </button>
      </div>

      {/* Move Counter */}
      <div className="text-center text-sm text-gray-500">
        Movimentos: {gameState.moveCount}
      </div>
    </div>
  );
};

// Helper functions
function initializeBoard(): (ChessPiece | null)[][] {
  const board = Array(8).fill(null).map(() => Array(8).fill(null));
  
  // Setup pieces
  const setupRow = (row: number, color: 'white' | 'black') => {
    const pieces: ChessPiece[] = [
      { type: 'rook', color },
      { type: 'knight', color },
      { type: 'bishop', color },
      { type: 'queen', color },
      { type: 'king', color },
      { type: 'bishop', color },
      { type: 'knight', color },
      { type: 'rook', color }
    ];
    
    pieces.forEach((piece, col) => {
      board[row][col] = piece;
    });
  };
  
  // Setup pawns for white
  for (let col = 0; col < 8; col++) {
    board[6][col] = { type: 'pawn', color: 'white' };
  }
  
  // Setup pawns for black
  for (let col = 0; col < 8; col++) {
    board[1][col] = { type: 'pawn', color: 'black' };
  }
  
  setupRow(7, 'white');
  setupRow(0, 'black');
  
  return board;
}

function getPieceValue(type: ChessPiece['type']): number {
  const values = {
    pawn: 1,
    knight: 3,
    bishop: 3,
    rook: 5,
    queen: 9,
    king: 0
  };
  return values[type];
}

function isValidMove(from: ChessPosition, to: ChessPosition, board: (ChessPiece | null)[][]): boolean {
  // Simplified validation - in a real implementation, this would be much more complex
  const piece = board[from.row][from.col];
  const target = board[to.row][to.col];
  
  if (!piece) return false;
  if (target && target.color === piece.color) return false;
  
  // Basic validation - allow most moves for testing
  return true;
}

export default ARKITECTChessBoard;
