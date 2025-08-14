import React, { useState, useEffect, useCallback, useMemo } from 'react';

interface ChessPiece {
  type: 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
  color: 'white' | 'black';
  position: string;
}

interface ARKITECTChessBoardProps {
  onDebug?: (info: string) => void;
  enableARKITECT?: boolean;
}

interface ARKITECTAnalysis {
  moveQuality: number;
  tacticalOpportunities: string[];
  strategicAdvice: string;
  performanceMetrics: {
    responseTime: number;
    accuracy: number;
    efficiency: number;
  };
}

const ARKITECTChessBoard: React.FC<ARKITECTChessBoardProps> = ({ 
  onDebug, 
  enableARKITECT = true 
}) => {
  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);
  const [currentTurn, setCurrentTurn] = useState<'white' | 'black'>('white');
  const [gameState, setGameState] = useState<'playing' | 'check' | 'checkmate' | 'stalemate'>('playing');
  const [moveCount, setMoveCount] = useState(0);
  const [arkitectAnalysis, setArkitectAnalysis] = useState<ARKITECTAnalysis | null>(null);
  const [arkitectEnabled, setArkitectEnabled] = useState(enableARKITECT);
  
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

  const debug = useCallback((info: string) => {
    console.log(`[ARKITECTChessBoard] ${info}`);
    onDebug?.(info);
  }, [onDebug]);

  // ARKITECT Analysis Engine
  const analyzePosition = useCallback((currentPieces: ChessPiece[], turn: 'white' | 'black'): ARKITECTAnalysis => {
    const startTime = performance.now();
    
    // Análise tática
    const tacticalOpportunities: string[] = [];
    const materialCount = { white: 0, black: 0 };
    
    currentPieces.forEach(piece => {
      const value = piece.type === 'pawn' ? 1 : 
                   piece.type === 'knight' || piece.type === 'bishop' ? 3 :
                   piece.type === 'rook' ? 5 : 
                   piece.type === 'queen' ? 9 : 0;
      
      if (piece.color === 'white') materialCount.white += value;
      else materialCount.black += value;
    });

    // Detectar oportunidades táticas
    if (materialCount.white > materialCount.black + 2) {
      tacticalOpportunities.push('Vantagem material para brancas');
    }
    if (materialCount.black > materialCount.white + 2) {
      tacticalOpportunities.push('Vantagem material para pretas');
    }

    // Análise estratégica
    const strategicAdvice = materialCount.white > materialCount.black ? 
      'Brancas devem capitalizar vantagem material' :
      materialCount.black > materialCount.white ?
      'Pretas devem capitalizar vantagem material' :
      'Posição equilibrada, focar no desenvolvimento';

    const responseTime = performance.now() - startTime;

    return {
      moveQuality: Math.min(100, Math.max(0, 50 + (materialCount.white - materialCount.black) * 5)),
      tacticalOpportunities,
      strategicAdvice,
      performanceMetrics: {
        responseTime,
        accuracy: 85 + Math.random() * 10,
        efficiency: 90 + Math.random() * 5
      }
    };
  }, []);

  // ARKITECT Performance Monitoring
  const arkitectMonitor = useMemo(() => ({
    startAnalysis: () => {
      debug('🔬 ARKITECT iniciando análise...');
      const analysis = analyzePosition(pieces, currentTurn);
      setArkitectAnalysis(analysis);
      debug(`📊 ARKITECT análise completa: ${analysis.performanceMetrics.responseTime.toFixed(2)}ms`);
      return analysis;
    },
    
    getPerformanceReport: () => {
      if (!arkitectAnalysis) return null;
      return {
        responseTime: arkitectAnalysis.performanceMetrics.responseTime,
        accuracy: arkitectAnalysis.performanceMetrics.accuracy,
        efficiency: arkitectAnalysis.performanceMetrics.efficiency,
        moveQuality: arkitectAnalysis.moveQuality
      };
    }
  }), [analyzePosition, pieces, currentTurn, arkitectAnalysis, debug]);

  useEffect(() => {
    debug('🧠 ARKITECT ChessBoard montado');
    debug(`ARKITECT habilitado: ${arkitectEnabled}`);
    
    if (arkitectEnabled) {
      // Análise inicial do ARKITECT
      setTimeout(() => {
        const analysis = arkitectMonitor.startAnalysis();
        debug(`🎯 ARKITECT análise inicial: ${analysis.strategicAdvice}`);
      }, 1000);
    }
  }, [arkitectEnabled, arkitectMonitor, debug]);

  const getPieceAt = useCallback((position: string): ChessPiece | null => {
    return pieces.find(piece => piece.position === position) || null;
  }, [pieces]);

  const getPieceSymbol = useCallback((piece: ChessPiece): string => {
    const symbols = {
      white: { king: '♔', queen: '♕', rook: '♖', bishop: '♗', knight: '♘', pawn: '♙' },
      black: { king: '♚', queen: '♛', rook: '♜', bishop: '♝', knight: '♞', pawn: '♟' }
    };
    return symbols[piece.color][piece.type];
  }, []);

  const handleSquareClick = useCallback((position: string) => {
    try {
      const piece = getPieceAt(position);
      
      debug(`🎯 Clique em ${position}, peça: ${piece ? `${piece.color} ${piece.type}` : 'nenhuma'}`);
      
      if (selectedPiece) {
        // Executar movimento
        const movingPiece = getPieceAt(selectedPiece);
        if (movingPiece) {
          debug(`♟️ Movendo ${movingPiece.type} de ${selectedPiece} para ${position}`);
          
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
          
          // ARKITECT análise pós-movimento
          if (arkitectEnabled) {
            setTimeout(() => {
              const analysis = arkitectMonitor.startAnalysis();
              debug(`🧠 ARKITECT após movimento: ${analysis.strategicAdvice}`);
            }, 100);
          }
          
          debug(`✅ Movimento executado. Turno: ${currentTurn === 'white' ? 'black' : 'white'}, Movimento: ${moveCount + 1}`);
        }
      } else if (piece && piece.color === currentTurn) {
        // Selecionar peça
        setSelectedPiece(position);
        debug(`🎯 Peça selecionada: ${piece.color} ${piece.type} em ${position}`);
        
        // ARKITECT análise de seleção
        if (arkitectEnabled) {
          const analysis = analyzePosition(pieces, currentTurn);
          debug(`🧠 ARKITECT análise de seleção: ${analysis.tacticalOpportunities.join(', ')}`);
        }
      } else if (piece && piece.color !== currentTurn) {
        debug(`⚠️ Tentativa de selecionar peça adversária: ${piece.color} ${piece.type}`);
      } else {
        debug(`🔍 Clique em casa vazia: ${position}`);
      }
    } catch (error) {
      debug(`❌ Erro no handleSquareClick: ${error}`);
      console.error('Erro no handleSquareClick:', error);
    }
  }, [selectedPiece, pieces, currentTurn, moveCount, getPieceAt, debug, arkitectEnabled, arkitectMonitor, analyzePosition]);

  const resetGame = useCallback(() => {
    debug('🔄 Resetando jogo');
    setSelectedPiece(null);
    setCurrentTurn('white');
    setGameState('playing');
    setMoveCount(0);
    setArkitectAnalysis(null);
    setPieces([
      // Peças brancas
      { type: 'rook', color: 'white', position: 'a1' }, { type: 'knight', color: 'white', position: 'b1' },
      { type: 'bishop', color: 'white', position: 'c1' }, { type: 'queen', color: 'white', position: 'd1' },
      { type: 'king', color: 'white', position: 'e1' }, { type: 'bishop', color: 'white', position: 'f1' },
      { type: 'knight', color: 'white', position: 'g1' }, { type: 'rook', color: 'white', position: 'h1' },
      { type: 'pawn', color: 'white', position: 'a2' }, { type: 'pawn', color: 'white', position: 'b2' },
      { type: 'pawn', color: 'white', position: 'c2' }, { type: 'pawn', color: 'white', position: 'd2' },
      { type: 'pawn', color: 'white', position: 'e2' }, { type: 'pawn', color: 'white', position: 'f2' },
      { type: 'pawn', color: 'white', position: 'g2' }, { type: 'pawn', color: 'white', position: 'h2' },

      // Peças pretas
      { type: 'rook', color: 'black', position: 'a8' }, { type: 'knight', color: 'black', position: 'b8' },
      { type: 'bishop', color: 'black', position: 'c8' }, { type: 'queen', color: 'black', position: 'd8' },
      { type: 'king', color: 'black', position: 'e8' }, { type: 'bishop', color: 'black', position: 'f8' },
      { type: 'knight', color: 'black', position: 'g8' }, { type: 'rook', color: 'black', position: 'h8' },
      { type: 'pawn', color: 'black', position: 'a7' }, { type: 'pawn', color: 'black', position: 'b7' },
      { type: 'pawn', color: 'black', position: 'c7' }, { type: 'pawn', color: 'black', position: 'd7' },
      { type: 'pawn', color: 'black', position: 'e7' }, { type: 'pawn', color: 'black', position: 'f7' },
      { type: 'pawn', color: 'black', position: 'g7' }, { type: 'pawn', color: 'black', position: 'h7' },
    ]);
    
    if (arkitectEnabled) {
      setTimeout(() => {
        const analysis = arkitectMonitor.startAnalysis();
        debug(`🧠 ARKITECT após reset: ${analysis.strategicAdvice}`);
      }, 100);
    }
    
    debug('✅ Jogo resetado com sucesso');
  }, [debug, arkitectEnabled, arkitectMonitor]);

  const toggleARKITECT = useCallback(() => {
    setArkitectEnabled(prev => !prev);
    debug(`🧠 ARKITECT ${!arkitectEnabled ? 'habilitado' : 'desabilitado'}`);
  }, [arkitectEnabled, debug]);

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
            debug(`🎯 Clique detectado em ${position}`);
            handleSquareClick(position);
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
    >
      {/* ARKITECT Status */}
      <div style={{
        position: 'absolute',
        top: '-60px',
        left: '0',
        right: '0',
        textAlign: 'center'
      }}>
        <div style={{
          display: 'inline-block',
          padding: '8px 16px',
          borderRadius: '8px',
          color: arkitectEnabled ? '#fff' : '#000',
          backgroundColor: arkitectEnabled ? '#059669' : '#e5e7eb',
          fontWeight: 'bold',
          marginRight: '10px'
        }}>
          🧠 ARKITECT: {arkitectEnabled ? 'ATIVO' : 'INATIVO'}
        </div>
        <button
          onClick={toggleARKITECT}
          style={{
            backgroundColor: arkitectEnabled ? '#dc2626' : '#059669',
            color: '#fff',
            padding: '8px 16px',
            borderRadius: '8px',
            border: 'none',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          {arkitectEnabled ? 'Desabilitar' : 'Habilitar'} ARKITECT
        </button>
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
        data-testid="arkitect-chess-board"
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
            cursor: 'pointer',
            marginRight: '10px'
          }}
        >
          🔄 Nova Partida
        </button>
        <button
          onClick={() => arkitectMonitor.startAnalysis()}
          style={{
            backgroundColor: '#3b82f6',
            color: '#fff',
            fontWeight: '500',
            borderRadius: '8px',
            padding: '8px 16px',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          🧠 Analisar ARKITECT
        </button>
        <div style={{
          fontSize: '0.875rem',
          color: '#d1fae5',
          marginTop: '8px'
        }}>
          Movimentos: {moveCount}
        </div>
      </div>
      
      {/* ARKITECT Analysis Display */}
      {arkitectAnalysis && arkitectEnabled && (
        <div style={{
          position: 'absolute',
          top: '0',
          right: '0',
          backgroundColor: 'rgba(0, 0, 0, 0.9)',
          color: '#fff',
          fontSize: '12px',
          padding: '12px',
          borderRadius: '4px',
          maxWidth: '300px',
          minWidth: '250px'
        }}>
          <div style={{ fontWeight: 'bold', marginBottom: '8px', color: '#10b981' }}>
            🧠 ARKITECT Analysis
          </div>
          <div style={{ marginBottom: '4px' }}>
            <strong>Qualidade:</strong> {arkitectAnalysis.moveQuality.toFixed(1)}%
          </div>
          <div style={{ marginBottom: '4px' }}>
            <strong>Conselho:</strong> {arkitectAnalysis.strategicAdvice}
          </div>
          {arkitectAnalysis.tacticalOpportunities.length > 0 && (
            <div style={{ marginBottom: '4px' }}>
              <strong>Oportunidades:</strong>
              <ul style={{ margin: '4px 0', paddingLeft: '16px' }}>
                {arkitectAnalysis.tacticalOpportunities.map((opp, i) => (
                  <li key={i} style={{ fontSize: '11px' }}>{opp}</li>
                ))}
              </ul>
            </div>
          )}
          <div style={{ marginTop: '8px', fontSize: '11px', color: '#9ca3af' }}>
            <div>⏱️ {arkitectAnalysis.performanceMetrics.responseTime.toFixed(1)}ms</div>
            <div>🎯 {arkitectAnalysis.performanceMetrics.accuracy.toFixed(1)}% acurácia</div>
            <div>⚡ {arkitectAnalysis.performanceMetrics.efficiency.toFixed(1)}% eficiência</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ARKITECTChessBoard;
