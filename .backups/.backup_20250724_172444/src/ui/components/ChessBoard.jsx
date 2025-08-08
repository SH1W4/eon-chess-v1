import { useState, useEffect, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  Crown, 
  Brain, 
  RotateCcw, 
  Flag, 
  Clock,
  Zap,
  MessageCircle,
  Settings
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { useGame } from '../contexts/GameContext'
import { useToast } from '@/hooks/use-toast'

// Chess piece symbols
const PIECES = {
  'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
  'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

export default function ChessBoard() {
  const { user } = useUser()
  const { 
    currentGame, 
    boardState, 
    selectedSquare, 
    possibleMoves,
    gameMode,
    aiDifficulty,
    createGame, 
    makeMove, 
    selectSquare,
    setPossibleMoves,
    setGameMode,
    setAIDifficulty,
    calculatePossibleMoves,
    isValidMove,
    getPieceAt
  } = useGame()
  
  const [gameStarted, setGameStarted] = useState(false)
  const [aiThinking, setAiThinking] = useState(false)
  const [gameTime, setGameTime] = useState(0)
  const [aiCommentary, setAiCommentary] = useState('')
  const [culturalTheme, setCulturalTheme] = useState('modern')
  const { toast } = useToast()

  // Timer effect
  useEffect(() => {
    let interval
    if (gameStarted && currentGame?.game_status === 'active') {
      interval = setInterval(() => {
        setGameTime(prev => prev + 1)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [gameStarted, currentGame])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const handleStartGame = async () => {
    if (!user) {
      toast({
        title: "Erro",
        description: "Você precisa estar logado para jogar",
        variant: "destructive",
      })
      return
    }

    try {
      const gameData = {
        opponentType: 'ai',
        gameMode,
        difficulty: aiDifficulty,
        culturalTheme
      }

      await createGame(gameData, user.id)
      setGameStarted(true)
      setGameTime(0)
      
      toast({
        title: "Jogo iniciado!",
        description: "Boa sorte em sua partida!",
      })
    } catch (error) {
      toast({
        title: "Erro ao iniciar jogo",
        description: error.message,
        variant: "destructive",
      })
    }
  }

  const handleSquareClick = useCallback(async (square) => {
    if (!currentGame || currentGame.game_status !== 'active') return

    if (selectedSquare === square) {
      // Deselect if clicking the same square
      selectSquare(null)
      setPossibleMoves([])
      return
    }

    if (selectedSquare && isValidMove(selectedSquare, square)) {
      // Make a move
      setAiThinking(true)
      
      try {
        const piece = getPieceAt(selectedSquare)
        const moveData = {
          from_square: selectedSquare,
          to_square: square,
          piece: piece?.type || 'p',
          board_state: boardState,
          notation: `${selectedSquare}-${square}` // Simplified notation
        }

        const result = await makeMove(moveData)
        
        selectSquare(null)
        setPossibleMoves([])

        if (result.aiMove) {
          setAiCommentary(result.aiMove.commentary)
          
          // Simulate AI move delay
          setTimeout(() => {
            setAiThinking(false)
          }, result.aiMove.thinking_time_ms || 1000)
        } else {
          setAiThinking(false)
        }

        if (result.game.game_status === 'completed') {
          setGameStarted(false)
          toast({
            title: "Jogo finalizado!",
            description: `Resultado: ${result.game.result}`,
          })
        }
      } catch (error) {
        setAiThinking(false)
        toast({
          title: "Erro no movimento",
          description: error.message,
          variant: "destructive",
        })
      }
    } else {
      // Select a square
      const piece = getPieceAt(square)
      if (piece && piece.color === 'white') { // Assuming user plays white
        selectSquare(square)
        const moves = calculatePossibleMoves(square)
        setPossibleMoves(moves)
      }
    }
  }, [selectedSquare, currentGame, boardState, makeMove, selectSquare, setPossibleMoves, calculatePossibleMoves, isValidMove, getPieceAt, toast])

  const renderBoard = () => {
    const board = []
    const pieces = parseFEN(boardState)
    
    for (let rank = 8; rank >= 1; rank--) {
      for (let file = 0; file < 8; file++) {
        const square = String.fromCharCode(97 + file) + rank
        const isLight = (rank + file) % 2 === 0
        const piece = pieces[square]
        const isSelected = selectedSquare === square
        const isPossibleMove = possibleMoves.some(move => move.to === square)
        
        board.push(
          <div
            key={square}
            className={`
              aspect-square flex items-center justify-center text-4xl cursor-pointer
              transition-all duration-200 relative
              ${isLight ? 'bg-amber-100' : 'bg-emerald-800'}
              ${isSelected ? 'ring-4 ring-amber-400' : ''}
              ${isPossibleMove ? 'ring-2 ring-blue-400' : ''}
              hover:brightness-110
            `}
            onClick={() => handleSquareClick(square)}
          >
            {piece && (
              <span className={`select-none ${piece.color === 'white' ? 'text-gray-800' : 'text-gray-100'}`}>
                {PIECES[piece.type.toUpperCase()] || PIECES[piece.type]}
              </span>
            )}
            {isPossibleMove && !piece && (
              <div className="w-4 h-4 bg-blue-400 rounded-full opacity-60" />
            )}
            <span className="absolute bottom-0 left-1 text-xs text-gray-600 font-mono">
              {square}
            </span>
          </div>
        )
      }
    }
    
    return board
  }

  if (!gameStarted && !currentGame) {
    return (
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-4">Tabuleiro Inteligente</h1>
          <p className="text-emerald-100">Configure sua partida e comece a jogar</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Crown className="h-5 w-5 mr-2 text-amber-400" />
                  Configurações da Partida
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-emerald-100 text-sm font-medium">
                      Modo de Jogo
                    </label>
                    <Select value={gameMode} onValueChange={setGameMode}>
                      <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="casual">Casual</SelectItem>
                        <SelectItem value="ranked">Ranqueada</SelectItem>
                        <SelectItem value="training">Treinamento</SelectItem>
                        <SelectItem value="cultural">Cultural</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-emerald-100 text-sm font-medium">
                      Dificuldade da IA
                    </label>
                    <Select value={aiDifficulty.toString()} onValueChange={(v) => setAIDifficulty(parseInt(v))}>
                      <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1">Muito Fácil</SelectItem>
                        <SelectItem value="3">Fácil</SelectItem>
                        <SelectItem value="5">Médio</SelectItem>
                        <SelectItem value="7">Difícil</SelectItem>
                        <SelectItem value="9">Muito Difícil</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {gameMode === 'cultural' && (
                  <div className="space-y-2">
                    <label className="text-emerald-100 text-sm font-medium">
                      Tema Cultural
                    </label>
                    <Select value={culturalTheme} onValueChange={setCulturalTheme}>
                      <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="medieval">Medieval</SelectItem>
                        <SelectItem value="renaissance">Renascimento</SelectItem>
                        <SelectItem value="modern">Moderno</SelectItem>
                        <SelectItem value="ancient">Antigo</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                )}

                <Button 
                  onClick={handleStartGame}
                  className="w-full bg-amber-500 hover:bg-amber-600 text-emerald-900 text-lg py-6"
                >
                  <Crown className="h-5 w-5 mr-2" />
                  Iniciar Partida
                </Button>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-4">
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Brain className="h-5 w-5 mr-2 text-blue-400" />
                  IA EstrategiX
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-emerald-200 text-sm">
                  Sua IA personalizada está pronta para se adaptar ao seu estilo de jogo 
                  e fornecer coaching em tempo real.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white text-sm">Dicas Rápidas</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="text-emerald-200 text-sm space-y-1">
                  <li>• Clique em uma peça para selecioná-la</li>
                  <li>• Movimentos possíveis serão destacados</li>
                  <li>• A IA fornecerá comentários durante o jogo</li>
                  <li>• Use o modo cultural para uma experiência imersiva</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Game Header */}
      <div className="flex flex-col md:flex-row justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Partida em Andamento</h1>
          <p className="text-emerald-100">
            {gameMode} • Dificuldade {aiDifficulty} • {culturalTheme}
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <Badge variant="secondary" className="bg-emerald-700 text-emerald-100">
            <Clock className="h-4 w-4 mr-1" />
            {formatTime(gameTime)}
          </Badge>
          <Badge 
            variant={currentGame?.current_turn === 'white' ? 'default' : 'secondary'}
            className="bg-amber-500/20 text-amber-400"
          >
            {currentGame?.current_turn === 'white' ? 'Sua vez' : 'IA pensando...'}
          </Badge>
        </div>
      </div>

      <div className="grid lg:grid-cols-4 gap-6">
        {/* Chess Board */}
        <div className="lg:col-span-3">
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardContent className="p-6">
              <div className="grid grid-cols-8 gap-0 max-w-2xl mx-auto border-4 border-emerald-700 rounded-lg overflow-hidden">
                {renderBoard()}
              </div>
              
              {aiThinking && (
                <div className="mt-4 text-center">
                  <div className="inline-flex items-center space-x-2 text-blue-400">
                    <Brain className="h-4 w-4 animate-pulse" />
                    <span>IA EstrategiX está pensando...</span>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Game Info Sidebar */}
        <div className="space-y-4">
          {/* AI Commentary */}
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white text-sm flex items-center">
                <MessageCircle className="h-4 w-4 mr-2 text-blue-400" />
                Comentários da IA
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-emerald-200 text-sm">
                {aiCommentary || "A IA fornecerá comentários durante a partida..."}
              </p>
            </CardContent>
          </Card>

          {/* Game Stats */}
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white text-sm">Estatísticas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-emerald-200">Movimentos:</span>
                  <span className="text-white">{currentGame?.total_moves || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-emerald-200">Capturas:</span>
                  <span className="text-white">0</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-emerald-200">Tempo médio:</span>
                  <span className="text-white">--</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Game Controls */}
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white text-sm">Controles</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full border-emerald-600 text-emerald-100 hover:bg-emerald-700"
              >
                <RotateCcw className="h-4 w-4 mr-2" />
                Desfazer
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full border-emerald-600 text-emerald-100 hover:bg-emerald-700"
              >
                <Zap className="h-4 w-4 mr-2" />
                Dica
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full border-red-600 text-red-400 hover:bg-red-700"
              >
                <Flag className="h-4 w-4 mr-2" />
                Desistir
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
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

