# Guia de Estilo - AEON Chess

## 🎨 Identidade Visual

### Cores

#### Cores Principais
```scss
$primary: #2C3E50     // Azul Profundo
$secondary: #E74C3C   // Vermelho Vibrante
$accent: #F1C40F      // Amarelo Energia
```

#### Tons Neutros
```scss
$dark: #1A1A1A        // Preto Rico
$light: #ECF0F1       // Branco Suave
$gray: #95A5A6        // Cinza Neutro
```

#### Cores de Feedback
```scss
$success: #2ECC71     // Verde Sucesso
$warning: #F39C12     // Laranja Alerta
$error: #C0392B       // Vermelho Erro
$info: #3498DB        // Azul Info
```

### Tipografia

#### Fontes
- Título Principal: **Quantum** (custom)
- Subtítulos: **Exo 2**
- Corpo: **Inter**
- Monospace: **JetBrains Mono**

#### Hierarquia
```scss
h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.75rem; }
h4 { font-size: 1.5rem; }
body { font-size: 1rem; }
small { font-size: 0.875rem; }
```

### Ícones e Símbolos

#### Sistema de Ícones
- Estilo: Outlined
- Peso: Regular
- Corner Radius: 2px
- Stroke: 1.5px

#### Símbolos Especiais
- Peças de Xadrez: Custom Vector
- Emblemas: Flat Design
- Badges: Circular com borda

## 🖼️ Interface

### Grid System
- Base: 8px
- Colunas: 12
- Gutters: 16px
- Margins: 24px

### Componentes

#### Botões
```scss
.button {
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: 600;
  transition: all 0.3s;
}

.button--primary {
  background: $primary;
  color: $light;
}

.button--secondary {
  background: transparent;
  border: 2px solid $primary;
}
```

#### Cards
```scss
.card {
  background: $light;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

#### Inputs
```scss
.input {
  padding: 8px 16px;
  border: 1px solid $gray;
  border-radius: 4px;
  font-size: 1rem;
}
```

### Espaçamento

#### Margins
```scss
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xl: 32px;
```

#### Padding
```scss
$padding-xs: 4px;
$padding-sm: 8px;
$padding-md: 16px;
$padding-lg: 24px;
$padding-xl: 32px;
```

## 🎮 Game UI

### HUD Elements

#### Barra de Status
- Posição: Superior
- Altura: 64px
- Background: Semi-transparente
- Informações: Vida, Energia, Score

#### Menu de Jogo
- Trigger: ESC
- Overlay: 70% opacidade
- Blur: 5px
- Animação: Fade (0.3s)

### Feedback Visual

#### Highlights
- Seleção: Borda pulsante
- Hover: Glow suave
- Ação: Flash rápido

#### Animações
- Entrada: 0.3s ease-out
- Saída: 0.2s ease-in
- Loop: 1s linear

## 📱 Responsividade

### Breakpoints
```scss
$mobile: 320px;
$tablet: 768px;
$desktop: 1024px;
$wide: 1440px;
```

### Adaptações
- Mobile: UI simplificada
- Tablet: Layout híbrido
- Desktop: UI completa
- Wide: Multiview support

## 🎥 Motion Design

### Transições

#### Page Transitions
- Tipo: Fade + Slide
- Duração: 0.4s
- Timing: ease-in-out

#### Component Transitions
- Tipo: Scale + Fade
- Duração: 0.2s
- Timing: ease-out

### Animações

#### Loading
- Spinner personalizado
- Duração: 1s
- Loop: Infinito
- Easing: linear

#### Feedback
- Success: Bounce
- Error: Shake
- Warning: Pulse

## 📸 Assets

### Texturas

#### Tabuleiro
- Resolution: 2048x2048
- Format: PNG
- Compression: Medium
- Mipmaps: Yes

#### Peças
- Resolution: 1024x1024
- Format: PNG
- Compression: Low
- Normal Maps: Yes

### Efeitos

#### Partículas
- Resolution: 512x512
- Format: PNG
- Transparency: Yes
- Atlas: 4x4

#### VFX
- Format: Sprite sheets
- FPS: 30
- Resolution: 256x256
- Compression: Low

## 📝 Guidelines de Conteúdo

### Textos

#### Tom de Voz
- Profissional mas amigável
- Direto e claro
- Inspirador
- Inclusivo

#### Nomenclatura
- Consistente
- Intuitiva
- Memorável
- Traduzível

### Localização

#### Suporte
- Português (BR)
- English (US)
- Español
- 日本語

#### Adaptações
- Culturais
- Linguísticas
- Visuais
- Monetização
