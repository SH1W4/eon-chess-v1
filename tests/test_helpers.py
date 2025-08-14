"""
Helper functions and utilities for tests.
"""

import asyncio
from typing import Any, Callable, Coroutine
from functools import wraps


def async_wrapper(func: Callable) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    Wrapper to convert synchronous functions to async.
    
    This is useful for tests that need to await methods that are not async.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # If the result is a coroutine, await it
        result = func(*args, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result
    return wrapper


class AsyncBoardAdapter:
    """
    Adapter to make synchronous Board methods compatible with async tests.
    """
    
    def __init__(self, board):
        self.board = board
        
    async def move_piece(self, from_pos: str, to_pos: str) -> dict:
        """Async wrapper for move_piece."""
        result = self.board.move_piece(from_pos, to_pos)
        if asyncio.iscoroutine(result):
            return await result
        return result
    
    async def make_move(self, move) -> bool:
        """Async wrapper for make_move."""
        if hasattr(self.board, 'make_move'):
            result = self.board.make_move(move)
            if asyncio.iscoroutine(result):
                return await result
            return result
        else:
            # Fallback to move_piece
            result = self.board.move_piece(move.from_square, move.to_square)
            if asyncio.iscoroutine(result):
                result = await result
            return result.get('success', False)
            
    def __getattr__(self, name):
        """Proxy other attributes to the wrapped board."""
        return getattr(self.board, name)
