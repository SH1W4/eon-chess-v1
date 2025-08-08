import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius, Shadows } from '../constants/theme';

const AICoachScreen: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('tactics');

  const categories = [
    { id: 'tactics', name: 'Táticas', icon: 'flash' as const },
    { id: 'strategy', name: 'Estratégia', icon: 'map' as const },
    { id: 'openings', name: 'Aberturas', icon: 'play' as const },
    { id: 'endgame', name: 'Finais', icon: 'flag' as const },
  ];

  const lessons = {
    tactics: [
      { title: 'Garfo com Cavalo', difficulty: 'Iniciante', time: '10 min' },
      { title: 'Ataque Duplo', difficulty: 'Intermediário', time: '15 min' },
      { title: 'Cravada Absoluta', difficulty: 'Avançado', time: '20 min' },
    ],
    strategy: [
      { title: 'Controle do Centro', difficulty: 'Iniciante', time: '12 min' },
      { title: 'Estrutura de Peões', difficulty: 'Intermediário', time: '18 min' },
      { title: 'Jogo Posicional', difficulty: 'Avançado', time: '25 min' },
    ],
    openings: [
      { title: 'Abertura Italiana', difficulty: 'Iniciante', time: '15 min' },
      { title: 'Defesa Siciliana', difficulty: 'Intermediário', time: '20 min' },
      { title: 'Gambito da Dama', difficulty: 'Avançado', time: '30 min' },
    ],
    endgame: [
      { title: 'Rei e Torre vs Rei', difficulty: 'Iniciante', time: '10 min' },
      { title: 'Finais de Peões', difficulty: 'Intermediário', time: '15 min' },
      { title: 'Finais Complexos', difficulty: 'Avançado', time: '25 min' },
    ],
  };

  const renderCategoryButton = (category: typeof categories[0]) => (
    <TouchableOpacity
      key={category.id}
      style={[
        styles.categoryButton,
        selectedCategory === category.id && styles.selectedCategory
      ]}
      onPress={() => setSelectedCategory(category.id)}
    >
      <Ionicons 
        name={category.icon} 
        size={20} 
        color={selectedCategory === category.id ? Colors.text : Colors.textMuted} 
      />
      <Text style={[
        styles.categoryText,
        selectedCategory === category.id && styles.selectedCategoryText
      ]}>
        {category.name}
      </Text>
    </TouchableOpacity>
  );

  const renderLessonCard = (lesson: any, index: number) => (
    <TouchableOpacity key={index} style={styles.lessonCard}>
      <View style={styles.lessonHeader}>
        <Text style={styles.lessonTitle}>{lesson.title}</Text>
        <View style={[
          styles.difficultyBadge,
          lesson.difficulty === 'Iniciante' && styles.beginnerBadge,
          lesson.difficulty === 'Intermediário' && styles.intermediateBadge,
          lesson.difficulty === 'Avançado' && styles.advancedBadge,
        ]}>
          <Text style={styles.difficultyText}>{lesson.difficulty}</Text>
        </View>
      </View>
      <View style={styles.lessonFooter}>
        <Text style={styles.lessonTime}>⏱️ {lesson.time}</Text>
        <Ionicons name="chevron-forward" size={16} color={Colors.textMuted} />
      </View>
    </TouchableOpacity>
  );

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={[Colors.primary, Colors.accent]}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>EstrategiX Coach</Text>
        <Text style={styles.headerSubtitle}>
          Seu mentor pessoal de xadrez
        </Text>
      </LinearGradient>

      {/* Progress Overview */}
      <View style={styles.progressSection}>
        <Text style={styles.sectionTitle}>Seu Progresso</Text>
        <View style={styles.progressCards}>
          <View style={styles.progressCard}>
            <Text style={styles.progressValue}>85%</Text>
            <Text style={styles.progressLabel}>Táticas</Text>
          </View>
          <View style={styles.progressCard}>
            <Text style={styles.progressValue}>72%</Text>
            <Text style={styles.progressLabel}>Estratégia</Text>
          </View>
          <View style={styles.progressCard}>
            <Text style={styles.progressValue}>91%</Text>
            <Text style={styles.progressLabel}>Aberturas</Text>
          </View>
        </View>
      </View>

      {/* Categories */}
      <View style={styles.categoriesSection}>
        <Text style={styles.sectionTitle}>Categorias de Treinamento</Text>
        <View style={styles.categoriesContainer}>
          {categories.map(renderCategoryButton)}
        </View>
      </View>

      {/* Lessons */}
      <View style={styles.lessonsSection}>
        <Text style={styles.sectionTitle}>
          Lições de {categories.find(c => c.id === selectedCategory)?.name}
        </Text>
        {lessons[selectedCategory as keyof typeof lessons].map(renderLessonCard)}
      </View>

      {/* AI Insights */}
      <View style={styles.insightsSection}>
        <Text style={styles.sectionTitle}>Insights da IA</Text>
        <View style={styles.insightCard}>
          <Ionicons name="bulb" size={24} color={Colors.secondary} />
          <View style={styles.insightContent}>
            <Text style={styles.insightTitle}>Recomendação Personalizada</Text>
            <Text style={styles.insightText}>
              Baseado em suas últimas partidas, recomendo focar em finais de torre. 
              Você perdeu 3 posições vencedoras nesta área.
            </Text>
          </View>
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
  header: {
    padding: Spacing.xl,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: Typography.sizes.xxxl,
    fontWeight: Typography.weights.bold,
    color: Colors.text,
    marginBottom: Spacing.sm,
  },
  headerSubtitle: {
    fontSize: Typography.sizes.lg,
    color: Colors.textSecondary,
  },
  progressSection: {
    padding: Spacing.lg,
  },
  sectionTitle: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.md,
  },
  progressCards: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  progressCard: {
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    alignItems: 'center',
    flex: 1,
    marginHorizontal: Spacing.xs,
    ...Shadows.sm,
  },
  progressValue: {
    fontSize: Typography.sizes.xxl,
    fontWeight: Typography.weights.bold,
    color: Colors.secondary,
  },
  progressLabel: {
    fontSize: Typography.sizes.sm,
    color: Colors.textMuted,
    marginTop: Spacing.xs,
  },
  categoriesSection: {
    padding: Spacing.lg,
  },
  categoriesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  categoryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.md,
    marginBottom: Spacing.sm,
    minWidth: '48%',
    justifyContent: 'center',
  },
  selectedCategory: {
    backgroundColor: Colors.primary,
  },
  categoryText: {
    color: Colors.textMuted,
    marginLeft: Spacing.sm,
    fontSize: Typography.sizes.sm,
  },
  selectedCategoryText: {
    color: Colors.text,
  },
  lessonsSection: {
    padding: Spacing.lg,
  },
  lessonCard: {
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.md,
    ...Shadows.sm,
  },
  lessonHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Spacing.sm,
  },
  lessonTitle: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    flex: 1,
  },
  difficultyBadge: {
    paddingHorizontal: Spacing.sm,
    paddingVertical: Spacing.xs,
    borderRadius: BorderRadius.sm,
  },
  beginnerBadge: {
    backgroundColor: Colors.success,
  },
  intermediateBadge: {
    backgroundColor: Colors.warning,
  },
  advancedBadge: {
    backgroundColor: Colors.error,
  },
  difficultyText: {
    fontSize: Typography.sizes.xs,
    color: Colors.text,
    fontWeight: Typography.weights.medium,
  },
  lessonFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  lessonTime: {
    fontSize: Typography.sizes.sm,
    color: Colors.textMuted,
  },
  insightsSection: {
    padding: Spacing.lg,
  },
  insightCard: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    ...Shadows.sm,
  },
  insightContent: {
    flex: 1,
    marginLeft: Spacing.md,
  },
  insightTitle: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.sm,
  },
  insightText: {
    fontSize: Typography.sizes.sm,
    color: Colors.textSecondary,
    lineHeight: 20,
  },
});

export default AICoachScreen;

