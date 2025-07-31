# Motor Cultural do ChessMaster

Este diretório contém todos os dados culturais que alimentam o motor cultural do ChessMaster, incluindo pesquisas históricas, configurações culturais e conteúdo narrativo.

## Estrutura de Diretórios

```
cultural_data/
├── research/              # Pesquisa do Notion importada
│   ├── historical/        # Dados históricos
│   ├── cultural/         # Aspectos culturais
│   └── strategic/        # Estratégias históricas
│
├── configurations/        # Configurações do motor cultural
│   ├── themes/           # Temas culturais
│   ├── narratives/       # Padrões narrativos
│   └── pieces/           # Metáforas das peças
│
└── content/              # Conteúdo cultural
    ├── stories/          # Histórias e narrativas
    ├── lessons/          # Lições de xadrez
    └── philosophy/       # Aspectos filosóficos
```

## Integração DOCSYNC

O sistema utiliza o DOCSYNC para manter todos os dados organizados e sincronizados. Principais recursos:

1. **Importação do Notion**
   - Importação automática a cada hora
   - Validação automática dos dados
   - Organização em categorias apropriadas

2. **Validação de Dados**
   - Schemas definidos para cada tipo de conteúdo
   - Validação automática diária
   - Alertas para inconsistências

3. **Automação**
   - Sincronização automática com Notion
   - Validação periódica de conteúdo
   - Organização automática de arquivos

4. **Monitoramento**
   - Métricas de completude de conteúdo
   - Status de sincronização
   - Saúde da organização

## Uso

### Importação do Notion

Para importar dados do Notion:

```bash
python .docsync/scripts/notion_import.py
```

### Validação Manual

Para validar os dados manualmente:

```bash
python .docsync/init.py --validate
```

### Adicionar Novo Conteúdo

1. Use os templates em `.docsync/templates/cultural/`
2. Salve no diretório apropriado
3. Execute a validação

## Convenções

### Nomes de Arquivos
- Usar lowercase
- Separar palavras com underscores
- Incluir categoria no nome: `medieval_europe_theme.yaml`

### Formato de Dados
- YAML para configurações
- Markdown para conteúdo narrativo
- JSON para dados estruturados

### Idiomas
- Português (Brasil) como idioma principal
- Inglês para termos técnicos quando necessário
- Documentar traduções em metadata

## Integração com Motor Cultural

O conteúdo deste diretório é usado pelo motor cultural para:

1. **Geração de Narrativas**
   - Descrições culturais de movimentos
   - Histórias temáticas
   - Eventos especiais

2. **Comportamento da IA**
   - Perfis culturais de jogadores
   - Estratégias históricas
   - Padrões de jogo culturais

3. **Interface do Usuário**
   - Temas visuais
   - Terminologia cultural
   - Descrições contextuais

## Contribuição

1. Clone o repositório
2. Crie uma branch para sua contribuição
3. Use os templates disponíveis
4. Valide seu conteúdo
5. Envie um pull request

## Manutenção

O sistema executa automaticamente:

- Backup diário
- Validação de conteúdo
- Sincronização com Notion
- Organização de arquivos

## Contato

Para questões relacionadas ao motor cultural:
- **Autor**: NEO_SH1W4
- **Email**: [seu-email@dominio.com]
- **Discord**: [seu-usuario]
