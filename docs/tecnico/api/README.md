# API Reference - AEON Chess

## Visão Geral

A API do AEON Chess fornece interfaces para interagir com o motor de xadrez, sistema de IA adaptativa e recursos culturais.

## Endpoints Base

- Desenvolvimento: `http://localhost:3000/api/v1`
- Produção: `https://api.aeonchess.com/v1`

## Autenticação

```bash
POST /auth/login
POST /auth/refresh
POST /auth/logout
```

### Headers necessários
```
Authorization: Bearer <token>
Content-Type: application/json
```

## Endpoints do Motor de Xadrez

### Movimentos
```bash
# Obter movimentos válidos
GET /moves/valid
{
  "position": "fen_string",
  "piece": {"x": 0, "y": 0}
}

# Executar movimento
POST /moves/execute
{
  "from": {"x": 0, "y": 0},
  "to": {"x": 1, "y": 1}
}

# Validar movimento
POST /moves/validate
{
  "from": {"x": 0, "y": 0},
  "to": {"x": 1, "y": 1},
  "position": "fen_string"
}
```

### Posição
```bash
# Obter posição atual
GET /position/current

# Carregar posição específica
POST /position/load
{
  "fen": "fen_string"
}

# Avaliar posição
GET /position/evaluate
{
  "fen": "fen_string",
  "depth": 20
}
```

## API do Sistema de Análise

### Perfil Técnico
```bash
# Obter perfil do jogador
GET /analysis/profile/{player_id}

# Atualizar perfil
PUT /analysis/profile/{player_id}
{
  "tactical_style": 0.7,    # Preferência por jogo tático
  "positional_style": 0.5,  # Preferência por jogo posicional
  "dynamic_style": 0.3     # Preferência por posições dinâmicas
}

# Obter recomendações de análise
GET /analysis/recommendations
{
  "position": "fen_string",
  "profile_id": "player_profile_id"
}
```

### Sistema de Aprendizado
```bash
# Registrar análise de partida
POST /analysis/games/record
{
  "game_id": "uuid",
  "result": "win|loss|draw",
  "moves": ["e4", "e5", ...],
  "analysis": {
    "accuracy": 85.5,
    "critical_positions": [...],
    "improvement_areas": [...]
  }
}

# Atualizar modelo de análise
POST /analysis/model/update
{
  "profile_id": "player_profile_id",
  "training_data": {...}
}
```

## API de Escolas de Xadrez

### Conteúdo Técnico
```bash
# Obter material de estudo
GET /chess-school/content
{
  "category": "classical|modern|hypermodern",
  "language": "pt-BR|en-US",
  "school": "russian|italian|spanish"
}

# Adicionar material didático
POST /chess-school/content
{
  "type": "game_analysis|study_material|exercise",
  "school": "russian|italian|spanish",
  "content": {...},
  "metadata": {...}
}
```

### Progressão Técnica
```bash
# Registrar progresso de estudo
POST /chess-school/progress
{
  "content_id": "uuid",
  "type": "study|exercise|analysis",
  "results": {
    "accuracy": 85,
    "completion_time": 1200,
    "difficulty_level": "basic|intermediate|advanced"
  }
}

# Obter relatório de progressão
GET /chess-school/progress/{player_id}
```

## Websockets

### Eventos em Tempo Real
```javascript
// Conexão
ws://api.aeonchess.com/v1/ws

// Eventos
{
  "type": "move|analysis|suggestion|cultural",
  "data": {...},
  "timestamp": "ISO8601"
}
```

## Códigos de Erro

- 400: Requisição inválida
- 401: Não autorizado
- 403: Acesso negado
- 404: Recurso não encontrado
- 429: Muitas requisições
- 500: Erro interno do servidor

## Limites de Taxa

- 100 requisições/minuto para endpoints públicos
- 1000 requisições/minuto para endpoints autenticados
- 5000 requisições/dia por API key

## Formatos de Dados

### Posição FEN
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

### Movimento
```json
{
  "from": {
    "x": 0-7,
    "y": 0-7
  },
  "to": {
    "x": 0-7,
    "y": 0-7
  },
  "promotion": "q|r|b|n"  // opcional
}
```

### Perfil Técnico do Jogador
```json
{
  "id": "uuid",
  "playing_style": {
    "tactical": 0.0-1.0,      # Orientação tática
    "positional": 0.0-1.0,    # Orientação posicional
    "dynamic": 0.0-1.0        # Orientação dinâmica
  },
  "statistics": {
    "games_total": 0,
    "victories": 0,
    "defeats": 0,
    "draws": 0,
    "accuracy": {
      "tactical": 0.0-1.0,
      "positional": 0.0-1.0,
      "endgame": 0.0-1.0
    }
  },
  "technical_preferences": {
    "opening_repertoire": "classical|modern|hypermodern",
    "time_control": "bullet|blitz|rapid|classical",
    "study_focus": ["tactics", "strategy", "endgame"]
  },
  "chess_school": {
    "primary": "russian|italian|spanish",
    "influences": ["modern", "hypermodern"],
    "current_curriculum": {
      "level": "basic|intermediate|advanced",
      "focus_areas": ["pawn_structure", "piece_coordination"]
    }
  }
}
```

## Exemplos de Uso

### Curl
```bash
# Autenticação
curl -X POST https://api.aeonchess.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "player", "password": "secret"}'

# Obter movimentos válidos
curl https://api.aeonchess.com/v1/moves/valid \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"position": "fen_string", "piece": {"x": 0, "y": 0}}'
```

### Python
```python
import requests

# Configuração
API_URL = "https://api.aeonchess.com/v1"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Obter perfil
response = requests.get(
    f"{API_URL}/ai/profile/{player_id}",
    headers=headers
)

# Executar movimento
response = requests.post(
    f"{API_URL}/moves/execute",
    headers=headers,
    json={
        "from": {"x": 0, "y": 0},
        "to": {"x": 1, "y": 1}
    }
)
```

## Considerações de Segurança

1. Use HTTPS para todas as requisições
2. Mantenha tokens seguros
3. Implemente rate limiting
4. Valide todas as entradas
5. Use timeouts apropriados

## Suporte

- Email: api@aeonchess.com
- Documentação: https://docs.aeonchess.com
- Status: https://status.aeonchess.com
