import React from 'react';
import Head from 'next/head';
import SimpleChessBoard from '../components/SimpleChessBoard';

const TestChessPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Teste - Tabuleiro Funcional</title>
        <meta name="description" content="Teste do tabuleiro de xadrez funcional" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            🧪 Teste do Tabuleiro Funcional
          </h1>
          
          <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6 mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">
              ♟️ Tabuleiro de Xadrez Funcional
            </h2>
            <p className="text-emerald-100 mb-4">
              Clique em uma peça para selecioná-la, depois clique em uma casa para movê-la.
            </p>
            
            <div className="flex justify-center">
              <SimpleChessBoard />
            </div>
          </div>

          <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6">
            <h3 className="text-xl font-bold text-white mb-4">
              📋 Instruções de Teste
            </h3>
            <ul className="text-emerald-100 space-y-2">
              <li>✅ Clique em uma peça branca (brancas começam)</li>
              <li>✅ A peça deve ficar destacada em azul</li>
              <li>✅ Clique em qualquer casa para mover a peça</li>
              <li>✅ O turno deve alternar para as pretas</li>
              <li>✅ Teste capturar peças adversárias</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
};

export default TestChessPage;
