# 🎨 Como Adicionar Novas Culturas ao CHESS

> **Este guia explica como criar e integrar novas culturas usando os templates existentes**

## 📋 Visão Geral

O sistema cultural do CHESS foi projetado para ser **extensível e modular**. Você pode adicionar quantas culturas quiser usando os templates e estruturas já criados.

---

## 🚀 Guia Rápido (5 Passos)

### 1️⃣ Copie o Template Python
```bash
cp templates/cultural/culture_template.py src/cultural/cultures/your_culture.py
```

### 2️⃣ Crie a Configuração YAML
```bash
cp templates/cultural/culture_config_template.yaml cultural_data/configurations/themes/your_culture.yaml
```

### 3️⃣ Adicione Narrativas
```bash
# Edite config/narrative/cultures_expanded.yaml
# Adicione sua seção de cultura
```

### 4️⃣ Registre no Sistema
```python
# Edite src/cultural/cultural_registry.py
# Adicione sua cultura ao registro
```

### 5️⃣ Teste
```bash
python3 examples/test_new_culture.py --culture=your_culture
```

---

## 📝 Guia Detalhado

### Passo 1: Planejamento da Cultura

Antes de começar, defina:

#### Características Essenciais
- **Nome**: Como será identificada (ex: "Roman", "Cyberpunk")
- **Categoria**: Historical, Temporal, Futuristic, Regional, ou Special
- **Valores Principais**: 3-5 valores que definem a cultura
- **Período/Contexto**: Quando/onde a cultura existe
- **Estilo Narrativo**: Tom das narrativas (formal, poético, técnico, etc.)

#### Metáforas de Peças
Defina como cada peça será representada:
```yaml
peças:
  peão: [Seu equivalente cultural]
  torre: [Seu equivalente cultural]
  cavalo: [Seu equivalente cultural]
  bispo: [Seu equivalente cultural]
  rainha: [Seu equivalente cultural]
  rei: [Seu equivalente cultural]
```

### Passo 2: Criar Arquivo Python

Crie `src/cultural/cultures/your_culture.py`:

```python
"""
Your Culture Implementation
"""

from typing import Dict, List
from dataclasses import dataclass
from ..culture_framework import ChessCulture, CulturalValues

@dataclass
class YourCultureValues(CulturalValues):
    """Valores específicos da sua cultura"""
    # Adicione valores específicos aqui
    your_value_1: float = 0.0
    your_value_2: float = 0.0
    
class YourCulture(ChessCulture):
    """Implementação da cultura [Nome]"""
    
    def __init__(self):
        super().__init__(
            name="Your Culture Name",
            description="Descrição detalhada da cultura",
            historical_period="Período ou contexto",
            geographical_origin="Origem geográfica ou conceitual"
        )
        self.values = YourCultureValues(
            honor=0.8,  # Ajuste conforme a cultura
            tradition=0.7,
            innovation=0.3,
            spirituality=0.6,
            your_value_1=0.9,
            your_value_2=0.5
        )
        
    def get_piece_metaphors(self) -> Dict[str, str]:
        """Retorna metáforas culturais para as peças"""
        return {
            'pawn': 'Sua metáfora para peão',
            'rook': 'Sua metáfora para torre',
            'knight': 'Sua metáfora para cavalo',
            'bishop': 'Sua metáfora para bispo',
            'queen': 'Sua metáfora para rainha',
            'king': 'Sua metáfora para rei'
        }
    
    def get_move_narrative(self, move_type: str, piece: str, **kwargs) -> str:
        """Gera narrativa para um movimento"""
        narratives = {
            'advance': [
                f"O {piece} avança com [característica cultural]",
                f"Com [valor cultural], o {piece} move-se para frente"
            ],
            'capture': [
                f"O {piece} [ação cultural] o oponente",
                f"Em um ato de [valor], o {piece} elimina o adversário"
            ],
            'check': [
                f"O [líder] está em perigo!",
                f"[Expressão cultural de ameaça]!"
            ],
            'checkmate': [
                f"[Expressão cultural de vitória]!",
                f"O [líder] foi derrotado!"
            ]
        }
        
        import random
        return random.choice(narratives.get(move_type, [f"O {piece} se move"]))
    
    def get_phase_description(self, phase: str) -> str:
        """Descreve a fase do jogo em contexto cultural"""
        descriptions = {
            'opening': "[Descrição cultural da abertura]",
            'middlegame': "[Descrição cultural do meio-jogo]",
            'endgame': "[Descrição cultural do final]"
        }
        return descriptions.get(phase, "")
    
    def get_cultural_greeting(self) -> str:
        """Saudação cultural no início do jogo"""
        return "[Saudação na cultura]"
    
    def get_victory_message(self) -> str:
        """Mensagem de vitória cultural"""
        return "[Expressão de vitória na cultura]"
    
    def get_defeat_message(self) -> str:
        """Mensagem de derrota cultural"""
        return "[Expressão de derrota honrosa]"
```

### Passo 3: Criar Configuração YAML

Crie `cultural_data/configurations/themes/your_culture.yaml`:

```yaml
# Configuração da Cultura [Nome]
culture:
  id: "your_culture"
  name: "Your Culture Name"
  display_name: "Nome de Exibição"
  category: "historical|temporal|futuristic|regional|special"
  
metadata:
  version: "1.0.0"
  author: "Seu Nome"
  created_date: "2025-08-08"
  last_updated: "2025-08-08"
  
characteristics:
  primary_values:
    - valor1
    - valor2
    - valor3
    
  secondary_values:
    - valor4
    - valor5
    
  cultural_traits:
    - traço1
    - traço2
    
piece_metaphors:
  pawn:
    name: "Nome Cultural do Peão"
    description: "Descrição do papel"
    plural: "Nome no plural"
    
  rook:
    name: "Nome Cultural da Torre"
    description: "Descrição do papel"
    plural: "Nome no plural"
    
  knight:
    name: "Nome Cultural do Cavalo"
    description: "Descrição do papel"
    plural: "Nome no plural"
    
  bishop:
    name: "Nome Cultural do Bispo"
    description: "Descrição do papel"
    plural: "Nome no plural"
    
  queen:
    name: "Nome Cultural da Rainha"
    description: "Descrição do papel"
    plural: "Nome no plural"
    
  king:
    name: "Nome Cultural do Rei"
    description: "Descrição do papel"
    plural: "Nome no plural"
    
narratives:
  opening_narratives:
    - "Narrativa de abertura 1"
    - "Narrativa de abertura 2"
    - "Narrativa de abertura 3"
    
  capture_narratives:
    - "{attacker} [ação cultural] {defender}"
    - "Com [valor], {attacker} derrota {defender}"
    
  check_narratives:
    - "O {king} está ameaçado!"
    - "[Expressão de perigo]!"
    
  checkmate_narratives:
    - "[Expressão de vitória total]!"
    - "O {king} foi completamente derrotado!"
    
  tactical_narratives:
    fork: "{piece} executa [tática cultural]"
    pin: "{piece} [ação de imobilização]"
    skewer: "{piece} [ação penetrante]"
    
visual_theme:
  primary_color: "#HEX"
  secondary_color: "#HEX"
  accent_color: "#HEX"
  
  board_style: "traditional|modern|stylized"
  piece_style: "classic|cultural|abstract"
  
  background_image: "path/to/image.jpg"
  
audio_theme:
  background_music: "path/to/music.mp3"
  move_sound: "path/to/sound.wav"
  capture_sound: "path/to/capture.wav"
  check_sound: "path/to/check.wav"
  victory_sound: "path/to/victory.wav"
  
ai_behavior:
  aggression_level: 0.5  # 0.0 a 1.0
  defensive_tendency: 0.5
  tactical_preference: 0.5
  positional_play: 0.5
  
  opening_book_preference: "aggressive|balanced|defensive"
  endgame_style: "tactical|positional|mixed"
  
  personality_traits:
    - "trait1"
    - "trait2"
    
cultural_events:
  special_moves:
    - name: "Nome do Movimento Especial"
      description: "Descrição"
      trigger: "Condição"
      
  celebrations:
    - name: "Celebração Cultural"
      trigger: "capture_queen"
      message: "Mensagem especial"
      
historical_context:
  period: "Período histórico ou contexto"
  location: "Local geográfico ou conceitual"
  
  key_figures:
    - name: "Figura Importante"
      role: "Papel na cultura"
      
  key_events:
    - name: "Evento Importante"
      description: "Descrição"
      
  cultural_artifacts:
    - name: "Artefato"
      description: "Descrição"
      
integration:
  compatible_with:
    - "culture1"
    - "culture2"
    
  conflicts_with:
    - "culture3"
    
  hybrid_possibilities:
    - base: "this_culture"
      mix: "other_culture"
      result: "hybrid_culture"
```

### Passo 4: Adicionar Narrativas Expandidas

Edite `config/narrative/cultures_expanded.yaml`:

```yaml
chess_cultures:
  your_culture:
    themes:
      - name: "tema_principal"
        weight: 0.9
        keywords:
          - "palavra1"
          - "palavra2"
          
    piece_metaphors:
      # Copie a estrutura de outras culturas
      
    narrative_patterns:
      moves:
        advance:
          - "Padrão narrativo 1"
          - "Padrão narrativo 2"
        capture:
          - "Padrão de captura 1"
          - "Padrão de captura 2"
```

### Passo 5: Registrar no Sistema

Edite `src/cultural/cultural_registry.py`:

```python
# Adicione na seção apropriada do _initialize_cultures()

cultures['your_culture'] = CultureMetadata(
    id='your_culture',
    name='Your Culture',
    display_name='Your Culture - Descrição',
    category=CultureCategory.YOUR_CATEGORY,
    status=CultureStatus.FULLY_IMPLEMENTED,
    description='Descrição completa',
    values=['Valor1', 'Valor2', 'Valor3'],
    piece_metaphors={
        'pawn': 'Sua metáfora',
        # ... outras peças
    },
    narrative_examples=[
        'Exemplo 1',
        'Exemplo 2',
        'Exemplo 3'
    ],
    implementation_path='src/cultural/cultures/your_culture.py',
    config_path='cultural_data/configurations/themes/your_culture.yaml'
)
```

### Passo 6: Testar a Nova Cultura

Crie um script de teste:

```python
# test_new_culture.py
from src.cultural.cultures.your_culture import YourCulture
from src.cultural.cultural_registry import get_registry

# Teste do registro
registry = get_registry()
culture_meta = registry.get_culture('your_culture')
print(f"Cultura registrada: {culture_meta.display_name}")

# Teste da implementação
culture = YourCulture()
print(f"Saudação: {culture.get_cultural_greeting()}")
print(f"Peças: {culture.get_piece_metaphors()}")
print(f"Narrativa: {culture.get_move_narrative('advance', 'Guerreiro')}")
```

---

## 🎯 Exemplos de Culturas para Inspiração

### Culturas Históricas Sugeridas
- **Romana**: Legionários, Senado, Império
- **Chinesa Imperial**: Dinastia, Mandato Celestial
- **Persa**: Imortais, Sátrapas, Zoroastrismo
- **Celta**: Druidas, Guerreiros, Natureza

### Culturas Temporais Sugeridas
- **Idade do Bronze**: Primeiras civilizações
- **Era Industrial**: Revolução, Máquinas, Progresso
- **Belle Époque**: Arte, Cultura, Elegância

### Culturas Futuristas Sugeridas
- **Pós-Apocalíptica**: Sobrevivência, Recursos escassos
- **Transumanista**: Evolução, IA, Singularidade
- **Colonização Espacial**: Planetas, Alienígenas

### Culturas Regionais Sugeridas
- **Africana**: Reinos, Tribos, Ancestralidade
- **Polinésia**: Navegação, Ilhas, Oceano
- **Ártica**: Gelo, Sobrevivência, Aurora

### Estilos Especiais Sugeridos
- **Fantasia**: Dragões, Magia, Reinos
- **Horror**: Criaturas, Medo, Sobrevivência
- **Fairy Tale**: Contos, Magia, Final feliz

---

## 🔧 Ferramentas Auxiliares

### Script de Validação
```bash
# Valida se a cultura está corretamente configurada
python3 scripts/validation/validate_culture.py --culture=your_culture
```

### Gerador de Template
```bash
# Gera automaticamente os arquivos base
python3 scripts/generators/generate_culture.py \
  --name="Your Culture" \
  --category=historical \
  --values="honor,wisdom,courage"
```

### Testador de Narrativas
```bash
# Testa todas as narrativas da cultura
python3 scripts/test/test_narratives.py --culture=your_culture
```

---

## ✅ Checklist de Implementação

- [ ] Definir conceito e valores da cultura
- [ ] Criar arquivo Python em `src/cultural/cultures/`
- [ ] Criar configuração YAML em `cultural_data/configurations/themes/`
- [ ] Adicionar narrativas em `config/narrative/cultures_expanded.yaml`
- [ ] Registrar em `src/cultural/cultural_registry.py`
- [ ] Criar testes em `tests/cultural/`
- [ ] Adicionar documentação em `docs/cultural/cultures/`
- [ ] Testar integração com o jogo
- [ ] Validar narrativas e metáforas
- [ ] Adicionar ao CULTURAL_REGISTRY.md

---

## 📚 Recursos Adicionais

- [Template de Cultura Python](../../templates/cultural/culture_template.py)
- [Template de Configuração YAML](../../templates/cultural/culture_config_template.yaml)
- [Guia de Narrativas](../narrative/NARRATIVE_GUIDE.md)
- [Sistema de Valores Culturais](CULTURAL_VALUES.md)
- [Registro Cultural](CULTURAL_REGISTRY.md)

---

## 🤝 Contribuindo

Adoramos novas culturas! Para contribuir:

1. Fork o repositório
2. Crie sua cultura seguindo este guia
3. Teste completamente
4. Envie um Pull Request
5. Inclua exemplos e documentação

---

**Lembre-se:** Cada cultura deve ser única, respeitosa e adicionar valor à experiência do jogo!

*Happy Cultural Creation!* 🎨🌍♟️
