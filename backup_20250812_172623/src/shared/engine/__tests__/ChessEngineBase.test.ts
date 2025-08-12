import { ChessEngineBase } from '../ChessEngineBase';

describe('ChessEngineBase', () => {
  let engine: ChessEngineBase;

  beforeEach(() => {
    engine = new ChessEngineBase();
  });

  describe('FEN handling', () => {
    it('should accept valid FEN strings', () => {
      const validFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
      expect(() => engine.setFEN(validFEN)).not.toThrow();
      expect(engine.getFEN()).toBe(validFEN);
    });

    it('should reject invalid FEN strings', () => {
      const invalidFEN = 'invalid/fen/string';
      expect(() => engine.setFEN(invalidFEN)).toThrow('Invalid FEN string');
    });
  });

  describe('board state', () => {
    it('should return correct board representation', () => {
      const board = engine.getBoard();
      expect(board).toHaveLength(8);
      expect(board[0]).toHaveLength(8);
      
      // Check initial position pieces
      expect(board[0][4]).toEqual({
        type: 'k',
        color: 'black'
      });
      
      expect(board[7][4]).toEqual({
        type: 'k',
        color: 'white'
      });
    });
  });

  describe('move handling', () => {
    it('should make valid moves', () => {
      const result = engine.makeMove(
        { row: 6, col: 4 }, // e2
        { row: 4, col: 4 }  // e4
      );
      expect(result).toBe(true);
    });

    it('should reject invalid moves', () => {
      const result = engine.makeMove(
        { row: 6, col: 4 }, // e2
        { row: 2, col: 4 }  // e6 (too far)
      );
      expect(result).toBe(false);
    });
  });

  describe('game state', () => {
    it('should correctly identify check state', () => {
      // Position with check
      engine.setFEN('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 3');
      expect(engine.isCheck()).toBe(true);
    });

    it('should correctly identify checkmate state', () => {
      // Fool's mate position
      engine.setFEN('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3');
      expect(engine.isCheckmate()).toBe(true);
      expect(engine.isGameOver()).toBe(true);
    });
  });
});
