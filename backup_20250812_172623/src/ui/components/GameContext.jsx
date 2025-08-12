import { createContext, useContext, useReducer } from 'react'
import { apiService } from '../services/api'

const GameContext = createContext()

const initialState = {
  currentGame: null,
  gameHistory: [],
  isLoading: false,
  error: null,
  boardState: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', // Initial FEN
  selectedSquare: null,
  possibleMoves: [],
  gameMode: 'casual', // 'casual', 'ranked', 'training', 'cultural'
  aiDifficulty: 5
}

function gameReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false }
    case 'CREATE_GAME_SUCCESS':
      return {
        ...state,
        currentGame: action.payload,
        boardState: action.payload.board_state,
        isLoading: false,
        error: null
      }
    case 'UPDATE_GAME':
      return {
        ...state,
        currentGame: { ...state.currentGame, ...action.payload }
      }
    case 'UPDATE_BOARD_STATE':
      return {
        ...state,
        boardState: action.payload
      }
    case 'SET_SELECTED_SQUARE':
      return {
        ...state,
        selectedSquare: action.payload
      }
    case 'SET_POSSIBLE_MOVES':
      return {
        ...state,
        possibleMoves: action.payload
      }
    case 'SET_GAME_MODE':
      return {
        ...state,
        gameMode: action.payload
      }
    case 'SET_AI_DIFFICULTY':
      return {
        ...state,
        aiDifficulty: action.payload
      }
    case 'LOAD_GAME_HISTORY':
      return {
        ...state,
        gameHistory: action.payload,
        isLoading: false
      }
    case 'END_GAME':
      return {
        ...state,
        currentGame: null,
        boardState: initialState.boardState,
        selectedSquare: null,
        possibleMoves: []
      }
    default:
      return state
  }
}

export function GameProvider({ children }) {
  const [state, dispatch] = useReducer(gameReducer, initialState)

  const createGame = async (gameData, userId) => {
    dispatch({ type: 'SET_LOADING', payload: true })
    
    try {
      const response = await apiService.post('/games', {
        user_id: userId,
        opponent_type: gameData.opponentType || 'ai',
        game_mode: gameData.gameMode || state.gameMode,
        difficulty_level: gameData.difficulty || state.aiDifficulty,
        cultural_theme: gameData.culturalTheme,
        narrative_context: gameData.narrativeContext
      })
      
      const game = response.data.game
      dispatch({ type: 'CREATE_GAME_SUCCESS', payload: game })
      
      return game
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const makeMove = async (moveData) => {
    if (!state.currentGame) return

    dispatch({ type: 'SET_LOADING', payload: true })
    
    try {
      const response = await apiService.post(`/games/${state.currentGame.id}/move`, moveData)
      const updatedGame = response.data.game
      
      dispatch({ type: 'UPDATE_GAME', payload: updatedGame })
      dispatch({ type: 'UPDATE_BOARD_STATE', payload: updatedGame.board_state })
      dispatch({ type: 'SET_LOADING', payload: false })
      
      // Handle AI response if present
      if (response.data.ai_move) {
        return {
          game: updatedGame,
          aiMove: response.data.ai_move
        }
      }
      
      return { game: updatedGame }
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const loadGameHistory = async (userId) => {
    dispatch({ type: 'SET_LOADING', payload: true })
    
    try {
      const response = await apiService.get(`/games?user_id=${userId}`)
      const games = response.data.games
      
      dispatch({ type: 'LOAD_GAME_HISTORY', payload: games })
      
      return games
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const analyzeGame = async (gameId) => {
    dispatch({ type: 'SET_LOADING', payload: true })
    
    try {
      const response = await apiService.post(`/games/${gameId}/analysis`)
      const analysis = response.data.analysis
      
      dispatch({ type: 'SET_LOADING', payload: false })
      
      return analysis
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const selectSquare = (square) => {
    dispatch({ type: 'SET_SELECTED_SQUARE', payload: square })
  }

  const setPossibleMoves = (moves) => {
    dispatch({ type: 'SET_POSSIBLE_MOVES', payload: moves })
  }

  const setGameMode = (mode) => {
    dispatch({ type: 'SET_GAME_MODE', payload: mode })
  }

  const setAIDifficulty = (difficulty) => {
    dispatch({ type: 'SET_AI_DIFFICULTY', payload: difficulty })
  }

  const endGame = () => {
    dispatch({ type: 'END_GAME' })
  }

  const clearError = () => {
    dispatch({ type: 'SET_ERROR', payload: null })
  }

  // Chess utility functions
  const isValidMove = (from, to) => {
    // Basic validation - in a real implementation, this would use a chess library
    if (!from || !to) return false
    if (from === to) return false
    
    // Check if move is in possible moves
    return state.possibleMoves.some(move => 
      move.from === from && move.to === to
    )
  }

  const getPieceAt = (square) => {
    // This would parse the FEN string to get piece at square
    // For now, return a mock implementation
    const pieces = parseFEN(state.boardState)
    return pieces[square] || null
  }

  const calculatePossibleMoves = (square) => {
    // This would calculate all possible moves for a piece at the given square
    // For now, return mock moves
    const piece = getPieceAt(square)
    if (!piece) return []
    
    // Mock possible moves - in real implementation, use chess engine
    const mockMoves = [
      { from: square, to: 'e4', piece: piece.type },
      { from: square, to: 'e5', piece: piece.type }
    ]
    
    return mockMoves
  }

  const value = {
    ...state,
    createGame,
    makeMove,
    loadGameHistory,
    analyzeGame,
    selectSquare,
    setPossibleMoves,
    setGameMode,
    setAIDifficulty,
    endGame,
    clearError,
    isValidMove,
    getPieceAt,
    calculatePossibleMoves
  }

  return (
    <GameContext.Provider value={value}>
      {children}
    </GameContext.Provider>
  )
}

export function useGame() {
  const context = useContext(GameContext)
  if (!context) {
    throw new Error('useGame must be used within a GameProvider')
  }
  return context
}

// Utility function to parse FEN notation
function parseFEN(fen) {
  const pieces = {}
  const [board] = fen.split(' ')
  const ranks = board.split('/')
  
  const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  
  ranks.forEach((rank, rankIndex) => {
    let fileIndex = 0
    
    for (let char of rank) {
      if (isNaN(char)) {
        // It's a piece
        const square = files[fileIndex] + (8 - rankIndex)
        pieces[square] = {
          type: char.toLowerCase(),
          color: char === char.toUpperCase() ? 'white' : 'black'
        }
        fileIndex++
      } else {
        // It's a number, skip that many squares
        fileIndex += parseInt(char)
      }
    }
  })
  
  return pieces
}

