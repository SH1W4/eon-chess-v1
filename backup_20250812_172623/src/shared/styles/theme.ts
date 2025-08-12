// Tema base compartilhado entre web e mobile
import { patterns } from './patterns';

const colors = {
  // Cores primárias
  primary: {
    50: '#E6F6FF',
    100: '#BAE3FF',
    200: '#7CC4FA',
    300: '#47A3F3',
    400: '#2186EB',
    500: '#0967D2',
    600: '#0552B5',
    700: '#03449E',
    800: '#01337D',
    900: '#002159',
  },

  // Cores do tabuleiro
  board: {
    light: '#F0D9B5',
    dark: '#B58863',
    selected: '#829769',
    possible: '#BACA44',
    highlight: '#F7EC59',
    lastMove: '#AAD0B3',
  },

  // Cores de feedback
  feedback: {
    success: '#059669',
    warning: '#D97706',
    error: '#DC2626',
    info: '#3B82F6',
  },

  // Cores de interface
  interface: {
    background: '#1A1A1A',
    surface: '#2A2A2A',
    border: '#404040',
    text: {
      primary: '#FFFFFF',
      secondary: '#A3A3A3',
      disabled: '#666666',
    },
  },

  // Cores culturais (temas específicos)
  cultural: {
    medieval: {
      primary: '#794C24',
      secondary: '#C69C6D',
      accent: '#8B4513',
    },
    renaissance: {
      primary: '#4A90E2',
      secondary: '#D4E4F7',
      accent: '#2D9CDB',
    },
    modern: {
      primary: '#6B7280',
      secondary: '#E5E7EB',
      accent: '#4B5563',
    },
    ancient: {
      primary: '#B8860B',
      secondary: '#FFD700',
      accent: '#DAA520',
    },
  },
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const typography = {
  fontFamily: {
    sans: 'Inter, system-ui, sans-serif',
    serif: 'Merriweather, Georgia, serif',
    mono: 'JetBrains Mono, monospace',
  },
  fontSize: {
    xs: 12,
    sm: 14,
    md: 16,
    lg: 18,
    xl: 20,
    xxl: 24,
    display: 32,
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
};

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
};

export const transitions = {
  ease: 'cubic-bezier(0.4, 0, 0.2, 1)',
  duration: {
    fast: 150,
    normal: 250,
    slow: 350,
  },
};

export const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  xxl: 1536,
};

// Configurações específicas do tabuleiro
export const boardConfig = {
  animationDuration: 200,
  pieceScale: {
    default: 1,
    hover: 1.1,
    dragging: 1.2,
  },
  moveIndicator: {
    size: 12,
    opacity: 0.8,
  },
};

// Configurações culturais
export const culturalConfig = {
  medieval: {
    boardStyle: {
      light: colors.cultural.medieval.secondary,
      dark: colors.cultural.medieval.primary,
      accent: colors.cultural.medieval.accent,
    },
    pieceStyle: 'traditional',
    backgroundPattern: patterns.castle,
  },
  renaissance: {
    boardStyle: {
      light: colors.cultural.renaissance.secondary,
      dark: colors.cultural.renaissance.primary,
      accent: colors.cultural.renaissance.accent,
    },
    pieceStyle: 'artistic',
    backgroundPattern: patterns.floral,
  },
  modern: {
    boardStyle: {
      light: colors.cultural.modern.secondary,
      dark: colors.cultural.modern.primary,
      accent: colors.cultural.modern.accent,
    },
    pieceStyle: 'minimalist',
    backgroundPattern: patterns.geometric,
  },
  ancient: {
    boardStyle: {
      light: colors.cultural.ancient.secondary,
      dark: colors.cultural.ancient.primary,
      accent: colors.cultural.ancient.accent,
    },
    pieceStyle: 'hieroglyphic',
    backgroundPattern: patterns.papyrus,
  },
};

// Exporta o tema completo
export const theme = {
  colors: {
    ...colors,
    emerald: {
      50: '#ecfdf5',
      100: '#d1fae5',
      200: '#a7f3d0',
      300: '#6ee7b7',
      400: '#34d399',
      500: '#10b981',
      600: '#059669',
      700: '#047857',
      800: '#065f46',
      900: '#064e3b',
    }
  },
  colors,
  spacing,
  typography,
  shadows,
  transitions,
  breakpoints,
  boardConfig,
  culturalConfig,
};

export type Theme = typeof theme;

// Utilitário para acessar o tema com type safety
export const getThemeValue = <T extends keyof Theme>(
  key: T,
  ...path: string[]
): any => {
  let value: any = theme[key];
  for (const p of path) {
    value = value?.[p];
  }
  return value;
};
