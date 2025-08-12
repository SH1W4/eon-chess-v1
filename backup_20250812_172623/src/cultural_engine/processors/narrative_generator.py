from typing import Dict, List, Any, Optional
import random
import logging
from pathlib import Path

class NarrativeGenerator:
    """
    Gerador de narrativas culturais baseado em perfis de liderança e estado do jogo.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self._load_narrative_templates()

    def _setup_logging(self):
        """Configura o logging para o gerador."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _load_narrative_templates(self):
        """Carrega templates de narrativa."""
        self.templates = {
            'opening': {
                'aggressive': [
                    "Como {leader}, que dominava o campo de batalha com ousadia, este movimento demonstra uma clara intenção de controle central.",
                    "Seguindo a filosofia agressiva de {leader}, esta jogada estabelece uma presença forte no centro.",
                ],
                'strategic': [
                    "Ecoando a sabedoria estratégica de {leader}, este movimento estabelece uma base sólida para operações futuras.",
                    "Com a visão de longo prazo característica de {leader}, esta posição oferece múltiplas possibilidades.",
                ],
                'defensive': [
                    "Refletindo a cautela calculada de {leader}, esta estrutura proporciona uma defesa robusta.",
                    "Como {leader}, que valorizava a preparação adequada, este movimento fortalece a posição defensiva.",
                ]
            },
            'middlegame': {
                'tactical': [
                    "Um golpe tático digno de {leader}, criando múltiplas ameaças simultaneamente.",
                    "Como nas batalhas de {leader}, este movimento força o oponente a reagir em múltiplas frentes.",
                ],
                'positional': [
                    "Demonstrando o domínio posicional que fez {leader} legendário, esta jogada restringe as opções do oponente.",
                    "Com a precisão estratégica de {leader}, este movimento consolida o controle territorial.",
                ],
                'dynamic': [
                    "Um movimento dinâmico que reflete a adaptabilidade de {leader} em situações complexas.",
                    "Como {leader} em momentos cruciais, esta jogada transforma a natureza da posição.",
                ]
            },
            'endgame': {
                'technical': [
                    "Com a precisão técnica que caracterizava {leader}, este movimento maximiza a vantagem posicional.",
                    "Demonstrando a eficiência de {leader} na conversão de vantagens, esta jogada simplifica o caminho para a vitória.",
                ],
                'creative': [
                    "Um final criativo digno de {leader}, encontrando recursos únicos na posição.",
                    "Como {leader}, que via oportunidades onde outros viam limitações, este movimento explora possibilidades sutis.",
                ],
                'strategic': [
                    "Ecoando a visão estratégica de {leader}, este movimento prepara o caminho para um final vitorioso.",
                    "Com a clareza de propósito de {leader}, esta jogada direciona o jogo para um final favorável.",
                ]
            }
        }

    def generate_narrative(self, 
                         profile: Dict[str, Any], 
                         game_state: Dict[str, Any],
                         move_info: Dict[str, Any]) -> str:
        """
        Gera uma narrativa cultural baseada no perfil de liderança e estado do jogo.
        """
        try:
            # Determina a fase do jogo
            game_phase = self._determine_game_phase(game_state)
            
            # Determina o estilo do movimento
            move_style = self._analyze_move_style(move_info, profile)
            
            # Seleciona template apropriado
            narrative = self._select_and_fill_template(
                game_phase,
                move_style,
                profile,
                game_state
            )
            
            # Adiciona contexto cultural
            narrative = self._add_cultural_context(narrative, profile, game_state)
            
            return narrative

        except Exception as e:
            self.logger.error(f"Erro ao gerar narrativa: {str(e)}")
            return "Movimento realizado."  # Fallback básico

    def _determine_game_phase(self, game_state: Dict[str, Any]) -> str:
        """Determina a fase atual do jogo."""
        move_number = game_state.get('move_number', 0)
        material_count = game_state.get('material_count', 32)
        
        if move_number <= 10:
            return 'opening'
        elif material_count <= 16:
            return 'endgame'
        else:
            return 'middlegame'

    def _analyze_move_style(self, 
                          move_info: Dict[str, Any], 
                          profile: Dict[str, Any]) -> str:
        """Analisa o estilo do movimento realizado."""
        # Análise baseada em critérios como:
        # - Captura de peça
        # - Controle central
        # - Desenvolvimento de peças
        # - Estrutura de peões
        is_capture = move_info.get('is_capture', False)
        is_central = move_info.get('is_central', False)
        is_development = move_info.get('is_development', False)
        
        if is_capture and profile.get('leadership_style', '').lower() == 'aggressive':
            return 'tactical'
        elif is_central and is_development:
            return 'positional'
        else:
            return 'strategic'

    def _select_and_fill_template(self,
                                game_phase: str,
                                move_style: str,
                                profile: Dict[str, Any],
                                game_state: Dict[str, Any]) -> str:
        """Seleciona e preenche um template narrativo apropriado."""
        # Seleciona template baseado na fase e estilo
        available_templates = self.templates.get(game_phase, {}).get(move_style, [])
        if not available_templates:
            available_templates = self.templates.get(game_phase, {}).get('strategic', [])
        
        template = random.choice(available_templates)
        
        # Preenche o template com informações do perfil
        narrative = template.format(
            leader=profile.get('name', 'um líder'),
            style=profile.get('leadership_style', 'estratégico')
        )
        
        return narrative

    def _add_cultural_context(self,
                            narrative: str,
                            profile: Dict[str, Any],
                            game_state: Dict[str, Any]) -> str:
        """Adiciona contexto cultural à narrativa."""
        cultural_elements = profile.get('cultural_impact', '')
        era = profile.get('era', '')
        
        # Adiciona referência histórica se relevante
        if era and cultural_elements:
            context = f"\nEsta abordagem reflete a era de {era}, quando {cultural_elements}"
            narrative += context
        
        return narrative

    def generate_strategic_insight(self,
                                 profile: Dict[str, Any],
                                 game_state: Dict[str, Any]) -> str:
        """Gera insights estratégicos baseados no perfil de liderança."""
        leadership_style = profile.get('leadership_style', '')
        strategic_elements = profile.get('strategic_elements', [])
        
        insights = [
            f"Seguindo os princípios de {profile.get('name', 'liderança')}:",
            f"• Estilo: {leadership_style}"
        ]
        
        # Adiciona elementos estratégicos relevantes
        if strategic_elements:
            insights.append("• Elementos estratégicos principais:")
            for element in strategic_elements[:3]:  # Limita a 3 elementos
                insights.append(f"  - {element}")
        
        return "\n".join(insights)

    def generate_cultural_perspective(self,
                                   profile: Dict[str, Any],
                                   game_state: Dict[str, Any]) -> str:
        """Gera uma perspectiva cultural sobre a posição atual."""
        cultural_impact = profile.get('cultural_impact', '')
        domain = profile.get('domain', '')
        achievements = profile.get('achievements', [])
        
        perspective = [
            f"Na perspectiva de {profile.get('name', 'um líder')}:",
            f"• Domínio: {domain}"
        ]
        
        # Adiciona realizações relevantes
        if achievements:
            perspective.append("• Contexto histórico relevante:")
            achievement = random.choice(achievements)
            perspective.append(f"  - {achievement}")
        
        if cultural_impact:
            perspective.append(f"• Impacto cultural: {cultural_impact}")
        
        return "\n".join(perspective)
