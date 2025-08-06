# Estrutura de Interface do CHESS

## Organização de Diretórios

```
src/
├── web/                    # Interface Web (React/Next.js)
│   ├── components/        # Componentes React reutilizáveis
│   │   ├── board/        # Componentes do tabuleiro
│   │   ├── ui/          # Componentes de UI genéricos
│   │   └── analysis/    # Componentes de análise
│   ├── screens/         # Páginas/Telas da aplicação
│   ├── hooks/           # Custom React Hooks
│   ├── contexts/        # Contextos React (estados globais)
│   ├── utils/           # Funções utilitárias
│   ├── styles/          # Estilos e temas
│   ├── api/             # Integrações com API
│   └── tests/           # Testes unitários e de integração
│
├── mobile/               # Interface Mobile (React Native)
│   ├── components/      # Componentes React Native
│   ├── screens/         # Telas do aplicativo
│   ├── hooks/           # Custom Hooks
│   ├── contexts/        # Contextos React Native
│   ├── utils/           # Funções utilitárias
│   ├── styles/          # Estilos e temas
│   ├── api/             # Integrações com API
│   └── tests/           # Testes
│
└── shared/              # Código compartilhado entre web e mobile
    ├── types/          # Tipos TypeScript
    ├── constants/      # Constantes compartilhadas
    └── utils/          # Funções utilitárias compartilhadas

```

## Principais Componentes

### Interface Web

- `components/board/`: Componentes relacionados ao tabuleiro de xadrez
  - `ChessBoard.tsx`: Tabuleiro principal
  - `Piece.tsx`: Componente de peça
  - `Square.tsx`: Componente de casa do tabuleiro
  - `MoveIndicator.tsx`: Indicadores de movimento

- `components/analysis/`: Componentes de análise
  - `GameAnalysis.tsx`: Análise de partida
  - `MovesTimeline.tsx`: Linha do tempo de movimentos
  - `PositionEvaluation.tsx`: Avaliação de posição

- `components/ui/`: Componentes de UI
  - `Button.tsx`: Botões customizados
  - `Card.tsx`: Cards e containers
  - `Modal.tsx`: Modais e popups

### Interface Mobile

Segue a mesma estrutura da web, mas adaptada para React Native:

- `components/board/`: Versão mobile do tabuleiro
- `components/analysis/`: Análises adaptadas para mobile
- `components/ui/`: Componentes UI mobile-first

## Convenções de Código

1. **Nomenclatura**:
   - Componentes: PascalCase (ex: ChessBoard.tsx)
   - Funções/Hooks: camelCase (ex: useGameState.ts)
   - Constantes: SNAKE_CASE (ex: BOARD_SIZE)

2. **Imports**:
   - Absolutos para módulos externos
   - Relativos para módulos internos
   - Agrupados por tipo (React, componentes, utils, etc.)

3. **Estilos**:
   - Web: Tailwind CSS para componentes
   - Mobile: StyleSheet do React Native
   - Temas compartilhados em `styles/theme`

4. **Estado**:
   - Global: React Context
   - Local: useState/useReducer
   - Cache: React Query

5. **Testes**:
   - Jest para testes unitários
   - React Testing Library para testes de componente
   - Cypress para testes E2E (web)

## Integração com ARQUIMAX

A interface se integra com o ARQUIMAX através dos seguintes pontos:

1. **Monitoramento**:
   - Coleta de métricas de uso
   - Health checks da interface
   - Logs de performance

2. **Análise**:
   - Integração com sistema de análise arquitetural
   - Feedback em tempo real
   - Métricas de qualidade

3. **Cache**:
   - Sistema de cache distribuído
   - Invalidação seletiva
   - Warm-up automático

## Desenvolvimento

1. **Setup do Ambiente**:
   ```bash
   # Web
   cd src/web
   npm install
   npm run dev

   # Mobile
   cd src/mobile
   npm install
   npm run start
   ```

2. **Build**:
   ```bash
   # Web
   npm run build

   # Mobile
   npm run build:android
   npm run build:ios
   ```

3. **Testes**:
   ```bash
   # Unitários
   npm run test

   # E2E
   npm run test:e2e
   ```

## Considerações de Performance

1. **Code Splitting**:
   - Lazy loading de componentes pesados
   - Chunking otimizado de bundles
   - Prefetch de rotas comuns

2. **Otimizações**:
   - Memoização de componentes (useMemo, useCallback)
   - Virtualização de listas longas
   - Compressão de assets

3. **Cache**:
   - Service Workers (web)
   - AsyncStorage (mobile)
   - Cache de API com React Query
