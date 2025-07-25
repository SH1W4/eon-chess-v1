from typing import Dict, List, Optional
from dataclasses import dataclass
from ..core.engine import Move

@dataclass
class DramaticMoment:
    description: str
    importance: float
    cultural_impact: Dict[str, float]
    triggered_by: str

class CulturalNarrative:
    """Sistema de narrativas culturais para xadrez"""
    
    def __init__(self, culture_type: str):
        self.culture = culture_type
        self.dramatic_moments: List[DramaticMoment] = []
        self.story_arc: List[str] = []
        self.move_count = 0
        
        # Frases culturais específicas
        self.medieval_phrases = {
            'piece_capture': [
                "Em um embate glorioso, {attacker} conquista {defender}!",
                "Com bravura, {attacker} derrota {defender} em combate!",
                "Uma vitória honrosa de {attacker} sobre {defender}!"
            ],
            'check': [
                "O Rei encontra-se sob ameaça! A honra do reino está em jogo!",
                "Uma ameaça direta à coroa! Os defensores devem agir!",
                "O trono está em perigo! Que a nobreza proteja seu Rei!"
            ],
            'castling': [
                "O Rei busca refúgio em sua fortaleza!",
                "As muralhas do castelo oferecem proteção ao monarca!",
                "Uma manobra estratégica para proteger a realeza!"
            ],
            'development': [
                "{piece} assume sua posição de batalha!",
                "Com honra, {piece} marcha para o combate!",
                "{piece} prepara-se para defender o reino!"
            ],
            'sacrifice': [
                "Um sacrifício nobre pela glória do reino!",
                "Honra e coragem manifestam-se neste sacrifício!",
                "Uma oferenda heroica pelo bem maior!"
            ],
            'opening': [
                "As forças se alinham para a grande batalha!",
                "Os exércitos tomam suas posições iniciais!",
                "O campo de batalha testemunhará grandes feitos!"
            ],
            'middlegame': [
                "A batalha atinge seu momento mais intenso!",
                "Os exércitos se enfrentam com toda força!",
                "O fragor da batalha ecoa pelo reino!"
            ],
            'endgame': [
                "O destino do reino será decidido!",
                "A batalha se aproxima de seu momento decisivo!",
                "Apenas os mais valorosos prevalecerão!"
            ]
        }
        
        self.futuristic_phrases = {
            'piece_capture': [
                "Unidade {defender} neutralizada por {attacker}. Eficiência: 100%",
                "Protocolo de eliminação executado: {attacker} remove {defender}",
                "Objetivo alcançado: {attacker} desativa {defender}"
            ],
            'check': [
                "Alerta crítico: núcleo central sob ameaça direta",
                "Violação de segurança detectada. Contramedidas necessárias",
                "Prioridade máxima: proteger unidade central de comando"
            ],
            'castling': [
                "Protocolo de realocação defensiva ativado",
                "Executando manobra de segurança prioritária",
                "Reconfiguração estrutural para máxima proteção"
            ],
            'development': [
                "Unidade {piece} assumindo posição otimizada",
                "Configurando {piece} para eficiência máxima",
                "Implantando {piece} em coordenadas estratégicas"
            ],
            'sacrifice': [
                "Executando troca calculada de recursos",
                "Sacrifício tático: benefício projetado superior a 87%",
                "Otimização via eliminação controlada de unidade"
            ],
            'opening': [
                "Iniciando sequência de implantação tática",
                "Configuração inicial de unidades em andamento",
                "Estabelecendo padrão estratégico primário"
            ],
            'middlegame': [
                "Fase crítica de operações atingida",
                "Máxima densidade de interações detectada",
                "Executando protocolos táticos avançados"
            ],
            'endgame': [
                "Iniciando protocolo de resolução final",
                "Otimizando recursos para conclusão eficiente",
                "Fase terminal: maximizando probabilidade de sucesso"
            ]
        }
    
    def _get_phrases(self, category: str) -> List[str]:
        """Retorna frases apropriadas para a cultura atual"""
        phrases = self.medieval_phrases if self.culture == 'medieval' else self.futuristic_phrases
        return phrases.get(category, [])
    
    def _format_piece_name(self, piece_type: str) -> str:
        """Formata nome da peça de acordo com a cultura"""
        if self.culture == 'medieval':
            names = {
                'pawn': 'Peão',
                'knight': 'Cavaleiro',
                'bishop': 'Bispo',
                'rook': 'Torre',
                'queen': 'Rainha',
                'king': 'Rei'
            }
        else:
            names = {
                'pawn': 'Drone',
                'knight': 'Mecha',
                'bishop': 'Hacker',
                'rook': 'Fortaleza',
                'queen': 'IA Suprema',
                'king': 'Comandante'
            }
        return names.get(piece_type, piece_type)
    
    def generate_move_narrative(self, move: Move, context: Dict) -> str:
        """Gera narrativa para um movimento específico"""
        self.move_count += 1
        
        # Verifica se é um movimento de abertura conhecido
        if context.get('type') != 'unknown':
            opening_name = context['type']
            progress = context.get('progress', 0)
            if progress <= 0.3:
                return f"Seguindo a {opening_name}: {context.get('description', '')}"
            elif progress <= 0.7:
                recommendations = context.get('recommendations', [])
                if recommendations:
                    return f"Desenvolvendo a {opening_name}. {recommendations[0]}"
        
        # Captura
        if move.captured_piece:
            phrases = self._get_phrases('piece_capture')
            return phrases[self.move_count % len(phrases)].format(
                attacker=self._format_piece_name(move.piece.type),
                defender=self._format_piece_name(move.captured_piece.type)
            )
        
        # Roque
        if move.is_castling:
            phrases = self._get_phrases('castling')
            return phrases[self.move_count % len(phrases)]
        
        # Desenvolvimento de peça
        if not move.piece.has_moved and move.piece.type in ['knight', 'bishop']:
            phrases = self._get_phrases('development')
            return phrases[self.move_count % len(phrases)].format(
                piece=self._format_piece_name(move.piece.type)
            )
        
        # Cheque
        if move.is_check:
            phrases = self._get_phrases('check')
            return phrases[self.move_count % len(phrases)]
        
        # Fase do jogo
        phase = context.get('phase', 'middlegame')
        if self.move_count % 10 == 0:  # Periodicamente comenta sobre a fase
            phrases = self._get_phrases(phase)
            if phrases:
                return phrases[self.move_count % len(phrases)]
        
        # Movimento padrão
        piece_name = self._format_piece_name(move.piece.type)
        if self.culture == 'medieval':
            return f"{piece_name} move-se estrategicamente"
        else:
            return f"Reposicionando unidade {piece_name}"
    
    def generate_dramatic_moment(self, position_eval: float, phase: str,
                               material_balance: float) -> Optional[str]:
        """Gera um momento dramático baseado na situação"""
        moment = None
        
        # Vantagem significativa
        if abs(position_eval) > 3.0:
            if self.culture == 'medieval':
                moment = ("As forças se desequilibram! " +
                         ("O reino prevalece!" if position_eval > 0 else 
                          "O reino enfrenta adversidade!"))
            else:
                moment = ("Análise: Desequilíbrio detectado. " +
                         ("Vantagem: +{:.1f}%".format(position_eval * 10) if position_eval > 0 else
                          "Desvantagem: {:.1f}%".format(position_eval * 10)))
        
        # Fase crítica
        elif phase == 'middlegame' and self.move_count == 15:
            if self.culture == 'medieval':
                moment = "A batalha atinge seu momento mais intenso!"
            else:
                moment = "Fase crítica: Iniciando protocolos táticos avançados"
        
        # Tensão material
        elif abs(material_balance) >= 3:
            if self.culture == 'medieval':
                moment = ("As forças se mostram desiguais no campo de batalha" +
                         (" a nosso favor!" if material_balance > 0 else "!"))
            else:
                moment = ("Balanço de recursos alterado: " +
                         ("+{:.1f} unidades".format(material_balance) if material_balance > 0 else
                          "{:.1f} unidades".format(material_balance)))
        
        if moment:
            dramatic_moment = DramaticMoment(
                description=moment,
                importance=abs(position_eval) + abs(material_balance),
                cultural_impact={
                    "tension": min(1.0, abs(position_eval) / 5),
                    "drama": min(1.0, abs(material_balance) / 5)
                },
                triggered_by=f"eval={position_eval:.2f},mat={material_balance:.2f}"
            )
            self.dramatic_moments.append(dramatic_moment)
            self.story_arc.append(moment)
        
        return moment
    
    def get_game_summary(self) -> str:
        """Gera um resumo narrativo do jogo"""
        if self.culture == 'medieval':
            summary = ["A batalha foi travada com bravura e honra."]
            
            if self.dramatic_moments:
                summary.append("\nMomentos decisivos:")
                top_moments = sorted(
                    self.dramatic_moments,
                    key=lambda x: x.importance,
                    reverse=True
                )[:3]
                for moment in top_moments:
                    summary.append(f"- {moment.description}")
            
            if self.move_count > 0:
                summary.append(f"\nAo todo, {self.move_count} movimentos definiram este embate.")
            
            tension = sum(m.cultural_impact.get("tension", 0)
                        for m in self.dramatic_moments) / max(1, len(self.dramatic_moments))
            if tension > 0.7:
                summary.append("Foi uma batalha memorável, digna das canções dos bardos!")
            elif tension > 0.4:
                summary.append("Os guerreiros lutaram com honra e determinação.")
            else:
                summary.append("A estratégia prevaleceu sobre a força bruta.")
        
        else:
            summary = ["Análise final da simulação tática:"]
            
            if self.dramatic_moments:
                summary.append("\nEventos críticos registrados:")
                top_moments = sorted(
                    self.dramatic_moments,
                    key=lambda x: x.importance,
                    reverse=True
                )[:3]
                for i, moment in enumerate(top_moments, 1):
                    summary.append(f"[{i}] {moment.description}")
            
            if self.move_count > 0:
                summary.append(f"\nTotal de ciclos executados: {self.move_count}")
            
            efficiency = sum(m.cultural_impact.get("tension", 0)
                           for m in self.dramatic_moments) / max(1, len(self.dramatic_moments))
            if efficiency > 0.7:
                summary.append("Performance otimizada: Objetivos alcançados com máxima eficiência.")
            elif efficiency > 0.4:
                summary.append("Eficiência operacional dentro dos parâmetros esperados.")
            else:
                summary.append("Resultados sub-ótimos detectados. Recalibragem recomendada.")
        
        return "\n".join(summary)
