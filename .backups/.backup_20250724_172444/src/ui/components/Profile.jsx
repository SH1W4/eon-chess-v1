import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { 
  User, 
  Settings, 
  Trophy, 
  Target,
  Brain,
  Save,
  Edit,
  Star,
  Calendar,
  TrendingUp
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { useToast } from '@/hooks/use-toast'

export default function Profile() {
  const { user, aiProfile, updateUser, updateAIProfile } = useUser()
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({})
  const [aiSettings, setAiSettings] = useState({})
  const { toast } = useToast()

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        email: user.email || '',
        country: user.country || '',
        chess_experience: user.chess_experience || 'beginner'
      })
    }
  }, [user])

  useEffect(() => {
    if (aiProfile) {
      setAiSettings({
        learning_style: aiProfile.learning_style || 'adaptive',
        coaching_tone: aiProfile.coaching_tone || 'encouraging',
        difficulty_preference: aiProfile.difficulty_preference || 'adaptive',
        focus_areas: aiProfile.focus_areas || []
      })
    }
  }, [aiProfile])

  const handleSaveProfile = async () => {
    try {
      await updateUser(formData)
      setEditing(false)
      toast({
        title: "Perfil atualizado!",
        description: "Suas informações foram salvas com sucesso.",
      })
    } catch (error) {
      toast({
        title: "Erro ao salvar",
        description: error.message,
        variant: "destructive",
      })
    }
  }

  const handleSaveAISettings = async () => {
    try {
      await updateAIProfile(aiSettings)
      toast({
        title: "Configurações da IA atualizadas!",
        description: "A IA EstrategiX foi personalizada para você.",
      })
    } catch (error) {
      toast({
        title: "Erro ao salvar configurações",
        description: error.message,
        variant: "destructive",
      })
    }
  }

  if (!user) {
    return (
      <div className="text-center py-20">
        <User className="h-16 w-16 text-amber-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Perfil do Usuário</h2>
        <p className="text-emerald-200">Faça login para acessar seu perfil</p>
      </div>
    )
  }

  const achievements = [
    { id: 1, name: "Primeira Vitória", description: "Ganhe sua primeira partida", earned: true },
    { id: 2, name: "Estudioso", description: "Complete 10 lições culturais", earned: true },
    { id: 3, name: "Tático", description: "Resolva 25 puzzles táticos", earned: false },
    { id: 4, name: "Mestre", description: "Alcance rating 1500", earned: false }
  ]

  const stats = {
    total_games: 23,
    wins: 15,
    losses: 6,
    draws: 2,
    current_rating: 1247,
    peak_rating: 1289,
    study_time: "12h 34m",
    favorite_opening: "Italian Game"
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4 flex items-center justify-center">
          <User className="h-10 w-10 mr-3 text-amber-400" />
          Meu Perfil
        </h1>
        <p className="text-emerald-100">Gerencie suas informações e configurações</p>
      </div>

      <Tabs defaultValue="profile" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="profile">Perfil</TabsTrigger>
          <TabsTrigger value="ai-settings">IA Settings</TabsTrigger>
          <TabsTrigger value="stats">Estatísticas</TabsTrigger>
          <TabsTrigger value="achievements">Conquistas</TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-6">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Profile Info */}
            <div className="lg:col-span-2">
              <Card className="bg-emerald-800/50 border-emerald-600">
                <CardHeader>
                  <CardTitle className="text-white flex items-center justify-between">
                    <span className="flex items-center">
                      <User className="h-5 w-5 mr-2" />
                      Informações Pessoais
                    </span>
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-emerald-600 text-emerald-100 hover:bg-emerald-700"
                      onClick={() => setEditing(!editing)}
                    >
                      <Edit className="h-4 w-4 mr-2" />
                      {editing ? 'Cancelar' : 'Editar'}
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="full_name" className="text-emerald-100">
                        Nome Completo
                      </Label>
                      <Input
                        id="full_name"
                        value={formData.full_name || ''}
                        onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                        disabled={!editing}
                        className="bg-emerald-700/50 border-emerald-600 text-white disabled:opacity-60"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="email" className="text-emerald-100">
                        Email
                      </Label>
                      <Input
                        id="email"
                        type="email"
                        value={formData.email || ''}
                        onChange={(e) => setFormData({...formData, email: e.target.value})}
                        disabled={!editing}
                        className="bg-emerald-700/50 border-emerald-600 text-white disabled:opacity-60"
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="country" className="text-emerald-100">
                        País
                      </Label>
                      <Input
                        id="country"
                        value={formData.country || ''}
                        onChange={(e) => setFormData({...formData, country: e.target.value})}
                        disabled={!editing}
                        className="bg-emerald-700/50 border-emerald-600 text-white disabled:opacity-60"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="experience" className="text-emerald-100">
                        Experiência no Xadrez
                      </Label>
                      <Select 
                        value={formData.chess_experience}
                        onValueChange={(value) => setFormData({...formData, chess_experience: value})}
                        disabled={!editing}
                      >
                        <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="beginner">Iniciante</SelectItem>
                          <SelectItem value="intermediate">Intermediário</SelectItem>
                          <SelectItem value="advanced">Avançado</SelectItem>
                          <SelectItem value="expert">Expert</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {editing && (
                    <div className="flex space-x-4 pt-4">
                      <Button 
                        onClick={handleSaveProfile}
                        className="bg-amber-500 hover:bg-amber-600 text-emerald-900"
                      >
                        <Save className="h-4 w-4 mr-2" />
                        Salvar Alterações
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Quick Stats */}
            <div className="space-y-4">
              <Card className="bg-emerald-800/50 border-emerald-600">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Rating Atual</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white">{stats.current_rating}</div>
                    <p className="text-emerald-200 text-sm">Pico: {stats.peak_rating}</p>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-emerald-800/50 border-emerald-600">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Partidas Jogadas</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white">{stats.total_games}</div>
                    <p className="text-emerald-200 text-sm">
                      {Math.round((stats.wins / stats.total_games) * 100)}% vitórias
                    </p>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-emerald-800/50 border-emerald-600">
                <CardHeader>
                  <CardTitle className="text-white text-sm">Tempo de Estudo</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-white">{stats.study_time}</div>
                    <p className="text-emerald-200 text-sm">Total acumulado</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="ai-settings" className="space-y-6">
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Brain className="h-5 w-5 mr-2 text-blue-400" />
                Configurações da IA EstrategiX
              </CardTitle>
              <CardDescription className="text-emerald-200">
                Personalize como a IA interage e ensina você
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-emerald-100">Estilo de Aprendizado</Label>
                    <Select 
                      value={aiSettings.learning_style}
                      onValueChange={(value) => setAiSettings({...aiSettings, learning_style: value})}
                    >
                      <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="visual">Visual</SelectItem>
                        <SelectItem value="analytical">Analítico</SelectItem>
                        <SelectItem value="practical">Prático</SelectItem>
                        <SelectItem value="adaptive">Adaptativo</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-emerald-100">Tom do Coach</Label>
                    <Select 
                      value={aiSettings.coaching_tone}
                      onValueChange={(value) => setAiSettings({...aiSettings, coaching_tone: value})}
                    >
                      <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="encouraging">Encorajador</SelectItem>
                        <SelectItem value="direct">Direto</SelectItem>
                        <SelectItem value="friendly">Amigável</SelectItem>
                        <SelectItem value="professional">Profissional</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-emerald-100">Preferência de Dificuldade</Label>
                    <Select 
                      value={aiSettings.difficulty_preference}
                      onValueChange={(value) => setAiSettings({...aiSettings, difficulty_preference: value})}
                    >
                      <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="easy">Fácil</SelectItem>
                        <SelectItem value="moderate">Moderado</SelectItem>
                        <SelectItem value="challenging">Desafiador</SelectItem>
                        <SelectItem value="adaptive">Adaptativo</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-emerald-100">Áreas de Foco</Label>
                    <div className="space-y-2">
                      {['Táticas', 'Aberturas', 'Finais', 'Estratégia'].map((area) => (
                        <label key={area} className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={aiSettings.focus_areas?.includes(area.toLowerCase()) || false}
                            onChange={(e) => {
                              const areas = aiSettings.focus_areas || []
                              if (e.target.checked) {
                                setAiSettings({
                                  ...aiSettings, 
                                  focus_areas: [...areas, area.toLowerCase()]
                                })
                              } else {
                                setAiSettings({
                                  ...aiSettings,
                                  focus_areas: areas.filter(a => a !== area.toLowerCase())
                                })
                              }
                            }}
                            className="rounded border-emerald-600"
                          />
                          <span className="text-emerald-100">{area}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <Button 
                onClick={handleSaveAISettings}
                className="bg-blue-500 hover:bg-blue-600 text-white"
              >
                <Save className="h-4 w-4 mr-2" />
                Salvar Configurações da IA
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="stats" className="space-y-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white text-sm flex items-center">
                  <Trophy className="h-4 w-4 mr-2 text-amber-400" />
                  Vitórias
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{stats.wins}</div>
                <p className="text-emerald-200 text-sm">
                  {Math.round((stats.wins / stats.total_games) * 100)}% taxa
                </p>
              </CardContent>
            </Card>

            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white text-sm flex items-center">
                  <Target className="h-4 w-4 mr-2 text-red-400" />
                  Derrotas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{stats.losses}</div>
                <p className="text-emerald-200 text-sm">
                  {Math.round((stats.losses / stats.total_games) * 100)}% taxa
                </p>
              </CardContent>
            </Card>

            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white text-sm flex items-center">
                  <Calendar className="h-4 w-4 mr-2 text-yellow-400" />
                  Empates
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{stats.draws}</div>
                <p className="text-emerald-200 text-sm">
                  {Math.round((stats.draws / stats.total_games) * 100)}% taxa
                </p>
              </CardContent>
            </Card>

            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white text-sm flex items-center">
                  <TrendingUp className="h-4 w-4 mr-2 text-green-400" />
                  Rating
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{stats.current_rating}</div>
                <p className="text-emerald-200 text-sm">Pico: {stats.peak_rating}</p>
              </CardContent>
            </Card>
          </div>

          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white">Estatísticas Detalhadas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="text-white font-medium">Performance</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-emerald-200">Abertura favorita:</span>
                      <span className="text-white">{stats.favorite_opening}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-200">Tempo médio por movimento:</span>
                      <span className="text-white">28.5s</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-200">Precisão média:</span>
                      <span className="text-white">84%</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-white font-medium">Atividade</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-emerald-200">Tempo total de estudo:</span>
                      <span className="text-white">{stats.study_time}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-200">Puzzles resolvidos:</span>
                      <span className="text-white">47</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-200">Lições completadas:</span>
                      <span className="text-white">12</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="achievements" className="space-y-6">
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Star className="h-5 w-5 mr-2 text-amber-400" />
                Suas Conquistas
              </CardTitle>
              <CardDescription className="text-emerald-200">
                Marcos alcançados em sua jornada no xadrez
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                {achievements.map((achievement) => (
                  <div
                    key={achievement.id}
                    className={`p-4 rounded-lg border ${
                      achievement.earned
                        ? 'bg-amber-500/10 border-amber-500/20'
                        : 'bg-emerald-700/30 border-emerald-600/30 opacity-60'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-white font-medium">{achievement.name}</h4>
                      {achievement.earned ? (
                        <Badge className="bg-amber-500/20 text-amber-400">
                          <Star className="h-3 w-3 mr-1" />
                          Conquistado
                        </Badge>
                      ) : (
                        <Badge variant="secondary" className="bg-gray-500/20 text-gray-400">
                          Bloqueado
                        </Badge>
                      )}
                    </div>
                    <p className="text-emerald-200 text-sm">{achievement.description}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

