# AEON Chess - Documentação Central

## Visão Geral
AEON Chess é um sistema de xadrez avançado que integra inteligência artificial adaptativa, computação quântica e aprendizado simbiótico através das plataformas ARQUIMAX e NEXUS.

## Guia Rápido

### Instalação
```bash
# Clonar repositório
git clone https://github.com/NEO-SH1W4/AEON_CHESS.git

# Instalar dependências
pip install -e .

# Configurar ambiente
aeon setup --mode symbiotic
```

### Uso Básico
```python
from aeon_chess import AEONChess

# Inicializar sistema
chess = AEONChess()

# Ativar modo simbiótico
chess.enable_symbiotic_mode()

# Iniciar partida
chess.start_game()
```

## Documentação Técnica

### Arquitetura Base
- [Matemática do Xadrez](CHESS_MATHEMATICS.md)
- [Design do Sistema](CHESS_SYSTEM_DESIGN.md)
- [Abordagem Quântica](QUANTUM_CHESS_APPROACH.md)

### Integrações
- [Integração ARQUIMAX-NEXUS](INTEGRATION_PLAN.md)
- [Sistema Simbiótico](SYMBIOTIC_CHESS_SYSTEM.md)
- [Validação Simbiótica](SYMBIOTIC_CHESS_VALIDATION.md)

### Implementação
- [Plano de Execução](EXECUTION_PLAN.md)
- [Estrutura do Projeto (WBS)](PROJECT_WBS.md)
- [Plano de Validação](VALIDATION_PLAN.md)

## Status do Projeto

### Componentes Principais
| Componente | Status | Progresso |
|------------|--------|-----------|
| Core do Xadrez | ✅ Completo | 100% |
| IA Adaptativa | 🟡 Em Desenvolvimento | 70% |
| Campo Quântico | 🟡 Em Desenvolvimento | 60% |
| Integração ARQUIMAX | 🟡 Em Desenvolvimento | 60% |
| Integração NEXUS | 🟡 Em Desenvolvimento | 50% |
| Sistema Simbiótico | 🟡 Em Desenvolvimento | 55% |

### Métricas Atuais
- Cobertura de Testes: 83%
- Integração Simbiótica: 65%
- Performance Quântica: 72%
- Evolução Adaptativa: 58%

## Roadmap

### Fase Atual (v0.7)
- [x] Implementação do core de xadrez
- [x] Integração inicial ARQUIMAX
- [x] Campo quântico básico
- [ ] Sistema simbiótico completo
- [ ] Validação end-to-end

### Próxima Fase (v0.8)
- [ ] Otimização do campo quântico
- [ ] Expansão da IA adaptativa
- [ ] Evolução simbiótica avançada
- [ ] Interface gráfica quântica
- [ ] Documentação completa

### Futuro (v1.0)
- [ ] Sistema totalmente autônomo
- [ ] Auto-evolução simbiótica
- [ ] Integração com torneios
- [ ] API pública
- [ ] Ecossistema de plugins

## Recursos

### Ferramentas
- VS Code com extensões recomendadas
- Docker para ambiente isolado
- Pre-commit hooks configurados
- Linters e formatadores

### Dependências Principais
- Python 3.11+
- NumPy para computação
- PyTorch para IA
- Qiskit para aspectos quânticos

## Contribuição
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um Pull Request

## Suporte
- Documentação: `/docs`
- Issues: GitHub Issues
- Discussões: GitHub Discussions
- Chat: Discord

## Licença
MIT License - veja [LICENSE](../LICENSE) para detalhes
