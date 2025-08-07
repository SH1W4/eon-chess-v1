# Guia de Desenvolvimento - CHESS (Cultural Heritage & Evolution Symbiotic System)

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
git clone git@github.com:NEO_SH1W4/CHESS.git
cd CHESS
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
/CHESS
├── src/                # Código fonte
│   ├── core/          # Núcleo do sistema
│   │   ├── cultural_patterns.py    # Sistema de padrões culturais
│   │   ├── cultural_validation.py   # Validação de padrões
│   │   ├── cultural_training_data.py # Dados de treinamento
│   │   └── cultural_integration.py   # Integração cultural
│   ├── ai/           # Sistema de IA adaptativa
│   ├── cultural/     # Motor cultural e perfis
│   ├── ui/           # Interface do usuário
│   ├── symbiotic/    # Sistema simbiótico
│   └── utils/        # Utilitários
...
```

### 📊 Status dos Componentes

#### Sistema Cultural [Em Desenvolvimento]
- ✅ Sistema base de padrões culturais implementado
- ✅ Sistema de validação implementado
- ✅ Dados de treinamento e warm-up adicionados
- ✅ Integração com culturas existentes (Persa, Mongol, Chinesa, Viking, Samurai, Maia)
- ⏳ Testes unitários e de integração pendentes
- ⏳ Otimização de performance pendente

#### Sistema Narrativo [Em Desenvolvimento]
- ✅ Motor narrativo base
- ✅ Geração de eventos
- ⏳ Integração cultural-narrativa pendente
- ⏳ Validação de narrativas pendente

#### Sistema Simbiótico [Em Progresso]
- ✅ Framework base implementado
- ✅ Integração ARQUIMAX
- ⏳ Integração NEXUS pendente
- ⏳ Evolução adaptativa em desenvolvimento

#### Motor de Xadrez [Em Desenvolvimento]
- ✅ Implementação básica do tabuleiro
- ✅ Movimentação das peças implementada
- ✅ Framework base de avaliação de posição
- ⏳ Ajustes na avaliação de posição:
  - Melhorar avaliação de controle do centro
  - Refinar avaliação de estrutura de peões
  - Otimizar penalidades para peões isolados
  - Balancear pesos das avaliações
- ⏳ Testes unitários em andamento:
  - Testes de movimentação: 80% completo
  - Testes de avaliação: 40% completo
  - Testes de integração: 20% completo
- ⏳ Otimização de performance pendente

##### Critérios de Qualidade do Motor
- Precisão da avaliação de posição > 85%
- Tempo máximo de avaliação < 100ms por posição
- Cobertura de testes > 90%
- Profundidade mínima de análise: 4 movimentos

##### Integração com Outros Sistemas
- Sistema Cultural:
  - Adaptação do estilo de jogo baseado no perfil cultural
  - Pesos de avaliação ajustáveis por cultura
  - Biblioteca de aberturas culturalmente relevantes

- Sistema Narrativo:
  - Geração de comentários sobre movimentos
  - Identificação de momentos críticos do jogo
  - Integração com histórico de partidas

- Sistema Simbiótico:
  - Adaptação em tempo real do estilo de jogo
  - Aprendizado contínuo através do ARQUIMAX
  - Otimização via NEXUS

#### Próximas Prioridades
1. Corrigir avaliação de posição no motor de xadrez
2. Implementar aprendizado por reforço na IA adaptativa
3. Implementar testes para o sistema cultural
4. Completar integração cultural-narrativa
5. Otimizar performance de validação
6. Implementar auto-ajuste de parâmetros da IA
7. Expandir dados de treinamento
8. Otimizar performance do motor de xadrez

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

## 📊 Estrutura Analítica do Projeto (EAP)

### 1. Motor de Xadrez [60%]
1.1. Núcleo do Motor [85%]
   - ✅ Representação do tabuleiro
   - ✅ Regras e movimentação
   - ✅ Validação de movimentos
   - ⏳ Otimização de performance

1.2. Sistema de Avaliação [40%]
   - ✅ Framework base
   - 🔄 Avaliação de posição
   - 🔄 Estrutura de peões
   - ⏳ Avaliação estratégica

1.3. Testes e Qualidade [45%]
   - 🔄 Testes unitários
   - 🔄 Testes de integração
   - ⏳ Benchmarks

### 2. Sistema Cultural [70%]
2.1. Núcleo Cultural [90%]
   - ✅ Sistema de padrões
   - ✅ Perfis culturais
   - ✅ Validação
   - 🔄 Otimização

2.2. Integração [65%]
   - ✅ Interface básica
   - 🔄 Conectores culturais
   - ⏳ Adaptação dinâmica

2.3. Dados e Treinamento [55%]
   - ✅ Dataset base
   - 🔄 Expansão de dados
   - ⏳ Validação cruzada

### 3. Sistema Narrativo [45%]
3.1. Motor Narrativo [75%]
   - ✅ Geração básica
   - 🔄 Contextualização
   - ⏳ Personalização

3.2. Integração Cultural [30%]
   - 🔄 Interface cultural
   - ⏳ Adaptação narrativa
   - ⏳ Validação

3.3. Análise e Feedback [30%]
   - 🔄 Coleta de dados
   - ⏳ Análise de impacto
   - ⏳ Otimização

### 4. Sistema de IA Adaptativa [55%]
4.1. Núcleo de IA [70%]
   - ✅ Arquitetura neural base
   - ✅ Sistemas de inferência
   - 🔄 Otimização de modelos
   - ⏳ Auto-ajuste de parâmetros

4.2. Aprendizado [55%]
   - ✅ Pipeline de treinamento
   - 🔄 Aprendizado por reforço
   - 🔄 Adaptação dinâmica
   - ⏳ Meta-learning

4.3. Integração Cultural-Cognitiva [40%]
   - ✅ Interface cultural base
   - 🔄 Adaptação cultural
   - ⏳ Evolução cognitiva
   - ⏳ Auto-otimização

### 5. Sistema Simbiótico [50%]
4.1. Framework Base [85%]
   - ✅ ARQUIMAX
   - 🔄 NEXUS
   - 🔄 Integração

4.2. Evolução Adaptativa [35%]
   - 🔄 Aprendizado
   - ⏳ Otimização
   - ⏳ Validação

4.3. Monitoramento [30%]
   - 🔄 Métricas base
   - ⏳ Análise avançada
   - ⏳ Ajuste automático

Legenda:
✅ Completo
🔄 Em progresso
⏳ Pendente

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
