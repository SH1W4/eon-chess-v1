import { renderHook, act } from '@testing-library/react';
import { useChessStore } from '../chess-store';

describe('Chess Store', () => {
  beforeEach(() => {
    // Reset store before each test
    act(() => {
      useChessStore.getState().resetGame();
    });
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => useChessStore());

    expect(result.current.game.fen()).toBe('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
    expect(result.current.evaluation).toBe(0);
    expect(result.current.history).toEqual([]);
    expect(result.current.aiLevel).toBe('club');
    expect(result.current.culturalContext).toBe('classical');
  });

  it('should make a move and update state', () => {
    const { result } = renderHook(() => useChessStore());

    act(() => {
      result.current.makeMove({ from: 'e2', to: 'e4', piece: 'p' });
    });

    expect(result.current.game.fen()).toBe('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1');
    expect(result.current.history).toHaveLength(1);
    expect(result.current.history[0]).toEqual({ from: 'e2', to: 'e4', piece: 'p' });
  });

  it('should set AI intelligence level', () => {
    const { result } = renderHook(() => useChessStore());

    act(() => {
      result.current.setAIIntelligence('master');
    });

    expect(result.current.aiLevel).toBe('master');
  });

  it('should reset game to initial state', () => {
    const { result } = renderHook(() => useChessStore());

    // Make a move first
    act(() => {
      result.current.makeMove({ from: 'e2', to: 'e4', piece: 'p' });
    });

    // Reset game
    act(() => {
      result.current.resetGame();
    });

    expect(result.current.game.fen()).toBe('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');
    expect(result.current.history).toEqual([]);
    expect(result.current.evaluation).toBe(0);
  });

  it('should handle multiple moves correctly', () => {
    const { result } = renderHook(() => useChessStore());

    act(() => {
      result.current.makeMove({ from: 'e2', to: 'e4', piece: 'p' });
      result.current.makeMove({ from: 'e7', to: 'e5', piece: 'p' });
      result.current.makeMove({ from: 'g1', to: 'f3', piece: 'n' });
    });

    expect(result.current.history).toHaveLength(3);
    expect(result.current.game.fen()).toBe('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2');
  });
});
