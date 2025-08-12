import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius, Shadows } from '../constants/theme';

const CulturalScreen: React.FC = () => {
  const [selectedFilter, setSelectedFilter] = useState('all');

  const filters = [
    { id: 'all', name: 'Todos', icon: 'apps' as const },
    { id: 'history', name: 'História', icon: 'time' as const },
    { id: 'philosophy', name: 'Filosofia', icon: 'bulb' as const },
    { id: 'masters', name: 'Mestres', icon: 'people' as const },
    { id: 'culture', name: 'Cultura', icon: 'globe' as const },
  ];

  const culturalContent = [
    {
      id: 1,
      title: 'A Origem do Xadrez na Índia',
      category: 'history',
      readTime: '8 min',
      difficulty: 'Iniciante',
      description: 'Descubra como o Chaturanga evoluiu para o xadrez moderno',
      image: '🏛️',
    },
    {
      id: 2,
      title: 'A Filosofia de Capablanca',
      category: 'philosophy',
      readTime: '12 min',
      difficulty: 'Intermediário',
      description: 'Os princípios fundamentais do jogo posicional',
      image: '🤔',
    },
    {
      id: 3,
      title: 'Garry Kasparov: O Ogro de Baku',
      category: 'masters',
      readTime: '15 min',
      difficulty: 'Avançado',
      description: 'A vida e carreira do maior jogador de todos os tempos',
      image: '👑',
    },
    {
      id: 4,
      title: 'Xadrez na Literatura Russa',
      category: 'culture',
      readTime: '10 min',
      difficulty: 'Intermediário',
      description: 'Como o xadrez influenciou grandes obras literárias',
      image: '📚',
    },
    {
      id: 5,
      title: 'O Sacrifício da Dama: Arte ou Ciência?',
      category: 'philosophy',
      readTime: '6 min',
      difficulty: 'Avançado',
      description: 'Quando a intuição supera o cálculo',
      image: '♛',
    },
  ];

  const filteredContent = selectedFilter === 'all' 
    ? culturalContent 
    : culturalContent.filter(item => item.category === selectedFilter);

  const renderFilterButton = (filter: typeof filters[0]) => (
    <TouchableOpacity
      key={filter.id}
      style={[
        styles.filterButton,
        selectedFilter === filter.id && styles.selectedFilter
      ]}
      onPress={() => setSelectedFilter(filter.id)}
    >
      <Ionicons 
        name={filter.icon} 
        size={16} 
        color={selectedFilter === filter.id ? Colors.text : Colors.textMuted} 
      />
      <Text style={[
        styles.filterText,
        selectedFilter === filter.id && styles.selectedFilterText
      ]}>
        {filter.name}
      </Text>
    </TouchableOpacity>
  );

  const renderContentCard = (item: typeof culturalContent[0]) => (
    <TouchableOpacity key={item.id} style={styles.contentCard}>
      <View style={styles.contentImage}>
        <Text style={styles.contentEmoji}>{item.image}</Text>
      </View>
      
      <View style={styles.contentInfo}>
        <View style={styles.contentHeader}>
          <Text style={styles.contentTitle}>{item.title}</Text>
          <View style={[
            styles.difficultyBadge,
            item.difficulty === 'Iniciante' && styles.beginnerBadge,
            item.difficulty === 'Intermediário' && styles.intermediateBadge,
            item.difficulty === 'Avançado' && styles.advancedBadge,
          ]}>
            <Text style={styles.difficultyText}>{item.difficulty}</Text>
          </View>
        </View>
        
        <Text style={styles.contentDescription}>{item.description}</Text>
        
        <View style={styles.contentFooter}>
          <Text style={styles.readTime}>📖 {item.readTime}</Text>
          <Ionicons name="chevron-forward" size={16} color={Colors.textMuted} />
        </View>
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
        <Text style={styles.headerTitle}>Narrativas Culturais</Text>
        <Text style={styles.headerSubtitle}>
          Explore a rica história e filosofia do xadrez
        </Text>
      </LinearGradient>

      {/* Featured Story */}
      <View style={styles.featuredSection}>
        <Text style={styles.sectionTitle}>História em Destaque</Text>
        <TouchableOpacity style={styles.featuredCard}>
          <LinearGradient
            colors={[Colors.secondary, Colors.warning]}
            style={styles.featuredGradient}
          >
            <View style={styles.featuredContent}>
              <Text style={styles.featuredEmoji}>⚔️</Text>
              <Text style={styles.featuredTitle}>
                A Partida do Século: Fischer vs Spassky
              </Text>
              <Text style={styles.featuredDescription}>
                Reviva o duelo épico que transcendeu o xadrez e se tornou 
                símbolo da Guerra Fria
              </Text>
              <View style={styles.featuredFooter}>
                <Text style={styles.featuredTime}>20 min de leitura</Text>
                <Ionicons name="star" size={16} color={Colors.text} />
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {/* Filters */}
      <View style={styles.filtersSection}>
        <Text style={styles.sectionTitle}>Categorias</Text>
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          style={styles.filtersContainer}
        >
          {filters.map(renderFilterButton)}
        </ScrollView>
      </View>

      {/* Content List */}
      <View style={styles.contentSection}>
        <Text style={styles.sectionTitle}>
          {selectedFilter === 'all' ? 'Todo Conteúdo' : 
           filters.find(f => f.id === selectedFilter)?.name}
        </Text>
        {filteredContent.map(renderContentCard)}
      </View>

      {/* Cultural Events */}
      <View style={styles.eventsSection}>
        <Text style={styles.sectionTitle}>Eventos Culturais</Text>
        <View style={styles.eventCard}>
          <Ionicons name="calendar" size={24} color={Colors.secondary} />
          <View style={styles.eventContent}>
            <Text style={styles.eventTitle}>Semana Capablanca</Text>
            <Text style={styles.eventDescription}>
              Celebre o legado do gênio cubano com conteúdo especial
            </Text>
            <Text style={styles.eventDate}>15-22 de Novembro</Text>
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
    textAlign: 'center',
  },
  featuredSection: {
    padding: Spacing.lg,
  },
  sectionTitle: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.md,
  },
  featuredCard: {
    borderRadius: BorderRadius.lg,
    overflow: 'hidden',
    ...Shadows.lg,
  },
  featuredGradient: {
    padding: Spacing.xl,
  },
  featuredContent: {
    alignItems: 'center',
  },
  featuredEmoji: {
    fontSize: 48,
    marginBottom: Spacing.md,
  },
  featuredTitle: {
    fontSize: Typography.sizes.xl,
    fontWeight: Typography.weights.bold,
    color: Colors.text,
    textAlign: 'center',
    marginBottom: Spacing.sm,
  },
  featuredDescription: {
    fontSize: Typography.sizes.md,
    color: Colors.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: Spacing.md,
  },
  featuredFooter: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  featuredTime: {
    fontSize: Typography.sizes.sm,
    color: Colors.text,
    marginRight: Spacing.sm,
  },
  filtersSection: {
    paddingHorizontal: Spacing.lg,
    paddingBottom: Spacing.md,
  },
  filtersContainer: {
    flexDirection: 'row',
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderRadius: BorderRadius.md,
    marginRight: Spacing.sm,
  },
  selectedFilter: {
    backgroundColor: Colors.primary,
  },
  filterText: {
    color: Colors.textMuted,
    marginLeft: Spacing.xs,
    fontSize: Typography.sizes.sm,
  },
  selectedFilterText: {
    color: Colors.text,
  },
  contentSection: {
    padding: Spacing.lg,
  },
  contentCard: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    borderRadius: BorderRadius.lg,
    marginBottom: Spacing.md,
    overflow: 'hidden',
    ...Shadows.sm,
  },
  contentImage: {
    width: 80,
    height: 80,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Colors.primary,
  },
  contentEmoji: {
    fontSize: 32,
  },
  contentInfo: {
    flex: 1,
    padding: Spacing.md,
  },
  contentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: Spacing.sm,
  },
  contentTitle: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    flex: 1,
    marginRight: Spacing.sm,
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
  contentDescription: {
    fontSize: Typography.sizes.sm,
    color: Colors.textSecondary,
    lineHeight: 18,
    marginBottom: Spacing.sm,
  },
  contentFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  readTime: {
    fontSize: Typography.sizes.sm,
    color: Colors.textMuted,
  },
  eventsSection: {
    padding: Spacing.lg,
  },
  eventCard: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    padding: Spacing.lg,
    borderRadius: BorderRadius.lg,
    ...Shadows.sm,
  },
  eventContent: {
    flex: 1,
    marginLeft: Spacing.md,
  },
  eventTitle: {
    fontSize: Typography.sizes.md,
    fontWeight: Typography.weights.semibold,
    color: Colors.text,
    marginBottom: Spacing.sm,
  },
  eventDescription: {
    fontSize: Typography.sizes.sm,
    color: Colors.textSecondary,
    lineHeight: 18,
    marginBottom: Spacing.sm,
  },
  eventDate: {
    fontSize: Typography.sizes.sm,
    color: Colors.secondary,
    fontWeight: Typography.weights.medium,
  },
});

export default CulturalScreen;

