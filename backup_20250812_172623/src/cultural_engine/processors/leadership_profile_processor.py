from typing import Dict, List, Any, Optional
import yaml
from pathlib import Path
import logging

class LeadershipProfileProcessor:
    """
    Processador responsável por analisar e extrair informações relevantes dos perfis de liderança.
    """
    def __init__(self, profiles_path: str):
        self.profiles_path = Path(profiles_path)
        self.logger = logging.getLogger(__name__)
        self._cached_profiles = {}
        self._pattern_index = {}
        self._setup_logging()

    def _setup_logging(self):
        """Configura o logging para o processador."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def load_profiles(self) -> Dict[str, Any]:
        """Carrega todos os perfis de liderança do arquivo YAML."""
        try:
            with open(self.profiles_path, 'r', encoding='utf-8') as f:
                profiles = yaml.safe_load(f)
            self._cached_profiles = profiles
            self._build_pattern_index()
            return profiles
        except Exception as e:
            self.logger.error(f"Erro ao carregar perfis: {str(e)}")
            return {}

    def _build_pattern_index(self):
        """Constrói um índice de padrões estratégicos dos perfis."""
        self._pattern_index = {}
        for profile_id, profile in self._cached_profiles.items():
            if 'strategic_elements' in profile:
                for element in profile['strategic_elements']:
                    if element not in self._pattern_index:
                        self._pattern_index[element] = []
                    self._pattern_index[element].append(profile_id)

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Recupera um perfil específico."""
        return self._cached_profiles.get(profile_id)

    def find_patterns(self, pattern_type: str) -> List[Dict[str, Any]]:
        """Encontra todos os perfis que contêm um determinado padrão estratégico."""
        profile_ids = self._pattern_index.get(pattern_type, [])
        return [self._cached_profiles[pid] for pid in profile_ids]

    def analyze_strategic_elements(self, profile_id: str) -> Dict[str, Any]:
        """Analisa os elementos estratégicos de um perfil específico."""
        profile = self.get_profile(profile_id)
        if not profile:
            return {}

        return {
            'strategic_patterns': profile.get('strategic_elements', []),
            'effectiveness_metrics': profile.get('adaptative_metrics', {}),
            'cultural_impact': profile.get('cultural_impact', ''),
            'leadership_style': profile.get('leadership_style', '')
        }

    def get_narrative_elements(self, profile_id: str) -> List[str]:
        """Recupera os elementos narrativos de um perfil."""
        profile = self.get_profile(profile_id)
        if not profile:
            return []
        return profile.get('narrative_elements', [])

    def match_strategy(self, game_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Encontra perfis de liderança que melhor se adequam ao estado atual do jogo.
        """
        matched_profiles = []
        for profile_id, profile in self._cached_profiles.items():
            match_score = self._calculate_strategy_match(profile, game_state)
            if match_score > 0.7:  # Threshold de correspondência
                matched_profiles.append({
                    'profile_id': profile_id,
                    'match_score': match_score,
                    'strategic_elements': profile.get('strategic_elements', []),
                    'leadership_style': profile.get('leadership_style', '')
                })
        
        return sorted(matched_profiles, key=lambda x: x['match_score'], reverse=True)

    def _calculate_strategy_match(self, profile: Dict[str, Any], game_state: Dict[str, Any]) -> float:
        """
        Calcula o quanto um perfil corresponde ao estado atual do jogo.
        """
        score = 0.0
        total_weights = 0.0

        # Análise de posição
        if 'position_type' in game_state:
            pos_type = game_state['position_type']
            if any(pos_type in elem for elem in profile.get('strategic_elements', [])):
                score += 0.4
            total_weights += 0.4

        # Fase do jogo
        if 'game_phase' in game_state:
            phase = game_state['game_phase']
            if any(phase in elem for elem in profile.get('strategic_elements', [])):
                score += 0.3
            total_weights += 0.3

        # Vantagem material
        if 'material_advantage' in game_state:
            adv = game_state['material_advantage']
            if (adv > 0 and 'aggressive' in profile.get('leadership_style', '').lower()) or \
               (adv < 0 and 'defensive' in profile.get('leadership_style', '').lower()):
                score += 0.3
            total_weights += 0.3

        return score / total_weights if total_weights > 0 else 0.0

    def extract_cultural_elements(self, profile_id: str) -> Dict[str, Any]:
        """
        Extrai elementos culturais relevantes de um perfil.
        """
        profile = self.get_profile(profile_id)
        if not profile:
            return {}

        return {
            'cultural_impact': profile.get('cultural_impact', ''),
            'era': profile.get('era', ''),
            'domain': profile.get('domain', ''),
            'achievements': profile.get('achievements', []),
            'narrative_elements': profile.get('narrative_elements', [])
        }

    def generate_strategic_advice(self, profile_id: str, game_state: Dict[str, Any]) -> str:
        """
        Gera conselhos estratégicos baseados em um perfil de liderança.
        """
        profile = self.get_profile(profile_id)
        if not profile:
            return ""

        # Analisa o estado do jogo e o perfil para gerar conselhos
        strategic_elements = profile.get('strategic_elements', [])
        leadership_style = profile.get('leadership_style', '')
        
        advice = [f"Seguindo o estilo de {profile['name']} ({leadership_style}):"]
        
        # Adiciona conselhos baseados nos elementos estratégicos
        for element in strategic_elements:
            if self._is_element_relevant(element, game_state):
                advice.append(f"- {self._format_strategic_advice(element, profile)}")

        return "\n".join(advice)

    def _is_element_relevant(self, element: str, game_state: Dict[str, Any]) -> bool:
        """Determina se um elemento estratégico é relevante para o estado atual do jogo."""
        # Implementar lógica de relevância
        return True  # Placeholder

    def _format_strategic_advice(self, element: str, profile: Dict[str, Any]) -> str:
        """Formata um elemento estratégico como conselho."""
        # Implementar formatação de conselho
        return f"Considere aplicar {element} como {profile['name']} faria"
