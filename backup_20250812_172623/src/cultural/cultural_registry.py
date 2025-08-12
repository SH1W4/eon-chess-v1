"""
CHESS Cultural Registry - Central Repository of All Cultures
=============================================================
This file serves as the single source of truth for all cultural implementations.
Never lose a culture again - everything is registered here!

Last Updated: 08/08/2025
Total Cultures: 15+
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum, auto


class CultureCategory(Enum):
    """Categories of cultural themes"""
    HISTORICAL = auto()      # Historical cultures (Aztec, Viking, etc.)
    TEMPORAL = auto()        # Time periods (Medieval, Renaissance)
    FUTURISTIC = auto()      # Future themes (Neo-Tokyo, Quantum)
    REGIONAL = auto()        # Regional cultures (Oriental, Nordic)
    SPECIAL = auto()         # Special themes (Pirate, Space)
    IN_DEVELOPMENT = auto()  # Cultures being developed


class CultureStatus(Enum):
    """Implementation status of cultures"""
    FULLY_IMPLEMENTED = "fully_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IN_DEVELOPMENT = "in_development"
    PLANNED = "planned"


@dataclass
class CultureMetadata:
    """Metadata for a cultural theme"""
    id: str
    name: str
    display_name: str
    category: CultureCategory
    status: CultureStatus
    description: str
    values: List[str]
    piece_metaphors: Dict[str, str]
    narrative_examples: List[str]
    implementation_path: Optional[str] = None
    config_path: Optional[str] = None
    version: str = "0.2.0"


class CulturalRegistry:
    """Central registry of all CHESS cultures"""
    
    def __init__(self):
        self._cultures = self._initialize_cultures()
        self._validate_registry()
    
    def _initialize_cultures(self) -> Dict[str, CultureMetadata]:
        """Initialize all registered cultures"""
        cultures = {}
        
        # ========== HISTORICAL CULTURES ==========
        
        cultures['aztec'] = CultureMetadata(
            id='aztec',
            name='Aztec',
            display_name='Azteca - Guerreiros do Sol',
            category=CultureCategory.HISTORICAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Guerreiros sagrados com rituais de sacrifício e honra divina',
            values=['Honra', 'Sacrifício', 'Guerra Sagrada', 'Divindade'],
            piece_metaphors={
                'pawn': 'Guerreiro Águia',
                'rook': 'Templo/Pirâmide',
                'knight': 'Guerreiro Jaguar',
                'bishop': 'Sacerdote',
                'queen': 'Sacerdotisa',
                'king': 'Tlatoani (Imperador)'
            },
            narrative_examples=[
                'O Guerreiro Águia avança com a bênção de Huitzilopochtli',
                'O Templo sagrado protege o campo de batalha',
                'O Tlatoani comanda com a sabedoria dos ancestrais'
            ],
            implementation_path='src/cultural/cultures/aztec_culture.py',
            config_path='cultural_data/configurations/themes/aztec_empire.yaml'
        )
        
        cultures['viking'] = CultureMetadata(
            id='viking',
            name='Viking',
            display_name='Viking - Exploradores Nórdicos',
            category=CultureCategory.HISTORICAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Bravos guerreiros do norte em busca de glória e Valhalla',
            values=['Bravura', 'Conquista', 'Honra em Batalha', 'Glória'],
            piece_metaphors={
                'pawn': 'Guerreiro Viking',
                'rook': 'Fortaleza/Drakkar',
                'knight': 'Berserker',
                'bishop': 'Skald (Poeta Guerreiro)',
                'queen': 'Valquíria',
                'king': 'Jarl'
            },
            narrative_examples=[
                'O Berserker entra em fúria de batalha',
                'A Valquíria escolhe os dignos para Valhalla',
                'O Jarl lidera seu clã para a glória'
            ],
            implementation_path='src/cultural/cultures/viking_culture.py',
            config_path='cultural_data/configurations/themes/viking_raiders.yaml'
        )
        
        cultures['samurai'] = CultureMetadata(
            id='samurai',
            name='Samurai',
            display_name='Samurai - Código Bushido',
            category=CultureCategory.HISTORICAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Guerreiros disciplinados seguindo o caminho da honra',
            values=['Bushido', 'Disciplina', 'Lealdade', 'Perfeição'],
            piece_metaphors={
                'pawn': 'Ashigaru (Soldado)',
                'rook': 'Castelo/Pagode',
                'knight': 'Samurai Montado',
                'bishop': 'Monge Guerreiro',
                'queen': 'Onna-bugeisha',
                'king': 'Daimyo'
            },
            narrative_examples=[
                'O Samurai move-se com precisão mortal',
                'A honra do Bushido guia cada movimento',
                'O Daimyo mantém a harmonia do han'
            ],
            implementation_path='src/cultural/cultures/samurai_culture.py',
            config_path='cultural_data/configurations/themes/samurai_honor.yaml'
        )
        
        cultures['maya'] = CultureMetadata(
            id='maya',
            name='Maya',
            display_name='Maia - Sabedoria Astronômica',
            category=CultureCategory.HISTORICAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Sábios astrônomos em harmonia com os ciclos celestiais',
            values=['Astronomia', 'Matemática', 'Harmonia Cósmica', 'Profecia'],
            piece_metaphors={
                'pawn': 'Guerreiro Quetzal',
                'rook': 'Observatório',
                'knight': 'Guerreiro Jaguar',
                'bishop': 'Sacerdote Astronômico',
                'queen': 'Sacerdotisa Lunar',
                'king': 'Ahau (Rei Divino)'
            },
            narrative_examples=[
                'As estrelas alinham-se para guiar o movimento',
                'O calendário sagrado prevê a vitória',
                'O Ahau move-se em harmonia com os ciclos celestiais'
            ],
            implementation_path='src/cultural/cultures/mayan_culture.py',
            config_path='cultural_data/configurations/themes/mayan_prophecy.yaml'
        )
        
        # ========== TEMPORAL EPOCHS ==========
        
        cultures['medieval'] = CultureMetadata(
            id='medieval',
            name='Medieval',
            display_name='Medieval - Era dos Cavaleiros',
            category=CultureCategory.TEMPORAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Cavaleiros nobres defendendo reinos com honra e fé',
            values=['Cavalaria', 'Honra Feudal', 'Fé', 'Lealdade'],
            piece_metaphors={
                'pawn': 'Soldado/Camponês',
                'rook': 'Castelo/Torre de Vigia',
                'knight': 'Cavaleiro',
                'bishop': 'Clérigo',
                'queen': 'Rainha/Dama',
                'king': 'Rei/Monarca'
            },
            narrative_examples=[
                'O nobre cavaleiro avança para defender o reino',
                'O castelo permanece como bastião impenetrável',
                'Pela honra e pela glória do reino!'
            ],
            implementation_path='src/cultural/narratives_config.json',
            config_path='config/narrative/cultures_expanded.yaml'
        )
        
        cultures['renaissance'] = CultureMetadata(
            id='renaissance',
            name='Renaissance',
            display_name='Renascimento - Arte e Humanismo',
            category=CultureCategory.TEMPORAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Era de arte, ciência e despertar humanista',
            values=['Arte', 'Ciência', 'Humanismo', 'Inovação'],
            piece_metaphors={
                'pawn': 'Artesão',
                'rook': 'Fortaleza Cultural',
                'knight': 'Condottiero',
                'bishop': 'Humanista',
                'queen': 'Patrona das Artes',
                'king': 'Príncipe Iluminado'
            },
            narrative_examples=[
                'Com graça artística, a peça move-se harmoniosamente',
                'O equilíbrio perfeito entre força e beleza',
                'Uma jogada digna de Da Vinci'
            ],
            implementation_path=None,
            config_path='config/narrative/cultures_expanded.yaml'
        )
        
        # ========== FUTURISTIC THEMES ==========
        
        cultures['neo_tokyo'] = CultureMetadata(
            id='neo_tokyo',
            name='Neo-Tokyo 2050',
            display_name='Neo-Tokyo 2050 - Cyberpunk Avançado',
            category=CultureCategory.FUTURISTIC,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Metrópole cyberpunk com IA avançada e tecnologia de ponta',
            values=['Eficiência', 'Inovação', 'Tecnologia', 'Controle'],
            piece_metaphors={
                'pawn': 'Cyber-Soldado',
                'rook': 'Torre de Dados',
                'knight': 'Mecha Ligeiro',
                'bishop': 'Hacker Neural',
                'queen': 'IA Suprema',
                'king': 'CEO Corporativo'
            },
            narrative_examples=[
                'Sistema tático otimizado, executando movimento',
                'Interface neural sincronizada para máxima eficiência',
                'Protocolo de vitória em execução'
            ],
            implementation_path='examples/cultural_ai_demo.py',
            config_path='config/aeon_core.yaml'
        )
        
        cultures['steampunk'] = CultureMetadata(
            id='steampunk',
            name='Steampunk',
            display_name='Steampunk - Vapor e Engrenagens',
            category=CultureCategory.FUTURISTIC,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Era vitoriana alternativa movida a vapor e mecânica',
            values=['Engenhosidade', 'Mecânica', 'Vapor', 'Invenção'],
            piece_metaphors={
                'pawn': 'Autômato',
                'rook': 'Torre de Vapor',
                'knight': 'Cavalaria Mecânica',
                'bishop': 'Engenheiro',
                'queen': 'Inventora Suprema',
                'king': 'Lorde Industrial'
            },
            narrative_examples=[
                'Engrenagens giram em perfeita sincronia',
                'O vapor impulsiona o avanço mecânico',
                'Uma manobra digna da era das máquinas'
            ],
            implementation_path=None,
            config_path='config/narrative/config.yaml'
        )
        
        cultures['quantum'] = CultureMetadata(
            id='quantum',
            name='Quantum Realm',
            display_name='Quantum Realm - Superposição Quântica',
            category=CultureCategory.FUTURISTIC,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Realidade quântica onde probabilidades definem o destino',
            values=['Probabilidade', 'Superposição', 'Entrelaçamento', 'Incerteza'],
            piece_metaphors={
                'pawn': 'Partícula Quântica',
                'rook': 'Estabilizador Dimensional',
                'knight': 'Salto Quântico',
                'bishop': 'Observador',
                'queen': 'Entrelaçamento Supremo',
                'king': 'Núcleo Quântico'
            },
            narrative_examples=[
                'A peça existe em superposição até ser observada',
                'Colapso da função de onda em posição favorável',
                'Entrelaçamento quântico estabelecido'
            ],
            implementation_path='src/quantum/',
            config_path='config/aeon_core.yaml'
        )
        
        # ========== REGIONAL CULTURES ==========
        
        cultures['oriental'] = CultureMetadata(
            id='oriental',
            name='Oriental/Eastern',
            display_name='Oriental - Filosofia e Equilíbrio',
            category=CultureCategory.REGIONAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Sabedoria oriental focada em harmonia e equilíbrio',
            values=['Harmonia', 'Equilíbrio', 'Sabedoria', 'Fluidez'],
            piece_metaphors={
                'pawn': 'Discípulo',
                'rook': 'Pagode',
                'knight': 'Guerreiro Montado',
                'bishop': 'Monge Sábio',
                'queen': 'Imperatriz Celestial',
                'king': 'Imperador do Céu'
            },
            narrative_examples=[
                'O movimento flui como água, adaptando-se ao terreno',
                'Em perfeito equilíbrio com o Tao do tabuleiro',
                'A sabedoria milenar guia a estratégia'
            ],
            implementation_path=None,
            config_path='config/narrative/cultures_expanded.yaml'
        )
        
        cultures['nordic'] = CultureMetadata(
            id='nordic',
            name='Nordic',
            display_name='Nórdica - Mitologia e Sagas',
            category=CultureCategory.REGIONAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Mitologia nórdica com runas, destino e sagas épicas',
            values=['Destino', 'Runas', 'Mitologia', 'Wyrd'],
            piece_metaphors={
                'pawn': 'Guerreiro do Norte',
                'rook': 'Salão dos Heróis',
                'knight': 'Cavaleiro de Odin',
                'bishop': 'Vidente Rúnico',
                'queen': 'Frigg/Freyja',
                'king': 'Odin/Thor'
            },
            narrative_examples=[
                'As runas preveem o caminho da vitória',
                'Pelos nove reinos, a batalha será vencida!',
                'O destino tecido pelas Nornas se cumpre'
            ],
            implementation_path=None,
            config_path='config/narrative/cultures_expanded.yaml'
        )
        
        # ========== SPECIAL STYLES ==========
        
        cultures['pirate'] = CultureMetadata(
            id='pirate',
            name='Pirate',
            display_name='Pirata - Aventura nos Sete Mares',
            category=CultureCategory.SPECIAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Vida pirata com liberdade, aventura e busca por tesouros',
            values=['Liberdade', 'Aventura', 'Tesouro', 'Código Pirata'],
            piece_metaphors={
                'pawn': 'Marujo',
                'rook': 'Navio/Fortaleza Costeira',
                'knight': 'Corsário',
                'bishop': 'Navegador',
                'queen': 'Capitã Pirata',
                'king': 'Lorde Pirata'
            },
            narrative_examples=[
                'Içar velas! Rumo ao tesouro!',
                'O código pirata guia nossa estratégia',
                'Pelos sete mares, a vitória será nossa!'
            ],
            implementation_path=None,
            config_path=None
        )
        
        cultures['space'] = CultureMetadata(
            id='space',
            name='Space',
            display_name='Espacial - Conquista Galáctica',
            category=CultureCategory.SPECIAL,
            status=CultureStatus.FULLY_IMPLEMENTED,
            description='Exploração espacial e conquista galáctica',
            values=['Exploração', 'Conquista Galáctica', 'Tecnologia', 'Fronteira Final'],
            piece_metaphors={
                'pawn': 'Soldado Espacial',
                'rook': 'Estação Orbital',
                'knight': 'Caça Estelar',
                'bishop': 'Navegador Cósmico',
                'queen': 'Comandante da Frota',
                'king': 'Almirante Galáctico'
            },
            narrative_examples=[
                'Iniciando manobra orbital para posição estratégica',
                'A frota estelar avança pelo quadrante',
                'Pelo domínio da galáxia!'
            ],
            implementation_path=None,
            config_path=None
        )
        
        # ========== IN DEVELOPMENT ==========
        
        cultures['egyptian'] = CultureMetadata(
            id='egyptian',
            name='Egyptian',
            display_name='Egípcia - Mistérios Antigos',
            category=CultureCategory.IN_DEVELOPMENT,
            status=CultureStatus.PARTIALLY_IMPLEMENTED,
            description='Antiga civilização do Nilo com divindades e eternidade',
            values=['Eternidade', "Ma'at", 'Divindade', 'Mistério'],
            piece_metaphors={
                'pawn': 'Soldado do Faraó',
                'rook': 'Pirâmide',
                'knight': 'Carruagem de Guerra',
                'bishop': 'Alto Sacerdote',
                'queen': 'Cleópatra/Nefertiti',
                'king': 'Faraó'
            },
            narrative_examples=[
                'Pelos deuses do Nilo, a vitória será nossa',
                'A pirâmide permanece eterna no campo',
                'O Faraó comanda com poder divino'
            ],
            implementation_path=None,
            config_path=None
        )
        
        cultures['byzantine'] = CultureMetadata(
            id='byzantine',
            name='Byzantine',
            display_name='Bizantina - Diplomacia Imperial',
            category=CultureCategory.IN_DEVELOPMENT,
            status=CultureStatus.PARTIALLY_IMPLEMENTED,
            description='Império de estratégia complexa e diplomacia refinada',
            values=['Diplomacia', 'Estratégia', 'Império', 'Intriga'],
            piece_metaphors={
                'pawn': 'Legionário',
                'rook': 'Muralha de Constantinopla',
                'knight': 'Catafracto',
                'bishop': 'Patriarca',
                'queen': 'Imperatriz',
                'king': 'Basileus'
            },
            narrative_examples=[
                'A diplomacia bizantina supera a força bruta',
                'As muralhas de Constantinopla são inexpugnáveis',
                'O Basileus governa com astúcia imperial'
            ],
            implementation_path=None,
            config_path='cultural_data/configurations/themes/byzantine_empire.yaml'
        )
        
        cultures['greek'] = CultureMetadata(
            id='greek',
            name='Greek',
            display_name='Grega - Filosofia e Democracia',
            category=CultureCategory.IN_DEVELOPMENT,
            status=CultureStatus.PARTIALLY_IMPLEMENTED,
            description='Berço da filosofia ocidental e estratégia militar',
            values=['Filosofia', 'Democracia', 'Areté (Excelência)', 'Logos'],
            piece_metaphors={
                'pawn': 'Hoplita',
                'rook': 'Acrópole',
                'knight': 'Cavalaria Tessália',
                'bishop': 'Filósofo',
                'queen': 'Atena',
                'king': 'Estratego'
            },
            narrative_examples=[
                'A falange avança em formação perfeita',
                'A sabedoria de Atena guia a estratégia',
                'Pela glória de Atenas e da Hélade!'
            ],
            implementation_path=None,
            config_path=None
        )
        
        return cultures
    
    def _validate_registry(self):
        """Validate the cultural registry integrity"""
        implemented_count = sum(
            1 for c in self._cultures.values() 
            if c.status == CultureStatus.FULLY_IMPLEMENTED
        )
        
        if implemented_count < 13:
            print(f"⚠️ Warning: Expected at least 13 fully implemented cultures, found {implemented_count}")
        
        # Check for duplicates
        names = [c.name for c in self._cultures.values()]
        if len(names) != len(set(names)):
            print("⚠️ Warning: Duplicate culture names detected!")
    
    def get_all_cultures(self) -> List[CultureMetadata]:
        """Get all registered cultures"""
        return list(self._cultures.values())
    
    def get_culture(self, culture_id: str) -> Optional[CultureMetadata]:
        """Get a specific culture by ID"""
        return self._cultures.get(culture_id)
    
    def get_cultures_by_category(self, category: CultureCategory) -> List[CultureMetadata]:
        """Get all cultures in a specific category"""
        return [c for c in self._cultures.values() if c.category == category]
    
    def get_cultures_by_status(self, status: CultureStatus) -> List[CultureMetadata]:
        """Get all cultures with a specific status"""
        return [c for c in self._cultures.values() if c.status == status]
    
    def get_implemented_cultures(self) -> List[CultureMetadata]:
        """Get all fully implemented cultures"""
        return self.get_cultures_by_status(CultureStatus.FULLY_IMPLEMENTED)
    
    def get_statistics(self) -> Dict:
        """Get registry statistics"""
        return {
            'total_cultures': len(self._cultures),
            'fully_implemented': len(self.get_cultures_by_status(CultureStatus.FULLY_IMPLEMENTED)),
            'partially_implemented': len(self.get_cultures_by_status(CultureStatus.PARTIALLY_IMPLEMENTED)),
            'in_development': len(self.get_cultures_by_status(CultureStatus.IN_DEVELOPMENT)),
            'by_category': {
                category.name: len(self.get_cultures_by_category(category))
                for category in CultureCategory
            }
        }
    
    def print_summary(self):
        """Print a summary of all cultures"""
        print("\n" + "="*60)
        print("CHESS CULTURAL REGISTRY SUMMARY")
        print("="*60)
        
        stats = self.get_statistics()
        print(f"\nTotal Cultures: {stats['total_cultures']}")
        print(f"Fully Implemented: {stats['fully_implemented']}")
        print(f"In Development: {stats['in_development'] + stats['partially_implemented']}")
        
        print("\nBy Category:")
        for category in CultureCategory:
            cultures = self.get_cultures_by_category(category)
            if cultures:
                print(f"\n{category.name}:")
                for culture in cultures:
                    status_icon = "✅" if culture.status == CultureStatus.FULLY_IMPLEMENTED else "🚧"
                    print(f"  {status_icon} {culture.display_name}")
        
        print("\n" + "="*60)


# Global registry instance
CULTURAL_REGISTRY = CulturalRegistry()


def get_registry() -> CulturalRegistry:
    """Get the global cultural registry instance"""
    return CULTURAL_REGISTRY


if __name__ == "__main__":
    # Test the registry
    registry = get_registry()
    registry.print_summary()
    
    # Example usage
    print("\n📋 Example: Getting Neo-Tokyo culture:")
    neo_tokyo = registry.get_culture('neo_tokyo')
    if neo_tokyo:
        print(f"  Name: {neo_tokyo.display_name}")
        print(f"  Description: {neo_tokyo.description}")
        print(f"  Values: {', '.join(neo_tokyo.values)}")
    
    print("\n📊 Registry Statistics:")
    stats = registry.get_statistics()
    for key, value in stats.items():
        if key != 'by_category':
            print(f"  {key}: {value}")
