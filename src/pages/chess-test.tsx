import React, { useState, useCallback } from 'react';
import Head from 'next/head';
import ARKITECTChessBoard from '../components/ARKITECTChessBoard';

export default function ChessTestPage() {
  const [debugInfo, setDebugInfo] = useState<string[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);
  const [arkitectEnabled, setArkitectEnabled] = useState(false);

  const addDebugInfo = useCallback((info: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setDebugInfo(prev => [...prev, `[${timestamp}] ${info}`]);
  }, []);

  const toggleARKITECT = useCallback(() => {
    setArkitectEnabled(prev => !prev);
    addDebugInfo(`ARKITECT ${!arkitectEnabled ? 'habilitado' : 'desabilitado'}`);
  }, [arkitectEnabled, addDebugInfo]);

  const clearLogs = useCallback(() => {
    setDebugInfo([]);
    addDebugInfo('Logs limpos');
  }, [addDebugInfo]);

  const testClick = useCallback(() => {
    addDebugInfo('Teste de clique executado');
    // Simular clique programático
    const testSquare = document.querySelector('[data-position="e2"]') as HTMLElement;
    if (testSquare) {
      testSquare.click();
      addDebugInfo('Clique simulado em e2');
    }
  }, [addDebugInfo]);

  const checkState = useCallback(() => {
    addDebugInfo('Verificando estado do tabuleiro...');
    const board = document.querySelector('.chess-board');
    if (board) {
      addDebugInfo('Tabuleiro encontrado no DOM');
    } else {
      addDebugInfo('Tabuleiro não encontrado no DOM');
    }
  }, [addDebugInfo]);

  return (
    <>
      <Head>
        <title>AEON CHESS - Tabuleiro Inteligente</title>
        <meta name="description" content="Sistema de Xadrez Inteligente com ARKITECT" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white">
        {/* Header */}
        <header className="bg-black/20 backdrop-blur-sm border-b border-white/10">
          <div className="container mx-auto px-6 py-4">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              🧠 AEON CHESS - Sistema Inteligente
            </h1>
            <p className="text-gray-300 mt-2">
              Tabuleiro com análise inteligente em tempo real e conselhos estratégicos
            </p>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-6 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Left Panel - Chess Board */}
            <div className="lg:col-span-2">
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-6">
                <div className="text-center mb-6">
                  <h2 className="text-2xl font-semibold text-blue-300 mb-2">
                    🎯 Tabuleiro ARKITECT
                  </h2>
                  <p className="text-gray-400">
                    Interface inteligente para análise e avaliação
                  </p>
                </div>

                {/* ARKITECT Status */}
                <div className="flex items-center justify-center mb-6">
                  <div className={`flex items-center space-x-3 px-4 py-2 rounded-full ${
                    arkitectEnabled 
                      ? 'bg-green-500/20 border border-green-400/50' 
                      : 'bg-red-500/20 border border-red-400/50'
                  }`}>
                    <div className={`w-3 h-3 rounded-full ${
                      arkitectEnabled ? 'bg-green-400 animate-pulse' : 'bg-red-400'
                    }`}></div>
                    <span className="text-sm font-medium">
                      ARKITECT: {arkitectEnabled ? 'ATIVO' : 'INATIVO'}
                    </span>
                  </div>
                </div>

                {/* Chess Board */}
                <div className="flex justify-center mb-6">
                  <div className="bg-gradient-to-br from-amber-100 to-amber-200 p-4 rounded-xl shadow-2xl">
                    <ARKITECTChessBoard 
                      onDebug={addDebugInfo}
                      enableARKITECT={arkitectEnabled}
                    />
                  </div>
                </div>

                {/* Control Buttons */}
                <div className="flex flex-wrap justify-center gap-4">
                  <button
                    onClick={toggleARKITECT}
                    className={`px-6 py-3 rounded-lg font-semibold transition-all duration-200 ${
                      arkitectEnabled
                        ? 'bg-red-600 hover:bg-red-700 text-white'
                        : 'bg-green-600 hover:bg-green-700 text-white'
                    }`}
                  >
                    {arkitectEnabled ? '🔴 Desabilitar' : '🟢 Habilitar'} ARKITECT
                  </button>
                  
                  <button
                    onClick={() => addDebugInfo('Nova partida iniciada')}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-all duration-200"
                  >
                    🆕 Nova Partida
                  </button>
                  
                  <button
                    onClick={() => addDebugInfo('Análise ARKITECT executada')}
                    className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold transition-all duration-200"
                  >
                    🧠 Analisar ARKITECT
                  </button>
                </div>
              </div>
            </div>

            {/* Right Panel - Debug Info */}
            <div className="lg:col-span-1">
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 p-6 h-fit">
                <h2 className="text-xl font-semibold text-purple-300 mb-6 flex items-center">
                  🔧 Painel de Controle
                </h2>

                {/* ARKITECT Controls */}
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-gray-300 mb-3 flex items-center">
                    🧠 Controles ARKITECT
                  </h3>
                  <div className="space-y-2">
                    <button
                      onClick={toggleARKITECT}
                      className={`w-full px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                        arkitectEnabled
                          ? 'bg-red-600/20 border border-red-400/50 text-red-300'
                          : 'bg-green-600/20 border border-green-400/50 text-green-300'
                      }`}
                    >
                      {arkitectEnabled ? 'Desabilitar' : 'Habilitar'} ARKITECT
                    </button>
                    <button
                      onClick={() => addDebugInfo('Status verificado')}
                      className="w-full px-4 py-2 bg-blue-600/20 border border-blue-400/50 text-blue-300 rounded-lg text-sm font-medium transition-all duration-200"
                    >
                      Status
                    </button>
                  </div>
                </div>

                {/* Test Controls */}
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-gray-300 mb-3 flex items-center">
                    🧪 Testes
                  </h3>
                  <div className="space-y-2">
                    <button
                      onClick={testClick}
                      className="w-full px-4 py-2 bg-purple-600/20 border border-purple-400/50 text-purple-300 rounded-lg text-sm font-medium transition-all duration-200"
                    >
                      Teste Clique
                    </button>
                    <button
                      onClick={checkState}
                      className="w-full px-4 py-2 bg-cyan-600/20 border border-cyan-400/50 text-cyan-300 rounded-lg text-sm font-medium transition-all duration-200"
                    >
                      Verificar Estado
                    </button>
                  </div>
                </div>

                {/* Simple Board Test */}
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-gray-300 mb-3 flex items-center">
                    🎯 Teste Simples
                  </h3>
                  <div className="grid grid-cols-4 gap-1 bg-gray-800 p-2 rounded-lg">
                    {Array.from({ length: 16 }, (_, i) => (
                      <div
                        key={i}
                        className={`w-8 h-8 flex items-center justify-center text-xs font-bold rounded ${
                          i % 2 === 0 ? 'bg-amber-200 text-amber-800' : 'bg-amber-800 text-amber-200'
                        }`}
                      >
                        {i}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Log Area */}
                <div className="mb-4">
                  <h3 className="text-sm font-medium text-gray-300 mb-3 flex items-center">
                    📋 Logs em Tempo Real
                  </h3>
                  <div className="bg-black/30 rounded-lg p-3 h-48 overflow-y-auto border border-white/10">
                    <div className="space-y-1 text-xs font-mono">
                      {debugInfo.map((log, index) => (
                        <div key={index} className="text-green-400">
                          {log}
                        </div>
                      ))}
                      {debugInfo.length === 0 && (
                        <div className="text-gray-500 italic">
                          Aguardando logs...
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Clear Logs Button */}
                <button
                  onClick={clearLogs}
                  className="w-full px-4 py-2 bg-red-600/20 border border-red-400/50 text-red-300 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-red-600/30"
                >
                  🗑️ Limpar Logs
                </button>
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-black/20 backdrop-blur-sm border-t border-white/10 mt-12">
          <div className="container mx-auto px-6 py-4">
            <div className="text-center text-gray-400 text-sm">
              <p>AEON CHESS v1.0.1 - Sistema de Xadrez Inteligente com ARKITECT</p>
              <p className="mt-1">Desenvolvido para avaliação e análise de performance</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
