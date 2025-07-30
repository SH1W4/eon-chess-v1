# A Matemática do Xadrez - Documentação Técnica

## 1. Sistema de Coordenadas

### 1.1 Tabuleiro como Matriz
O tabuleiro de xadrez é representado matematicamente como uma matriz 8x8:
- Ranks (fileiras): 1-8 (bottom-to-top)
- Files (colunas): 1-8 (left-to-right, tradicionalmente a-h)
- Total de casas: 8 × 8 = 64 posições únicas

### 1.2 Conversão de Coordenadas
Notação algébrica para coordenadas matriciais:
```python
file = ord(algebraic_char) - ord('a') + 1  # a->1, b->2, ..., h->8
rank = int(algebraic_number)                # Mantém valor numérico
```

## 2. Vetores de Movimento

### 2.1 Vetores Direcionais Básicos
Representados como tuplas (Δrank, Δfile):
- Horizontal: (0, ±1)
- Vertical: (±1, 0)
- Diagonal: (±1, ±1)

### 2.2 Movimentos por Peça

#### 2.2.1 Torre
Vetores de movimento:
```python
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
```
Alcance: 1-7 casas em cada direção

#### 2.2.2 Bispo
Vetores de movimento:
```python
directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
```
Alcance: 1-7 casas em cada direção

#### 2.2.3 Rainha
Combinação dos vetores da Torre e Bispo:
```python
directions = [(0, ±1), (±1, 0), (±1, ±1)]  # 8 direções
```
Alcance: 1-7 casas em cada direção

#### 2.2.4 Cavalo
Vetores de movimento L:
```python
moves = [
    (2, 1), (2, -1),    # Movimento 2 vertical, 1 horizontal
    (-2, 1), (-2, -1),  # Movimento 2 vertical inverso, 1 horizontal
    (1, 2), (1, -2),    # Movimento 1 vertical, 2 horizontal
    (-1, 2), (-1, -2)   # Movimento 1 vertical inverso, 2 horizontal
]
```
Propriedade matemática: |Δrank| + |Δfile| = 3 com Δrank ≠ Δfile

#### 2.2.5 Rei
Vetores para todas as direções adjacentes:
```python
moves = [
    (1, 0), (1, 1), (0, 1), (-1, 1),
    (-1, 0), (-1, -1), (0, -1), (1, -1)
]
```
Propriedade: max(|Δrank|, |Δfile|) = 1

#### 2.2.6 Peão
Vetores de movimento:
- Avanço: (direction * 1, 0)
- Avanço duplo inicial: (direction * 2, 0)
- Captura: (direction * 1, ±1)
Onde direction = 1 para brancas, -1 para pretas

## 3. Cálculos de Movimento

### 3.1 Fórmula Geral de Movimento
Para uma posição inicial (r₁, f₁):
```
Nova posição = (r₁ + Δr * d, f₁ + Δf * d)
Onde:
- (Δr, Δf) é o vetor de direção
- d é a distância (1-7 para peças deslizantes)
```

### 3.2 Validação de Posição
Uma posição (r, f) é válida se:
```python
1 ≤ r ≤ 8 and 1 ≤ f ≤ 8
```

## 4. Cálculos de Ataque e Defesa

### 4.1 Linha de Visão
Para peças deslizantes, a linha de visão é calculada como:
```python
pontos_na_linha = [
    (r₁ + Δr * d, f₁ + Δf * d)
    para d em range(1, 8)
    até encontrar obstáculo
]
```

### 4.2 Área de Controle
Conjunto de todas as casas atacadas por uma peça:
```python
área_controle = {
    (r, f) para cada vetor de movimento
    onde (r, f) é uma posição válida
    e não bloqueada por peça amiga
}
```

## 5. Matemática do Xeque

### 5.1 Detecção de Xeque
```python
xeque = rei_pos ∈ união(área_controle(p) para p em peças_adversárias)
```

### 5.2 Bloqueio de Xeque
Para xeque por peça deslizante:
```python
casas_bloqueio = pontos_na_linha(peça_atacante, rei)
```

## 6. Otimizações Matemáticas

### 6.1 Bitboards
Representação do tabuleiro como inteiro de 64 bits:
```
posição = 1 << (rank * 8 + file)
ocupação = soma(posição(p) para p em peças)
```

### 6.2 Máscaras de Movimento
Pré-cálculo de movimentos possíveis:
```python
mascara_movimento[posição][tipo_peça] = conjunto_casas_alcançáveis
```

## 7. Análise de Complexidade

### 7.1 Espaço de Estados
- Posições iniciais: 32 peças em 64 casas
- Ramificação média: ~35 movimentos por posição
- Profundidade média de jogo: ~40 movimentos

### 7.2 Complexidade Computacional
- Geração de movimentos: O(n) onde n = número de peças
- Validação de xeque: O(p) onde p = peças adversárias
- Validação de movimento: O(1) para movimentos simples
- Validação completa com xeque: O(p * m) onde m = movimentos possíveis

## 8. Fórmulas Úteis

### 8.1 Distância entre Posições
```python
distância_manhattan = |r₂ - r₁| + |f₂ - f₁|
distância_chebyshev = max(|r₂ - r₁|, |f₂ - f₁|)
```

### 8.2 Interseção de Linhas
Para verificar se duas peças se atacam mutuamente:
```python
intercepta = (Δr₁/Δf₁ = Δr₂/Δf₂) para movimentos diagonais
intercepta = (Δr₁ = 0 and Δr₂ = 0) para horizontais
intercepta = (Δf₁ = 0 and Δf₂ = 0) para verticais
```

## 9. Considerações de Performance

### 9.1 Cache de Movimentos
```python
cache_key = hash(board_state)
cached_moves[cache_key] = movimentos_válidos
```

### 9.2 Pré-cálculo de Ataques
```python
ataques[tipo_peça][posição] = conjunto_casas_atacadas
```

## Conclusão
A matemática por trás do xadrez combina:
1. Geometria vetorial para movimentos
2. Teoria dos conjuntos para áreas de controle
3. Álgebra linear para transformações
4. Teoria dos grafos para análise de posições
5. Otimização combinatória para validações

Esta base matemática permite uma implementação eficiente e correta das regras do xadrez, além de fornecer fundamentos para análises mais avançadas e desenvolvimento de IA.
