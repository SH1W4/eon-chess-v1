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

## API da IA Adaptativa

### Perfil
```bash
# Obter perfil do jogador
GET /ai/profile/{player_id}

# Atualizar perfil
PUT /ai/profile/{player_id}
{
  "aggression": 0.7,
  "positional": 0.5,
  "risk_taking": 0.3
}

# Obter sugestões adaptativas
GET /ai/suggestions
{
  "position": "fen_string",
  "profile_id": "player_profile_id"
}
```

### Aprendizado
```bash
# Registrar resultado de partida
POST /ai/learning/game-result
{
  "game_id": "uuid",
  "result": "win|loss|draw",
  "moves": ["e4", "e5", ...]
}

# Atualizar modelo de aprendizado
POST /ai/learning/update
{
  "profile_id": "player_profile_id",
  "game_data": {...}
}
```

## API Cultural

### Conteúdo
```bash
# Obter elementos culturais
GET /cultural/elements
{
  "category": "historical|strategic|tactical",
  "language": "pt-BR|en-US"
}

# Adicionar elemento cultural
POST /cultural/elements
{
  "type": "story|lesson|challenge",
  "content": {...},
  "metadata": {...}
}
```

### Interação
```bash
# Registrar interação cultural
POST /cultural/interaction
{
  "element_id": "uuid",
  "type": "view|complete|share",
  "metadata": {...}
}

# Obter progresso cultural
GET /cultural/progress/{player_id}
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

### Perfil do Jogador
```json
{
  "id": "uuid",
  "style": {
    "aggression": 0.0-1.0,
    "positional": 0.0-1.0,
    "risk_taking": 0.0-1.0
  },
  "stats": {
    "games_played": 0,
    "wins": 0,
    "losses": 0,
    "draws": 0
  },
  "preferences": {
    "opening_style": "open|closed|dynamic",
    "time_control": "bullet|blitz|rapid|classical"
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
