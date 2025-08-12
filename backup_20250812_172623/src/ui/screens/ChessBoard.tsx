import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useGameStore } from '../../stores/gameStore';
import { ChessPosition, ChessPiece } from '../../types/chess';
import { Colors, Spacing, BorderRadius, Shadows } from '../../constants/theme';
import { 
  getPieceSymbol, 
  getSquareColor, 
  isSamePosition,
  getPossibleMoves 
} from '../../utils/chessUtils';

const { width } = Dimensions.get('window');
const BOARD_SIZE = width - Spacing.lg * 2;
const SQUARE_SIZE = BOARD_SIZE / 8;

interface ChessBoardProps {
  interactive?: boolean;
  showCoordinates?: boolean;
  highlightLastMove?: boolean;
}

export const ChessBoard: React.FC<ChessBoardProps> = ({
  interactive = true,
  showCoordinates = true,
  highlightLastMove = true,
}) => {
  const {
    currentGame,
    selectedSquare,
    possibleMoves,
    selectSquare,
    clearSelection,
  } = useGameStore();

  if (!currentGame) {
    return (
      <View style={styles.emptyBoard}>
        <Text style={styles.emptyText}>Nenhum jogo ativo</Text>
      </View>
    );
  }

  const { board } = currentGame;
  const lastMove = board.moveHistory[board.moveHistory.length - 1];

  const handleSquarePress = (row: number, col: number) => {
    if (!interactive) return;
    
    const position: ChessPosition = { row, col };
    selectSquare(position);
  };

  const isSquareSelected = (row: number, col: number): boolean => {
    return selectedSquare ? isSamePosition(selectedSquare, { row, col }) : false;
  };

  const isSquarePossibleMove = (row: number, col: number): boolean => {
    return possibleMoves.some(move => isSamePosition(move, { row, col }));
  };

  const isSquareLastMove = (row: number, col: number): boolean => {
    if (!highlightLastMove || !lastMove) return false;
    return (
      isSamePosition(lastMove.from, { row, col }) ||
      isSamePosition(lastMove.to, { row, col })
    );
  };

  const getSquareStyle = (row: number, col: number) => {
    const baseColor = getSquareColor(row, col) === 'light' ? '#F0D9B5' : '#B58863';
    const isSelected = isSquareSelected(row, col);
    const isPossibleMove = isSquarePossibleMove(row, col);
    const isLastMove = isSquareLastMove(row, col);

    let backgroundColor = baseColor;
    if (isSelected) {
      backgroundColor = Colors.accent;
    } else if (isLastMove) {
      backgroundColor = Colors.secondary;
    } else if (isPossibleMove) {
      backgroundColor = Colors.primary;
    }

    return {
      backgroundColor,
      opacity: isPossibleMove ? 0.7 : 1,
    };
  };

  const renderSquare = (row: number, col: number) => {
    const piece = board.squares[row][col];
    const squareStyle = getSquareStyle(row, col);
    const isPossibleMove = isSquarePossibleMove(row, col);

    return (
      <TouchableOpacity
        key={`${row}-${col}`}
        style={[styles.square, squareStyle]}
        onPress={() => handleSquarePress(row, col)}
        activeOpacity={0.7}
      >
        {piece && (
          <Text style={styles.piece}>
            {getPieceSymbol(piece)}
          </Text>
        )}
        {isPossibleMove && !piece && (
          <View style={styles.possibleMoveIndicator} />
        )}
        {isPossibleMove && piece && (
          <View style={styles.captureIndicator} />
        )}
        {showCoordinates && row === 7 && (
          <Text style={styles.fileLabel}>
            {String.fromCharCode(97 + col)}
          </Text>
        )}
        {showCoordinates && col === 0 && (
          <Text style={styles.rankLabel}>
            {8 - row}
          </Text>
        )}
      </TouchableOpacity>
    );
  };

  const renderRow = (row: number) => (
    <View key={row} style={styles.row}>
      {Array.from({ length: 8 }, (_, col) => renderSquare(row, col))}
    </View>
  );

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[Colors.primary, Colors.accent]}
        style={styles.boardContainer}
      >
        <View style={styles.board}>
          {Array.from({ length: 8 }, (_, row) => renderRow(row))}
        </View>
      </LinearGradient>
      
      {/* Game Info */}
      <View style={styles.gameInfo}>
        <Text style={styles.currentPlayer}>
          Vez: {board.currentPlayer === 'white' ? 'Brancas' : 'Pretas'}
        </Text>
        {board.isCheck && (
          <Text style={styles.checkWarning}>XEQUE!</Text>
        )}
        {board.isCheckmate && (
          <Text style={styles.checkmateWarning}>XEQUE-MATE!</Text>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: Spacing.md,
  },
  emptyBoard: {
    width: BOARD_SIZE,
    height: BOARD_SIZE,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
  },
  emptyText: {
    color: Colors.textMuted,
    fontSize: 16,
  },
  boardContainer: {
    padding: Spacing.sm,
    borderRadius: BorderRadius.lg,
    ...Shadows.lg,
  },
  board: {
    width: BOARD_SIZE,
    height: BOARD_SIZE,
    borderRadius: BorderRadius.md,
    overflow: 'hidden',
  },
  row: {
    flexDirection: 'row',
  },
  square: {
    width: SQUARE_SIZE,
    height: SQUARE_SIZE,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  piece: {
    fontSize: SQUARE_SIZE * 0.6,
    textAlign: 'center',
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  possibleMoveIndicator: {
    width: SQUARE_SIZE * 0.3,
    height: SQUARE_SIZE * 0.3,
    borderRadius: SQUARE_SIZE * 0.15,
    backgroundColor: Colors.accent,
    opacity: 0.8,
  },
  captureIndicator: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    borderWidth: 3,
    borderColor: Colors.accent,
    borderRadius: 4,
  },
  fileLabel: {
    position: 'absolute',
    bottom: 2,
    right: 2,
    fontSize: 10,
    color: Colors.textMuted,
    fontWeight: 'bold',
  },
  rankLabel: {
    position: 'absolute',
    top: 2,
    left: 2,
    fontSize: 10,
    color: Colors.textMuted,
    fontWeight: 'bold',
  },
  gameInfo: {
    marginTop: Spacing.md,
    alignItems: 'center',
  },
  currentPlayer: {
    color: Colors.text,
    fontSize: 18,
    fontWeight: '600',
    marginBottom: Spacing.sm,
  },
  checkWarning: {
    color: Colors.warning,
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  checkmateWarning: {
    color: Colors.error,
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});

