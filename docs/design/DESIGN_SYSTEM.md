# Sistema de Design - AEON Chess

## Introdução

O Sistema de Design do AEON Chess estabelece os princípios visuais, componentes e padrões que criam uma experiência unificada e adaptativa. Este documento serve como fonte única de verdade para todas as decisões de design.

## Princípios Fundamentais

### 1. Adaptabilidade Temporal
O design evolui com o jogador, refletindo seu crescimento e estilo único.

### 2. Clareza Estratégica
Informação apresentada de forma clara, priorizando decisões táticas.

### 3. Imersão Narrativa
Elementos visuais que suportam e amplificam a narrativa emergente.

### 4. Elegância Atemporal
Design sofisticado que honra a tradição do xadrez enquanto abraça inovação.

## Identidade Visual

### Logotipo e Marca

```svg
<!-- AEON Chess Logo Structure -->
<svg viewBox="0 0 200 200">
  <!-- Símbolo Infinito + Rei -->
  <path d="M50,100 C50,50 100,50 100,100 S150,150 150,100 S100,50 100,100"/>
  <!-- Coroa estilizada -->
  <path d="M80,40 L100,20 L120,40"/>
</svg>
```

### Paleta de Cores

#### Cores Primárias
```scss
// Modo Clássico
$obsidian: #0A0E1A;      // Base profunda
$ivory: #F8F4E6;         // Contraste elegante
$gold: #D4AF37;          // Realce premium
$crimson: #8B0000;       // Ação crítica

// Modo Adaptativo
$quantum-blue: #00D4FF;   // Estado quântico
$neural-purple: #8B5CF6;  // Processamento IA
$temporal-green: #10B981; // Fluxo temporal
$void-black: #000000;     // Profundidade infinita
```

#### Paletas Temáticas

```typescript
interface ThemePalette {
  name: string;
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  text: string;
}

const themes: ThemePalette[] = [
  {
    name: 'Clássico',
    primary: '#0A0E1A',
    secondary: '#F8F4E6',
    accent: '#D4AF37',
    background: '#1A1A1A',
    surface: '#2A2A2A',
    text: '#FFFFFF'
  },
  {
    name: 'Aurora',
    primary: '#1E3A5F',
    secondary: '#4A7C7E',
    accent: '#F4A460',
    background: '#0F1419',
    surface: '#1C2833',
    text: '#E8E8E8'
  },
  {
    name: 'Cyberpunk',
    primary: '#FF00FF',
    secondary: '#00FFFF',
    accent: '#FFFF00',
    background: '#0A0A0A',
    surface: '#1A0A1A',
    text: '#FF00FF'
  }
];
```

### Tipografia

#### Hierarquia Tipográfica

```css
/* Família de Fontes */
--font-display: 'Cinzel', serif;        /* Títulos épicos */
--font-primary: 'Inter', sans-serif;    /* Interface principal */
--font-mono: 'JetBrains Mono', monospace; /* Notação, código */
--font-narrative: 'Crimson Text', serif; /* Narrativas */

/* Escala Tipográfica */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
```

#### Estilos de Texto

```scss
// Títulos
.heading-epic {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: var(--text-5xl);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background: linear-gradient(135deg, $gold 0%, $ivory 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

// Interface
.text-interface {
  font-family: var(--font-primary);
  font-weight: 400;
  font-size: var(--text-base);
  line-height: 1.5;
  color: var(--text-primary);
}

// Notação
.notation {
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: var(--text-sm);
  letter-spacing: 0.05em;
}
```

## Grid e Layout

### Sistema de Grid

```css
/* Grid Base - 8px */
--grid-unit: 8px;
--spacing-xs: calc(var(--grid-unit) * 0.5);  /* 4px */
--spacing-sm: var(--grid-unit);              /* 8px */
--spacing-md: calc(var(--grid-unit) * 2);    /* 16px */
--spacing-lg: calc(var(--grid-unit) * 3);    /* 24px */
--spacing-xl: calc(var(--grid-unit) * 4);    /* 32px */
--spacing-2xl: calc(var(--grid-unit) * 6);   /* 48px */
--spacing-3xl: calc(var(--grid-unit) * 8);   /* 64px */
```

### Layouts Responsivos

```scss
// Breakpoints
$breakpoints: (
  'mobile': 320px,
  'tablet': 768px,
  'desktop': 1024px,
  'wide': 1440px,
  'ultrawide': 1920px
);

// Container System
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
  
  @media (min-width: 768px) {
    max-width: 750px;
  }
  
  @media (min-width: 1024px) {
    max-width: 1000px;
  }
  
  @media (min-width: 1440px) {
    max-width: 1400px;
  }
}

// Grid Layout
.game-layout {
  display: grid;
  gap: var(--spacing-lg);
  
  @media (min-width: 1024px) {
    grid-template-columns: 300px 1fr 300px;
    grid-template-areas:
      "sidebar-left board sidebar-right"
      "history board analysis";
  }
}
```

## Componentes

### Tabuleiro de Xadrez

```typescript
interface BoardTheme {
  lightSquare: string;
  darkSquare: string;
  highlight: string;
  lastMove: string;
  check: string;
  border: string;
  coordinates: string;
}

const boardThemes: Record<string, BoardTheme> = {
  classic: {
    lightSquare: '#F0D9B5',
    darkSquare: '#B58863',
    highlight: 'rgba(255, 255, 0, 0.5)',
    lastMove: 'rgba(155, 199, 0, 0.4)',
    check: 'rgba(255, 0, 0, 0.5)',
    border: '#8B4513',
    coordinates: '#8B4513'
  },
  aeon: {
    lightSquare: '#E8E8E8',
    darkSquare: '#2A2A2A',
    highlight: 'rgba(0, 212, 255, 0.5)',
    lastMove: 'rgba(139, 92, 246, 0.4)',
    check: 'rgba(255, 0, 127, 0.5)',
    border: '#0A0E1A',
    coordinates: '#D4AF37'
  }
};
```

### Peças de Xadrez

```scss
// Estilos de Peças
.chess-piece {
  width: var(--square-size);
  height: var(--square-size);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &.dragging {
    cursor: grabbing;
    z-index: 1000;
    transform: scale(1.1);
    filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.5));
  }
  
  &.captured {
    animation: fade-out 0.5s ease-out;
    opacity: 0;
  }
  
  &.promoted {
    animation: glow-promotion 1s ease-in-out;
  }
}

@keyframes glow-promotion {
  0%, 100% { filter: drop-shadow(0 0 0 transparent); }
  50% { filter: drop-shadow(0 0 20px var(--gold)); }
}
```

### Cards e Containers

```tsx
// Card Component
const Card: React.FC<CardProps> = ({ 
  variant = 'default',
  elevated = false,
  interactive = false,
  children 
}) => {
  return (
    <div className={cn(
      'card',
      `card--${variant}`,
      elevated && 'card--elevated',
      interactive && 'card--interactive'
    )}>
      {children}
    </div>
  );
};

// Estilos
.card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--border);
  
  &--elevated {
    box-shadow: 
      0 10px 25px rgba(0, 0, 0, 0.1),
      0 6px 10px rgba(0, 0, 0, 0.08);
  }
  
  &--interactive {
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 
        0 14px 28px rgba(0, 0, 0, 0.12),
        0 10px 14px rgba(0, 0, 0, 0.08);
    }
  }
}
```

### Botões

```scss
// Sistema de Botões
.btn {
  font-family: var(--font-primary);
  font-weight: 500;
  border-radius: var(--radius-md);
  padding: var(--spacing-sm) var(--spacing-lg);
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  
  // Variantes
  &--primary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border: none;
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
  
  &--ghost {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
    
    &:hover {
      background: var(--surface-hover);
      border-color: var(--border-hover);
    }
  }
  
  &--danger {
    background: var(--danger);
    color: white;
    
    &:hover {
      background: var(--danger-dark);
    }
  }
  
  // Tamanhos
  &--sm {
    padding: var(--spacing-xs) var(--spacing-md);
    font-size: var(--text-sm);
  }
  
  &--lg {
    padding: var(--spacing-md) var(--spacing-xl);
    font-size: var(--text-lg);
  }
  
  // Estados
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  &.loading {
    color: transparent;
    
    &::after {
      content: '';
      position: absolute;
      width: 16px;
      height: 16px;
      margin: auto;
      border: 2px solid transparent;
      border-radius: 50%;
      border-top-color: white;
      animation: spin 0.6s linear infinite;
    }
  }
}
```

## Animações e Transições

### Biblioteca de Animações

```css
/* Transições Base */
--transition-fast: 150ms ease;
--transition-base: 250ms ease;
--transition-slow: 350ms ease;
--transition-slower: 500ms ease;

/* Curvas de Bezier */
--ease-in-out-quart: cubic-bezier(0.77, 0, 0.175, 1);
--ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
```

### Animações de Interface

```scss
// Entrada suave
@keyframes fade-in {
  from { 
    opacity: 0;
    transform: translateY(10px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

// Pulse para atenção
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

// Rotação contínua
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

// Onda de energia
@keyframes energy-wave {
  0% {
    box-shadow: 0 0 0 0 rgba(var(--primary-rgb), 0.7);
  }
  70% {
    box-shadow: 0 0 0 20px rgba(var(--primary-rgb), 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(var(--primary-rgb), 0);
  }
}
```

### Micro-interações

```typescript
// Feedback háptico visual
const microInteractions = {
  hover: {
    scale: 1.02,
    transition: 'all 0.2s ease'
  },
  click: {
    scale: 0.98,
    transition: 'all 0.1s ease'
  },
  success: {
    animation: 'success-bounce 0.5s ease'
  },
  error: {
    animation: 'error-shake 0.5s ease'
  }
};
```

## Ícones e Ilustrações

### Sistema de Ícones

```tsx
// Biblioteca de ícones customizados
const ChessIcons = {
  king: '♔',
  queen: '♕',
  rook: '♖',
  bishop: '♗',
  knight: '♘',
  pawn: '♙',
  
  // Ícones de interface
  play: '▶',
  pause: '⏸',
  stop: '⏹',
  settings: '⚙',
  analysis: '📊',
  history: '📜',
  
  // Estados
  check: '⚠',
  checkmate: '🏁',
  draw: '🤝',
  timeout: '⏰'
};
```

### Ilustrações Temáticas

```scss
// Backgrounds ilustrados
.illustration-bg {
  &--opening {
    background-image: 
      radial-gradient(circle at 20% 80%, rgba(var(--primary-rgb), 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(var(--accent-rgb), 0.1) 0%, transparent 50%);
  }
  
  &--endgame {
    background-image: 
      linear-gradient(180deg, transparent 0%, rgba(var(--primary-rgb), 0.05) 100%);
  }
  
  &--victory {
    background-image: 
      radial-gradient(circle at center, rgba(var(--gold-rgb), 0.2) 0%, transparent 70%);
  }
}
```

## Estados e Feedback

### Estados de Interface

```typescript
interface UIState {
  idle: 'default';
  hover: 'highlighted';
  active: 'pressed';
  focus: 'focused';
  disabled: 'inactive';
  loading: 'processing';
  success: 'completed';
  error: 'failed';
  warning: 'attention';
}

// Estilos por estado
const stateStyles = {
  idle: {
    opacity: 1,
    cursor: 'pointer'
  },
  hover: {
    opacity: 0.9,
    transform: 'translateY(-1px)',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  },
  active: {
    transform: 'scale(0.98)'
  },
  disabled: {
    opacity: 0.5,
    cursor: 'not-allowed',
    pointerEvents: 'none'
  },
  loading: {
    cursor: 'wait',
    animation: 'pulse 1.5s infinite'
  }
};
```

### Sistema de Notificações

```tsx
// Componente de Toast
const Toast: React.FC<ToastProps> = ({ 
  type,
  message,
  duration = 3000 
}) => {
  const icons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ'
  };
  
  return (
    <div className={`toast toast--${type}`}>
      <span className="toast__icon">{icons[type]}</span>
      <span className="toast__message">{message}</span>
    </div>
  );
};

// Estilos
.toast {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  animation: slide-in 0.3s ease, slide-out 0.3s ease 2.7s;
  
  &--success {
    background: var(--success);
    color: white;
  }
  
  &--error {
    background: var(--danger);
    color: white;
  }
}
```

## Acessibilidade

### Diretrizes WCAG 2.1

```scss
// Contraste de cores
:root {
  --contrast-ratio-AA: 4.5;  // Texto normal
  --contrast-ratio-AAA: 7;   // Texto pequeno
  
  // Focus indicators
  --focus-outline: 2px solid var(--primary);
  --focus-offset: 2px;
}

// Focus visível
*:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-offset);
}

// Skip links
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--primary);
  color: white;
  padding: var(--spacing-sm);
  z-index: 100;
  
  &:focus {
    top: 0;
  }
}
```

### Suporte a Screen Readers

```html
<!-- Exemplo de markup acessível -->
<div role="application" aria-label="Tabuleiro de xadrez AEON">
  <div role="grid" aria-label="Tabuleiro">
    <div role="row">
      <div role="gridcell" 
           aria-label="Casa a8, torre preta"
           tabindex="0">
        <img src="black-rook.svg" alt="Torre preta" />
      </div>
    </div>
  </div>
  
  <!-- Live regions para atualizações -->
  <div aria-live="polite" aria-atomic="true">
    <span id="game-status">Vez das brancas</span>
  </div>
</div>
```

## Dark Mode e Temas

### Sistema de Temas

```typescript
interface ThemeConfig {
  name: string;
  mode: 'light' | 'dark' | 'auto';
  colors: ColorPalette;
  typography: TypographyScale;
  spacing: SpacingScale;
  shadows: ShadowScale;
}

// Implementação
const themeManager = {
  current: 'dark',
  
  apply(theme: string) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('preferred-theme', theme);
  },
  
  toggle() {
    const next = this.current === 'dark' ? 'light' : 'dark';
    this.apply(next);
  },
  
  detectPreference() {
    const stored = localStorage.getItem('preferred-theme');
    if (stored) return stored;
    
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDark ? 'dark' : 'light';
  }
};
```

### Variáveis de Tema

```css
/* Tema Claro */
[data-theme="light"] {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F5F5F5;
  --text-primary: #1A1A1A;
  --text-secondary: #666666;
  --border: #E0E0E0;
}

/* Tema Escuro */
[data-theme="dark"] {
  --bg-primary: #0A0E1A;
  --bg-secondary: #1A1E2A;
  --text-primary: #FFFFFF;
  --text-secondary: #A0A0A0;
  --border: #2A2E3A;
}

/* Tema Auto */
@media (prefers-color-scheme: dark) {
  [data-theme="auto"] {
    --bg-primary: #0A0E1A;
    /* ... */
  }
}
```

## Performance Visual

### Otimizações CSS

```scss
// GPU Acceleration
.animated-element {
  will-change: transform, opacity;
  transform: translateZ(0); // Force GPU layer
  backface-visibility: hidden;
}

// Contenção de layout
.container {
  contain: layout style paint;
}

// Font loading optimization
@font-face {
  font-family: 'Inter';
  font-display: swap; // FOUT > FOIT
  src: url('/fonts/inter.woff2') format('woff2');
}

// Critical CSS
/* Inline no HTML para renderização inicial */
.critical {
  /* Estilos essenciais para above-the-fold */
}
```

### Lazy Loading

```typescript
// Componentes lazy
const BoardAnalysis = lazy(() => import('./BoardAnalysis'));
const GameHistory = lazy(() => import('./GameHistory'));

// Imagens lazy
const LazyImage: React.FC<{src: string; alt: string}> = ({ src, alt }) => {
  return (
    <img 
      loading="lazy"
      src={src}
      alt={alt}
      decoding="async"
    />
  );
};
```

## Guia de Implementação

### Estrutura de Arquivos

```
styles/
├── base/
│   ├── reset.scss
│   ├── typography.scss
│   └── variables.scss
├── components/
│   ├── buttons.scss
│   ├── cards.scss
│   └── forms.scss
├── layouts/
│   ├── grid.scss
│   └── containers.scss
├── themes/
│   ├── dark.scss
│   └── light.scss
├── utilities/
│   ├── animations.scss
│   └── helpers.scss
└── main.scss
```

### Convenções de Nomenclatura

```scss
// BEM Methodology
.block {}
.block__element {}
.block--modifier {}

// Utility classes
.u-hidden {}
.u-text-center {}
.u-mt-lg {}

// State classes
.is-active {}
.is-disabled {}
.has-error {}
```

## Recursos e Assets

### Fontes
- **Display**: Cinzel (Google Fonts)
- **Interface**: Inter (Google Fonts)
- **Monospace**: JetBrains Mono
- **Narrative**: Crimson Text

### Ferramentas
- **Design**: Figma
- **Ícones**: Custom SVG library
- **Animações**: Framer Motion
- **CSS**: Tailwind CSS + Custom

### Referências
- [Material Design 3](https://m3.material.io/)
- [Human Interface Guidelines](https://developer.apple.com/design/)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)

---

*Sistema de Design em constante evolução, adaptando-se como o próprio AEON Chess.*
