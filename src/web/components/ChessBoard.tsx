import React, { useState, useEffect, useCallback } from 'react';
import { Position, Move, PieceType, Color } from '../../types/chess';
import { ChessEngine } from '../../engine/ChessEngine';
import { AdaptiveAI } from '../../ai/AdaptiveAI';
import { CulturalTheme } from './CulturalTheme';
import { NarrativeDisplay } from './NarrativeDisplay';
import './ChessBoard.css';

interface ChessBoardProps {
  culturalProfile?: string;
  aiDifficulty?: 'easy' | 'medium' | 'hard' | 'adaptive';
  enableNarrative?: boolean;
}

interface BoardState {
  pieces: Map<string, { type: PieceType; color: Color }>;
  selectedSquare: string | null;
  validMoves: string[];
  currentTurn: Color;
  isCheck: boolean;
  isCheckmate: boolean;
  moveHistory: Move[];
}

export const ChessBoard: React.FC<ChessBoardProps> = ({
  culturalProfile = 'persian',
  aiDifficulty = 'adaptive',
  enableNarrative = true
}) => {
  const [boardState, setBoardState] = useState<BoardState>({
    pieces: new Map(),
    selectedSquare: null,
    validMoves: [],
    currentTurn: 'white',
    isCheck: false,
    isCheckmate: false,
    moveHistory: []
  });

  const [narrative, setNarrative] = useState<string>('');
  const [culturalTheme, setCulturalTheme] = useState(culturalProfile);
  const [isThinking, setIsThinking] = useState(false);

  // Inicializar o motor de xadrez
  const engine = useCallback(() => {
    return new ChessEngine({
      culturalProfile,
      aiDifficulty
    });
  }, [culturalProfile, aiDifficulty]);

  // Inicializar o tabuleiro
  useEffect(() => {
    const game = engine();
    const initialState = game.getInitialState();
    setBoardState({
      ...boardState,
      pieces: new Map(Object.entries(initialState.pieces)),
      currentTurn: initialState.currentTurn
    });
  }, []);

  // Manipular clique em quadrado
  const handleSquareClick = async (square: string) => {
    if (isThinking || boardState.isCheckmate) return;

    const { selectedSquare, validMoves } = boardState;

    // Se não há quadrado selecionado, selecionar se houver peça da cor atual
    if (!selectedSquare) {
      const piece = boardState.pieces.get(square);
      if (piece && piece.color === boardState.currentTurn) {
        const moves = await engine().getValidMoves(square);
        setBoardState({
          ...boardState,
          selectedSquare: square,
          validMoves: moves
        });
      }
      return;
    }

    // Se o mesmo quadrado for clicado, desselecionar
    if (selectedSquare === square) {
      setBoardState({
        ...boardState,
        selectedSquare: null,
        validMoves: []
      });
      return;
    }

    // Se for um movimento válido, executar
    if (validMoves.includes(square)) {
      await executeMove(selectedSquare, square);
    } else {
      // Selecionar nova peça se for da cor atual
      const piece = boardState.pieces.get(square);
      if (piece && piece.color === boardState.currentTurn) {
        const moves = await engine().getValidMoves(square);
        setBoardState({
          ...boardState,
          selectedSquare: square,
          validMoves: moves
        });
      }
    }
  };

  // Executar movimento
  const executeMove = async (from: string, to: string) => {
    setIsThinking(true);

    try {
      const game = engine();
      const move: Move = { from, to, piece: boardState.pieces.get(from)!.type };
      
      // Executar movimento
      const result = await game.makeMove(move);
      
      // Atualizar estado do tabuleiro
      const newPieces = new Map(boardState.pieces);
      const piece = newPieces.get(from)!;
      newPieces.delete(from);
      newPieces.set(to, piece);

      // Verificar promoção de peão
      if (piece.type === 'pawn' && (to[1] === '8' || to[1] === '1')) {
        piece.type = 'queen'; // Promover para rainha por padrão
      }

      const newHistory = [...boardState.moveHistory, move];

      setBoardState({
        pieces: newPieces,
        selectedSquare: null,
        validMoves: [],
        currentTurn: boardState.currentTurn === 'white' ? 'black' : 'white',
        isCheck: result.isCheck || false,
        isCheckmate: result.isCheckmate || false,
        moveHistory: newHistory
      });

      // Gerar narrativa se habilitado
      if (enableNarrative) {
        const narrativeText = await game.generateNarrative(move, culturalTheme);
        setNarrative(narrativeText);
      }

      // Se for a vez da IA, fazer movimento
      if (!result.isCheckmate && boardState.currentTurn === 'white') {
        setTimeout(() => makeAIMove(), 1000);
      }
    } catch (error) {
      console.error('Erro ao executar movimento:', error);
    } finally {
      setIsThinking(false);
    }
  };

  // Fazer movimento da IA
  const makeAIMove = async () => {
    setIsThinking(true);

    try {
      const ai = new AdaptiveAI({
        difficulty: aiDifficulty,
        culturalProfile: culturalTheme
      });

      const bestMove = await ai.getBestMove(boardState);
      
      if (bestMove) {
        await executeMove(bestMove.from, bestMove.to);
      }
    } catch (error) {
      console.error('Erro no movimento da IA:', error);
    } finally {
      setIsThinking(false);
    }
  };

  // Renderizar quadrado do tabuleiro
  const renderSquare = (file: string, rank: string) => {
    const square = `${file}${rank}`;
    const piece = boardState.pieces.get(square);
    const isSelected = boardState.selectedSquare === square;
    const isValidMove = boardState.validMoves.includes(square);
    const isDark = (file.charCodeAt(0) + parseInt(rank)) % 2 === 0;

    const squareClasses = [
      'chess-square',
      isDark ? 'dark' : 'light',
      isSelected ? 'selected' : '',
      isValidMove ? 'valid-move' : '',
      boardState.isCheck && piece?.type === 'king' && piece?.color === boardState.currentTurn ? 'in-check' : ''
    ].filter(Boolean).join(' ');

    return (
      <div
        key={square}
        className={squareClasses}
        onClick={() => handleSquareClick(square)}
        data-square={square}
      >
        {piece && (
          <div className={`piece ${piece.color} ${piece.type}`}>
            {getPieceSymbol(piece.type, piece.color)}
          </div>
        )}
        {isValidMove && !piece && <div className="move-dot" />}
      </div>
    );
  };

  // Obter símbolo da peça
  const getPieceSymbol = (type: PieceType, color: Color): string => {
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
    return symbols[color][type];
  };

  return (
    <div className="chess-board-container">
      <CulturalTheme 
        culture={culturalTheme} 
        onThemeChange={setCulturalTheme}
      />
      
      <div className="chess-board">
        <div className="board-status">
          {boardState.isCheckmate && (
            <div className="checkmate">Xeque-mate!</div>
          )}
          {boardState.isCheck && !boardState.isCheckmate && (
            <div className="check">Xeque!</div>
          )}
          {isThinking && (
            <div className="thinking">IA pensando...</div>
          )}
          <div className="turn-indicator">
            Vez: {boardState.currentTurn === 'white' ? 'Brancas' : 'Pretas'}
          </div>
        </div>

        <div className="board-grid">
          {['8', '7', '6', '5', '4', '3', '2', '1'].map(rank => (
            <div key={rank} className="board-row">
              {['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map(file => 
                renderSquare(file, rank)
              )}
            </div>
          ))}
        </div>

        <div className="file-labels">
          {['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map(file => (
            <span key={file}>{file}</span>
          ))}
        </div>
      </div>

      {enableNarrative && narrative && (
        <NarrativeDisplay 
          narrative={narrative}
          culture={culturalTheme}
        />
      )}
    </div>
  );
};

export default ChessBoard;
