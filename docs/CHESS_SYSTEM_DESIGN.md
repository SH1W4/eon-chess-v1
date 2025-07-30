# Sistema de Xadrez - Documentação de Design

## Visão Geral
Este documento detalha a implementação de um sistema de xadrez em Python, descrevendo a lógica do tabuleiro, movimento das peças e regras do jogo.

## Estrutura Base

### Enums Básicos
- **PieceType**: Enumera os tipos de peças (Rei, Rainha, Torre, Bispo, Cavalo, Peão)
- **Color**: Define as cores das peças (Branco, Preto)

### Classes Fundamentais

#### Position
Representa uma posição no tabuleiro usando coordenadas rank (1-8) e file (1-8).

**Características:**
- Imutável (frozen dataclass)
- Validação de coordenadas (1-8)
- Conversão de/para notação algébrica (ex: "e4")
- Implementação de hash e equals para uso em dicionários

#### Piece
Representa uma peça do xadrez.

**Atributos:**
- type: PieceType
- color: Color
- position: Position
- has_moved: bool (importante para movimentos especiais)

**Funcionalidades:**
- Símbolos ASCII para representação visual
- Rastreamento de movimento para regras especiais

#### Board
Classe principal que gerencia o estado do jogo.

**Estado:**
- pieces: Dict[Position, Piece] - Mapa de posições para peças
- captured_pieces: List[Piece] - Peças capturadas
- move_history: List[Tuple[Position, Position]] - Histórico de movimentos
- current_turn: Color - Cor que deve jogar

## Lógica de Movimento

### Regras Gerais
1. Verificação de turno
2. Validação de posição inicial/final
3. Verificação de xeque
4. Atualização do estado do tabuleiro

### Movimentos por Peça

#### Peão
- Movimento frontal (1 casa)
- Movimento duplo inicial
- Capturas diagonais
- (Pendente: En passant)
- (Pendente: Promoção)

#### Cavalo
- Movimento em L (2+1)
- Único que pode pular outras peças

#### Bispo
- Movimento diagonal
- Bloqueado por peças no caminho

#### Torre
- Movimento horizontal/vertical
- Bloqueado por peças no caminho
- Participa do roque

#### Rainha
- Combina movimentos de Torre e Bispo
- Bloqueada por peças no caminho

#### Rei
- Movimento de 1 casa em qualquer direção
- Roque (kingside e queenside)
- Não pode se mover para posição atacada

### Lógica de Xeque

#### Detecção de Xeque
1. Localiza o rei da cor atual
2. Para cada peça adversária:
   - Calcula movimentos possíveis
   - Verifica se algum alcança o rei
   - Considera bloqueios por outras peças

#### Validação de Movimento em Xeque
1. Faz movimento temporário
2. Verifica se ainda está em xeque
3. Reverte movimento se inválido

### Movimentos Especiais

#### Roque (Castling)
**Condições:**
- Rei e Torre não movidos
- Caminho livre entre eles
- Rei não em xeque
- Rei não atravessa casas atacadas
- Posições finais não atacadas

**Implementação:**
1. Verifica condições
2. Move Rei e Torre
3. Atualiza status has_moved

## Estados do Jogo

### Xeque-mate
Verificação:
1. Jogador está em xeque
2. Nenhum movimento legal disponível

### Empate (Stalemate)
Verificação:
1. Jogador não está em xeque
2. Nenhum movimento legal disponível

## Estrutura do Código

### Principais Métodos

#### Board
- `move_piece()`: Move peças e valida regras
- `is_in_check()`: Detecta situação de xeque
- `get_valid_moves()`: Lista movimentos válidos
- `_get_piece_moves_no_check()`: Movimentos básicos sem validação de xeque

### Validações
1. Posição dentro do tabuleiro
2. Turno correto
3. Movimento válido para a peça
4. Não deixa próprio rei em xeque
5. Respeita regras especiais

## Otimizações e Melhorias Futuras

### Otimizações Planejadas
1. Cache de movimentos válidos
2. Pré-cálculo de ataques
3. Bitboards para representação mais eficiente

### Funcionalidades Pendentes
1. En passant
2. Promoção de peão
3. Detecção de empate por:
   - Repetição
   - 50 movimentos
   - Material insuficiente

## Lições Aprendidas
1. Importância da imutabilidade (Position)
2. Separação de validações básicas/complexas
3. Manejo de estado temporário para validações
4. Complexidade das regras especiais

## Conclusão
O sistema demonstra a complexidade do xadrez através de uma implementação modular e extensível. Cada aspecto do jogo é cuidadosamente modelado e validado, permitindo uma experiência de jogo completa e correta.
