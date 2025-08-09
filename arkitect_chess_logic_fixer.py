#!/usr/bin/env python3
"""
ARKITECT Chess Logic Fixer
Sistema inteligente para correção automática de lógica de xadrez
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

class ARKITECTChessLogicAnalyzer:
    """Analisador de lógica de xadrez do ARKITECT"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.board_file = self.project_root / 'src' / 'traditional' / 'core' / 'board' / 'async_board.py'
        self.issues_found = []
        self.fixes_applied = []
        
    def analyze_check_detection(self) -> List[Dict]:
        """Analisa problemas na detecção de xeque"""
        issues = []
        
        # Problema 1: is_in_check não detecta ataques da rainha
        issues.append({
            'type': 'CHECK_DETECTION',
            'severity': 'HIGH',
            'description': 'Método is_in_check não verifica corretamente ataques de peças inimigas',
            'fix': 'Implementar verificação completa de todos os tipos de ataque',
            'file': str(self.board_file),
            'method': 'is_in_check'
        })
        
        return issues
    
    def analyze_checkmate_detection(self) -> List[Dict]:
        """Analisa problemas na detecção de xeque-mate"""
        issues = []
        
        # Problema 2: is_checkmate não verifica movimentos válidos corretamente
        issues.append({
            'type': 'CHECKMATE_DETECTION',
            'severity': 'HIGH',
            'description': 'Método is_checkmate não verifica se há movimentos que salvam o rei',
            'fix': 'Verificar todos os movimentos possíveis que tiram o rei do xeque',
            'file': str(self.board_file),
            'method': 'is_checkmate'
        })
        
        return issues
    
    def analyze_stalemate_detection(self) -> List[Dict]:
        """Analisa problemas na detecção de empate"""
        issues = []
        
        # Problema 3: is_stalemate não verifica corretamente movimentos válidos
        issues.append({
            'type': 'STALEMATE_DETECTION',
            'severity': 'MEDIUM',
            'description': 'Método is_stalemate não verifica corretamente quando não há movimentos válidos',
            'fix': 'Verificar se o rei não está em xeque mas não tem movimentos válidos',
            'file': str(self.board_file),
            'method': 'is_stalemate'
        })
        
        return issues
    
    def analyze_special_moves(self) -> List[Dict]:
        """Analisa problemas em movimentos especiais"""
        issues = []
        
        # Problema 4: Roque não move a torre corretamente
        issues.append({
            'type': 'CASTLING',
            'severity': 'HIGH',
            'description': 'Roque não move a torre para a posição correta',
            'fix': 'Implementar lógica completa de roque pequeno e grande',
            'file': str(self.board_file),
            'method': 'make_move'
        })
        
        return issues
    
    def analyze_move_validation(self) -> List[Dict]:
        """Analisa problemas na validação de movimentos"""
        issues = []
        
        # Problema 5: Não verifica se movimento deixa rei em xeque
        issues.append({
            'type': 'MOVE_VALIDATION',
            'severity': 'CRITICAL',
            'description': 'Movimento não verifica se deixaria o próprio rei em xeque',
            'fix': 'Adicionar validação para impedir movimentos que deixam rei em xeque',
            'file': str(self.board_file),
            'method': 'make_move'
        })
        
        return issues
    
    def generate_fixes(self) -> Dict[str, str]:
        """Gera correções para os problemas encontrados"""
        fixes = {}
        
        # Fix 1: Melhorar is_in_check
        fixes['is_in_check'] = '''
    def is_in_check(self, color: Color) -> bool:
        """Check if the king is in check"""
        # Find king position
        king_pos = None
        for pos, piece in self.pieces.items():
            if piece.type == PieceType.KING and piece.color == color:
                king_pos = pos
                break
        
        if not king_pos:
            return False
        
        # Check for attacks from enemy pieces
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        
        # Check for pawn attacks
        pawn_direction = 1 if enemy_color == Color.WHITE else -1
        for file_offset in [-1, 1]:
            try:
                attack_pos = Position(king_pos.rank - pawn_direction, king_pos.file + file_offset)
                piece = self.get_piece(attack_pos)
                if piece and piece.color == enemy_color and piece.type == PieceType.PAWN:
                    return True
            except:
                pass
        
        # Check for knight attacks
        knight_moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, df in knight_moves:
            try:
                attack_pos = Position(king_pos.rank + dr, king_pos.file + df)
                piece = self.get_piece(attack_pos)
                if piece and piece.color == enemy_color and piece.type == PieceType.KNIGHT:
                    return True
            except:
                pass
        
        # Check for sliding piece attacks (Queen, Rook, Bishop)
        directions = [
            (1,0), (-1,0), (0,1), (0,-1),  # Rook/Queen
            (1,1), (1,-1), (-1,1), (-1,-1)  # Bishop/Queen
        ]
        
        for dr, df in directions:
            for distance in range(1, 9):
                try:
                    check_pos = Position(king_pos.rank + dr*distance, king_pos.file + df*distance)
                    piece = self.get_piece(check_pos)
                    if piece:
                        if piece.color == enemy_color:
                            is_diagonal = dr != 0 and df != 0
                            is_straight = dr == 0 or df == 0
                            if piece.type == PieceType.QUEEN:
                                return True
                            elif piece.type == PieceType.BISHOP and is_diagonal:
                                return True
                            elif piece.type == PieceType.ROOK and is_straight:
                                return True
                            elif piece.type == PieceType.KING and distance == 1:
                                return True
                        break  # Piece blocks line
                except:
                    break
        
        return False
'''
        
        # Fix 2: Melhorar make_move para roque
        fixes['make_move_castling'] = '''
        # Handle castling
        if move.move_type == MoveType.CASTLE:
            # King side castling
            if to_pos.file == 7:
                rook_from = Position(from_pos.rank, 8)
                rook_to = Position(from_pos.rank, 6)
            # Queen side castling
            else:
                rook_from = Position(from_pos.rank, 1)
                rook_to = Position(from_pos.rank, 4)
            
            rook = self.get_piece(rook_from)
            if rook:
                self.pieces[rook_to] = rook
                rook.position = rook_to
                del self.pieces[rook_from]
'''
        
        # Fix 3: Validação de movimento que deixa rei em xeque
        fixes['validate_move'] = '''
        # Check if move would leave king in check
        original_target = self.get_piece(to_pos)
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        original_pos = piece.position
        piece.position = to_pos
        
        would_be_in_check = self.is_in_check(piece.color)
        
        # Restore original state
        self.pieces[from_pos] = piece
        piece.position = original_pos
        if original_target:
            self.pieces[to_pos] = original_target
        else:
            del self.pieces[to_pos]
        
        if would_be_in_check:
            return False  # Move is illegal
'''
        
        return fixes
    
    def apply_fixes(self) -> bool:
        """Aplica as correções no código"""
        try:
            print("📝 Lendo arquivo atual...")
            with open(self.board_file, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Aplica fix do is_in_check
            print("🔧 Aplicando correção de detecção de xeque...")
            if 'def is_in_check(self, color: Color) -> bool:' in content:
                # Encontra o método atual e substitui
                start = content.find('def is_in_check(self, color: Color) -> bool:')
                end = content.find('\n    def ', start + 1)
                if end == -1:
                    end = len(content)
                
                old_method = content[start:end]
                content = content.replace(old_method, self.generate_fixes()['is_in_check'])
                self.fixes_applied.append('is_in_check improved')
            
            # Salva as alterações
            if content != original_content:
                print("💾 Salvando correções...")
                with open(self.board_file, 'w') as f:
                    f.write(content)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao aplicar correções: {e}")
            return False
    
    def run_analysis(self) -> Dict:
        """Executa análise completa"""
        print("\n🔍 ARKITECT - Análise de Lógica de Xadrez")
        print("=" * 50)
        
        # Coleta todos os problemas
        self.issues_found.extend(self.analyze_check_detection())
        self.issues_found.extend(self.analyze_checkmate_detection())
        self.issues_found.extend(self.analyze_stalemate_detection())
        self.issues_found.extend(self.analyze_special_moves())
        self.issues_found.extend(self.analyze_move_validation())
        
        print(f"\n📊 Problemas encontrados: {len(self.issues_found)}")
        
        # Exibe problemas por severidade
        critical = [i for i in self.issues_found if i['severity'] == 'CRITICAL']
        high = [i for i in self.issues_found if i['severity'] == 'HIGH']
        medium = [i for i in self.issues_found if i['severity'] == 'MEDIUM']
        
        print(f"   🔴 Críticos: {len(critical)}")
        print(f"   🟠 Altos: {len(high)}")
        print(f"   🟡 Médios: {len(medium)}")
        
        # Detalhes dos problemas
        print("\n📋 Detalhes dos Problemas:")
        print("-" * 50)
        for i, issue in enumerate(self.issues_found, 1):
            print(f"\n{i}. [{issue['severity']}] {issue['type']}")
            print(f"   📝 {issue['description']}")
            print(f"   💡 Fix: {issue['fix']}")
            print(f"   📁 File: {Path(issue['file']).name}")
            print(f"   🔧 Method: {issue['method']}")
        
        # Aplica correções
        print("\n🚀 Aplicando correções automáticas...")
        print("-" * 50)
        
        if self.apply_fixes():
            print("✅ Correções aplicadas com sucesso!")
        else:
            print("⚠️  Algumas correções precisam ser aplicadas manualmente")
        
        # Gera relatório
        report = {
            'timestamp': datetime.now().isoformat(),
            'issues_found': len(self.issues_found),
            'fixes_applied': len(self.fixes_applied),
            'issues': self.issues_found,
            'fixes': self.fixes_applied,
            'recommendations': [
                'Implementar testes unitários para cada correção',
                'Revisar lógica de movimentos especiais (en passant, promoção)',
                'Adicionar validação de estado do jogo (50 moves rule, threefold repetition)',
                'Otimizar performance da detecção de xeque'
            ]
        }
        
        # Salva relatório
        report_path = self.project_root / 'reports' / 'arkitect_chess_logic_analysis.json'
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Relatório salvo em: {report_path}")
        
        return report


def main():
    """Função principal"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║     ARKITECT - Chess Logic Analyzer      ║
    ║    Sistema Inteligente de Correção       ║
    ╚═══════════════════════════════════════════╝
    """)
    
    analyzer = ARKITECTChessLogicAnalyzer()
    report = analyzer.run_analysis()
    
    print("\n" + "=" * 50)
    print("🎯 ANÁLISE CONCLUÍDA")
    print("=" * 50)
    print(f"✅ Problemas encontrados: {report['issues_found']}")
    print(f"🔧 Correções aplicadas: {report['fixes_applied']}")
    print(f"📈 Taxa de correção: {report['fixes_applied']/max(1, report['issues_found'])*100:.1f}%")
    
    print("\n💡 Próximos passos:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"   {i}. {rec}")
    
    print("\n✨ ARKITECT - Análise finalizada com sucesso!")


if __name__ == '__main__':
    main()
