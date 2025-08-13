# Tabuleiro de Xadrez Funcional - Guia de Funcionalidades

## ✅ Funcionalidades Implementadas

### 1. **Movimentação de Peças**
- **Arrastar e Soltar**: Arraste qualquer peça para movê-la
- **Clique para Mover**: 
  - Clique em uma peça para selecioná-la
  - Os movimentos válidos serão destacados:
    - 🔵 **Círculo azul**: Casas vazias onde a peça pode se mover
    - 🔴 **Círculo vermelho**: Casas com peças adversárias (capturas possíveis)
    - 🟡 **Destaque dourado**: Peça selecionada atualmente
  - Clique em uma casa destacada para mover

### 2. **Validação de Movimentos**
- Todos os movimentos seguem as regras oficiais do xadrez
- Movimentos inválidos são automaticamente rejeitados
- A peça retorna à posição original se o movimento não for permitido

### 3. **Controles do Tabuleiro**
- **Botão "Desfazer"**: Desfaz o último movimento
- **Botão "Reset"**: Reinicia o jogo para a posição inicial

### 4. **Barra de Avaliação**
- Mostra visualmente o equilíbrio material da partida
- Exibe pontuação numérica (positiva = vantagem das Brancas)
- Atualiza dinamicamente após cada movimento

### 5. **Jogar Contra IA**
- Clique em "Jogar Agora" na navegação ou hero section
- Você joga com as peças Brancas
- A IA responde automaticamente aos seus movimentos
- **Níveis de IA disponíveis**:
  - Iniciante
  - Clube (padrão)
  - Mestre
- **Opção "IA Forte (Stockfish)"**: Ativa o engine Stockfish para análise mais profunda

### 6. **Análise Inteligente do Nível**
Durante a partida demonstrativa, o sistema analisa:
- Tempo de pensamento por jogada
- Precisão dos movimentos
- Habilidade tática
- Conhecimento de aberturas
- Estilo de jogo (agressivo, sólido, equilibrado)
- Estimativa de rating ELO

Após 8 movimentos, o sistema gera uma recomendação personalizada de plano baseada no seu nível detectado.

## 🎮 Como Usar

1. **Modo Exploração** (padrão):
   - Mova as peças livremente
   - Experimente diferentes posições
   - Use os controles para desfazer/resetar

2. **Modo Partida vs IA**:
   - Clique em "Jogar Agora"
   - Faça seu primeiro movimento (você é as Brancas)
   - A IA responderá automaticamente
   - Continue jogando e observe a análise em tempo real

3. **Visualizar Movimentos Possíveis**:
   - Clique em qualquer peça
   - Observe os destaques coloridos
   - Clique em uma casa destacada ou arraste a peça

## 🔧 Detalhes Técnicos

- **Biblioteca de Tabuleiro**: chessboard-element (Web Component)
- **Lógica de Xadrez**: chess.js
- **Engine IA**: Stockfish WASM (opcional)
- **Validação**: Todos os movimentos são validados pela chess.js
- **Responsivo**: Funciona em desktop e mobile

## 📍 Status e Narração

- **Linha de Status**: Mostra de quem é a vez e situações especiais (xeque, xeque-mate)
- **Narração Inteligente**: Durante partidas vs IA, exibe análise do seu nível e sugestões

Agora você tem um tabuleiro de xadrez totalmente funcional com todas as regras implementadas e destaque visual dos movimentos possíveis!
