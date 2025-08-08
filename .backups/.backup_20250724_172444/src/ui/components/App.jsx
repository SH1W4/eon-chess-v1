import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import './App.css'

// Components
import Navbar from './components/Navbar'
import Home from './components/Home'
import ChessBoard from './components/ChessBoard'
import AICoach from './components/AICoach'
import CulturalContent from './components/CulturalContent'
import GameAnalysis from './components/GameAnalysis'
import Profile from './components/Profile'
import Login from './components/Login'

// Context
import { UserProvider } from './contexts/UserContext'
import { GameProvider } from './contexts/GameContext'

function App() {
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate app initialization
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-900 via-emerald-800 to-emerald-700 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-amber-400 mx-auto mb-4"></div>
          <h1 className="text-4xl font-bold text-white mb-2">XadrezMaster</h1>
          <p className="text-amber-200">Carregando sua experiência simbiótica...</p>
        </div>
      </div>
    )
  }

  return (
    <UserProvider>
      <GameProvider>
        <Router>
          <div className="min-h-screen bg-gradient-to-br from-emerald-900 via-emerald-800 to-emerald-700">
            <Navbar />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/play" element={<ChessBoard />} />
                <Route path="/ai-coach" element={<AICoach />} />
                <Route path="/cultural" element={<CulturalContent />} />
                <Route path="/analysis" element={<GameAnalysis />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </main>
            <Toaster />
          </div>
        </Router>
      </GameProvider>
    </UserProvider>
  )
}

export default App

