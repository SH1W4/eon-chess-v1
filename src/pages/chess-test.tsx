import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import UltraChessBoard from '../components/UltraChessBoard';

const ChessTestPage: React.FC = () => {
  const [debugInfo, setDebugInfo] = useState<string[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
    setDebugInfo(prev => [...prev, 'Página carregada']);
  }, []);

  const addDebugInfo = (info: string) => {
    console.log(info);
    setDebugInfo(prev => [...prev, `${new Date().toLocaleTimeString()}: ${info}`]);
  };

  return (
    <>
      <Head>
        <title>Teste - Tabuleiro Funcional</title>
        <meta name="description" content="Teste direto do tabuleiro de xadrez funcional" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700 p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            🧪 Teste Direto - Tabuleiro Funcional
          </h1>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Tabuleiro */}
            <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6">
              <h2 className="text-2xl font-bold text-white mb-4">
                ♟️ UltraChessBoard - Teste Direto
              </h2>
              <p className="text-emerald-100 mb-4">
                Esta é uma página de teste direta para verificar se o tabuleiro funcional está funcionando.
              </p>
              
              <div className="flex justify-center items-center h-[500px] bg-emerald-800/20 rounded-xl border border-emerald-600/30 p-4">
                {isLoaded && <UltraChessBoard onDebug={addDebugInfo} />}
              </div>
            </div>

            {/* Debug Info */}
            <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6">
              <h3 className="text-xl font-bold text-white mb-4">
                🐛 Debug Info
              </h3>
              
              {/* Teste de clique simples */}
              <div className="mb-4 p-4 bg-blue-900/30 rounded-lg">
                <h4 className="text-lg font-semibold text-white mb-2">🧪 Teste de Clique</h4>
                <button
                  onClick={() => addDebugInfo('Teste de clique funcionando!')}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg mr-2"
                >
                  Teste Clique
                </button>
                <button
                  onClick={() => addDebugInfo(`Estado atual: ${new Date().toISOString()}`)}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
                >
                  Estado
                </button>
              </div>
              
              {/* Teste de tabuleiro simples */}
              <div className="mb-4 p-4 bg-purple-900/30 rounded-lg">
                <h4 className="text-lg font-semibold text-white mb-2">♟️ Teste de Tabuleiro Simples</h4>
                <div 
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(4, 1fr)',
                    gap: '2px',
                    width: '200px',
                    height: '200px',
                    backgroundColor: '#000',
                    padding: '2px'
                  }}
                >
                  {Array.from({ length: 16 }, (_, i) => (
                    <div
                      key={i}
                      style={{
                        backgroundColor: i % 2 === 0 ? '#fff' : '#000',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        fontSize: '12px',
                        color: i % 2 === 0 ? '#000' : '#fff'
                      }}
                      onClick={() => addDebugInfo(`Casa ${i} clicada!`)}
                    >
                      {i}
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="bg-black/50 rounded-lg p-4 h-[200px] overflow-y-auto">
                {debugInfo.map((info, index) => (
                  <div key={index} className="text-green-400 text-sm font-mono mb-1">
                    {info}
                  </div>
                ))}
                {debugInfo.length === 0 && (
                  <div className="text-gray-400 text-sm">
                    Aguardando eventos...
                  </div>
                )}
              </div>
              <button
                onClick={() => setDebugInfo([])}
                className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg"
              >
                Limpar Logs
              </button>
            </div>
          </div>

          <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6 mt-8">
            <h3 className="text-xl font-bold text-white mb-4">
              📋 Instruções de Teste
            </h3>
            <ul className="text-emerald-100 space-y-2">
              <li>✅ Clique em uma peça branca (brancas começam)</li>
              <li>✅ A peça deve ficar destacada em azul</li>
              <li>✅ Clique em qualquer casa para mover a peça</li>
              <li>✅ O turno deve alternar para as pretas</li>
              <li>✅ Teste capturar peças adversárias</li>
              <li>✅ Use o botão "🔄 Nova Partida" para resetar</li>
              <li>🐛 Verifique os logs de debug ao lado</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChessTestPage;
