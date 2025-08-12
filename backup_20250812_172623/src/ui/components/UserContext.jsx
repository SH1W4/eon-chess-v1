import { createContext, useContext, useReducer, useEffect } from 'react'
import { apiService } from '../services/api'

const UserContext = createContext()

const initialState = {
  user: null,
  aiProfile: null,
  isAuthenticated: false,
  isLoading: false,
  error: null
}

function userReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload }
    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false }
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        aiProfile: action.payload.aiProfile,
        isAuthenticated: true,
        isLoading: false,
        error: null
      }
    case 'LOGOUT':
      return {
        ...initialState
      }
    case 'UPDATE_USER':
      return {
        ...state,
        user: { ...state.user, ...action.payload }
      }
    case 'UPDATE_AI_PROFILE':
      return {
        ...state,
        aiProfile: { ...state.aiProfile, ...action.payload }
      }
    default:
      return state
  }
}

export function UserProvider({ children }) {
  const [state, dispatch] = useReducer(userReducer, initialState)

  useEffect(() => {
    // Check for existing session on app load
    const savedUser = localStorage.getItem('xadrezmaster_user')
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser)
        loginUser(userData.id)
      } catch (error) {
        console.error('Error loading saved user:', error)
        localStorage.removeItem('xadrezmaster_user')
      }
    }
  }, [])

  const loginUser = async (userId) => {
    dispatch({ type: 'SET_LOADING', payload: true })
    
    try {
      // Get user data
      const userResponse = await apiService.get(`/users/${userId}`)
      const user = userResponse.data.user

      // Get AI profile
      const aiResponse = await apiService.get(`/ai/profile/${userId}`)
      const aiProfile = aiResponse.data.ai_profile

      const userData = { user, aiProfile }
      
      // Save to localStorage
      localStorage.setItem('xadrezmaster_user', JSON.stringify(user))
      
      dispatch({ type: 'LOGIN_SUCCESS', payload: userData })
      
      return userData
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const createUser = async (userData) => {
    dispatch({ type: 'SET_LOADING', payload: true })
    
    try {
      const response = await apiService.post('/users', userData)
      const newUser = response.data.user
      
      // Auto-login after creation
      await loginUser(newUser.id)
      
      return newUser
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const updateUser = async (updates) => {
    if (!state.user) return

    try {
      const response = await apiService.put(`/users/${state.user.id}`, updates)
      const updatedUser = response.data.user
      
      dispatch({ type: 'UPDATE_USER', payload: updatedUser })
      
      // Update localStorage
      localStorage.setItem('xadrezmaster_user', JSON.stringify(updatedUser))
      
      return updatedUser
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const updateAIProfile = async (updates) => {
    if (!state.user) return

    try {
      const response = await apiService.put(`/ai/profile/${state.user.id}`, updates)
      const updatedProfile = response.data.ai_profile
      
      dispatch({ type: 'UPDATE_AI_PROFILE', payload: updatedProfile })
      
      return updatedProfile
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message })
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('xadrezmaster_user')
    dispatch({ type: 'LOGOUT' })
  }

  const clearError = () => {
    dispatch({ type: 'SET_ERROR', payload: null })
  }

  const value = {
    ...state,
    loginUser,
    createUser,
    updateUser,
    updateAIProfile,
    logout,
    clearError
  }

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)
  if (!context) {
    throw new Error('useUser must be used within a UserProvider')
  }
  return context
}

