import React, { useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';

import { useGameStore } from '../stores/gameStore';
import { ChessBoard } from '../components/chess/ChessBoard';
import { Colors, Spacing, Typography, BorderRadius, Shadows } from '../constants/theme';
import { RootStackParamList } from '../navigation/AppNavigator';

const { width } = Dimensions.get('window');

type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList>;

const HomeScreen: React.FC = () => {
  const navigation = useNavigation<HomeScreenNavigationProp>();
  const { 
    currentGame, 
    currentUser, 
    startNewGame, 
    setUser,
    gameHistory 
  } = useGameStore();

  useEffect(() => {
    // Initialize demo user if none exists
    if (!currentUser) {
      setUser({
        id: 'demo_user',
        name: 'Jogador Demo',
        rating: 1200,
      });
    }
  }, [currentUser, setUser]);

  const handleNewGame = (mode: string) => {
    startNewGame(mode as any);
    navigation.navigate('Game', { gameMode: mode });
  };

  const handleContinueGame = () => {
    if (currentGame) {
      navigation.navigate('Game');
    }
  };

  const renderGameModeCard = (
    title: string,
    description: string,
    icon: keyof typeof Ionicons.glyphMap,
    mode: string,
    color: string
  ) => (
    <TouchableOpacity
      style={styles.gameModeCard}
      onPress={() => handleNewGame(mode)}
      activeOpacity={0.8}
    >
      <LinearGradient
        colors={[color, Colors.primary]}
        style={styles.gameModeGradient}
      >
        <View style={styles.gameModeContent}>
          <Ionicons name={icon} size={32} color={Colors.text} />
          <Text style={styles.gameModeTitle}>{title}</Text>
          <Text style={styles.gameModeDescription}>{description}</Text>
        </View>
      </LinearGradient>
    </TouchableOpacity>
  );

  const renderQuickStats = () => (
    <View style={styles.statsContainer}>
      <Text style={styles.sectionTitle}>Suas Estatísticas</Text>
      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{gameHistory.length}</Text>
          <Text style={styles.statLabel}>Jogos</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{currentUser?.rating || 1200}</Text>
          <Text style={styles.statLabel}>Rating</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>
            {gameHistory.filter(g => g.result === 'white_wins').length}
          </Text>
          <Text style={styles.statLabel}>Vitórias</Text>
        </View>
      </View>
    </View>
  );

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Welcome Section */}
      <LinearGradient
        colors={[Colors.primary, Colors.accent]}
        style={styles.welcomeSection}
      >
        <Text style={styles.welcomeTitle}>
          Bem-vindo ao XadrezMaster
        </Text>
        <Text style={styles.welcomeSubtitle}>
          Onde tradição encontra inovação
        </Text>
      </LinearGradient>

      {/* Current Game Section */}
      {currentGame && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Jogo Atual</Text>
          <View style={styles.currentGameCard}>
            <View style={styles.miniBoard}>
              <ChessBoard 
                interactive={false} 
                showCoordinates={false}
                highlightLastMove={true}
              />
            </View>
            <TouchableOpacity
              style={styles.continueButton}
              onPress={handleContinueGame}
            >
              <Text style={styles.continueButtonText}>Continuar Jogo</Text>
              <Ionicons name="play" size={20} color={Colors.text} />
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Game Modes Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Modos de Jogo</Text>
        <View style={styles.gameModesGrid}>
          {renderGameModeCard(
            'Casual',
            'Jogue relaxadamente contra a IA',
            'game-controller',
            'casual',
            Colors.accent
          )}
          {renderGameModeCard(
            'Ranqueado',
            'Teste suas habilidades',
            'trophy',
            'ranked',
            Colors.secondary
          )}
          {renderGameModeCard(
            'Treinamento',
            'Aprimore sua técnica',
            'school',
            'training',
            Colors.info
          )}
          {renderGameModeCard(
            'Cultural',
            'Explore a história do xadrez',
            'library',
            'cultural',
            Colors.warning
          )}
        </View>
      </View>

      {/* Quick Stats */}
      {renderQuickStats()}

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Ações Rápidas</Text>
        <View style={styles.quickActions}>
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => navigation.navigate('Analysis')}
          >
            <Ionicons name="analytics" size={24} color={Colors.secondary} />
            <Text style={styles.actionButtonText}>Análise</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => navigation.navigate('Settings')}
          >
            <Ionicons name="settings" size={24} color={Colors.secondary} />
            <Text style={styles.actionButtonText}>Configurações</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  welcomeSection: {
    padding: Spacing.xl,
    alignItems: 'center',
    marginBottom: Spacing.lg,
  },
  welcomeTitle: {
    fontSize: Typography.sizes.xxxl,
    fontWeight: Typography.weights.bold,
    color: Colors.text,
    textAlign: 'center',
    marginBottom: Spacing.sm,
  },
  welcomeSubtitle: {
    fontSize: Typography.sizes.lg,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  section: {
    padding: Spacing.lg,
    marginBottom: Spacing.md,
  },
  sectionTitle: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.md,
  },
  currentGameCard: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.md,
    ...Shadows.md,
  },
  miniBoard: {
    transform: [{ scale: 0.6 }],
    alignSelf: 'center',
  },
  continueButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.primary,
    padding: Spacing.md,
    borderRadius: BorderRadius.md,
    marginTop: Spacing.sm,
  },
  continueButtonText: {
    color: Colors.text,
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    marginRight: Spacing.sm,
  },
  gameModesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  gameModeCard: {
    width: (width - Spacing.lg * 3) / 2,
    marginBottom: Spacing.md,
    borderRadius: BorderRadius.lg,
    overflow: 'hidden',
    ...Shadows.md,
  },
  gameModeGradient: {
    padding: Spacing.lg,
    minHeight: 120,
  },
  gameModeContent: {
    alignItems: 'center',
  },
  gameModeTitle: {
    fontSize: Typography.sizes.lg,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginTop: Spacing.sm,
    marginBottom: Spacing.xs,
  },
  gameModeDescription: {
    fontSize: Typography.sizes.sm,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  statsContainer: {
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    padding: Spacing.lg,
    ...Shadows.md,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statCard: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: Typography.sizes.xxl,
    fontWeight: Typography.weights.bold,
    color: Colors.secondary,
  },
  statLabel: {
    fontSize: Typography.sizes.sm,
    color: Colors.textMuted,
    marginTop: Spacing.xs,
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    alignItems: 'center',
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    minWidth: 100,
    ...Shadows.sm,
  },
  actionButtonText: {
    color: Colors.text,
    fontSize: Typography.sizes.sm,
    marginTop: Spacing.sm,
    fontWeight: Typography.weights.medium,
  },
});

export default HomeScreen;

