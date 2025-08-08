import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Crown, 
  Brain, 
  BookOpen, 
  BarChart3, 
  Users, 
  Zap,
  Star,
  TrendingUp,
  Calendar,
  Award
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { apiService } from '../services/api'

export default function Home() {
  const { user, isAuthenticated } = useUser()
  const navigate = useNavigate()
  const [recommendations, setRecommendations] = useState(null)
  const [culturalEvents, setCulturalEvents] = useState([])
  const [recentGames, setRecentGames] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isAuthenticated && user) {
      loadDashboardData()
    }
  }, [isAuthenticated, user])

  const loadDashboardData = async () => {
    setLoading(true)
    try {
      // Load personalized recommendations
      const recsResponse = await apiService.getPersonalizedRecommendations(user.id)
      setRecommendations(recsResponse.recommendations)

      // Load cultural events
      const eventsResponse = await apiService.getCulturalEvents({ user_id: user.id })
      setCulturalEvents(eventsResponse.personalized_events || eventsResponse.events.slice(0, 3))

      // Load recent games
      const gamesResponse = await apiService.getUserGames(user.id)
      setRecentGames(gamesResponse.games.slice(0, 3))
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const features = [
    {
      icon: Crown,
      title: 'Tabuleiro Inteligente',
      description: 'Conecte seu tabuleiro físico e jogue com detecção automática de movimentos',
      color: 'text-amber-400'
    },
    {
      icon: Brain,
      title: 'IA EstrategiX',
      description: 'Treinador pessoal que se adapta ao seu estilo e evolui com você',
      color: 'text-blue-400'
    },
    {
      icon: BookOpen,
      title: 'Narrativas Culturais',
      description: 'Explore a rica história e filosofia do xadrez através de histórias envolventes',
      color: 'text-green-400'
    },
    {
      icon: BarChart3,
      title: 'Análise Avançada',
      description: 'Análises profundas de suas partidas com insights personalizados',
      color: 'text-purple-400'
    }
  ]

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex flex-col">
        {/* Hero Section */}
        <section className="flex-1 flex items-center justify-center py-20">
          <div className="text-center max-w-4xl mx-auto px-4">
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              Bem-vindo ao
              <span className="text-amber-400 block">XadrezMaster</span>
            </h1>
            <p className="text-xl md:text-2xl text-emerald-100 mb-8 max-w-2xl mx-auto">
              O primeiro ecossistema simbiótico de xadrez que une tradição milenar 
              com inteligência artificial avançada
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="bg-amber-500 hover:bg-amber-600 text-emerald-900 text-lg px-8 py-3"
                onClick={() => navigate('/login')}
              >
                Começar Jornada
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="border-emerald-300 text-emerald-100 hover:bg-emerald-700 text-lg px-8 py-3"
                onClick={() => navigate('/cultural')}
              >
                Explorar Cultura
              </Button>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-emerald-800/50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-white mb-12">
              Uma Nova Era do Xadrez
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <Card key={index} className="bg-emerald-700/50 border-emerald-600 hover:bg-emerald-700/70 transition-colors">
                    <CardHeader className="text-center">
                      <Icon className={`h-12 w-12 mx-auto mb-4 ${feature.color}`} />
                      <CardTitle className="text-white">{feature.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-emerald-100 text-center">
                        {feature.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Pronto para Evoluir seu Xadrez?
            </h2>
            <p className="text-xl text-emerald-100 mb-8 max-w-2xl mx-auto">
              Junte-se à revolução do xadrez inteligente e descubra seu potencial máximo
            </p>
            <Button 
              size="lg" 
              className="bg-amber-500 hover:bg-amber-600 text-emerald-900 text-lg px-8 py-3"
              onClick={() => navigate('/login')}
            >
              Criar Conta Gratuita
            </Button>
          </div>
        </section>
      </div>
    )
  }

  // Authenticated user dashboard
  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-2">
          Bem-vindo de volta, {user?.username}!
        </h1>
        <p className="text-emerald-100">
          Continue sua jornada no mundo do xadrez inteligente
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-4 gap-4">
        <Button 
          className="h-20 bg-amber-500 hover:bg-amber-600 text-emerald-900"
          onClick={() => navigate('/play')}
        >
          <div className="flex flex-col items-center">
            <Crown className="h-6 w-6 mb-1" />
            <span>Jogar Agora</span>
          </div>
        </Button>
        <Button 
          variant="outline" 
          className="h-20 border-emerald-300 text-emerald-100 hover:bg-emerald-700"
          onClick={() => navigate('/ai-coach')}
        >
          <div className="flex flex-col items-center">
            <Brain className="h-6 w-6 mb-1" />
            <span>IA Coach</span>
          </div>
        </Button>
        <Button 
          variant="outline" 
          className="h-20 border-emerald-300 text-emerald-100 hover:bg-emerald-700"
          onClick={() => navigate('/cultural')}
        >
          <div className="flex flex-col items-center">
            <BookOpen className="h-6 w-6 mb-1" />
            <span>Explorar</span>
          </div>
        </Button>
        <Button 
          variant="outline" 
          className="h-20 border-emerald-300 text-emerald-100 hover:bg-emerald-700"
          onClick={() => navigate('/analysis')}
        >
          <div className="flex flex-col items-center">
            <BarChart3 className="h-6 w-6 mb-1" />
            <span>Análises</span>
          </div>
        </Button>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Recommendations */}
        <div className="lg:col-span-2">
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Zap className="h-5 w-5 mr-2 text-amber-400" />
                Recomendações Personalizadas
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-3">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="h-16 bg-emerald-700/50 rounded animate-pulse" />
                  ))}
                </div>
              ) : recommendations ? (
                <div className="space-y-4">
                  {recommendations.training_focus?.slice(0, 3).map((focus, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-emerald-700/50 rounded">
                      <div>
                        <h4 className="text-white font-medium">{focus.area}</h4>
                        <p className="text-emerald-200 text-sm">{focus.description}</p>
                      </div>
                      <Badge variant="secondary" className="bg-amber-500/20 text-amber-400">
                        {focus.priority}
                      </Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-emerald-200">Carregando recomendações...</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Stats */}
        <div className="space-y-4">
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-green-400" />
                Seu Progresso
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-emerald-200">Rating Atual</span>
                  <span className="text-white font-bold">1247</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-emerald-200">Partidas Jogadas</span>
                  <span className="text-white font-bold">23</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-emerald-200">Taxa de Vitória</span>
                  <span className="text-white font-bold">68%</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Calendar className="h-5 w-5 mr-2 text-blue-400" />
                Próximos Eventos
              </CardTitle>
            </CardHeader>
            <CardContent>
              {culturalEvents.length > 0 ? (
                <div className="space-y-3">
                  {culturalEvents.map((event, index) => (
                    <div key={index} className="p-3 bg-emerald-700/50 rounded">
                      <h4 className="text-white font-medium text-sm">{event.title}</h4>
                      <p className="text-emerald-200 text-xs">{event.cultural_theme}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-emerald-200 text-sm">Nenhum evento próximo</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Recent Games */}
      {recentGames.length > 0 && (
        <Card className="bg-emerald-800/50 border-emerald-600">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Award className="h-5 w-5 mr-2 text-purple-400" />
              Partidas Recentes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              {recentGames.map((game, index) => (
                <div key={index} className="p-4 bg-emerald-700/50 rounded">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-white font-medium">
                      vs {game.opponent_name || 'IA'}
                    </span>
                    <Badge 
                      variant={game.result === 'white_wins' ? 'default' : 'secondary'}
                      className={
                        game.result === 'white_wins' 
                          ? 'bg-green-500/20 text-green-400' 
                          : game.result === 'black_wins'
                          ? 'bg-red-500/20 text-red-400'
                          : 'bg-yellow-500/20 text-yellow-400'
                      }
                    >
                      {game.result === 'white_wins' ? 'Vitória' : 
                       game.result === 'black_wins' ? 'Derrota' : 'Empate'}
                    </Badge>
                  </div>
                  <p className="text-emerald-200 text-sm">
                    {game.total_moves} movimentos • {game.game_mode}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

