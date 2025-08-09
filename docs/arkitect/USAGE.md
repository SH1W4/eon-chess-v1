# Arkitect - Guia de Uso

## Visão Geral

O Arkitect é um sistema simbiótico de análise arquitetural e evolução adaptativa, composto por dois componentes principais:

- **ARQUIMAX**: Sistema de análise arquitetural e monitoramento
- **NEXUS**: Sistema de integração adaptativa e evolução

## Comandos Disponíveis

### Via Makefile (Recomendado)

```bash
# Verificar status do sistema
make arkitect-status

# Iniciar integração completa
make arkitect-run

# Monitorar métricas em tempo real
make arkitect-monitor

# Inicializar modo simbiótico
make arkitect-init

# Executar evolução adaptativa
make arkitect-evolve

# Testar integração
make arkitect-test
```

### Via Scripts Diretos

```bash
# Ativação completa
./activate_arkitect.sh

# Status detalhado
python scripts/check_arkitect_status.py

# Monitor em tempo real
python scripts/arkitect_monitor.py

# Inicialização simbiótica
python scripts/init_symbiotic.py

# Evolução adaptativa
python scripts/arkitect_full_extension.py --evolve

# Testes de integração
python tests/run_nexus_arquimax_tests.py
```

## Configuração

### Arquivos Principais

- `src/arkitect/config.yaml` - Configuração principal do Arkitect
- `config/arquimax/config.yaml` - Configuração específica do ARQUIMAX
- `config/nexus.yaml` - Configuração do NEXUS
- `workflows/symbiotic_arquimax_nexus.yaml` - Workflows de integração

### Variáveis de Ambiente

```bash
# .env
ARKITECT_MODE=symbiotic
ARKITECT_LOG_LEVEL=info
ARQUIMAX_ENABLED=true
NEXUS_ENABLED=true
SYMBIOTIC_INDEX_THRESHOLD=0.7
```

## Modos de Operação

### 1. Modo Análise

Foca em análise arquitetural e qualidade de código:

```bash
python scripts/arkitect_monitor.py --mode=analysis
```

Recursos:
- Análise de estrutura de código
- Detecção de padrões arquiteturais
- Identificação de débito técnico
- Métricas de qualidade

### 2. Modo Simbiótico

Integração completa com adaptação contínua:

```bash
python scripts/init_symbiotic.py --mode=full
```

Recursos:
- Aprendizado adaptativo
- Evolução de capacidades
- Sincronização bidirecional
- Auto-otimização

### 3. Modo Monitoramento

Observação e métricas em tempo real:

```bash
python scripts/arkitect_monitor.py --realtime
```

Recursos:
- Dashboard em tempo real
- Alertas configuráveis
- Histórico de métricas
- Relatórios automáticos

## Fases de Integração

### Fase 1: Bootstrap
- Inicialização de capacidades
- Análise de requisitos
- Configuração de ambiente

### Fase 2: Adaptação
- Ponte ARQUIMAX ativa
- Ponte NEXUS ativa
- Sincronização inicial

### Fase 3: Evolução
- Aprendizado simbiótico
- Evolução de capacidades
- Otimização contínua

### Fase 4: Autônomo
- Operação independente
- Auto-manutenção
- Evolução emergente

## Métricas e Indicadores

### Métricas ARQUIMAX
- **Capacidades Ativas**: Número de módulos ativos
- **Taxa de Sucesso**: Porcentagem de operações bem-sucedidas
- **Tempo de Execução**: Performance das análises

### Métricas NEXUS
- **Conectores Ativos**: Integrações funcionando
- **Taxa de Sincronização**: Eficiência da sincronização
- **Convergência**: Nível de adaptação alcançado

### Índice Simbiótico
- **0.0-0.3**: Iniciando integração
- **0.3-0.7**: Adaptação em progresso
- **0.7-0.9**: Sistema integrado
- **0.9-1.0**: Operação autônoma

## Troubleshooting

### Sistema não inicia

```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar configuração
python scripts/check_arkitect_status.py --verbose

# Limpar cache
rm -rf .arkitect/cache/*
```

### Métricas não aparecem

```bash
# Verificar serviços
make arkitect-status

# Reiniciar monitoramento
make arkitect-monitor
```

### Evolução travada

```bash
# Forçar evolução
python scripts/arkitect_full_extension.py --force-evolve

# Reset de estado
python scripts/init_symbiotic.py --reset
```

## Integração com CHESS

O Arkitect está profundamente integrado com o sistema CHESS:

### Componentes Monitorados
- **Cultural Engine**: Análise de padrões culturais
- **Narrative System**: Evolução de narrativas
- **Cache System**: Otimização de performance
- **AI Adaptativa**: Aprendizado e evolução

### Otimizações Automáticas
- Cache inteligente
- Prefetching adaptativo
- Batch processing
- Query optimization

## Dashboards e Relatórios

### Dashboard Web

Acesse o dashboard em: `http://localhost:8080/arkitect`

### Relatórios Automáticos

Relatórios são gerados em:
- `reports/arkitect_evolution_report.md`
- `reports/arkitect_ai_integration.json`
- `reports/arkitect_extension_report.json`

### Logs

Logs detalhados em:
- `logs/arkitect.log`
- `logs/arquimax.log`
- `logs/nexus.log`

## Exemplos de Uso

### Análise de Código Específica

```bash
python scripts/arkitect_monitor.py \
  --component=cultural_engine \
  --depth=deep \
  --output=report.json
```

### Evolução Direcionada

```bash
python scripts/arkitect_full_extension.py \
  --target=narrative_system \
  --evolution-rate=0.8 \
  --iterations=10
```

### Monitoramento Customizado

```bash
python scripts/arkitect_monitor.py \
  --metrics=performance,quality,evolution \
  --interval=30 \
  --alert-threshold=0.7
```

## API Programática

### Python

```python
from src.arkitect import Arkitect

# Inicializar
arkitect = Arkitect(mode='symbiotic')

# Analisar componente
result = arkitect.analyze('cultural_engine')

# Evoluir sistema
arkitect.evolve(target='all', rate=0.7)

# Obter métricas
metrics = arkitect.get_metrics()
```

### JavaScript

```javascript
import { ArkitectClient } from './src/arkitect/client.js';

// Inicializar
const arkitect = new ArkitectClient();

// Monitorar
arkitect.monitor({
  components: ['cultural_engine', 'narrative_system'],
  realtime: true
});

// Obter status
const status = await arkitect.getStatus();
```

## Contribuindo

Para contribuir com o Arkitect:

1. Familiarize-se com a arquitetura em `docs/SYMBIOTIC_ARCHITECTURE.md`
2. Leia o guia de contribuição em `docs/contributing/CONTRIBUTING.md`
3. Execute os testes: `make arkitect-test`
4. Submeta PR com descrição detalhada

## Suporte

- **Documentação**: `docs/arkitect/`
- **Issues**: GitHub Issues
- **Discord**: Canal #arkitect
- **Email**: arkitect@aeon-chess.com
