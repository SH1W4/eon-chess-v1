import React from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useGameStore } from '../stores/gameStore';
import { Colors, Spacing, Typography, BorderRadius, Shadows } from '../constants/theme';

const ProfileScreen: React.FC = () => {
  const { currentUser, gameHistory } = useGameStore();

  const stats = {
    gamesPlayed: gameHistory.length,
    wins: gameHistory.filter(g => g.result === 'white_wins').length,
    draws: gameHistory.filter(g => g.result === 'draw').length,
    losses: gameHistory.filter(g => g.result === 'black_wins').length,
    winRate: gameHistory.length > 0 ? 
      Math.round((gameHistory.filter(g => g.result === 'white_wins').length / gameHistory.length) * 100) : 0,
  };

  const achievements = [
    { id: 1, title: 'Primeiro Jogo', description: 'Complete sua primeira partida', unlocked: true },
    { id: 2, title: 'Estrategista', description: 'Vença 10 partidas', unlocked: stats.wins >= 10 },
    { id: 3, title: 'Mestre Cultural', description: 'Leia 5 narrativas culturais', unlocked: false },
    { id: 4, title: 'Estudioso', description: 'Complete 20 lições de IA', unlocked: false },
  ];

  return (
    <ScrollView style={styles.container}>
      {/* Profile Header */}
      <LinearGradient
        colors={[Colors.primary, Colors.accent]}
        style={styles.profileHeader}
      >
        <View style={styles.avatarContainer}>
          <Text style={styles.avatarText}>
            {currentUser?.name?.charAt(0) || 'U'}
          </Text>
        </View>
        <Text style={styles.userName}>{currentUser?.name || 'Usuário'}</Text>
        <Text style={styles.userRating}>Rating: {currentUser?.rating || 1200}</Text>
      </LinearGradient>

      {/* Statistics */}
      <View style={styles.statsSection}>
        <Text style={styles.sectionTitle}>Estatísticas</Text>
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.gamesPlayed}</Text>
            <Text style={styles.statLabel}>Jogos</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.wins}</Text>
            <Text style={styles.statLabel}>Vitórias</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.draws}</Text>
            <Text style={styles.statLabel}>Empates</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statValue}>{stats.losses}</Text>
            <Text style={styles.statLabel}>Derrotas</Text>
          </View>
        </View>
        <View style={styles.winRateCard}>
          <Text style={styles.winRateLabel}>Taxa de Vitória</Text>
          <Text style={styles.winRateValue}>{stats.winRate}%</Text>
        </View>
      </View>

      {/* Achievements */}
      <View style={styles.achievementsSection}>
        <Text style={styles.sectionTitle}>Conquistas</Text>
        {achievements.map((achievement) => (
          <View key={achievement.id} style={[
            styles.achievementCard,
            !achievement.unlocked && styles.lockedAchievement
          ]}>
            <Ionicons 
              name={achievement.unlocked ? 'trophy' : 'lock-closed'} 
              size={24} 
              color={achievement.unlocked ? Colors.secondary : Colors.textMuted} 
            />
            <View style={styles.achievementContent}>
              <Text style={[
                styles.achievementTitle,
                !achievement.unlocked && styles.lockedText
              ]}>
                {achievement.title}
              </Text>
              <Text style={[
                styles.achievementDescription,
                !achievement.unlocked && styles.lockedText
              ]}>
                {achievement.description}
              </Text>
            </View>
          </View>
        ))}
      </View>

      {/* Settings */}
      <View style={styles.settingsSection}>
        <Text style={styles.sectionTitle}>Configurações</Text>
        <TouchableOpacity style={styles.settingItem}>
          <Ionicons name="person" size={20} color={Colors.textMuted} />
          <Text style={styles.settingText}>Editar Perfil</Text>
          <Ionicons name="chevron-forward" size={16} color={Colors.textMuted} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.settingItem}>
          <Ionicons name="notifications" size={20} color={Colors.textMuted} />
          <Text style={styles.settingText}>Notificações</Text>
          <Ionicons name="chevron-forward" size={16} color={Colors.textMuted} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.settingItem}>
          <Ionicons name="help-circle" size={20} color={Colors.textMuted} />
          <Text style={styles.settingText}>Ajuda</Text>
          <Ionicons name="chevron-forward" size={16} color={Colors.textMuted} />
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  profileHeader: {
    alignItems: 'center',
    padding: Spacing.xl,
  },
  avatarContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: Colors.secondary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: Spacing.md,
  },
  avatarText: {
    fontSize: Typography.sizes.xxxl,
    fontWeight: Typography.weights.bold,
    color: Colors.text,
  },
  userName: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.sm,
  },
  userRating: {
    fontSize: Typography.sizes.md,
    color: Colors.textSecondary,
  },
  statsSection: {
    padding: Spacing.lg,
  },
  sectionTitle: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.md,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: Spacing.md,
  },
  statCard: {
    backgroundColor: Colors.surface,
    padding: Spacing.md,
    borderRadius: BorderRadius.lg,
    alignItems: 'center',
    width: '48%',
    marginBottom: Spacing.sm,
    ...Shadows.sm,
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
  winRateCard: {
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    alignItems: 'center',
    ...Shadows.sm,
  },
  winRateLabel: {
    fontSize: Typography.sizes.md,
    color: Colors.textMuted,
    marginBottom: Spacing.sm,
  },
  winRateValue: {
    fontSize: Typography.sizes.xxxl,
    fontWeight: Typography.weights.bold,
    color: Colors.accent,
  },
  achievementsSection: {
    padding: Spacing.lg,
  },
  achievementCard: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.md,
    alignItems: 'center',
    ...Shadows.sm,
  },
  lockedAchievement: {
    opacity: 0.6,
  },
  achievementContent: {
    flex: 1,
    marginLeft: Spacing.md,
  },
  achievementTitle: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.xs,
  },
  achievementDescription: {
    fontSize: Typography.sizes.sm,
    color: Colors.textSecondary,
  },
  lockedText: {
    color: Colors.textMuted,
  },
  settingsSection: {
    padding: Spacing.lg,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.sm,
    ...Shadows.sm,
  },
  settingText: {
    flex: 1,
    fontSize: Typography.sizes.md,
    color: Colors.text,
    marginLeft: Spacing.md,
  },
});

export default ProfileScreen;

