"""
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
