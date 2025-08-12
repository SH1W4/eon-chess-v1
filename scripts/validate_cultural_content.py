#!/usr/bin/env python3
"""
AEON Chess - Validação de Conteúdo Cultural
Script para validar se as culturas foram implementadas corretamente
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

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
            print(f"\n--- Validando {culture.name} ---")
            
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
        
        print("\n🎉 Todas as culturas validadas com sucesso!")
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
