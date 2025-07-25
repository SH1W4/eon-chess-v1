# Guia de Desenvolvimento - AEON CHESS

## 🚀 Começando

Este guia contém instruções detalhadas para configurar e desenvolver o AEON CHESS.

### Pré-requisitos

- Python 3.11.0+
- Node.js 18.0.0+
- TypeScript 4.9.0+
- PostgreSQL 14+
- Redis 6+
- Stockfish 15+

### Configuração do Ambiente

1. Clone o repositório (privado):
```bash
git clone git@github.com:NEO_SH1W4/AEON_CHESS.git
cd AEON_CHESS
```

2. Crie e ative o ambiente virtual Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
npm install
```

4. Configure as variáveis de ambiente:
```bash
cp config/secrets.yaml.example config/secrets.yaml
# Edite config/secrets.yaml com suas configurações
```

5. Inicialize o banco de dados:
```bash
python scripts/setup_db.py
```

### 🏗️ Estrutura do Projeto

```
/AEON
├── src/                # Código fonte
│   ├── core/          # Núcleo do sistema
│   ├── ai/           # Sistema de IA adaptativa
│   ├── mind/         # AEON MIND - Coaching IA
│   ├── ui/           # Interface do usuário
│   ├── cultural/     # Elementos culturais
│   └── utils/        # Utilitários
...
```

### 🔄 Fluxo de Desenvolvimento

1. **Branches**:
   - `main`: Código em produção
   - `develop`: Branch principal de desenvolvimento
   - `feature/*`: Novas funcionalidades
   - `bugfix/*`: Correções de bugs
   - `hotfix/*`: Correções urgentes em produção

2. **Commits**:
   ```
   tipo(escopo): descrição curta

   Descrição longa explicando o que e por que (não o como).
   ```
   Tipos: feat, fix, docs, style, refactor, test, chore

3. **Pull Requests**:
   - Título descritivo
   - Descrição detalhada
   - Referência a issues relacionadas
   - Testes incluídos
   - Documentação atualizada

### 🧪 Testes

```bash
# Testes unitários
pytest src/tests/unit

# Testes de integração
pytest src/tests/integration

# Cobertura de testes
pytest --cov=src tests/
```

### 📚 Documentação

- Mantenha a documentação atualizada em `/docs`
- Siga o padrão estabelecido nos templates
- Use docstrings em todas as funções/classes
- Atualize o CHANGELOG.md

### 🔧 Scripts Úteis

```bash
# Ativar ambiente de desenvolvimento
./scripts/dev_setup.sh

# Gerar documentação
./scripts/generate_docs.sh

# Executar linters
./scripts/lint.sh

# Formatar código
./scripts/format.sh
```

### 🚨 Padrões de Código

- Use Black para formatação Python
- Use ESLint/Prettier para JavaScript/TypeScript
- Mantenha complexidade ciclomática < 10
- Cobertura de testes > 80%
- Docstrings em todas as funções públicas

### 🔍 Code Review

Checklist para revisão:
- [ ] Segue os padrões de código
- [ ] Testes adequados incluídos
- [ ] Documentação atualizada
- [ ] Sem problemas de segurança
- [ ] Performance adequada
- [ ] Código limpo e legível

### 🚀 Deploy

1. Staging:
   ```bash
   ./scripts/deploy_staging.sh
   ```

2. Produção:
   ```bash
   ./scripts/deploy_prod.sh
   ```

### 🎯 Objetivos de Qualidade

- Cobertura de testes: > 80%
- Tempo de resposta API: < 200ms
- Uptime: > 99.9%
- Taxa de erros: < 0.1%

### 📞 Suporte

- Issue Tracker: GitHub Issues
- Wiki: Documentação detalhada
- Chat: Discord do projeto

## 🛠️ Tecnologias Principais

- **Backend**: Python (FastAPI)
- **IA**: TensorFlow, PyTorch
- **Frontend**: TypeScript, React
- **Mobile**: React Native
- **Banco de Dados**: PostgreSQL, Redis
- **Cache**: Redis
- **Queue**: RabbitMQ
- **Monitoramento**: Datadog, Sentry

## 📜 Licença

Proprietária - Todos os direitos reservados
