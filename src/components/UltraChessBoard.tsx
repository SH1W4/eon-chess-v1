import React, { useState, useEffect } from 'react';

interface ChessPiece {
  type: 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
  color: 'white' | 'black';
  position: string;
}

interface UltraChessBoardProps {
  onDebug?: (info: string) => void;
}

const UltraChessBoard: React.FC<UltraChessBoardProps> = ({ onDebug }) => {
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const [currentTurn, setCurrentTurn] = useState<'white' | 'black'>('white');
  const [gameState, setGameState] = useState<'playing' | 'check' | 'checkmate' | 'stalemate'>('playing');
  const [moveCount, setMoveCount] = useState(0);
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

  const debug = (info: string) => {
    console.log(`[UltraChessBoard] ${info}`);
    onDebug?.(info);
  };

  useEffect(() => {
    debug('Componente UltraChessBoard montado');
    debug(`Estado inicial: ${pieces.length} peças, turno: ${currentTurn}`);
    
    // Teste de clique programático
    setTimeout(() => {
      debug('Teste de clique programático em 1 segundo...');
      const testSquare = document.querySelector('[data-position="e2"]');
      if (testSquare && testSquare instanceof HTMLElement) {
        debug('Casa e2 encontrada, simulando clique...');
        testSquare.dispatchEvent(new MouseEvent('click', {
          bubbles: true,
          cancelable: true,
          view: window
        }));
      } else {
        debug('Casa e2 NÃO encontrada!');
      }
    }, 1000);
    
    // Teste de clique direto
    setTimeout(() => {
      debug('Teste de clique direto em 2 segundos...');
      testClickDirect('e2');
    }, 2000);
    
    // Teste de clique direto em peça preta
    setTimeout(() => {
      debug('Teste de clique direto em peça preta em 3 segundos...');
      testClickDirect('e7');
    }, 3000);
    
    // Teste de clique direto em casa vazia
    setTimeout(() => {
      debug('Teste de clique direto em casa vazia em 4 segundos...');
      testClickEmpty('e4');
    }, 4000);
  }, []);

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
    try {
      const piece = getPieceAt(position);
      
      debug(`Clique em ${position}, peça: ${piece ? `${piece.color} ${piece.type}` : 'nenhuma'}`);
      debug(`Estado atual: selectedPiece=${selectedPiece}, currentTurn=${currentTurn}`);
      
      if (selectedPiece) {
        // Executar movimento
        const movingPiece = getPieceAt(selectedPiece);
        if (movingPiece) {
          debug(`Movendo ${movingPiece.type} de ${selectedPiece} para ${position}`);
          
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
          setMoveCount(prev => prev + 1);
          setSelectedPiece(null);
          
          debug(`Movimento executado. Turno: ${currentTurn === 'white' ? 'black' : 'white'}, Movimento: ${moveCount + 1}`);
        }
      } else if (piece && piece.color === currentTurn) {
        // Selecionar peça
        setSelectedPiece(position);
        debug(`Peça selecionada: ${piece.color} ${piece.type} em ${position}`);
      } else if (piece && piece.color !== currentTurn) {
        debug(`Tentativa de selecionar peça adversária: ${piece.color} ${piece.type}`);
      } else {
        debug(`Clique em casa vazia: ${position}`);
      }
    } catch (error) {
      debug(`Erro no handleSquareClick: ${error}`);
      console.error('Erro no handleSquareClick:', error);
    }
  };

  // Teste de clique programático
  const testClick = (position: string) => {
    debug(`Teste de clique programático em ${position}`);
    handleSquareClick(position);
  };

  // Teste de clique direto
  const testClickDirect = (position: string) => {
    debug(`Teste de clique direto em ${position}`);
    const piece = getPieceAt(position);
    debug(`Peça em ${position}: ${piece ? `${piece.color} ${piece.type}` : 'nenhuma'}`);
    
    if (piece && piece.color === currentTurn) {
      setSelectedPiece(position);
      debug(`Peça selecionada via teste: ${piece.color} ${piece.type} em ${position}`);
    } else if (piece && piece.color !== currentTurn) {
      debug(`Tentativa de selecionar peça adversária via teste: ${piece.color} ${piece.type}`);
    } else {
      debug(`Casa vazia via teste: ${position}`);
    }
  };

  // Teste de clique direto em casa vazia
  const testClickEmpty = (position: string) => {
    debug(`Teste de clique direto em casa vazia: ${position}`);
    const piece = getPieceAt(position);
    debug(`Peça em ${position}: ${piece ? `${piece.color} ${piece.type}` : 'nenhuma'}`);
    
    if (!piece) {
      debug(`Casa ${position} está vazia, selecionando...`);
      setSelectedPiece(position);
    }
  };

  const resetGame = () => {
    debug('Resetando jogo');
    setSelectedPiece(null);
    setCurrentTurn('white');
    setGameState('playing');
    setMoveCount(0);
    setPieces([
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
    debug('Jogo resetado com sucesso');
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
          style={{
            width: '100%',
            height: '100%',
            backgroundColor: isLightSquare ? '#fef3c7' : '#92400e',
            border: isSelected ? '4px solid #3b82f6' : '1px solid #000',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative'
          }}
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            debug(`Clique detectado em ${position}`);
            handleSquareClick(position);
          }}
          onMouseDown={(e) => {
            e.preventDefault();
            debug(`Mouse down em ${position}`);
          }}
          onMouseUp={(e) => {
            e.preventDefault();
            debug(`Mouse up em ${position}`);
          }}
          data-position={position}
          data-piece={piece ? `${piece.color}-${piece.type}` : 'empty'}
          data-testid={`square-${position}`}
        >
          {piece && (
            <div style={{ fontSize: '2rem', userSelect: 'none' }}>
              {getPieceSymbol(piece)}
            </div>
          )}
          {/* Debug info na casa */}
          <div style={{
            position: 'absolute',
            bottom: '2px',
            right: '2px',
            fontSize: '0.75rem',
            color: '#dc2626',
            fontWeight: 'bold'
          }}>
            {position}
          </div>
        </div>
      );
    }
  }

  return (
    <div 
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        border: '2px solid #ef4444'
      }}
      onClick={() => debug('Container principal clicado')}
      onMouseDown={() => debug('Container principal mouse down')}
      onMouseUp={() => debug('Container principal mouse up')}
    >
      {/* Teste de clique direto */}
      <div
        style={{
          position: 'absolute',
          top: '50px',
          left: '50px',
          width: '100px',
          height: '100px',
          backgroundColor: '#ff0000',
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          zIndex: 1000
        }}
        onClick={(e) => {
          e.stopPropagation();
          debug('Botão de teste clicado!');
        }}
      >
        TESTE
      </div>
      
      <div 
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(8, 1fr)',
          borderRadius: '6px',
          overflow: 'hidden',
          border: '4px solid #065f46',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          backgroundColor: '#fef3c7',
          width: 'min(400px, 80vw)',
          height: 'min(400px, 80vw)',
          maxWidth: '100%',
          maxHeight: '100%'
        }}
        data-testid="ultra-chess-board"
        onClick={(e) => {
          e.stopPropagation();
          debug('Grid do tabuleiro clicado');
        }}
      >
        {squares}
      </div>
      
      {/* Indicador de turno */}
      <div style={{
        position: 'absolute',
        top: '-32px',
        left: '0',
        right: '0',
        textAlign: 'center'
      }}>
        <div style={{
          display: 'inline-block',
          padding: '8px 16px',
          borderRadius: '8px',
          color: currentTurn === 'white' ? '#000' : '#fff',
          backgroundColor: currentTurn === 'white' ? '#fff' : '#000',
          fontWeight: 'bold'
        }}>
          Vez das {currentTurn === 'white' ? 'Brancas' : 'Pretas'}
        </div>
      </div>

      {/* Controles */}
      <div style={{
        position: 'absolute',
        bottom: '-48px',
        left: '0',
        right: '0',
        textAlign: 'center'
      }}>
        <button
          onClick={resetGame}
          style={{
            backgroundColor: '#059669',
            color: '#fff',
            fontWeight: '500',
            borderRadius: '8px',
            padding: '8px 16px',
            border: 'none',
            cursor: 'pointer'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = '#10b981';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = '#059669';
          }}
        >
          🔄 Nova Partida
        </button>
        <div style={{
          fontSize: '0.875rem',
          color: '#d1fae5',
          marginTop: '8px'
        }}>
          Movimentos: {moveCount}
        </div>
      </div>
      
      {/* Debug info */}
      <div style={{
        position: 'absolute',
        top: '0',
        left: '0',
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        color: '#fff',
        fontSize: '12px',
        padding: '8px',
        borderRadius: '4px'
      }}>
        <div>Peças: {pieces.length}</div>
        <div>Selecionado: {selectedPiece || 'nenhum'}</div>
        <div>Turno: {currentTurn}</div>
        <div>Movimentos: {moveCount}</div>
        
        {/* Botões de teste */}
        <div style={{ marginTop: '8px' }}>
          <button
            onClick={() => testClickDirect('e2')}
            style={{
              backgroundColor: '#3b82f6',
              color: '#fff',
              fontSize: '10px',
              padding: '2px 4px',
              margin: '1px',
              border: 'none',
              borderRadius: '2px',
              cursor: 'pointer'
            }}
          >
            Teste e2
          </button>
          <button
            onClick={() => testClickDirect('e7')}
            style={{
              backgroundColor: '#3b82f6',
              color: '#fff',
              fontSize: '10px',
              padding: '2px 4px',
              margin: '1px',
              border: 'none',
              borderRadius: '2px',
              cursor: 'pointer'
            }}
          >
            Teste e7
          </button>
        </div>
      </div>
    </div>
  );
};

export default UltraChessBoard;
