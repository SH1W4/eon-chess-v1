import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import ARKITECTChessBoard from '../components/ARKITECTChessBoard';

const ChessTestPage: React.FC = () => {
  const [debugInfo, setDebugInfo] = useState<string[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);
  const [arkitectEnabled, setArkitectEnabled] = useState(true);

  useEffect(() => {
    setIsLoaded(true);
    setDebugInfo(prev => [...prev, '🧠 Página ARKITECT carregada']);
  }, []);

  const addDebugInfo = (info: string) => {
    console.log(info);
    setDebugInfo(prev => [...prev, `${new Date().toLocaleTimeString()}: ${info}`]);
  };

  const toggleARKITECT = () => {
    setArkitectEnabled(prev => !prev);
    addDebugInfo(`🧠 ARKITECT ${!arkitectEnabled ? 'habilitado' : 'desabilitado'} via controle externo`);
  };

  return (
    <>
      <Head>
        <title>Teste ARKITECT - Tabuleiro Inteligente</title>
        <meta name="description" content="Teste do tabuleiro de xadrez com ARKITECT integrado" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700 p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            🧠 Teste ARKITECT - Tabuleiro Inteligente
          </h1>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Tabuleiro ARKITECT */}
            <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6">
              <h2 className="text-2xl font-bold text-white mb-4">
                🧠 ARKITECT ChessBoard - Sistema Inteligente
              </h2>
              <p className="text-emerald-100 mb-4">
                Tabuleiro com análise inteligente em tempo real, conselhos estratégicos e monitoramento de performance.
              </p>
              
              <div className="flex justify-center items-center h-[500px] bg-emerald-800/20 rounded-xl border border-emerald-600/30 p-4">
                {isLoaded && <ARKITECTChessBoard onDebug={addDebugInfo} enableARKITECT={arkitectEnabled} />}
              </div>
            </div>

            {/* Debug Info */}
            <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6">
              <h3 className="text-xl font-bold text-white mb-4">
                🐛 Debug Info - ARKITECT
              </h3>
              
              {/* Controles ARKITECT */}
              <div className="mb-4 p-4 bg-blue-900/30 rounded-lg">
                <h4 className="text-lg font-semibold text-white mb-2">🧠 Controles ARKITECT</h4>
                <button
                  onClick={toggleARKITECT}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg mr-2"
                >
                  {arkitectEnabled ? 'Desabilitar' : 'Habilitar'} ARKITECT
                </button>
                <button
                  onClick={() => addDebugInfo(`Status ARKITECT: ${arkitectEnabled ? 'ATIVO' : 'INATIVO'}`)}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
                >
                  Status
                </button>
              </div>
              
              {/* Teste de clique simples */}
              <div className="mb-4 p-4 bg-purple-900/30 rounded-lg">
                <h4 className="text-lg font-semibold text-white mb-2">🧪 Teste de Clique</h4>
                <button
                  onClick={() => addDebugInfo('Teste de clique funcionando!')}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg mr-2"
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
              <div className="mb-4 p-4 bg-orange-900/30 rounded-lg">
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
                    Aguardando eventos ARKITECT...
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
              📋 Instruções de Teste - ARKITECT
            </h3>
            <ul className="text-emerald-100 space-y-2">
              <li>✅ Clique em uma peça branca (brancas começam)</li>
              <li>✅ A peça deve ficar destacada em azul</li>
              <li>✅ Clique em qualquer casa para mover a peça</li>
              <li>✅ O turno deve alternar para as pretas</li>
              <li>✅ Teste capturar peças adversárias</li>
              <li>✅ Use o botão "🔄 Nova Partida" para resetar</li>
              <li>🧠 Verifique a análise ARKITECT em tempo real</li>
              <li>🧠 Teste habilitar/desabilitar o ARKITECT</li>
              <li>🧠 Use "🧠 Analisar ARKITECT" para análise manual</li>
              <li>🐛 Verifique os logs de debug ao lado</li>
            </ul>
          </div>

          <div className="bg-blue-900/30 backdrop-blur-sm rounded-xl border border-blue-600/50 p-6 mt-8">
            <h3 className="text-xl font-bold text-white mb-4">
              🧠 Funcionalidades ARKITECT
            </h3>
            <ul className="text-blue-100 space-y-2">
              <li>🔬 <strong>Análise Automática:</strong> Avaliação de posição em tempo real</li>
              <li>🎯 <strong>Conselhos Estratégicos:</strong> Sugestões baseadas na posição atual</li>
              <li>⚡ <strong>Monitoramento de Performance:</strong> Tempo de resposta e eficiência</li>
              <li>📊 <strong>Métricas de Qualidade:</strong> Avaliação de movimentos</li>
              <li>🔍 <strong>Detecção de Oportunidades:</strong> Identificação de vantagens táticas</li>
              <li>🔄 <strong>Análise Pós-Movimento:</strong> Avaliação após cada jogada</li>
              <li>🎮 <strong>Controle Manual:</strong> Habilitação/desabilitação do sistema</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChessTestPage;
