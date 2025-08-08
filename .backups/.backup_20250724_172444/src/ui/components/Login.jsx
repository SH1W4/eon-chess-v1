import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Crown, Mail, User, Lock, Globe } from 'lucide-react'
import { useUser } from '../contexts/UserContext'
import { useToast } from '@/hooks/use-toast'

export default function Login() {
  const [isLoading, setIsLoading] = useState(false)
  const [loginData, setLoginData] = useState({ username: '', password: '' })
  const [registerData, setRegisterData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
    country: '',
    chessExperience: 'beginner'
  })

  const { createUser, loginUser } = useUser()
  const navigate = useNavigate()
  const { toast } = useToast()

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      // For demo purposes, we'll create a demo user if login fails
      // In a real app, this would authenticate against the backend
      const demoUser = {
        id: 1,
        username: loginData.username || 'demo_user',
        email: 'demo@xadrezmaster.com',
        full_name: 'Usuário Demo',
        chess_experience: 'intermediate'
      }

      await loginUser(demoUser.id)
      
      toast({
        title: "Login realizado com sucesso!",
        description: "Bem-vindo ao XadrezMaster",
      })
      
      navigate('/')
    } catch (error) {
      toast({
        title: "Erro no login",
        description: error.message,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    
    if (registerData.password !== registerData.confirmPassword) {
      toast({
        title: "Erro no cadastro",
        description: "As senhas não coincidem",
        variant: "destructive",
      })
      return
    }

    setIsLoading(true)

    try {
      const userData = {
        username: registerData.username,
        email: registerData.email,
        full_name: registerData.fullName,
        country: registerData.country,
        chess_experience: registerData.chessExperience
      }

      await createUser(userData)
      
      toast({
        title: "Conta criada com sucesso!",
        description: "Bem-vindo ao XadrezMaster",
      })
      
      navigate('/')
    } catch (error) {
      toast({
        title: "Erro no cadastro",
        description: error.message,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleDemoLogin = async () => {
    setIsLoading(true)
    try {
      // Create a demo user for testing
      const demoUser = {
        username: 'demo_user',
        email: 'demo@xadrezmaster.com',
        full_name: 'Usuário Demo',
        country: 'Brasil',
        chess_experience: 'intermediate'
      }

      await createUser(demoUser)
      
      toast({
        title: "Conta demo criada!",
        description: "Explore todas as funcionalidades do XadrezMaster",
      })
      
      navigate('/')
    } catch (error) {
      // If demo user already exists, just login
      try {
        await loginUser(1) // Assume demo user has ID 1
        navigate('/')
      } catch (loginError) {
        toast({
          title: "Erro",
          description: "Não foi possível criar conta demo",
          variant: "destructive",
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Crown className="h-12 w-12 text-amber-400 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-white">XadrezMaster</h1>
          <p className="text-emerald-100 mt-2">Entre na sua conta ou crie uma nova</p>
        </div>

        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="login">Entrar</TabsTrigger>
            <TabsTrigger value="register">Cadastrar</TabsTrigger>
          </TabsList>

          <TabsContent value="login">
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white">Entrar na sua conta</CardTitle>
                <CardDescription className="text-emerald-200">
                  Digite suas credenciais para acessar o XadrezMaster
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleLogin} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="username" className="text-emerald-100">
                      Usuário
                    </Label>
                    <div className="relative">
                      <User className="absolute left-3 top-3 h-4 w-4 text-emerald-400" />
                      <Input
                        id="username"
                        type="text"
                        placeholder="Seu nome de usuário"
                        value={loginData.username}
                        onChange={(e) => setLoginData({...loginData, username: e.target.value})}
                        className="pl-10 bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                        required
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="password" className="text-emerald-100">
                      Senha
                    </Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-emerald-400" />
                      <Input
                        id="password"
                        type="password"
                        placeholder="Sua senha"
                        value={loginData.password}
                        onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                        className="pl-10 bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                        required
                      />
                    </div>
                  </div>

                  <Button 
                    type="submit" 
                    className="w-full bg-amber-500 hover:bg-amber-600 text-emerald-900"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Entrando...' : 'Entrar'}
                  </Button>
                </form>

                <div className="mt-4">
                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <span className="w-full border-t border-emerald-600" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                      <span className="bg-emerald-800 px-2 text-emerald-300">Ou</span>
                    </div>
                  </div>

                  <Button 
                    type="button"
                    variant="outline"
                    className="w-full mt-4 border-emerald-600 text-emerald-100 hover:bg-emerald-700"
                    onClick={handleDemoLogin}
                    disabled={isLoading}
                  >
                    Entrar como Demo
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="register">
            <Card className="bg-emerald-800/50 border-emerald-600">
              <CardHeader>
                <CardTitle className="text-white">Criar nova conta</CardTitle>
                <CardDescription className="text-emerald-200">
                  Junte-se à comunidade XadrezMaster
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleRegister} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="fullName" className="text-emerald-100">
                        Nome Completo
                      </Label>
                      <Input
                        id="fullName"
                        type="text"
                        placeholder="Seu nome"
                        value={registerData.fullName}
                        onChange={(e) => setRegisterData({...registerData, fullName: e.target.value})}
                        className="bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="username" className="text-emerald-100">
                        Usuário
                      </Label>
                      <Input
                        id="username"
                        type="text"
                        placeholder="Nome de usuário"
                        value={registerData.username}
                        onChange={(e) => setRegisterData({...registerData, username: e.target.value})}
                        className="bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                        required
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email" className="text-emerald-100">
                      Email
                    </Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-4 w-4 text-emerald-400" />
                      <Input
                        id="email"
                        type="email"
                        placeholder="seu@email.com"
                        value={registerData.email}
                        onChange={(e) => setRegisterData({...registerData, email: e.target.value})}
                        className="pl-10 bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                        required
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="country" className="text-emerald-100">
                        País
                      </Label>
                      <div className="relative">
                        <Globe className="absolute left-3 top-3 h-4 w-4 text-emerald-400" />
                        <Input
                          id="country"
                          type="text"
                          placeholder="Brasil"
                          value={registerData.country}
                          onChange={(e) => setRegisterData({...registerData, country: e.target.value})}
                          className="pl-10 bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="experience" className="text-emerald-100">
                        Experiência
                      </Label>
                      <Select 
                        value={registerData.chessExperience}
                        onValueChange={(value) => setRegisterData({...registerData, chessExperience: value})}
                      >
                        <SelectTrigger className="bg-emerald-700/50 border-emerald-600 text-white">
                          <SelectValue placeholder="Nível" />
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

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="password" className="text-emerald-100">
                        Senha
                      </Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-emerald-400" />
                        <Input
                          id="password"
                          type="password"
                          placeholder="Senha"
                          value={registerData.password}
                          onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                          className="pl-10 bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                          required
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword" className="text-emerald-100">
                        Confirmar Senha
                      </Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-emerald-400" />
                        <Input
                          id="confirmPassword"
                          type="password"
                          placeholder="Confirmar"
                          value={registerData.confirmPassword}
                          onChange={(e) => setRegisterData({...registerData, confirmPassword: e.target.value})}
                          className="pl-10 bg-emerald-700/50 border-emerald-600 text-white placeholder:text-emerald-300"
                          required
                        />
                      </div>
                    </div>
                  </div>

                  <Button 
                    type="submit" 
                    className="w-full bg-amber-500 hover:bg-amber-600 text-emerald-900"
                    disabled={isLoading}
                  >
                    {isLoading ? 'Criando conta...' : 'Criar Conta'}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

