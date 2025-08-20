import Head from 'next/head'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Head>
        <title>AEON CHESS - Sistema de Xadrez Inteligente</title>
        <meta name="description" content="AEON CHESS - Sistema de Xadrez Inteligente com ARKITECT" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-900 text-white">
        {/* Header */}
        <header className="bg-black/20 backdrop-blur-sm border-b border-white/10">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">♔</div>
                <div>
                  <h1 className="text-xl font-bold">AEON CHESS</h1>
                  <div className="text-xs bg-yellow-500 text-black px-2 py-1 rounded font-bold">PRO</div>
                </div>
              </div>
              
              <nav className="hidden md:flex items-center space-x-8">
                <a href="#recursos" className="text-gray-300 hover:text-white transition-colors">Recursos</a>
                <a href="#analise" className="text-gray-300 hover:text-white transition-colors">Análise IA</a>
                <a href="#torneios" className="text-gray-300 hover:text-white transition-colors">Torneios</a>
                <a href="#planos" className="text-gray-300 hover:text-white transition-colors">Planos</a>
              </nav>
              
              <Link 
                href="/chess-test"
                className="bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-2 px-6 rounded-lg transition-colors duration-200 flex items-center space-x-2"
              >
                <span>▶</span>
                <span>Jogar Agora</span>
              </Link>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-6 py-12">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            
            {/* Left Section - Marketing */}
            <div className="space-y-8">
              {/* Active Players Banner */}
              <div className="inline-flex items-center space-x-2 bg-yellow-500/20 border border-yellow-400/50 text-yellow-300 px-4 py-2 rounded-full text-sm">
                <span>👑</span>
                <span>Mais de 50,000 jogadores ativos</span>
              </div>

              {/* Main Title */}
              <div className="space-y-2">
                <h2 className="text-5xl font-bold">
                  <span className="text-white">Domine o</span>
                  <br />
                  <span className="text-blue-400">Xadrez</span>
                </h2>
                <h3 className="text-2xl">
                  <span className="text-white">com IA</span>
                  <span className="text-blue-400"> Avançada</span>
                </h3>
              </div>

              {/* Description */}
              <p className="text-gray-300 text-lg leading-relaxed">
                Análise profunda de partidas, treinamento personalizado e adversários de IA que se adaptam ao seu nível. 
                Evolua do iniciante ao mestre com tecnologia de ponta.
              </p>

              {/* Call to Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4">
                <Link 
                  href="/chess-test"
                  className="bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-4 px-8 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2 text-lg"
                >
                  <span>♔</span>
                  <span>Jogar Agora</span>
                </Link>
                
                <Link 
                  href="/revolution"
                  className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-4 px-8 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2 text-lg"
                >
                  <span>▶</span>
                  <span>Ver Demo</span>
                </Link>
              </div>

              {/* AI Configuration */}
              <div className="bg-gray-800/50 rounded-lg p-4 space-y-3">
                <h4 className="font-semibold text-gray-200">Configuração da IA</h4>
                <div className="flex items-center space-x-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">Nível da IA</label>
                    <select className="bg-gray-700 text-white px-3 py-2 rounded border border-gray-600">
                      <option>Clube</option>
                      <option>Nacional</option>
                      <option>Internacional</option>
                      <option>Mestre</option>
                    </select>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input type="checkbox" id="strong-ai" className="rounded" />
                    <label htmlFor="strong-ai" className="text-sm text-gray-300">IA Forte (Stockfish)</label>
                  </div>
                </div>
              </div>

              {/* Statistics */}
              <div className="grid grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-400">2800+</div>
                  <div className="text-sm text-gray-400">ELO da IA</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">100K+</div>
                  <div className="text-sm text-gray-400">Partidas/dia</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">99.9%</div>
                  <div className="text-sm text-gray-400">Precisão</div>
                </div>
              </div>
            </div>

            {/* Right Section - Chess Board Preview */}
            <div className="flex justify-center">
              <div className="bg-gradient-to-br from-amber-50 to-amber-100 p-6 rounded-lg shadow-2xl border border-amber-200">
                <div className="grid grid-cols-8 gap-0 border-2 border-amber-900 rounded overflow-hidden">
                  {Array.from({ length: 64 }, (_, i) => {
                    const row = Math.floor(i / 8);
                    const col = i % 8;
                    const isLight = (row + col) % 2 === 0;
                    
                    // Setup initial pieces
                    let piece = null;
                    if (row === 7) {
                      const pieces = ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'];
                      piece = pieces[col];
                    } else if (row === 6) {
                      piece = '♙';
                    } else if (row === 1) {
                      piece = '♟';
                    } else if (row === 0) {
                      const pieces = ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'];
                      piece = pieces[col];
                    }
                    
                    return (
                      <div
                        key={i}
                        className={`w-12 h-12 flex items-center justify-center text-lg font-bold ${
                          isLight ? 'bg-amber-100 text-amber-800' : 'bg-amber-800 text-amber-100'
                        }`}
                      >
                        {piece}
                      </div>
                    );
                  })}
                </div>
                
                {/* Board Controls */}
                <div className="flex justify-center space-x-4 mt-4">
                  <button className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm transition-colors duration-200 flex items-center space-x-1">
                    <span>↶</span>
                    <span>Desfazer</span>
                  </button>
                  <button className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm transition-colors duration-200 flex items-center space-x-1">
                    <span>↻</span>
                    <span>Reset</span>
                  </button>
                </div>
                
                {/* Evaluation Bar */}
                <div className="mt-4 flex items-center space-x-3">
                  <div className="text-sm text-gray-600 font-medium">Avaliação</div>
                  <div className="flex-1 bg-gray-300 rounded-full h-2">
                    <div className="bg-white h-2 rounded-full w-1/2"></div>
                  </div>
                </div>
                
                {/* Player Selector */}
                <div className="mt-4">
                  <select className="w-full bg-gray-700 text-white px-3 py-2 rounded text-sm border border-gray-600">
                    <option>Brancas / Pretas</option>
                    <option>Apenas Brancas</option>
                    <option>Apenas Pretas</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-black/20 backdrop-blur-sm border-t border-white/10 mt-16">
          <div className="container mx-auto px-6 py-8">
            <div className="text-center text-gray-400">
              <p className="text-lg font-semibold mb-2">AEON CHESS v1.0.1</p>
              <p className="text-sm">Sistema de Xadrez Inteligente com ARKITECT</p>
              <p className="text-xs mt-2">Desenvolvido para avaliação e análise de performance</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}
