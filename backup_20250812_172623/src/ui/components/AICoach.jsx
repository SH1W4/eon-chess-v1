import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Brain, 
  Target, 
  TrendingUp, 
  BookOpen, 
  Zap,
  MessageCircle,
  Star,
  Clock
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { apiService } from '../services/api'

export default function AICoach() {
  const { user, aiProfile } = useUser()
  const [recommendations, setRecommendations] = useState(null)
  const [coachingAdvice, setCoachingAdvice] = useState(null)
  const [learningSession, setLearningSession] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (user) {
      loadCoachingData()
    }
  }, [user])

  const loadCoachingData = async () => {
    setLoading(true)
    try {
      const [recsResponse, adviceResponse] = await Promise.all([
        apiService.getPersonalizedRecommendations(user.id),
        apiService.getCoachingAdvice(user.id, 'general')
      ])
      
      setRecommendations(recsResponse.recommendations)
      setCoachingAdvice(adviceResponse.coaching_advice)
    } catch (error) {
      console.error('Error loading coaching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const startLearningSession = async (sessionType, topic = null) => {
    setLoading(true)
    try {
      const response = await apiService.createLearningSession({
        user_id: user.id,
        session_type: sessionType,
        topic
      })
      
      setLearningSession(response.session)
    } catch (error) {
      console.error('Error starting learning session:', error)
    } finally {
      setLoading(false)
    }
  }

  const completeLearningSession = async (results) => {
    if (!learningSession) return
    
    try {
      const response = await apiService.completeLearningSession(learningSession.id, results)
      setLearningSession(null)
      loadCoachingData() // Refresh recommendations
    } catch (error) {
      console.error('Error completing session:', error)
    }
  }

  if (!user) {
    return (
      <div className="text-center py-20">
        <Brain className="h-16 w-16 text-amber-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">IA EstrategiX</h2>
        <p className="text-emerald-200">Faça login para acessar seu coach pessoal</p>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4 flex items-center justify-center">
          <Brain className="h-10 w-10 mr-3 text-blue-400" />
          IA EstrategiX
        </h1>
        <p className="text-emerald-100 max-w-2xl mx-auto">
          Seu treinador pessoal de xadrez que se adapta ao seu estilo e evolui com você
        </p>
      </div>

      <Tabs defaultValue="coaching" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="coaching">Coaching</TabsTrigger>
          <TabsTrigger value="training">Treinamento</TabsTrigger>
          <TabsTrigger value="analysis">Análise</TabsTrigger>
          <TabsTrigger value="progress">Progresso</TabsTrigger>
        </TabsList>

        <TabsContent value="coaching" className="space-y-6">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* AI Advice */}
            <div className="lg:col-span-2">
              <Card className="bg-emerald-800/50 border-emerald-600">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <MessageCircle className="h-5 w-5 mr-2 text-blue-400" />
                    Conselho Personalizado
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="space-y-3">
                      <div className="h-4 bg-emerald-700/50 rounded animate-pulse" />
                      <div className="h-4 bg-emerald-700/50 rounded animate-pulse w-3/4" />
                    </div>
                  ) : coachingAdvice ? (
                    <div className="space-y-4">
                      <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                        <p className="text-blue-200 font-medium mb-2">{coachingAdvice.encouragement}</p>
                        <p className="text-emerald-100">{coachingAdvice.message}</p>
                      </div>
                      
                      {coachingAdvice.specific_tips?.length > 0 && (
                        <div>
                          <h4 className="text-white font-medium mb-2">Dicas Específicas:</h4>
                          <ul className="space-y-1">
                            {coachingAdvice.specific_tips.map((tip, index) => (
                              <li key={index} className="text-emerald-200 text-sm flex items-start">
                                <span className="text-amber-400 mr-2">•</span>
                                {tip}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-emerald-200">Carregando conselhos personalizados...</p>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* AI Profile Summary */}
            <div className="space-y-4">
              <Card className="bg-emerald-800/50 border-emerald-600">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Seu Perfil IA</CardTitle>
                </CardHeader>
                <CardContent>
                  {aiProfile ? (
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-emerald-200 text-sm">Estilo:</span>
                        <Badge variant="secondary" className="bg-emerald-700 text-emerald-100">
                          {aiProfile.learning_style}
                        </Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-emerald-200 text-sm">Tom:</span>
                        <Badge variant="secondary" className="bg-emerald-700 text-emerald-100">
                          {aiProfile.coaching_tone}
                        </Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-emerald-200 text-sm">Rating:</span>
                        <span className="text-white font-bold">{aiProfile.current_rating}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-emerald-200 text-sm">Carregando perfil...</p>
                  )}
                </CardContent>
              </Card>

              <Card className="bg-emerald-800/50 border-emerald-600">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Sessão Rápida</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button 
                    size="sm" 
                    className="w-full bg-amber-500 hover:bg-amber-600 text-emerald-900"
                    onClick={() => startLearningSession('practice')}
                    disabled={loading}
                  >
                    <Target className="h-4 w-4 mr-2" />
                    Prática Tática
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline"
                    className="w-full border-emerald-600 text-emerald-100 hover:bg-emerald-700"
                    onClick={() => startLearningSession('lesson')}
                    disabled={loading}
                  >
                    <BookOpen className="h-4 w-4 mr-2" />
                    Lição Rápida
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Recommendations */}
          {recommendations && (
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Zap className="h-5 w-5 mr-2 text-amber-400" />
                  Recomendações de Treinamento
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {recommendations.training_focus?.map((focus, index) => (
                    <div key={index} className="p-4 bg-emerald-700/50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="text-white font-medium">{focus.area}</h4>
                        <Badge 
                          variant={focus.priority === 'high' ? 'destructive' : 'secondary'}
                          className={focus.priority === 'high' ? 'bg-red-500/20 text-red-400' : ''}
                        >
                          {focus.priority}
                        </Badge>
                      </div>
                      <p className="text-emerald-200 text-sm mb-3">{focus.description}</p>
                      <Button 
                        size="sm" 
                        variant="outline"
                        className="w-full border-emerald-600 text-emerald-100 hover:bg-emerald-700"
                        onClick={() => startLearningSession('practice', focus.area)}
                      >
                        Treinar Agora
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="training" className="space-y-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="bg-emerald-800/50 border-emerald-600 hover:bg-emerald-800/70 transition-colors cursor-pointer">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Target className="h-5 w-5 mr-2 text-red-400" />
                  Táticas
                </CardTitle>
                <CardDescription className="text-emerald-200">
                  Resolva puzzles táticos personalizados
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button 
                  className="w-full bg-red-500 hover:bg-red-600 text-white"
                  onClick={() => startLearningSession('practice', 'tactics')}
                >
                  Começar Treino
                </Button>
              </CardContent>
            </Card>

            <Card className="bg-emerald-800/50 border-emerald-600 hover:bg-emerald-800/70 transition-colors cursor-pointer">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <BookOpen className="h-5 w-5 mr-2 text-blue-400" />
                  Aberturas
                </CardTitle>
                <CardDescription className="text-emerald-200">
                  Estude e pratique aberturas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button 
                  className="w-full bg-blue-500 hover:bg-blue-600 text-white"
                  onClick={() => startLearningSession('lesson', 'openings')}
                >
                  Estudar Agora
                </Button>
              </CardContent>
            </Card>

            <Card className="bg-emerald-800/50 border-emerald-600 hover:bg-emerald-800/70 transition-colors cursor-pointer">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Crown className="h-5 w-5 mr-2 text-purple-400" />
                  Finais
                </CardTitle>
                <CardDescription className="text-emerald-200">
                  Domine técnicas de final de jogo
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button 
                  className="w-full bg-purple-500 hover:bg-purple-600 text-white"
                  onClick={() => startLearningSession('lesson', 'endgames')}
                >
                  Praticar Finais
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="analysis" className="space-y-6">
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white">Análise de Performance</CardTitle>
              <CardDescription className="text-emerald-200">
                Insights detalhados sobre seu progresso
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <TrendingUp className="h-16 w-16 text-amber-400 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Análise Avançada</h3>
                <p className="text-emerald-200 mb-4">
                  Jogue algumas partidas para gerar análises detalhadas
                </p>
                <Button className="bg-amber-500 hover:bg-amber-600 text-emerald-900">
                  Jogar Partida
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="progress" className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Star className="h-5 w-5 mr-2 text-amber-400" />
                  Conquistas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-emerald-700/50 rounded">
                    <div>
                      <h4 className="text-white font-medium">Primeira Vitória</h4>
                      <p className="text-emerald-200 text-sm">Ganhe sua primeira partida</p>
                    </div>
                    <Badge className="bg-amber-500/20 text-amber-400">
                      Conquistado
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-emerald-700/30 rounded opacity-60">
                    <div>
                      <h4 className="text-white font-medium">Mestre Tático</h4>
                      <p className="text-emerald-200 text-sm">Resolva 50 puzzles táticos</p>
                    </div>
                    <Badge variant="secondary" className="bg-gray-500/20 text-gray-400">
                      Bloqueado
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Clock className="h-5 w-5 mr-2 text-green-400" />
                  Tempo de Estudo
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white">2h 34m</div>
                    <p className="text-emerald-200 text-sm">Esta semana</p>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-emerald-200">Meta semanal:</span>
                      <span className="text-white">5h</span>
                    </div>
                    <div className="w-full bg-emerald-700/50 rounded-full h-2">
                      <div className="bg-green-400 h-2 rounded-full" style={{width: '51%'}}></div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Learning Session Modal */}
      {learningSession && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="bg-emerald-800 border-emerald-600 max-w-2xl w-full mx-4">
            <CardHeader>
              <CardTitle className="text-white">
                Sessão de {learningSession.session_type}
              </CardTitle>
              <CardDescription className="text-emerald-200">
                {learningSession.topic}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Brain className="h-16 w-16 text-blue-400 mx-auto mb-4 animate-pulse" />
                <h3 className="text-xl font-bold text-white mb-2">Preparando sua sessão...</h3>
                <p className="text-emerald-200 mb-6">
                  A IA está personalizando o conteúdo para você
                </p>
                <div className="flex space-x-4 justify-center">
                  <Button 
                    variant="outline"
                    className="border-emerald-600 text-emerald-100 hover:bg-emerald-700"
                    onClick={() => setLearningSession(null)}
                  >
                    Cancelar
                  </Button>
                  <Button 
                    className="bg-amber-500 hover:bg-amber-600 text-emerald-900"
                    onClick={() => completeLearningSession({ completion_rate: 100, accuracy_score: 0.85 })}
                  >
                    Simular Conclusão
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

