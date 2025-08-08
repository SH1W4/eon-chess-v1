import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Modal,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';

import { useGameStore } from '../stores/gameStore';
import { ChessBoard } from '../components/chess/ChessBoard';
import { Colors, Spacing, Typography, BorderRadius, Shadows } from '../constants/theme';
import { RootStackParamList } from '../navigation/AppNavigator';

type GameScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Game'>;
type GameScreenRouteProp = {
  params?: {
    gameMode?: string;
  };
};

const GameScreen: React.FC = () => {
  const navigation = useNavigation<GameScreenNavigationProp>();
  const route = useRoute<GameScreenRouteProp>();
  const [showMoveHistory, setShowMoveHistory] = useState(false);
  const [showAICoaching, setShowAICoaching] = useState(false);

  const {
    currentGame,
    isThinking,
    showAnalysis,
    toggleAnalysis,
    resetGame,
    startNewGame,
  } = useGameStore();

  useEffect(() => {
    // If no current game and gameMode is provided, start a new game
    if (!currentGame && route.params?.gameMode) {
      startNewGame(route.params.gameMode as any);
    }
  }, [currentGame, route.params?.gameMode, startNewGame]);

  const handleResignGame = () => {
    Alert.alert(
      'Desistir da Partida',
      'Tem certeza que deseja desistir desta partida?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Desistir',
          style: 'destructive',
          onPress: () => {
            resetGame();
            navigation.goBack();
          },
        },
      ]
    );
  };

  const handleOfferDraw = () => {
    Alert.alert(
      'Oferecer Empate',
      'Deseja oferecer empate ao seu oponente?',
      [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Oferecer', onPress: () => console.log('Draw offered') },
      ]
    );
  };

  const renderGameControls = () => (
    <View style={styles.gameControls}>
      <TouchableOpacity
        style={[styles.controlButton, styles.analysisButton]}
        onPress={toggleAnalysis}
      >
        <Ionicons 
          name={showAnalysis ? 'analytics' : 'analytics-outline'} 
          size={20} 
          color={Colors.text} 
        />
        <Text style={styles.controlButtonText}>
          {showAnalysis ? 'Ocultar' : 'Análise'}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.controlButton, styles.historyButton]}
        onPress={() => setShowMoveHistory(true)}
      >
        <Ionicons name="list" size={20} color={Colors.text} />
        <Text style={styles.controlButtonText}>Histórico</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.controlButton, styles.coachButton]}
        onPress={() => setShowAICoaching(true)}
      >
        <Ionicons name="brain" size={20} color={Colors.text} />
        <Text style={styles.controlButtonText}>Coach IA</Text>
      </TouchableOpacity>
    </View>
  );

  const renderGameActions = () => (
    <View style={styles.gameActions}>
      <TouchableOpacity
        style={[styles.actionButton, styles.drawButton]}
        onPress={handleOfferDraw}
      >
        <Ionicons name="handshake" size={18} color={Colors.text} />
        <Text style={styles.actionButtonText}>Empate</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.actionButton, styles.resignButton]}
        onPress={handleResignGame}
      >
        <Ionicons name="flag" size={18} color={Colors.text} />
        <Text style={styles.actionButtonText}>Desistir</Text>
      </TouchableOpacity>
    </View>
  );

  const renderPlayerInfo = (color: 'white' | 'black') => {
    if (!currentGame) return null;
    
    const player = currentGame.players[color];
    const isCurrentPlayer = currentGame.board.currentPlayer === color;
    const capturedPieces = currentGame.board.moveHistory
      .filter(move => move.capturedPiece?.color === (color === 'white' ? 'black' : 'white'))
      .map(move => move.capturedPiece!);

    return (
      <View style={[
        styles.playerInfo,
        isCurrentPlayer && styles.activePlayer,
        color === 'black' && styles.topPlayer
      ]}>
        <View style={styles.playerDetails}>
          <Text style={styles.playerName}>{player.name}</Text>
          {player.rating && (
            <Text style={styles.playerRating}>({player.rating})</Text>
          )}
          {isThinking && isCurrentPlayer && player.isAI && (
            <View style={styles.thinkingIndicator}>
              <Text style={styles.thinkingText}>Pensando...</Text>
            </View>
          )}
        </View>
        
        {capturedPieces.length > 0 && (
          <View style={styles.capturedPieces}>
            {capturedPieces.map((piece, index) => (
              <Text key={index} style={styles.capturedPiece}>
                {piece.type === 'pawn' ? '♟' : 
                 piece.type === 'rook' ? '♜' :
                 piece.type === 'knight' ? '♞' :
                 piece.type === 'bishop' ? '♝' :
                 piece.type === 'queen' ? '♛' : '♚'}
              </Text>
            ))}
          </View>
        )}
      </View>
    );
  };

  const renderMoveHistoryModal = () => (
    <Modal
      visible={showMoveHistory}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Histórico de Movimentos</Text>
          <TouchableOpacity onPress={() => setShowMoveHistory(false)}>
            <Ionicons name="close" size={24} color={Colors.text} />
          </TouchableOpacity>
        </View>
        
        <ScrollView style={styles.moveHistoryList}>
          {currentGame?.board.moveHistory.map((move, index) => (
            <View key={index} style={styles.moveItem}>
              <Text style={styles.moveNumber}>{Math.floor(index / 2) + 1}.</Text>
              <Text style={styles.moveText}>
                {move.piece.type} {move.from.row},{move.from.col} → {move.to.row},{move.to.col}
              </Text>
            </View>
          ))}
        </ScrollView>
      </View>
    </Modal>
  );

  const renderAICoachingModal = () => (
    <Modal
      visible={showAICoaching}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>EstrategiX Coach</Text>
          <TouchableOpacity onPress={() => setShowAICoaching(false)}>
            <Ionicons name="close" size={24} color={Colors.text} />
          </TouchableOpacity>
        </View>
        
        <ScrollView style={styles.coachingContent}>
          <View style={styles.coachingCard}>
            <Ionicons name="lightbulb" size={24} color={Colors.secondary} />
            <Text style={styles.coachingTitle}>Dica Estratégica</Text>
            <Text style={styles.coachingText}>
              Considere desenvolver suas peças menores antes de mover a dama. 
              Isso criará uma base sólida para seu ataque.
            </Text>
          </View>
          
          <View style={styles.coachingCard}>
            <Ionicons name="target" size={24} color={Colors.accent} />
            <Text style={styles.coachingTitle}>Oportunidade Tática</Text>
            <Text style={styles.coachingText}>
              Há uma possibilidade de garfo com o cavalo na casa f7. 
              Analise esta jogada cuidadosamente.
            </Text>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );

  if (!currentGame) {
    return (
      <View style={styles.noGameContainer}>
        <Text style={styles.noGameText}>Nenhum jogo ativo</Text>
        <TouchableOpacity
          style={styles.startGameButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.startGameButtonText}>Voltar ao Início</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Top Player Info */}
      {renderPlayerInfo('black')}

      {/* Chess Board */}
      <View style={styles.boardContainer}>
        <ChessBoard />
      </View>

      {/* Bottom Player Info */}
      {renderPlayerInfo('white')}

      {/* Game Controls */}
      {renderGameControls()}

      {/* Game Actions */}
      {renderGameActions()}

      {/* Analysis Panel */}
      {showAnalysis && (
        <View style={styles.analysisPanel}>
          <Text style={styles.analysisPanelTitle}>Análise da Posição</Text>
          <Text style={styles.analysisText}>
            Avaliação: +0.3 (ligeira vantagem das brancas)
          </Text>
          <Text style={styles.analysisText}>
            Melhor jogada: Cf3 (desenvolvimento do cavalo)
          </Text>
        </View>
      )}

      {/* Modals */}
      {renderMoveHistoryModal()}
      {renderAICoachingModal()}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  noGameContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.background,
  },
  noGameText: {
    fontSize: Typography.sizes.lg,
    color: Colors.textMuted,
    marginBottom: Spacing.lg,
  },
  startGameButton: {
    backgroundColor: Colors.primary,
    paddingHorizontal: Spacing.xl,
    paddingVertical: Spacing.md,
    borderRadius: BorderRadius.md,
  },
  startGameButtonText: {
    color: Colors.text,
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
  },
  playerInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.primary,
  },
  topPlayer: {
    borderBottomWidth: 0,
    borderTopWidth: 1,
    borderTopColor: Colors.primary,
  },
  activePlayer: {
    backgroundColor: Colors.primary,
  },
  playerDetails: {
    flex: 1,
  },
  playerName: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
  },
  playerRating: {
    fontSize: Typography.sizes.sm,
    color: Colors.textMuted,
  },
  thinkingIndicator: {
    marginTop: Spacing.xs,
  },
  thinkingText: {
    fontSize: Typography.sizes.sm,
    color: Colors.secondary,
    fontStyle: 'italic',
  },
  capturedPieces: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  capturedPiece: {
    fontSize: 16,
    marginLeft: Spacing.xs,
  },
  boardContainer: {
    flex: 1,
    justifyContent: 'center',
  },
  gameControls: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    backgroundColor: Colors.surface,
  },
  controlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.md,
    minWidth: 80,
    justifyContent: 'center',
  },
  analysisButton: {
    backgroundColor: Colors.info,
  },
  historyButton: {
    backgroundColor: Colors.accent,
  },
  coachButton: {
    backgroundColor: Colors.secondary,
  },
  controlButtonText: {
    color: Colors.text,
    fontSize: Typography.sizes.sm,
    marginLeft: Spacing.xs,
    fontWeight: Typography.weights.medium,
  },
  gameActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    backgroundColor: Colors.background,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.md,
    borderWidth: 1,
  },
  drawButton: {
    borderColor: Colors.warning,
  },
  resignButton: {
    borderColor: Colors.error,
  },
  actionButtonText: {
    color: Colors.text,
    fontSize: Typography.sizes.sm,
    marginLeft: Spacing.xs,
  },
  analysisPanel: {
    backgroundColor: Colors.surface,
    padding: Spacing.md,
    borderTopWidth: 1,
    borderTopColor: Colors.primary,
  },
  analysisPanelTitle: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.sm,
  },
  analysisText: {
    fontSize: Typography.sizes.sm,
    color: Colors.textSecondary,
    marginBottom: Spacing.xs,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: Spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: Colors.primary,
  },
  modalTitle: {
    fontSize: Typography.sizes.lg,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
  },
  moveHistoryList: {
    flex: 1,
    padding: Spacing.lg,
  },
  moveItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: Spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: Colors.surface,
  },
  moveNumber: {
    fontSize: Typography.sizes.sm,
    fontWeight: Typography.weights.semibold,
    color: Colors.secondary,
    width: 30,
  },
  moveText: {
    fontSize: Typography.sizes.sm,
    color: Colors.text,
    flex: 1,
  },
  coachingContent: {
    flex: 1,
    padding: Spacing.lg,
  },
  coachingCard: {
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.md,
    ...Shadows.sm,
  },
  coachingTitle: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginTop: Spacing.sm,
    marginBottom: Spacing.sm,
  },
  coachingText: {
    fontSize: Typography.sizes.sm,
    color: Colors.textSecondary,
    lineHeight: 20,
  },
});

export default GameScreen;

