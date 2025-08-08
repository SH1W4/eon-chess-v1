export const Colors = {
  // Tema Esmeralda
  primary: '#005240',      // Verde esmeralda escuro
  secondary: '#DDA36C',    // Dourado
  accent: '#00A86B',       // Verde esmeralda claro
  
  // Cores de texto
  text: '#FFFFFF',         // Branco
  textSecondary: '#E0E0E0', // Cinza claro
  textMuted: '#B0B0B0',    // Cinza médio
  
  // Cores de fundo
  background: '#001A14',   // Verde muito escuro
  surface: '#002D20',      // Verde escuro médio
  card: '#003D2B',         // Verde médio
  
  // Estados
  success: '#4CAF50',
  warning: '#FF9800',
  error: '#F44336',
  info: '#2196F3',
  
  // Transparências
  overlay: 'rgba(0, 0, 0, 0.5)',
  glassmorphism: 'rgba(0, 82, 64, 0.1)',
};

export const Typography = {
  // Tamanhos de fonte
  sizes: {
    xs: 12,
    sm: 14,
    md: 16,
    lg: 18,
    xl: 20,
    xxl: 24,
    xxxl: 32,
    display: 48,
  },
  
  // Pesos de fonte
  weights: {
    light: '300' as const,
    regular: '400' as const,
    medium: '500' as const,
    semibold: '600' as const,
    bold: '700' as const,
  },
  
  // Famílias de fonte
  families: {
    regular: 'System',
    heading: 'System',
  },
};

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
  xxxl: 64,
};

export const BorderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  round: 50,
};

export const Shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.23,
    shadowRadius: 2.62,
    elevation: 4,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 8,
  },
};

export const Layout = {
  window: {
    width: 0, // Will be set dynamically
    height: 0, // Will be set dynamically
  },
  isSmallDevice: false, // Will be set dynamically
};

export const Animations = {
  timing: {
    fast: 200,
    normal: 300,
    slow: 500,
  },
  easing: {
    ease: 'ease',
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
  },
};

