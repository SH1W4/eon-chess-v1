import random
from core.board.board import Board, Position, PieceType, Color, Piece

class NarrativeEngine:
    def __init__(self):
        # Nomes das peças para cada cultura
        self.piece_names_white = {
            PieceType.KING: "Basileus",      # Imperador bizantino
            PieceType.QUEEN: "Augusta",      # Imperatriz bizantina
            PieceType.ROOK: "Torre Imperial",
            PieceType.BISHOP: "Patriarca",    # Líder religioso bizantino
            PieceType.KNIGHT: "Catafracta",   # Cavalaria pesada bizantina
            PieceType.PAWN: "Soldado Romano"  # Soldado do exército bizantino
        }
        
        self.piece_names_black = {
            PieceType.KING: "Jarl",        # Líder viking
            PieceType.QUEEN: "Valquíria",   # Guerreira mítica nórdica
            PieceType.ROOK: "Drakkar",     # Navio viking
            PieceType.BISHOP: "Godi",       # Sacerdote nórdico
            PieceType.KNIGHT: "Berserker",  # Guerreiro viking furioso
            PieceType.PAWN: "Viking"       # Guerreiro nórdico
        }
        
    def generate_move_narrative(self, from_pos: str, to_pos: str, piece: Piece, cultural_impact: dict) -> str:
        if not piece:
            return "Movimento realizado."
            
        # Seleciona o nome da peça baseado em sua cor
        piece_names = self.piece_names_white if piece.color == Color.WHITE else self.piece_names_black
        piece_name = piece_names.get(piece.type, "Peça")
        
        if not cultural_impact or not cultural_impact.get("narrative_pool"):
            coord_from = f"{from_pos[0].upper()}{from_pos[1]}"
            coord_to = f"{to_pos[0].upper()}{to_pos[1]}"
            return f"O {piece_name} move de {coord_from} para {coord_to} com determinação imperial"
            
        narratives = cultural_impact.get("narrative_pool", [])
        if not narratives:
            return f"O {piece_name} realiza uma manobra estratégica digna do Império"
            
        narrative_template = random.choice(narratives)
        return narrative_template.format(piece=piece_name)
