from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class CulturalOpening:
    name: str
    moves: List[str]
    description: str
    cultural_values: Dict[str, float]
    recommendations: List[str]

class CulturalOpeningBook:
    """Livro de aberturas com aspectos culturais"""
    
    def __init__(self):
        self.medieval_openings = {
            "King's Gambit": CulturalOpening(
                name="King's Gambit",
                moves=["e2e4", "e7e5", "f2f4"],
                description="Uma abertura agressiva e cavalheiresca, onde as brancas "
                         "oferecem um peão em sacrifício pelo controle do centro e "
                         "iniciativa de ataque. Representa a nobreza do sacrifício "
                         "e a busca pela glória através de ações ousadas.",
                cultural_values={
                    "honor": 0.9,
                    "tradition": 0.7,
                    "aggression": 0.8,
                    "risk_taking": 0.9
                },
                recommendations=[
                    "Busque ataques diretos ao rei",
                    "Valorize sacrifícios por iniciativa",
                    "Mantenha a pressão constante"
                ]
            ),
            
            "Italian Game": CulturalOpening(
                name="Italian Game",
                moves=["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
                description="Uma abertura clássica que enfatiza o desenvolvimento "
                         "harmonioso das peças e o controle do centro. Reflete os "
                         "ideais medievais de ordem, desenvolvimento sistemático "
                         "e respeito às tradições.",
                cultural_values={
                    "honor": 0.7,
                    "tradition": 0.9,
                    "aggression": 0.5,
                    "risk_taking": 0.4
                },
                recommendations=[
                    "Desenvolva as peças de forma ordenada",
                    "Estabeleça controle central sólido",
                    "Prepare-se para um jogo posicional"
                ]
            ),
            
            "Vienna Game": CulturalOpening(
                name="Vienna Game",
                moves=["e2e4", "e7e5", "b1c3"],
                description="Uma abertura que combina elementos de controle central "
                         "com flexibilidade tática. Representa o equilíbrio entre "
                         "tradição e inovação na cultura medieval.",
                cultural_values={
                    "honor": 0.6,
                    "tradition": 0.6,
                    "aggression": 0.7,
                    "risk_taking": 0.6
                },
                recommendations=[
                    "Mantenha flexibilidade tática",
                    "Prepare-se para transições dinâmicas",
                    "Use a mobilidade do cavalo"
                ]
            ),
            
            "Sicilian Dragon": CulturalOpening(
                name="Sicilian Dragon",
                moves=["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "g7g6"],
                description="Uma variante agressiva e complexa que evoca a imagem do "
                         "dragão medieval. A estrutura de peões lembra as escamas "
                         "de um dragão protegendo o rei.",
                cultural_values={
                    "honor": 0.8,
                    "tradition": 0.5,
                    "aggression": 0.9,
                    "risk_taking": 0.8
                },
                recommendations=[
                    "Fortifique a estrutura do dragão",
                    "Prepare ataques no flanco do rei",
                    "Mantenha o bispo dragão ativo"
                ]
            )
        }
        
        self.futuristic_openings = {
            "Hypermodern Defense": CulturalOpening(
                name="Hypermodern Defense",
                moves=["g1f3", "d7d5", "c2c4"],
                description="Uma abordagem não-convencional que desafia os princípios "
                         "tradicionais. Representa a inovação tecnológica e o "
                         "pensamento disruptivo da cultura futurista.",
                cultural_values={
                    "innovation": 0.9,
                    "tradition": 0.2,
                    "efficiency": 0.8,
                    "adaptability": 0.9
                },
                recommendations=[
                    "Use controle flexível do centro",
                    "Explore padrões não convencionais",
                    "Adapte-se às respostas do oponente"
                ]
            ),
            
            "AI Variation": CulturalOpening(
                name="AI Variation",
                moves=["b1c3", "d7d5", "e2e4"],
                description="Uma sequência otimizada por análise computacional, "
                         "enfatizando eficiência e adaptabilidade. Representa a "
                         "fusão entre intuição estratégica e precisão algorítmica.",
                cultural_values={
                    "innovation": 0.8,
                    "efficiency": 0.9,
                    "adaptability": 0.8,
                    "calculation": 0.9
                },
                recommendations=[
                    "Maximize eficiência posicional",
                    "Calcule variantes precisas",
                    "Mantenha flexibilidade estrutural"
                ]
            ),
            
            "Quantum Defense": CulturalOpening(
                name="Quantum Defense",
                moves=["d2d4", "g8f6", "c2c4", "e7e6"],
                description="Uma defesa que enfatiza possibilidades múltiplas e "
                         "superposição de ameaças. Inspirada em princípios de "
                         "computação quântica e teoria da informação.",
                cultural_values={
                    "innovation": 0.9,
                    "complexity": 0.8,
                    "adaptability": 0.9,
                    "calculation": 0.7
                },
                recommendations=[
                    "Crie ameaças múltiplas",
                    "Mantenha opções abertas",
                    "Explore ambiguidades posicionais"
                ]
            ),
            
            "Cyborg System": CulturalOpening(
                name="Cyborg System",
                moves=["e2e4", "e7e6", "d2d4", "d7d5", "e4e5"],
                description="Um sistema que combina elementos clássicos com ideias "
                         "modernas. Representa a integração entre humano e máquina, "
                         "tradição e inovação.",
                cultural_values={
                    "innovation": 0.7,
                    "tradition": 0.4,
                    "efficiency": 0.8,
                    "hybridization": 0.9
                },
                recommendations=[
                    "Combine táticas clássicas e modernas",
                    "Busque sinergias entre peças",
                    "Mantenha equilíbrio dinâmico"
                ]
            )
        }
    
    def get_next_move(self, moves: List[str], culture_type: str) -> Optional[str]:
        """Sugere o próximo movimento de acordo com o livro de aberturas"""
        openings = self.medieval_openings if culture_type == 'medieval' else self.futuristic_openings
        
        for opening in openings.values():
            if len(moves) < len(opening.moves):
                # Verifica se os movimentos até agora seguem a abertura
                if moves == opening.moves[:len(moves)]:
                    return opening.moves[len(moves)]
        return None
    
    def get_opening(self, moves: List[str], culture_type: str) -> Optional[CulturalOpening]:
        """Encontra uma abertura correspondente à sequência de movimentos"""
        openings = self.medieval_openings if culture_type == 'medieval' else self.futuristic_openings
        
        for opening in openings.values():
            # Verifica se os movimentos correspondem ao início da abertura
            if len(moves) <= len(opening.moves):
                if moves == opening.moves[:len(moves)]:
                    return opening
        return None
    
    def get_cultural_context(self, moves: List[str], culture_type: str) -> Dict[str, Any]:
        """Retorna o contexto cultural da posição atual"""
        opening = self.get_opening(moves, culture_type)
        if not opening:
            return {
                "type": "unknown",
                "values": {},
                "recommendations": []
            }
        
        progress = len(moves) / len(opening.moves)
        return {
            "type": opening.name,
            "progress": progress,
            "values": opening.cultural_values,
            "description": opening.description,
            "recommendations": opening.recommendations
        }
