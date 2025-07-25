const API_BASE_URL = 'http://localhost:5000/api'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? `${endpoint}?${queryString}` : endpoint
    
    return this.request(url, {
      method: 'GET'
    })
  }

  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE'
    })
  }

  // User endpoints
  async createUser(userData) {
    return this.post('/users', userData)
  }

  async getUser(userId) {
    return this.get(`/users/${userId}`)
  }

  async updateUser(userId, updates) {
    return this.put(`/users/${userId}`, updates)
  }

  // Game endpoints
  async createGame(gameData) {
    return this.post('/games', gameData)
  }

  async getGame(gameId) {
    return this.get(`/games/${gameId}`)
  }

  async getUserGames(userId) {
    return this.get('/games', { user_id: userId })
  }

  async makeMove(gameId, moveData) {
    return this.post(`/games/${gameId}/move`, moveData)
  }

  async analyzeGame(gameId) {
    return this.post(`/games/${gameId}/analysis`)
  }

  async getGameAnalysis(gameId) {
    return this.get(`/games/${gameId}/analysis`)
  }

  // AI endpoints
  async getAIProfile(userId) {
    return this.get(`/ai/profile/${userId}`)
  }

  async updateAIProfile(userId, updates) {
    return this.put(`/ai/profile/${userId}`, updates)
  }

  async getPersonalizedRecommendations(userId) {
    return this.get(`/ai/recommendations/${userId}`)
  }

  async getCoachingAdvice(userId, context, data = {}) {
    return this.post(`/ai/coaching/${userId}`, { context, data })
  }

  async createLearningSession(sessionData) {
    return this.post('/ai/learning-session', sessionData)
  }

  async completeLearningSession(sessionId, results) {
    return this.post(`/ai/learning-session/${sessionId}/complete`, results)
  }

  async getAdaptiveDifficulty(userId) {
    return this.get(`/ai/adaptive-difficulty/${userId}`)
  }

  async getCulturalNarrative(userId, context = 'general') {
    return this.get(`/ai/cultural-narrative/${userId}`, { context })
  }

  // Cultural content endpoints
  async getCulturalContent(filters = {}) {
    return this.get('/cultural/content', filters)
  }

  async getContentDetail(contentId, userId = null) {
    const params = userId ? { user_id: userId } : {}
    return this.get(`/cultural/content/${contentId}`, params)
  }

  async updateContentProgress(contentId, progressData) {
    return this.post(`/cultural/content/${contentId}/progress`, progressData)
  }

  async likeContent(contentId, userId) {
    return this.post(`/cultural/content/${contentId}/like`, { user_id: userId })
  }

  async getCulturalEvents(filters = {}) {
    return this.get('/cultural/events', filters)
  }

  async joinCulturalEvent(eventId, userId) {
    return this.post(`/cultural/events/${eventId}/join`, { user_id: userId })
  }

  async getCulturalThemes() {
    return this.get('/cultural/themes')
  }

  async getUserLibrary(userId) {
    return this.get(`/cultural/user-library/${userId}`)
  }

  // Health check
  async healthCheck() {
    return this.get('/health')
  }
}

export const apiService = new ApiService()
export default apiService

