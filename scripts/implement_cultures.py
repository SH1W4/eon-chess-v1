#!/usr/bin/env python3
"""
AEON Chess - Implementação de Culturas Base
Script para implementar as 3 culturas essenciais para o lançamento Alpha
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List
import json

CULTURE_TEMPLATES = {
    "samurai": {
        "name": "Samurai",
        "description": "Cultura japonesa baseada em honra, disciplina e estratégia refinada",
        "traits": {
            "honor": 0.9,
            "discipline": 0.95,
            "aggression": 0.6,
            "patience": 0.9,
            "tactical": 0.8,
            "positional": 0.85
        },
        "play_style": {
            "opening_preference": "conservative",
            "midgame_focus": "positional",
            "endgame_strength": "technique",
            "risk_tolerance": 0.4,
            "sacrifice_willingness": 0.7
        },
        "pieces": {
            "king": {"model": "emperor", "special": "bushido_defense"},
            "queen": {"model": "shogun", "special": "strategic_vision"},
            "bishop": {"model": "monk", "special": "distant_wisdom"},
            "knight": {"model": "samurai", "special": "honor_leap"},
            "rook": {"model": "castle", "special": "fortress_power"},
            "pawn": {"model": "ashigaru", "special": "loyal_advance"}
        },
        "narratives": {
            "opening": [
                "O mestre samurai contempla o campo de batalha com serenidade...",
                "Com a disciplina de mil anos, a primeira jogada é executada...",
                "O bushido guia cada movimento, honra acima da vitória..."
            ],
            "midgame": [
                "A estratégia samurai se revela, cada peça em harmonia...",
                "Como folhas de cerejeira ao vento, as peças dançam em formação...",
                "A paciência do guerreiro aguarda o momento perfeito..."
            ],
            "endgame": [
                "Com precisão cirúrgica, o samurai finaliza com honra...",
                "A técnica ancestral se manifesta nos movimentos finais...",
                "Vitória com dignidade, derrota com honor - o caminho samurai..."
            ]
        },
        "colors": {
            "primary": "#8B0000",    # Vermelho escuro
            "secondary": "#FFD700",  # Dourado
            "accent": "#000000"      # Preto
        },
        "audio": {
            "ambient": "japanese_garden.mp3",
            "move_sound": "bamboo_strike.wav",
            "capture": "katana_slash.wav"
        }
    },
    
    "viking": {
        "name": "Viking", 
        "description": "Cultura nórdica baseada em agressividade, exploração e coragem",
        "traits": {
            "honor": 0.7,
            "discipline": 0.6,
            "aggression": 0.95,
            "patience": 0.4,
            "tactical": 0.9,
            "positional": 0.5
        },
        "play_style": {
            "opening_preference": "aggressive",
            "midgame_focus": "tactical",
            "endgame_strength": "material",
            "risk_tolerance": 0.8,
            "sacrifice_willingness": 0.9
        },
        "pieces": {
            "king": {"model": "jarl", "special": "warrior_king"},
            "queen": {"model": "valkyrie", "special": "battle_fury"},
            "bishop": {"model": "skald", "special": "saga_vision"},
            "knight": {"model": "berserker", "special": "rage_charge"},
            "rook": {"model": "longship", "special": "raid_power"},
            "pawn": {"model": "warrior", "special": "shield_wall"}
        },
        "narratives": {
            "opening": [
                "Os vikings partem para a batalha com sede de glória...",
                "O rugido de guerra ecoa pelo tabuleiro gelado...",
                "Com a força dos ancestrais, o primeiro golpe é desferido..."
            ],
            "midgame": [
                "A fúria berserker se intensifica no campo de batalha...",
                "Como lobos famintos, os guerreiros avançam sem medo...",
                "O sangue ferve com a proximidade da vitória..."
            ],
            "endgame": [
                "Com a força brutal dos martelos de Thor...",
                "A vitória é conquistada com honra e violência...",
                "Valhalla aguarda os corajosos, Hel recebe os covardes..."
            ]
        },
        "colors": {
            "primary": "#4169E1",    # Azul real
            "secondary": "#C0C0C0",  # Prata
            "accent": "#8B0000"      # Vermelho escuro
        },
        "audio": {
            "ambient": "nordic_winds.mp3",
            "move_sound": "axe_swing.wav",
            "capture": "shield_clash.wav"
        }
    },
    
    "persian": {
        "name": "Persa",
        "description": "Cultura persa baseada em estratégia elaborada, elegância e sofisticação",
        "traits": {
            "honor": 0.8,
            "discipline": 0.8,
            "aggression": 0.65,
            "patience": 0.85,
            "tactical": 0.75,
            "positional": 0.9
        },
        "play_style": {
            "opening_preference": "classical",
            "midgame_focus": "strategic",
            "endgame_strength": "calculation",
            "risk_tolerance": 0.5,
            "sacrifice_willingness": 0.6
        },
        "pieces": {
            "king": {"model": "shah", "special": "royal_decree"},
            "queen": {"model": "vizier", "special": "court_intrigue"},
            "bishop": {"model": "mage", "special": "arcane_sight"},
            "knight": {"model": "immortal", "special": "elite_strike"},
            "rook": {"model": "citadel", "special": "empire_strength"},
            "pawn": {"model": "soldier", "special": "disciplined_march"}
        },
        "narratives": {
            "opening": [
                "O xá contempla seu império no tabuleiro de mármore...",
                "Com a sabedoria de Cyrus, a partida se inicia...",
                "As pétalas de rosa marcam o início da dança estratégica..."
            ],
            "midgame": [
                "A complexa teia persa se desenvolve elegantemente...",
                "Como um jardim de Isfahan, cada peça tem seu lugar...",
                "A paciência do deserto aguarda o momento certo..."
            ],
            "endgame": [
                "Com a precisão de um relojoeiro, a vitória se aproxima...",
                "A geometria sagrada se revela nos movimentos finais...",
                "Elegância e eficiência coroam o triunfo persa..."
            ]
        },
        "colors": {
            "primary": "#800080",    # Púrpura
            "secondary": "#FFD700",  # Dourado
            "accent": "#228B22"      # Verde floresta
        },
        "audio": {
            "ambient": "persian_garden.mp3",
            "move_sound": "silk_rustle.wav",
            "capture": "scimitar_ring.wav"
        }
    }
}

def create_culture_file(culture_name: str, culture_data: Dict[str, Any]) -> bool:
    """Cria o arquivo Python para uma cultura específica"""
    
    culture_file = Path(f"src/cultural/cultures/{culture_name}_culture.py")
    culture_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        content = f'''"""
AEON Chess - {culture_data['name']} Culture
Auto-generated culture implementation
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from ..base_culture import BaseCulture, CulturalTrait

@dataclass
class {culture_data['name']}Culture(BaseCulture):
    """Implementação da cultura {culture_data['name']}"""
    
    def __init__(self):
        super().__init__(
            name="{culture_data['name']}",
            description="{culture_data['description']}"
        )
        
        # Características culturais
        self.traits = {{
{_generate_traits(culture_data['traits'])}
        }}
        
        # Estilo de jogo
        self.play_style = {{
{_generate_play_style(culture_data['play_style'])}
        }}
        
        # Configuração de peças
        self.pieces_config = {{
{_generate_pieces_config(culture_data['pieces'])}
        }}
        
        # Narrativas contextuais
        self.narratives = {{
{_generate_narratives(culture_data['narratives'])}
        }}
        
        # Configuração visual
        self.theme = {{
            "colors": {{
{_generate_colors(culture_data['colors'])}
            }},
            "audio": {{
{_generate_audio(culture_data['audio'])}
            }}
        }}
    
    def get_opening_move_weight(self, move: str) -> float:
        """Retorna peso cultural para um movimento de abertura"""
        if self.play_style["opening_preference"] == "aggressive":
            # Favorece aberturas agressivas
            aggressive_moves = ["e4", "f4", "Nf3", "d4"]
            if any(am in move for am in aggressive_moves):
                return 1.2
        elif self.play_style["opening_preference"] == "conservative":
            # Favorece aberturas posicionais
            positional_moves = ["d4", "Nf3", "c4", "g3"]
            if any(pm in move for pm in positional_moves):
                return 1.2
        elif self.play_style["opening_preference"] == "classical":
            # Favorece aberturas clássicas
            classical_moves = ["e4", "d4", "Nf3", "Nc3"]
            if any(cm in move for cm in classical_moves):
                return 1.1
                
        return 1.0
    
    def get_position_evaluation_bonus(self, position_type: str) -> float:
        """Retorna bônus de avaliação baseado no tipo de posição"""
        bonuses = {{
            "tactical": self.traits["tactical"] * 0.1,
            "positional": self.traits["positional"] * 0.1,
            "aggressive": self.traits["aggression"] * 0.15,
            "defensive": (1.0 - self.traits["aggression"]) * 0.1
        }}
        return bonuses.get(position_type, 0.0)
    
    def get_narrative_for_context(self, context: str) -> str:
        """Retorna narrativa apropriada para o contexto"""
        import random
        narratives = self.narratives.get(context, ["Movimento executado."])
        return random.choice(narratives)
    
    def adapt_to_opponent_style(self, opponent_aggression: float) -> Dict[str, float]:
        """Adapta estilo baseado no oponente"""
        adaptation = {{}}
        
        if opponent_aggression > 0.7:
            # Oponente agressivo - aumentar defesa
            adaptation["patience"] = min(1.0, self.traits["patience"] + 0.1)
            adaptation["aggression"] = max(0.0, self.traits["aggression"] - 0.05)
        elif opponent_aggression < 0.4:
            # Oponente passivo - aumentar agressão
            adaptation["aggression"] = min(1.0, self.traits["aggression"] + 0.1)
            adaptation["patience"] = max(0.0, self.traits["patience"] - 0.05)
        
        return adaptation

# Instância global da cultura
{culture_name}_culture = {culture_data['name']}Culture()

def get_culture():
    """Retorna a instância da cultura {culture_data['name']}"""
    return {culture_name}_culture
'''
        
        culture_file.write_text(content)
        print(f"✅ Cultura {culture_name} criada: {culture_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar {culture_name}: {e}")
        return False

def _generate_traits(traits: Dict[str, float]) -> str:
    """Gera código para os traits"""
    lines = []
    for trait, value in traits.items():
        lines.append(f'            "{trait}": {value}')
    return ",\n".join(lines)

def _generate_play_style(play_style: Dict[str, Any]) -> str:
    """Gera código para o estilo de jogo"""
    lines = []
    for key, value in play_style.items():
        if isinstance(value, str):
            lines.append(f'            "{key}": "{value}"')
        else:
            lines.append(f'            "{key}": {value}')
    return ",\n".join(lines)

def _generate_pieces_config(pieces: Dict[str, Dict[str, str]]) -> str:
    """Gera configuração das peças"""
    lines = []
    for piece, config in pieces.items():
        config_str = "{" + ", ".join(f'"{k}": "{v}"' for k, v in config.items()) + "}"
        lines.append(f'            "{piece}": {config_str}')
    return ",\n".join(lines)

def _generate_narratives(narratives: Dict[str, List[str]]) -> str:
    """Gera narrativas"""
    lines = []
    for context, texts in narratives.items():
        texts_str = "[" + ", ".join(f'"{text}"' for text in texts) + "]"
        lines.append(f'            "{context}": {texts_str}')
    return ",\n".join(lines)

def _generate_colors(colors: Dict[str, str]) -> str:
    """Gera configuração de cores"""
    lines = []
    for color_type, color_value in colors.items():
        lines.append(f'                "{color_type}": "{color_value}"')
    return ",\n".join(lines)

def _generate_audio(audio: Dict[str, str]) -> str:
    """Gera configuração de áudio"""
    lines = []
    for audio_type, audio_file in audio.items():
        lines.append(f'                "{audio_type}": "{audio_file}"')
    return ",\n".join(lines)

def create_base_culture_class():
    """Cria a classe base para todas as culturas"""
    base_file = Path("src/cultural/base_culture.py")
    base_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        content = '''"""
AEON Chess - Base Culture Class
Classe base para todas as implementações culturais
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class CulturalTrait(Enum):
    """Enumeration of cultural traits"""
    HONOR = "honor"
    DISCIPLINE = "discipline"
    AGGRESSION = "aggression"
    PATIENCE = "patience"
    TACTICAL = "tactical"
    POSITIONAL = "positional"

@dataclass
class BaseCulture:
    """Base class for all cultural implementations"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.traits: Dict[str, float] = {}
        self.play_style: Dict[str, Any] = {}
        self.pieces_config: Dict[str, Dict[str, str]] = {}
        self.narratives: Dict[str, List[str]] = {}
        self.theme: Dict[str, Any] = {}
    
    def get_trait_value(self, trait: str) -> float:
        """Get the value of a specific trait"""
        return self.traits.get(trait, 0.5)
    
    def get_opening_move_weight(self, move: str) -> float:
        """Calculate cultural weight for an opening move"""
        return 1.0
    
    def get_position_evaluation_bonus(self, position_type: str) -> float:
        """Get evaluation bonus for position type"""
        return 0.0
    
    def get_narrative_for_context(self, context: str) -> str:
        """Get narrative text for game context"""
        return "Move executed."
    
    def adapt_to_opponent_style(self, opponent_aggression: float) -> Dict[str, float]:
        """Adapt playing style based on opponent"""
        return {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert culture to dictionary representation"""
        return {
            "name": self.name,
            "description": self.description,
            "traits": self.traits,
            "play_style": self.play_style,
            "pieces_config": self.pieces_config,
            "narratives": self.narratives,
            "theme": self.theme
        }
'''
        
        base_file.write_text(content)
        print(f"✅ Classe base criada: {base_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar classe base: {e}")
        return False

def create_cultures_init():
    """Cria o arquivo __init__.py para as culturas"""
    init_file = Path("src/cultural/cultures/__init__.py")
    init_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        content = '''"""
AEON Chess - Cultures Package
Auto-generated cultures initialization
"""

from .samurai_culture import samurai_culture, get_culture as get_samurai_culture
from .viking_culture import viking_culture, get_culture as get_viking_culture  
from .persian_culture import persian_culture, get_culture as get_persian_culture

# Mapeamento de culturas disponíveis
AVAILABLE_CULTURES = {
    "samurai": samurai_culture,
    "viking": viking_culture,
    "persian": persian_culture
}

def get_culture_by_name(name: str):
    """Retorna uma cultura pelo nome"""
    return AVAILABLE_CULTURES.get(name.lower())

def list_available_cultures():
    """Lista todas as culturas disponíveis"""
    return list(AVAILABLE_CULTURES.keys())

# Exporta as culturas
__all__ = [
    "samurai_culture", "viking_culture", "persian_culture",
    "get_samurai_culture", "get_viking_culture", "get_persian_culture",
    "get_culture_by_name", "list_available_cultures", "AVAILABLE_CULTURES"
]
'''
        
        init_file.write_text(content)
        print(f"✅ __init__.py das culturas criado: {init_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar __init__.py: {e}")
        return False

def create_validation_script():
    """Cria script de validação das culturas"""
    validation_file = Path("scripts/validate_cultural_content.py")
    
    try:
        content = '''#!/usr/bin/env python3
"""
AEON Chess - Validação de Conteúdo Cultural
Script para validar se as culturas foram implementadas corretamente
"""

import sys
from pathlib import Path

def validate_cultures():
    """Valida se todas as culturas estão funcionais"""
    
    try:
        # Tenta importar todas as culturas
        from src.cultural.cultures import (
            samurai_culture, viking_culture, persian_culture,
            get_culture_by_name, list_available_cultures
        )
        
        cultures = [samurai_culture, viking_culture, persian_culture]
        
        print("🔍 Validando culturas implementadas...")
        
        for culture in cultures:
            print(f"\\n--- Validando {culture.name} ---")
            
            # Verifica atributos obrigatórios
            required_attrs = ["name", "description", "traits", "play_style"]
            for attr in required_attrs:
                if not hasattr(culture, attr):
                    print(f"❌ Atributo {attr} faltando")
                    return False
                print(f"✅ {attr}: OK")
            
            # Verifica traits
            required_traits = ["honor", "discipline", "aggression", "patience"]
            for trait in required_traits:
                if trait not in culture.traits:
                    print(f"❌ Trait {trait} faltando")
                    return False
                value = culture.traits[trait]
                if not 0.0 <= value <= 1.0:
                    print(f"❌ Trait {trait} com valor inválido: {value}")
                    return False
            print(f"✅ Traits: OK")
            
            # Testa métodos
            try:
                weight = culture.get_opening_move_weight("e4")
                bonus = culture.get_position_evaluation_bonus("tactical")
                narrative = culture.get_narrative_for_context("opening")
                adaptation = culture.adapt_to_opponent_style(0.8)
                print(f"✅ Métodos: OK")
            except Exception as e:
                print(f"❌ Erro nos métodos: {e}")
                return False
        
        # Testa funções utilitárias
        available = list_available_cultures()
        if len(available) != 3:
            print(f"❌ Número incorreto de culturas: {len(available)}")
            return False
        
        for culture_name in ["samurai", "viking", "persian"]:
            culture = get_culture_by_name(culture_name)
            if culture is None:
                print(f"❌ Cultura {culture_name} não encontrada")
                return False
        
        print("\\n🎉 Todas as culturas validadas com sucesso!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    success = validate_cultures()
    sys.exit(0 if success else 1)
'''
        
        validation_file.write_text(content)
        print(f"✅ Script de validação criado: {validation_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar validação: {e}")
        return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Implementa culturas base do AEON Chess")
    parser.add_argument(
        "--cultures",
        default="samurai,viking,persian",
        help="Culturas para implementar (separadas por vírgula)"
    )
    
    args = parser.parse_args()
    cultures_to_implement = [c.strip().lower() for c in args.cultures.split(",")]
    
    print("🚀 Iniciando implementação das culturas base...")
    print(f"📋 Culturas selecionadas: {', '.join(cultures_to_implement)}")
    
    results = {}
    
    # Cria classe base primeiro
    print(f"\\n--- Criando classe base ---")
    results["base_class"] = create_base_culture_class()
    
    # Implementa cada cultura
    for culture_name in cultures_to_implement:
        if culture_name not in CULTURE_TEMPLATES:
            print(f"❌ Cultura {culture_name} não disponível")
            results[culture_name] = False
            continue
            
        print(f"\\n--- Implementando {culture_name} ---")
        culture_data = CULTURE_TEMPLATES[culture_name]
        results[culture_name] = create_culture_file(culture_name, culture_data)
    
    # Cria __init__.py
    print(f"\\n--- Criando inicialização ---")
    results["init_file"] = create_cultures_init()
    
    # Cria script de validação
    print(f"\\n--- Criando validação ---")
    results["validation"] = create_validation_script()
    
    # Resumo dos resultados
    print("\\n" + "="*50)
    print("📊 RESUMO DA IMPLEMENTAÇÃO")
    print("="*50)
    
    success_count = 0
    total_tasks = len(results)
    
    for task, success in results.items():
        status = "✅ SUCESSO" if success else "❌ FALHOU"
        print(f"{status:<12} {task}")
        if success:
            success_count += 1
    
    success_rate = success_count / total_tasks * 100
    print(f"\\n🎯 Taxa de sucesso: {success_rate:.1f}% ({success_count}/{total_tasks})")
    
    if success_rate >= 90:
        print("🎉 Culturas base implementadas com sucesso!")
        return 0
    else:
        print("🚨 Problemas na implementação - verificar logs")
        return 1

if __name__ == "__main__":
    sys.exit(main())
