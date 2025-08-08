import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  BarChart3, 
  TrendingUp, 
  Target, 
  AlertTriangle,
  CheckCircle,
  Clock,
  Brain,
  Zap
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { apiService } from '../services/api'

export default function GameAnalysis() {
  const { user } = useUser()
  const [games, setGames] = useState([])
  const [selectedGame, setSelectedGame] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (user) {
      loadGames()
    }
  }, [user])

  const loadGames = async () => {
    setLoading(true)
    try {
      const response = await apiService.getUserGames(user.id)
      setGames(response.games || [])
    } catch (error) {
      console.error('Error loading games:', error)
    } finally {
      setLoading(false)
    }
  }

  const analyzeGame = async (gameId) => {
    setLoading(true)
    try {
      const response = await apiService.analyzeGame(gameId)
      setAnalysis(response.analysis)
    } catch (error) {
      console.error('Error analyzing game:', error)
    } finally {
      setLoading(false)
    }
  }

  const sampleGames = [
    {
      id: 1,
      opponent_name: "IA EstrategiX",
      result: "white_wins",
      total_moves: 42,
      game_mode: "casual",
      created_at: "2024-12-01T10:30:00Z",
      completed_at: "2024-12-01T11:15:00Z"
    },
    {
      id: 2,
      opponent_name: "IA EstrategiX",
      result: "black_wins",
      total_moves: 38,
      game_mode: "training",
      created_at: "2024-11-30T15:20:00Z",
      completed_at: "2024-11-30T16:05:00Z"
    },
    {
      id: 3,
      opponent_name: "IA EstrategiX",
      result: "draw",
      total_moves: 67,
      game_mode: "ranked",
      created_at: "2024-11-29T19:45:00Z",
      completed_at: "2024-11-29T21:20:00Z"
    }
  ]

  const sampleAnalysis = {
    accuracy_score: 0.84,
    blunders_count: 1,
    mistakes_count: 2,
    inaccuracies_count: 4,
    brilliant_moves_count: 1,
    opening_name: "Italian Game",
    opening_accuracy: 0.91,
    middlegame_score: 0.78,
    endgame_score: 0.89,
    average_move_time: 28.5,
    ai_commentary: "Jogo sólido com bom controle do centro. Trabalhe na conversão de vantagens posicionais.",
    improvement_suggestions: [
      "Pratique mais finais de torre",
      "Estude padrões táticos de garfo",
      "Melhore a gestão do tempo"
    ]
  }

  const displayGames = games.length > 0 ? games : sampleGames
  const displayAnalysis = analysis || sampleAnalysis

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getResultBadge = (result) => {
    switch (result) {
      case 'white_wins':
        return <Badge className="bg-green-500/20 text-green-400">Vitória</Badge>
      case 'black_wins':
        return <Badge className="bg-red-500/20 text-red-400">Derrota</Badge>
      case 'draw':
        return <Badge className="bg-yellow-500/20 text-yellow-400">Empate</Badge>
      default:
        return <Badge variant="secondary">Em andamento</Badge>
    }
  }

  if (!user) {
    return (
      <div className="text-center py-20">
        <BarChart3 className="h-16 w-16 text-amber-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Análise de Jogos</h2>
        <p className="text-emerald-200">Faça login para analisar suas partidas</p>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4 flex items-center justify-center">
          <BarChart3 className="h-10 w-10 mr-3 text-purple-400" />
          Análise de Jogos
        </h1>
        <p className="text-emerald-100 max-w-2xl mx-auto">
          Análises profundas de suas partidas com insights personalizados da IA
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Games List */}
        <div className="lg:col-span-1">
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white">Suas Partidas</CardTitle>
              <CardDescription className="text-emerald-200">
                Selecione uma partida para análise
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-3">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="h-16 bg-emerald-700/50 rounded animate-pulse" />
                  ))}
                </div>
              ) : (
                <div className="space-y-3">
                  {displayGames.map((game) => (
                    <div
                      key={game.id}
                      className={`p-3 rounded-lg cursor-pointer transition-colors ${
                        selectedGame?.id === game.id
                          ? 'bg-emerald-600/50 border border-emerald-500'
                          : 'bg-emerald-700/50 hover:bg-emerald-700/70'
                      }`}
                      onClick={() => setSelectedGame(game)}
                    >
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-white font-medium">
                          vs {game.opponent_name}
                        </span>
                        {getResultBadge(game.result)}
                      </div>
                      <div className="text-emerald-200 text-sm">
                        {game.total_moves} movimentos • {game.game_mode}
                      </div>
                      <div className="text-emerald-300 text-xs">
                        {formatDate(game.created_at)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Analysis Details */}
        <div className="lg:col-span-2">
          {selectedGame ? (
            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Visão Geral</TabsTrigger>
                <TabsTrigger value="moves">Movimentos</TabsTrigger>
                <TabsTrigger value="phases">Fases</TabsTrigger>
                <TabsTrigger value="insights">Insights</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <Card className="bg-emerald-800/50 border-emerald-600">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center justify-between">
                      <span>Análise da Partida</span>
                      <Button 
                        size="sm"
                        className="bg-purple-500 hover:bg-purple-600 text-white"
                        onClick={() => analyzeGame(selectedGame.id)}
                        disabled={loading}
                      >
                        <Brain className="h-4 w-4 mr-2" />
                        {loading ? 'Analisando...' : 'Analisar'}
                      </Button>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-6">
                      {/* Performance Metrics */}
                      <div className="space-y-4">
                        <h3 className="text-white font-medium">Performance</h3>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between">
                            <span className="text-emerald-200">Precisão:</span>
                            <div className="flex items-center">
                              <div className="w-20 bg-emerald-700/50 rounded-full h-2 mr-2">
                                <div 
                                  className="bg-green-400 h-2 rounded-full" 
                                  style={{width: `${displayAnalysis.accuracy_score * 100}%`}}
                                />
                              </div>
                              <span className="text-white font-bold">
                                {Math.round(displayAnalysis.accuracy_score * 100)}%
                              </span>
                            </div>
                          </div>
                          
                          <div className="flex justify-between">
                            <span className="text-emerald-200">Tempo médio:</span>
                            <span className="text-white">{displayAnalysis.average_move_time}s</span>
                          </div>
                        </div>
                      </div>

                      {/* Move Quality */}
                      <div className="space-y-4">
                        <h3 className="text-white font-medium">Qualidade dos Movimentos</h3>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-emerald-200 flex items-center">
                              <Zap className="h-4 w-4 mr-1 text-yellow-400" />
                              Brilhantes:
                            </span>
                            <span className="text-white font-bold">{displayAnalysis.brilliant_moves_count}</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="text-emerald-200 flex items-center">
                              <AlertTriangle className="h-4 w-4 mr-1 text-red-400" />
                              Blunders:
                            </span>
                            <span className="text-white font-bold">{displayAnalysis.blunders_count}</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="text-emerald-200 flex items-center">
                              <AlertTriangle className="h-4 w-4 mr-1 text-orange-400" />
                              Erros:
                            </span>
                            <span className="text-white font-bold">{displayAnalysis.mistakes_count}</span>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="text-emerald-200 flex items-center">
                              <AlertTriangle className="h-4 w-4 mr-1 text-yellow-400" />
                              Imprecisões:
                            </span>
                            <span className="text-white font-bold">{displayAnalysis.inaccuracies_count}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* AI Commentary */}
                <Card className="bg-emerald-800/50 border-emerald-600">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <Brain className="h-5 w-5 mr-2 text-blue-400" />
                      Comentário da IA
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-emerald-100 mb-4">{displayAnalysis.ai_commentary}</p>
                    
                    <h4 className="text-white font-medium mb-2">Sugestões de Melhoria:</h4>
                    <ul className="space-y-1">
                      {displayAnalysis.improvement_suggestions.map((suggestion, index) => (
                        <li key={index} className="text-emerald-200 flex items-start">
                          <CheckCircle className="h-4 w-4 mr-2 text-green-400 mt-0.5 flex-shrink-0" />
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="moves" className="space-y-6">
                <Card className="bg-emerald-800/50 border-emerald-600">
                  <CardHeader>
                    <CardTitle className="text-white">Análise de Movimentos</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-12">
                      <Target className="h-16 w-16 text-amber-400 mx-auto mb-4" />
                      <h3 className="text-xl font-bold text-white mb-2">Análise Detalhada</h3>
                      <p className="text-emerald-200 mb-4">
                        Visualização movimento por movimento em desenvolvimento
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="phases" className="space-y-6">
                <div className="grid md:grid-cols-3 gap-4">
                  <Card className="bg-emerald-800/50 border-emerald-600">
                    <CardHeader>
                      <CardTitle className="text-white text-sm">Abertura</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-white mb-1">
                          {Math.round(displayAnalysis.opening_accuracy * 100)}%
                        </div>
                        <p className="text-emerald-200 text-sm">{displayAnalysis.opening_name}</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-emerald-800/50 border-emerald-600">
                    <CardHeader>
                      <CardTitle className="text-white text-sm">Meio-jogo</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-white mb-1">
                          {Math.round(displayAnalysis.middlegame_score * 100)}%
                        </div>
                        <p className="text-emerald-200 text-sm">Performance</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-emerald-800/50 border-emerald-600">
                    <CardHeader>
                      <CardTitle className="text-white text-sm">Final</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-white mb-1">
                          {Math.round(displayAnalysis.endgame_score * 100)}%
                        </div>
                        <p className="text-emerald-200 text-sm">Técnica</p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="insights" className="space-y-6">
                <Card className="bg-emerald-800/50 border-emerald-600">
                  <CardHeader>
                    <CardTitle className="text-white flex items-center">
                      <TrendingUp className="h-5 w-5 mr-2 text-green-400" />
                      Insights Personalizados
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                        <h4 className="text-blue-200 font-medium mb-2">Padrão Identificado</h4>
                        <p className="text-emerald-100 text-sm">
                          Você tende a jogar melhor em posições abertas. Continue desenvolvendo 
                          seu estilo tático.
                        </p>
                      </div>
                      
                      <div className="p-4 bg-amber-500/10 border border-amber-500/20 rounded-lg">
                        <h4 className="text-amber-200 font-medium mb-2">Área de Melhoria</h4>
                        <p className="text-emerald-100 text-sm">
                          Gestão do tempo pode ser melhorada. Considere praticar com 
                          controles de tempo mais rápidos.
                        </p>
                      </div>
                      
                      <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                        <h4 className="text-green-200 font-medium mb-2">Ponto Forte</h4>
                        <p className="text-emerald-100 text-sm">
                          Excelente precisão na abertura. Seu conhecimento teórico 
                          está se desenvolvendo bem.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          ) : (
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardContent className="p-12 text-center">
                <BarChart3 className="h-16 w-16 text-amber-400 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Selecione uma Partida</h3>
                <p className="text-emerald-200">
                  Escolha uma partida da lista para ver a análise detalhada
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

