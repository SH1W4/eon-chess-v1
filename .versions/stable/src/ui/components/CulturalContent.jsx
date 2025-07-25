import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  BookOpen, 
  Search, 
  Heart, 
  Clock, 
  Star,
  Calendar,
  Users,
  Play
} from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { apiService } from '../services/api'

export default function CulturalContent() {
  const { user } = useUser()
  const [content, setContent] = useState([])
  const [events, setEvents] = useState([])
  const [themes, setThemes] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedTheme, setSelectedTheme] = useState('all')
  const [selectedType, setSelectedType] = useState('all')

  useEffect(() => {
    loadCulturalData()
  }, [user])

  const loadCulturalData = async () => {
    setLoading(true)
    try {
      const [contentResponse, eventsResponse, themesResponse] = await Promise.all([
        apiService.getCulturalContent({ user_id: user?.id }),
        apiService.getCulturalEvents({ user_id: user?.id }),
        apiService.getCulturalThemes()
      ])
      
      setContent(contentResponse.content || [])
      setEvents(eventsResponse.events || [])
      setThemes(themesResponse.themes || [])
    } catch (error) {
      console.error('Error loading cultural data:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredContent = content.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesTheme = selectedTheme === 'all' || item.cultural_theme === selectedTheme
    const matchesType = selectedType === 'all' || item.content_type === selectedType
    
    return matchesSearch && matchesTheme && matchesType
  })

  const handleLikeContent = async (contentId) => {
    if (!user) return
    
    try {
      await apiService.likeContent(contentId, user.id)
      // Update local state
      setContent(prev => prev.map(item => 
        item.id === contentId 
          ? { ...item, like_count: item.like_count + 1 }
          : item
      ))
    } catch (error) {
      console.error('Error liking content:', error)
    }
  }

  const sampleContent = [
    {
      id: 1,
      title: "O Xadrez na Corte de Carlos Magno",
      content_type: "story",
      cultural_theme: "medieval",
      description: "Uma fascinante história sobre como o xadrez chegou à Europa medieval.",
      difficulty_level: 2,
      view_count: 1247,
      like_count: 89,
      is_premium: false
    },
    {
      id: 2,
      title: "A Dama Poderosa: Evolução da Rainha",
      content_type: "historical",
      cultural_theme: "renaissance",
      description: "Como a peça mais poderosa do xadrez evoluiu ao longo dos séculos.",
      difficulty_level: 3,
      view_count: 892,
      like_count: 156,
      is_premium: true
    },
    {
      id: 3,
      title: "Filosofia do Xadrez: Lições de Vida",
      content_type: "philosophical",
      cultural_theme: "modern",
      description: "Como o xadrez pode ensinar importantes lições de vida e filosofia.",
      difficulty_level: 1,
      view_count: 2103,
      like_count: 234,
      is_premium: false
    }
  ]

  const sampleEvents = [
    {
      id: 1,
      title: "Noite Medieval de Xadrez",
      event_type: "tournament",
      cultural_theme: "medieval",
      start_time: "2024-12-15T19:00:00Z",
      max_participants: 20,
      current_participants: 12,
      is_premium: false
    },
    {
      id: 2,
      title: "Masterclass: Estratégias Renascentistas",
      event_type: "masterclass",
      cultural_theme: "renaissance",
      start_time: "2024-12-20T15:00:00Z",
      max_participants: 15,
      current_participants: 8,
      is_premium: true
    }
  ]

  const displayContent = filteredContent.length > 0 ? filteredContent : sampleContent
  const displayEvents = events.length > 0 ? events : sampleEvents

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4 flex items-center justify-center">
          <BookOpen className="h-10 w-10 mr-3 text-green-400" />
          Narrativas Culturais
        </h1>
        <p className="text-emerald-100 max-w-2xl mx-auto">
          Explore a rica história e filosofia do xadrez através de histórias envolventes
        </p>
      </div>

      {/* Filters */}
      <Card className="bg-emerald-800/50 border-emerald-600">
        <CardContent className="p-6">
          <div className="grid md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-emerald-400" />
              <Input
                placeholder="Buscar conteúdo..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
              />
            </div>
            
            <Select value={selectedTheme} onValueChange={setSelectedTheme}>
              <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                <SelectValue placeholder="Tema" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos os Temas</SelectItem>
                <SelectItem value="medieval">Medieval</SelectItem>
                <SelectItem value="renaissance">Renascimento</SelectItem>
                <SelectItem value="modern">Moderno</SelectItem>
                <SelectItem value="ancient">Antigo</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedType} onValueChange={setSelectedType}>
              <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                <SelectValue placeholder="Tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos os Tipos</SelectItem>
                <SelectItem value="story">História</SelectItem>
                <SelectItem value="historical">Histórico</SelectItem>
                <SelectItem value="philosophical">Filosófico</SelectItem>
                <SelectItem value="lesson">Lição</SelectItem>
              </SelectContent>
            </Select>

            <Button className="bg-amber-500 hover:bg-amber-600 text-emerald-900">
              <Search className="h-4 w-4 mr-2" />
              Buscar
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Content List */}
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-2xl font-bold text-white">Conteúdo Cultural</h2>
          
          {loading ? (
            <div className="space-y-4">
              {[1, 2, 3].map(i => (
                <Card key={i} className="bg-emerald-800/50 border-emerald-600">
                  <CardContent className="p-6">
                    <div className="space-y-3">
                      <div className="h-6 bg-emerald-700/50 rounded animate-pulse" />
                      <div className="h-4 bg-emerald-700/50 rounded animate-pulse w-3/4" />
                      <div className="h-4 bg-emerald-700/50 rounded animate-pulse w-1/2" />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {displayContent.map((item) => (
                <Card key={item.id} className="bg-emerald-800/50 border-emerald-600 hover:bg-emerald-800/70 transition-colors">
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-white mb-2">{item.title}</h3>
                        <p className="text-emerald-200 mb-3">{item.description}</p>
                      </div>
                      {item.is_premium && (
                        <Badge className="bg-amber-500/20 text-amber-400 ml-4">
                          Premium
                        </Badge>
                      )}
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4 text-sm text-emerald-300">
                        <Badge variant="secondary" className="bg-emerald-700 text-emerald-100">
                          {item.cultural_theme}
                        </Badge>
                        <Badge variant="secondary" className="bg-emerald-700 text-emerald-100">
                          {item.content_type}
                        </Badge>
                        <span className="flex items-center">
                          <Star className="h-4 w-4 mr-1" />
                          Nível {item.difficulty_level}
                        </span>
                      </div>
                      
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-2 text-emerald-300">
                          <span className="text-sm">{item.view_count} visualizações</span>
                          <Button
                            size="sm"
                            variant="ghost"
                            className="text-emerald-300 hover:text-red-400"
                            onClick={() => handleLikeContent(item.id)}
                          >
                            <Heart className="h-4 w-4 mr-1" />
                            {item.like_count}
                          </Button>
                        </div>
                        <Button size="sm" className="bg-amber-500 hover:bg-amber-600 text-emerald-900">
                          <Play className="h-4 w-4 mr-2" />
                          Ler
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Upcoming Events */}
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Calendar className="h-5 w-5 mr-2 text-blue-400" />
                Eventos Culturais
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {displayEvents.map((event) => (
                  <div key={event.id} className="p-3 bg-emerald-700/50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="text-white font-medium text-sm">{event.title}</h4>
                      {event.is_premium && (
                        <Badge className="bg-amber-500/20 text-amber-400 text-xs">
                          Premium
                        </Badge>
                      )}
                    </div>
                    <p className="text-emerald-200 text-xs mb-2">{event.cultural_theme}</p>
                    <div className="flex items-center justify-between text-xs text-emerald-300">
                      <span className="flex items-center">
                        <Users className="h-3 w-3 mr-1" />
                        {event.current_participants}/{event.max_participants}
                      </span>
                      <span className="flex items-center">
                        <Clock className="h-3 w-3 mr-1" />
                        Em breve
                      </span>
                    </div>
                    <Button size="sm" className="w-full mt-2 bg-blue-500 hover:bg-blue-600 text-white">
                      Participar
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Popular Themes */}
          <Card className="bg-emerald-800/50 border-emerald-600">
            <CardHeader>
              <CardTitle className="text-white text-sm">Temas Populares</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {['Medieval', 'Renascimento', 'Moderno', 'Filosófico'].map((theme) => (
                  <Button
                    key={theme}
                    variant="ghost"
                    size="sm"
                    className="w-full justify-start text-emerald-100 hover:bg-emerald-700"
                    onClick={() => setSelectedTheme(theme.toLowerCase())}
                  >
                    <BookOpen className="h-4 w-4 mr-2" />
                    {theme}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* User Progress */}
          {user && (
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white text-sm">Seu Progresso</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-emerald-200 text-sm">Conteúdo lido:</span>
                    <span className="text-white font-bold">12</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-emerald-200 text-sm">Eventos participados:</span>
                    <span className="text-white font-bold">3</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-emerald-200 text-sm">Tema favorito:</span>
                    <span className="text-white font-bold">Medieval</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

