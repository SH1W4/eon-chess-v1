# Changelog

## [0.2.1-rc.1] - 2025-08-09

### Compatibilidade e Infra de Testes
- Adicionados shims/aliases para compatibilidade com caminhos legados:
  - `src.core.quantum.*` reexporta implementações atuais
  - `narrative.engine_simple` e `narrative.engine.quantum_processor`
  - `cultural.cultures` expondo `persian_culture`, `mongol_culture`, `chinese_culture`
  - Alias `AEONOrchestrator` em `core/orchestration/aeon_orchestrator.py`
  - Compat de import para `traditional.models.models`
  - `AvaliadorPosicao` e método `avaliar()` com `EvaluationResult` (campos: `pontuacao_total`, `pontuacao_material`, `pontuacao_posicional`, `influencia_quantica`)
- Correções de indentação/sintaxe detectadas durante coleta do pytest.
- Status: suíte sob `tests/` em processo de migração; alguns testes já coletam, demais ajustes em andamento.

### Observações
- Esta é uma pré-release (rc) focada em alinhar compatibilidade de testes legados.
- Próximos passos: finalizar shims restantes, estabilizar coleta/execução completa e promover a release estável.

## [0.2.0] - 2025-08-08

### 🎯 Sistema Cultural
- ✨ Implementado banco de dados cultural completo com 15+ temas:
  - **Culturas Históricas**: Azteca, Viking, Samurai, Maia
  - **Épocas Temporais**: Medieval, Renascimento (Renaissance)  
  - **Temas Futuristas**: Neo-Tokyo 2050, Steampunk, Quantum Realm
  - **Culturas Regionais**: Oriental/Eastern, Nórdica (Nordic)
  - **Estilos Especiais**: Pirata, Espacial
- 🏺 Narrativas temáticas detalhadas para cada cultura
- 📝 Templates expansíveis e sistema de memória cultural
- 🔄 Configurado DOCSYNC para sincronização automática com Notion
- ✅ Implementada validação automatizada de conteúdo cultural

### 🏗️ Arquitetura e Organização
- 📁 Refatoração completa da estrutura do projeto
- 🗂️ Reorganização em diretórios: config/, docs/, scripts/, tests/
- 📋 Consolidação de scripts por categoria (setup, analysis, validation, workflow)
- 🧹 Limpeza de arquivos temporários e backup organizados
- 📖 Atualização completa de links e documentação

### 🔗 Integrações
- 🧠 Integração ARKITECT como motor do sistema adaptativo
- 🌐 Configuração NEXUS para gerenciamento de conectores
- 📊 Sistema DOCSYNC operacional para gestão de conhecimento
- 🔧 Conectores culturais implementados e validados

### 📚 Documentação
- 📝 Criação de índice abrangente de documentação
- 🎯 Documento de visão e impacto do projeto
- 📋 EAP (Estrutura Analítica do Projeto) completo
- 🔗 Correção e validação de todos os links do README
- 📊 Terminologia técnica refinada e padronizada

### 🛠️ DevOps e Qualidade
- 🔧 Configuração de arquivos de configuração organizados
- ✅ Sistema de validação cultural automatizado
- 📈 Métricas e monitoramento cultural implementados
- 🔄 Workflows ARQUIMAX e NEXUS configurados

### 🐛 Correções
- 🔧 Correção de histórico de commits (email consistency)
- 🔗 Correção de links quebrados na documentação
- 📁 Reorganização de arquivos de backup e temporários
- 🧹 Limpeza de arquivos desnecessários

## [0.1.0] - 2025-07-26

### Added
- Initial project structure and architecture
- Core chess engine module foundation
- AI pipeline infrastructure
- Integration framework setup
- Configuration system
- Documentation framework

### Structure
- Organized core modules: AI, Board, Game
- Established configuration management
- Set up development tooling
- Implemented test infrastructure
- Added monitoring capabilities

### Documentation
- Project structure documentation
- Development guidelines
- Architecture documentation
- Integration flows
- Module relationships

### Configuration
- Environment-specific configs (dev/prod)
- Monitoring setup
- Integration settings
- Framework configurations

### Development Setup
- Git workflow
- Testing framework
- Development tools
- Build system

For full details, see the [git_changes.diff](git_changes.diff) file.
