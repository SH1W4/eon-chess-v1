"""
Template for Creating New CHESS Cultures
=========================================
This template provides the base structure for implementing a new culture.
Copy this file and customize it for your specific culture.

Instructions:
1. Replace all [PLACEHOLDERS] with your culture-specific content
2. Implement all required methods
3. Add custom methods as needed
4. Test thoroughly before integration
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import random
from datetime import datetime

# Import the base framework
try:
    from cultural.culture_framework import ChessCulture, CulturalValues
except ImportError:
    # Fallback for different import paths
    from ..culture_framework import ChessCulture, CulturalValues


@dataclass
class [YourCultureName]Values(CulturalValues):
    """
    Cultural values specific to [Your Culture Name]
    
    Add custom values that are unique to your culture.
    All values should be floats between 0.0 and 1.0
    """
    # Example custom values (add your own)
    # mysticism: float = 0.0
    # technology: float = 0.0
    # nature_connection: float = 0.0
    pass  # Remove this when you add custom values


class [YourCultureName]Culture(ChessCulture):
    """
    [Your Culture Name] Implementation
    
    [Detailed description of your culture, its historical context,
    main characteristics, and what makes it unique in the CHESS universe]
    """
    
    def __init__(self):
        """Initialize the culture with its base properties"""
        super().__init__(
            name="[Your Culture Name]",
            description="[One-line description of the culture]",
            historical_period="[Time period or era, e.g., '500-1000 CE' or 'Far Future']",
            geographical_origin="[Location or conceptual origin]"
        )
        
        # Initialize cultural values
        self.values = [YourCultureName]Values(
            # Base values (adjust these to fit your culture)
            honor=0.5,        # How much honor matters
            tradition=0.5,    # Adherence to traditions
            innovation=0.5,   # Openness to new ideas
            spirituality=0.5, # Connection to spiritual/mystical
            aggression=0.5,   # Tendency toward conflict
            diplomacy=0.5,    # Preference for peaceful resolution
            wisdom=0.5,       # Value of knowledge and learning
            community=0.5,    # Collective vs individual focus
            
            # Add your custom values here
            # mysticism=0.8,
            # technology=0.2,
        )
        
        # Culture-specific attributes
        self.greeting_phrases = [
            "[Greeting 1 in your culture]",
            "[Greeting 2 in your culture]",
            "[Greeting 3 in your culture]"
        ]
        
        self.battle_cries = [
            "[Battle cry 1]",
            "[Battle cry 2]",
            "[Battle cry 3]"
        ]
        
        self.philosophical_quotes = [
            "[Philosophical quote 1]",
            "[Philosophical quote 2]",
            "[Philosophical quote 3]"
        ]
    
    def get_piece_metaphors(self) -> Dict[str, str]:
        """
        Return cultural metaphors for chess pieces
        
        Returns:
            Dictionary mapping piece types to cultural equivalents
        """
        return {
            'pawn': '[Your culture\'s equivalent of a pawn]',
            'rook': '[Your culture\'s equivalent of a rook]',
            'knight': '[Your culture\'s equivalent of a knight]',
            'bishop': '[Your culture\'s equivalent of a bishop]',
            'queen': '[Your culture\'s equivalent of a queen]',
            'king': '[Your culture\'s equivalent of a king]'
        }
    
    def get_piece_description(self, piece_type: str) -> str:
        """
        Get a detailed description of a piece in cultural context
        
        Args:
            piece_type: Type of chess piece
            
        Returns:
            Detailed cultural description
        """
        descriptions = {
            'pawn': "[Detailed description of pawn's role in your culture]",
            'rook': "[Detailed description of rook's role in your culture]",
            'knight': "[Detailed description of knight's role in your culture]",
            'bishop': "[Detailed description of bishop's role in your culture]",
            'queen': "[Detailed description of queen's role in your culture]",
            'king': "[Detailed description of king's role in your culture]"
        }
        return descriptions.get(piece_type, f"A {piece_type}")
    
    def get_move_narrative(self, move_type: str, piece: str, 
                          from_square: str = None, to_square: str = None,
                          captured_piece: str = None, **kwargs) -> str:
        """
        Generate narrative for a chess move
        
        Args:
            move_type: Type of move (advance, capture, check, checkmate, castle, etc.)
            piece: The piece making the move
            from_square: Starting position (optional)
            to_square: Ending position (optional)
            captured_piece: Piece being captured (optional)
            **kwargs: Additional context
            
        Returns:
            Narrative description of the move
        """
        narratives = {
            'advance': [
                f"[Narrative 1 for {piece} advancing]",
                f"[Narrative 2 for {piece} advancing]",
                f"[Narrative 3 for {piece} advancing]"
            ],
            'capture': [
                f"[Narrative 1 for {piece} capturing {captured_piece}]",
                f"[Narrative 2 for {piece} capturing {captured_piece}]",
                f"[Narrative 3 for {piece} capturing {captured_piece}]"
            ],
            'check': [
                "[Narrative 1 for check]",
                "[Narrative 2 for check]",
                "[Narrative 3 for check]"
            ],
            'checkmate': [
                "[Narrative 1 for checkmate - Victory!]",
                "[Narrative 2 for checkmate - Victory!]",
                "[Narrative 3 for checkmate - Victory!]"
            ],
            'castle': [
                "[Narrative 1 for castling]",
                "[Narrative 2 for castling]",
                "[Narrative 3 for castling]"
            ],
            'promotion': [
                f"[Narrative 1 for pawn promotion]",
                f"[Narrative 2 for pawn promotion]",
                f"[Narrative 3 for pawn promotion]"
            ],
            'en_passant': [
                "[Narrative 1 for en passant capture]",
                "[Narrative 2 for en passant capture]",
                "[Narrative 3 for en passant capture]"
            ],
            'draw': [
                "[Narrative 1 for draw]",
                "[Narrative 2 for draw]",
                "[Narrative 3 for draw]"
            ],
            'resign': [
                "[Narrative 1 for resignation]",
                "[Narrative 2 for resignation]",
                "[Narrative 3 for resignation]"
            ]
        }
        
        # Get appropriate narratives or use default
        move_narratives = narratives.get(move_type, [f"The {piece} moves"])
        return random.choice(move_narratives)
    
    def get_phase_description(self, phase: str, position_evaluation: float = 0.0) -> str:
        """
        Describe the current game phase in cultural context
        
        Args:
            phase: Game phase (opening, middlegame, endgame)
            position_evaluation: Current position evaluation (-1 to 1)
            
        Returns:
            Cultural description of the game phase
        """
        descriptions = {
            'opening': [
                "[Opening description 1 - Setting the stage]",
                "[Opening description 2 - Preparing forces]",
                "[Opening description 3 - Initial positioning]"
            ],
            'middlegame': [
                "[Middlegame description 1 - Battle intensifies]",
                "[Middlegame description 2 - Strategic maneuvering]",
                "[Middlegame description 3 - Complex positioning]"
            ],
            'endgame': [
                "[Endgame description 1 - Final confrontation]",
                "[Endgame description 2 - Decisive moments]",
                "[Endgame description 3 - Ultimate resolution]"
            ]
        }
        
        phase_descriptions = descriptions.get(phase, ["The game continues"])
        base_description = random.choice(phase_descriptions)
        
        # Add evaluation context
        if position_evaluation > 0.5:
            return f"{base_description} [Your culture's expression of advantage]"
        elif position_evaluation < -0.5:
            return f"{base_description} [Your culture's expression of disadvantage]"
        else:
            return f"{base_description} [Your culture's expression of balance]"
    
    def get_cultural_greeting(self) -> str:
        """
        Get a cultural greeting for the start of the game
        
        Returns:
            Cultural greeting message
        """
        return random.choice(self.greeting_phrases)
    
    def get_victory_message(self, victory_type: str = "checkmate") -> str:
        """
        Get a culturally appropriate victory message
        
        Args:
            victory_type: Type of victory (checkmate, resignation, time, etc.)
            
        Returns:
            Victory message
        """
        messages = {
            'checkmate': [
                "[Victory by checkmate message 1]",
                "[Victory by checkmate message 2]",
                "[Victory by checkmate message 3]"
            ],
            'resignation': [
                "[Victory by resignation message 1]",
                "[Victory by resignation message 2]",
                "[Victory by resignation message 3]"
            ],
            'time': [
                "[Victory by time message 1]",
                "[Victory by time message 2]",
                "[Victory by time message 3]"
            ]
        }
        
        victory_messages = messages.get(victory_type, messages['checkmate'])
        return random.choice(victory_messages)
    
    def get_defeat_message(self, defeat_type: str = "checkmate") -> str:
        """
        Get a culturally appropriate defeat message
        
        Args:
            defeat_type: Type of defeat (checkmate, resignation, time, etc.)
            
        Returns:
            Defeat message (should be honorable/gracious)
        """
        messages = {
            'checkmate': [
                "[Defeat by checkmate message 1 - Honorable]",
                "[Defeat by checkmate message 2 - Gracious]",
                "[Defeat by checkmate message 3 - Learning]"
            ],
            'resignation': [
                "[Defeat by resignation message 1]",
                "[Defeat by resignation message 2]",
                "[Defeat by resignation message 3]"
            ],
            'time': [
                "[Defeat by time message 1]",
                "[Defeat by time message 2]",
                "[Defeat by time message 3]"
            ]
        }
        
        defeat_messages = messages.get(defeat_type, messages['checkmate'])
        return random.choice(defeat_messages)
    
    def get_draw_message(self, draw_type: str = "agreement") -> str:
        """
        Get a culturally appropriate draw message
        
        Args:
            draw_type: Type of draw (stalemate, repetition, agreement, etc.)
            
        Returns:
            Draw message
        """
        messages = {
            'stalemate': "[Stalemate message in your culture]",
            'repetition': "[Repetition draw message in your culture]",
            'fifty_move': "[Fifty-move rule message in your culture]",
            'agreement': "[Mutual draw agreement message in your culture]",
            'insufficient': "[Insufficient material message in your culture]"
        }
        
        return messages.get(draw_type, "[General draw message in your culture]")
    
    def get_taunt(self, intensity: int = 1) -> str:
        """
        Get a cultural taunt or challenge (optional, for personality)
        
        Args:
            intensity: 1-3, how intense the taunt should be
            
        Returns:
            Taunt message (should be respectful even if challenging)
        """
        taunts = {
            1: [  # Mild
                "[Mild taunt 1]",
                "[Mild taunt 2]",
                "[Mild taunt 3]"
            ],
            2: [  # Medium
                "[Medium taunt 1]",
                "[Medium taunt 2]",
                "[Medium taunt 3]"
            ],
            3: [  # Intense (but still respectful)
                "[Intense taunt 1]",
                "[Intense taunt 2]",
                "[Intense taunt 3]"
            ]
        }
        
        intensity = max(1, min(3, intensity))
        return random.choice(taunts[intensity])
    
    def get_encouragement(self) -> str:
        """
        Get an encouraging message (for opponent or self)
        
        Returns:
            Encouragement message
        """
        encouragements = [
            "[Encouragement 1]",
            "[Encouragement 2]",
            "[Encouragement 3]",
            "[Encouragement 4]",
            "[Encouragement 5]"
        ]
        return random.choice(encouragements)
    
    def get_philosophical_quote(self) -> str:
        """
        Get a philosophical quote from the culture
        
        Returns:
            Philosophical quote or wisdom
        """
        return random.choice(self.philosophical_quotes)
    
    def get_time_pressure_message(self, time_remaining: int) -> str:
        """
        Get a message related to time pressure
        
        Args:
            time_remaining: Seconds remaining on clock
            
        Returns:
            Time pressure message
        """
        if time_remaining < 30:
            return "[Critical time pressure message]"
        elif time_remaining < 60:
            return "[High time pressure message]"
        elif time_remaining < 180:
            return "[Moderate time pressure message]"
        else:
            return "[Comfortable time message]"
    
    def get_special_move_description(self, move_type: str) -> str:
        """
        Get special descriptions for unique moves
        
        Args:
            move_type: Type of special move
            
        Returns:
            Special move description
        """
        special_moves = {
            'brilliant': "[Description of a brilliant move]",
            'blunder': "[Description of a blunder]",
            'sacrifice': "[Description of a sacrifice]",
            'fork': "[Description of a fork attack]",
            'pin': "[Description of a pin]",
            'skewer': "[Description of a skewer]",
            'discovered_attack': "[Description of discovered attack]",
            'double_attack': "[Description of double attack]",
            'zugzwang': "[Description of zugzwang position]",
            'stalemate_trap': "[Description of stalemate trap]"
        }
        
        return special_moves.get(move_type, f"A special {move_type} maneuver")
    
    def get_commentary(self, game_state: Dict) -> str:
        """
        Provide cultural commentary on the current game state
        
        Args:
            game_state: Dictionary containing game information
            
        Returns:
            Commentary message
        """
        # Example implementation - customize based on your culture
        move_number = game_state.get('move_number', 0)
        
        if move_number < 10:
            return "[Early game commentary]"
        elif move_number < 30:
            return "[Mid game commentary]"
        else:
            return "[Late game commentary]"
    
    def get_ai_personality_traits(self) -> Dict[str, float]:
        """
        Get AI personality traits for this culture
        
        Returns:
            Dictionary of personality traits (0.0 to 1.0)
        """
        return {
            'aggression': self.values.aggression,
            'defense': 1.0 - self.values.aggression,
            'tactical': 0.5,  # Customize based on culture
            'positional': 0.5,  # Customize based on culture
            'risk_taking': 0.5,  # Customize based on culture
            'time_management': 0.5,  # Customize based on culture
            'opening_knowledge': 0.5,  # Customize based on culture
            'endgame_skill': 0.5,  # Customize based on culture
            'psychological': 0.5  # Customize based on culture
        }
    
    def get_color_scheme(self) -> Dict[str, str]:
        """
        Get the color scheme for this culture's UI
        
        Returns:
            Dictionary of color definitions
        """
        return {
            'primary': '#[HEX_COLOR]',
            'secondary': '#[HEX_COLOR]',
            'accent': '#[HEX_COLOR]',
            'background': '#[HEX_COLOR]',
            'text': '#[HEX_COLOR]',
            'board_light': '#[HEX_COLOR]',
            'board_dark': '#[HEX_COLOR]',
            'highlight': '#[HEX_COLOR]',
            'danger': '#[HEX_COLOR]',
            'success': '#[HEX_COLOR]'
        }
    
    def get_audio_themes(self) -> Dict[str, str]:
        """
        Get audio theme preferences for this culture
        
        Returns:
            Dictionary of audio file paths or identifiers
        """
        return {
            'background_music': '[path/to/background/music]',
            'move_sound': '[path/to/move/sound]',
            'capture_sound': '[path/to/capture/sound]',
            'check_sound': '[path/to/check/sound]',
            'victory_sound': '[path/to/victory/sound]',
            'defeat_sound': '[path/to/defeat/sound]',
            'draw_sound': '[path/to/draw/sound]'
        }
    
    def __str__(self) -> str:
        """String representation of the culture"""
        return f"{self.name} Culture - {self.description}"
    
    def __repr__(self) -> str:
        """Developer representation of the culture"""
        return f"<{self.__class__.__name__}(name='{self.name}', period='{self.historical_period}')>"


# Example usage and testing
if __name__ == "__main__":
    # Create an instance of your culture
    culture = [YourCultureName]Culture()
    
    # Test basic information
    print(f"Culture: {culture.name}")
    print(f"Description: {culture.description}")
    print(f"Period: {culture.historical_period}")
    print(f"Origin: {culture.geographical_origin}")
    
    # Test piece metaphors
    print("\nPiece Metaphors:")
    for piece, metaphor in culture.get_piece_metaphors().items():
        print(f"  {piece}: {metaphor}")
    
    # Test narratives
    print("\nSample Narratives:")
    print(f"  Greeting: {culture.get_cultural_greeting()}")
    print(f"  Advance: {culture.get_move_narrative('advance', 'Warrior')}")
    print(f"  Capture: {culture.get_move_narrative('capture', 'Warrior', captured_piece='Enemy')}")
    print(f"  Victory: {culture.get_victory_message()}")
    print(f"  Philosophy: {culture.get_philosophical_quote()}")
    
    # Test AI personality
    print("\nAI Personality Traits:")
    for trait, value in culture.get_ai_personality_traits().items():
        print(f"  {trait}: {value:.2f}")
    
    print("\n✅ Culture template is ready for customization!")
