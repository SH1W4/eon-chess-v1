# 🌍 CHESS Cultural Registry - Registro Completo de Culturas

> **Este é o registro oficial de todas as culturas implementadas no CHESS.**  
> **Última atualização:** 08 de Agosto, 2025  
> **Total de Culturas:** 15+

---

## 📋 Índice de Culturas

### 🏛️ Culturas Históricas
1. [Azteca](#azteca) - Guerreiros do Sol
2. [Viking](#viking) - Exploradores Nórdicos  
3. [Samurai](#samurai) - Código Bushido
4. [Maia](#maia) - Sabedoria Astronômica

### ⏰ Épocas Temporais
5. [Medieval](#medieval) - Era dos Cavaleiros
6. [Renascimento](#renascimento) - Arte e Humanismo

### 🚀 Temas Futuristas
7. [Neo-Tokyo 2050](#neo-tokyo-2050) - Cyberpunk Avançado
8. [Steampunk](#steampunk) - Vapor e Engrenagens
9. [Quantum Realm](#quantum-realm) - Superposição Quântica

### 🌏 Culturas Regionais
10. [Oriental/Eastern](#orientaleastern) - Filosofia e Equilíbrio
11. [Nórdica](#nordica) - Mitologia e Sagas

### ⚓ Estilos Especiais
12. [Pirata](#pirata) - Aventura nos Sete Mares
13. [Espacial](#espacial) - Conquista Galáctica

### 🔮 Em Desenvolvimento
14. [Egípcia](#egipcia) - Mistérios Antigos
15. [Bizantina](#bizantina) - Diplomacia Imperial
16. [Grega](#grega) - Filosofia e Democracia

---

## 🏛️ Culturas Históricas

### Azteca
**Arquivo:** `src/cultural/cultures/aztec_culture.py`  
**Configuração:** `cultural_data/configurations/themes/aztec_empire.yaml`

#### Características:
- **Valores Principais:** Honra, Sacrifício, Guerra Sagrada
- **Metáforas de Peças:**
  - Peão → Guerreiro Águia
  - Torre → Templo/Pirâmide
  - Cavalo → Guerreiro Jaguar
  - Bispo → Sacerdote
  - Rainha → Sacerdotisa
  - Rei → Tlatoani (Imperador)

#### Narrativas Exemplo:
```yaml
- "O Guerreiro Águia avança com a bênção de Huitzilopochtli"
- "O Templo sagrado protege o campo de batalha"
- "O Tlatoani comanda com a sabedoria dos ancestrais"
```

---

### Viking
**Arquivo:** `src/cultural/cultures/viking_culture.py`  
**Configuração:** `cultural_data/configurations/themes/viking_raiders.yaml`

#### Características:
- **Valores Principais:** Bravura, Conquista, Honra em Batalha
- **Metáforas de Peças:**
  - Peão → Guerreiro Viking
  - Torre → Fortaleza/Drakkar
  - Cavalo → Berserker
  - Bispo → Skald (Poeta Guerreiro)
  - Rainha → Valquíria
  - Rei → Jarl

#### Narrativas Exemplo:
```yaml
- "O Berserker entra em fúria de batalha"
- "A Valquíria escolhe os dignos para Valhalla"
- "O Jarl lidera seu clã para a glória"
```

---

### Samurai
**Arquivo:** `src/cultural/cultures/samurai_culture.py`  
**Configuração:** `cultural_data/configurations/themes/samurai_honor.yaml`

#### Características:
- **Valores Principais:** Bushido, Disciplina, Lealdade
- **Metáforas de Peças:**
  - Peão → Ashigaru (Soldado)
  - Torre → Castelo/Pagode
  - Cavalo → Samurai Montado
  - Bispo → Monge Guerreiro
  - Rainha → Onna-bugeisha
  - Rei → Daimyo

#### Narrativas Exemplo:
```yaml
- "O Samurai move-se com precisão mortal"
- "A honra do Bushido guia cada movimento"
- "O Daimyo mantém a harmonia do han"
```

---

### Maia
**Arquivo:** `src/cultural/cultures/mayan_culture.py`  
**Configuração:** `cultural_data/configurations/themes/mayan_prophecy.yaml`

#### Características:
- **Valores Principais:** Astronomia, Matemática, Harmonia Cósmica
- **Metáforas de Peças:**
  - Peão → Guerreiro Quetzal
  - Torre → Observatório
  - Cavalo → Guerreiro Jaguar
  - Bispo → Sacerdote Astronômico
  - Rainha → Sacerdotisa Lunar
  - Rei → Ahau (Rei Divino)

#### Narrativas Exemplo:
```yaml
- "As estrelas alinham-se para guiar o movimento"
- "O calendário sagrado prevê a vitória"
- "O Ahau move-se em harmonia com os ciclos celestiais"
```

---

## ⏰ Épocas Temporais

### Medieval
**Arquivo:** `src/cultural/narratives_config.json`  
**Configuração:** `config/narrative/cultures_expanded.yaml`

#### Características:
- **Valores Principais:** Cavalaria, Honra Feudal, Fé
- **Metáforas de Peças:**
  - Peão → Soldado/Camponês
  - Torre → Castelo/Torre de Vigia
  - Cavalo → Cavaleiro
  - Bispo → Clérigo
  - Rainha → Rainha/Dama
  - Rei → Rei/Monarca

#### Narrativas Exemplo:
```yaml
- "O nobre cavaleiro avança para defender o reino"
- "O castelo permanece como bastião impenetrável"
- "Pela honra e pela glória do reino!"
```

---

### Renascimento
**Arquivo:** `config/narrative/cultures_expanded.yaml`  
**Tema:** Renaissance

#### Características:
- **Valores Principais:** Arte, Ciência, Humanismo
- **Metáforas de Peças:**
  - Peão → Artesão
  - Torre → Fortaleza Cultural
  - Cavalo → Condottiero
  - Bispo → Humanista
  - Rainha → Patrona das Artes
  - Rei → Príncipe Iluminado

#### Narrativas Exemplo:
```yaml
- "Com graça artística, a peça move-se harmoniosamente"
- "O equilíbrio perfeito entre força e beleza"
- "Uma jogada digna de Da Vinci"
```

---

## 🚀 Temas Futuristas

### Neo-Tokyo 2050
**Referências:** `examples/cultural_ai_demo.py`, `config/aeon_core.yaml`

#### Características:
- **Valores Principais:** Eficiência, Inovação, Tecnologia
- **Metáforas de Peças:**
  - Peão → Cyber-Soldado
  - Torre → Torre de Dados
  - Cavalo → Mecha Ligeiro
  - Bispo → Hacker Neural
  - Rainha → IA Suprema
  - Rei → CEO Corporativo

#### Narrativas Exemplo:
```yaml
- "Sistema tático otimizado, executando movimento"
- "Interface neural sincronizada para máxima eficiência"
- "Protocolo de vitória em execução"
```

---

### Steampunk
**Referências:** `config/narrative/config.yaml`, `docs/narrative/game.ink`

#### Características:
- **Valores Principais:** Engenhosidade, Mecânica, Vapor
- **Metáforas de Peças:**
  - Peão → Autômato
  - Torre → Torre de Vapor
  - Cavalo → Cavalaria Mecânica
  - Bispo → Engenheiro
  - Rainha → Inventora Suprema
  - Rei → Lorde Industrial

#### Narrativas Exemplo:
```yaml
- "Engrenagens giram em perfeita sincronia"
- "O vapor impulsiona o avanço mecânico"
- "Uma manobra digna da era das máquinas"
```

---

### Quantum Realm
**Referências:** `src/quantum/`, `config/aeon_core.yaml`

#### Características:
- **Valores Principais:** Probabilidade, Superposição, Entrelaçamento
- **Metáforas de Peças:**
  - Peão → Partícula Quântica
  - Torre → Estabilizador Dimensional
  - Cavalo → Salto Quântico
  - Bispo → Observador
  - Rainha → Entrelaçamento Supremo
  - Rei → Núcleo Quântico

#### Narrativas Exemplo:
```yaml
- "A peça existe em superposição até ser observada"
- "Colapso da função de onda em posição favorável"
- "Entrelaçamento quântico estabelecido"
```

---

## 🌏 Culturas Regionais

### Oriental/Eastern
**Arquivo:** `config/narrative/cultures_expanded.yaml`

#### Características:
- **Valores Principais:** Harmonia, Equilíbrio, Sabedoria
- **Metáforas de Peças:**
  - Peão → Discípulo
  - Torre → Pagode
  - Cavalo → Guerreiro Montado
  - Bispo → Monge Sábio
  - Rainha → Imperatriz Celestial
  - Rei → Imperador do Céu

#### Narrativas Exemplo:
```yaml
- "O movimento flui como água, adaptando-se ao terreno"
- "Em perfeito equilíbrio com o Tao do tabuleiro"
- "A sabedoria milenar guia a estratégia"
```

---

### Nórdica
**Arquivo:** `config/narrative/cultures_expanded.yaml`

#### Características:
- **Valores Principais:** Destino, Runas, Mitologia
- **Metáforas de Peças:**
  - Peão → Guerreiro do Norte
  - Torre → Salão dos Heróis
  - Cavalo → Cavaleiro de Odin
  - Bispo → Vidente Rúnico
  - Rainha → Frigg/Freyja
  - Rei → Odin/Thor

#### Narrativas Exemplo:
```yaml
- "As runas preveem o caminho da vitória"
- "Pelos nove reinos, a batalha será vencida!"
- "O destino tecido pelas Nornas se cumpre"
```

---

## ⚓ Estilos Especiais

### Pirata
**Referências:** Múltiplas menções em arquivos de configuração

#### Características:
- **Valores Principais:** Liberdade, Aventura, Tesouro
- **Metáforas de Peças:**
  - Peão → Marujo
  - Torre → Navio/Fortaleza Costeira
  - Cavalo → Corsário
  - Bispo → Navegador
  - Rainha → Capitã Pirata
  - Rei → Lorde Pirata

#### Narrativas Exemplo:
```yaml
- "Içar velas! Rumo ao tesouro!"
- "O código pirata guia nossa estratégia"
- "Pelos sete mares, a vitória será nossa!"
```

---

### Espacial
**Referências:** Menções em configurações futuristas

#### Características:
- **Valores Principais:** Exploração, Conquista Galáctica, Tecnologia
- **Metáforas de Peças:**
  - Peão → Soldado Espacial
  - Torre → Estação Orbital
  - Cavalo → Caça Estelar
  - Bispo → Navegador Cósmico
  - Rainha → Comandante da Frota
  - Rei → Almirante Galáctico

#### Narrativas Exemplo:
```yaml
- "Iniciando manobra orbital para posição estratégica"
- "A frota estelar avança pelo quadrante"
- "Pelo domínio da galáxia!"
```

---

## 🔮 Em Desenvolvimento

### Egípcia
**Status:** Parcialmente implementada  
**Planejado para:** v0.3.0

### Bizantina
**Status:** Parcialmente implementada  
**Planejado para:** v0.3.0

### Grega
**Status:** Parcialmente implementada  
**Planejado para:** v0.3.0

---

## 📁 Estrutura de Arquivos

### Implementações de Cultura
```
src/cultural/cultures/
├── aztec_culture.py
├── viking_culture.py
├── samurai_culture.py
├── mayan_culture.py
└── __init__.py
```

### Configurações Narrativas
```
config/narrative/
├── cultures_expanded.yaml
├── config.yaml
├── chess_config.yaml
└── chess_tactics_history.yaml
```

### Dados Culturais
```
cultural_data/
├── configurations/
│   └── themes/
│       ├── aztec_empire.yaml
│       ├── viking_raiders.yaml
│       ├── samurai_honor.yaml
│       └── mayan_prophecy.yaml
├── narratives/
└── metaphors/
```

### Exemplos e Demos
```
examples/
├── cultural_ai_demo.py
└── cultural_demo.py
```

---

## 🔧 Como Adicionar Nova Cultura

1. **Criar arquivo Python em** `src/cultural/cultures/`
2. **Adicionar configuração em** `cultural_data/configurations/themes/`
3. **Registrar narrativas em** `config/narrative/cultures_expanded.yaml`
4. **Atualizar este registro**
5. **Adicionar testes em** `tests/cultural/`
6. **Documentar em** `docs/cultural/`

---

## 📊 Estatísticas

- **Total de Culturas Implementadas:** 13
- **Em Desenvolvimento:** 3
- **Planejadas:** 10+
- **Narrativas Únicas:** 3000+
- **Arquivos de Cultura:** 50+

---

## 🔗 Links Relacionados

- [Guia de Implementação Cultural](IMPLEMENTATION_GUIDE.md)
- [Perfis de Antagonistas](profiles/ANTAGONIST_PROFILES.md)
- [Sistema de Narrativas](../narrative/README.md)
- [Configurações](../../config/narrative/)

---

**Última Verificação:** 08/08/2025  
**Mantido por:** CHESS Cultural Team  
**Contato:** neo.sh1w4@gmail.com

---

> "Cada cultura no CHESS não é apenas um tema visual, mas uma experiência completa de jogo com sua própria filosofia, estratégia e narrativa." - CHESS Team
