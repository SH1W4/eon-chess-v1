import React, { useState } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import SimpleChessBoard from '../components/SimpleChessBoard';

interface ChessPiece {
  type: 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
  color: 'white' | 'black';
  position: string;
  hasMoved?: boolean;
}

const Home: React.FC = () => {
  const [selectedStyle, setSelectedStyle] = useState<'modern' | 'medieval' | 'renaissance' | 'ancient'>('modern');
  const [gameStatus, setGameStatus] = useState<'playing' | 'check' | 'checkmate' | 'stalemate'>('playing');
  const [selectedPiece, setSelectedPiece] = useState<ChessPiece | null>(null);
  const [moveHistory, setMoveHistory] = useState<string[]>([]);
  const [evaluation, setEvaluation] = useState<number>(0.0);

  const handleMove = (from: string, to: string) => {
    const move = `${from} → ${to}`;
    setMoveHistory(prev => [...prev, move]);
    
    // Simular avaliação da posição
    const randomEval = (Math.random() - 0.5) * 2;
    setEvaluation(parseFloat(randomEval.toFixed(1)));
    
    console.log(`Movimento: ${from} → ${to}`);
  };

  const handlePieceSelect = (piece: ChessPiece) => {
    setSelectedPiece(piece);
    console.log(`Peça selecionada: ${piece.type} ${piece.color} em ${piece.position}`);
  };

  const handleNewGame = () => {
    setMoveHistory([]);
    setEvaluation(0.0);
    setSelectedPiece(null);
    setGameStatus('playing');
    console.log('Nova partida iniciada');
  };

  const handleFlipBoard = () => {
    console.log('Tabuleiro invertido');
  };

  const handleUndoMove = () => {
    if (moveHistory.length > 0) {
      setMoveHistory(prev => prev.slice(0, -1));
      console.log('Movimento desfeito');
    }
  };

  const getStatusText = () => {
    switch (gameStatus) {
      case 'playing':
        return 'Sua vez de jogar';
      case 'check':
        return 'Xeque!';
      case 'checkmate':
        return 'Xeque-mate!';
      case 'stalemate':
        return 'Empate!';
      default:
        return 'Sua vez de jogar';
    }
  };

  return (
    <>
      <Head>
        <title>AEON Chess - Sistema Cultural de Xadrez</title>
        <meta name="description" content="Uma experiência única de xadrez com elementos culturais adaptativos" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700">
        <div className="container mx-auto px-4 py-8">
          <div data-testid="app-container" className="flex flex-col gap-8">
            
            {/* Header */}
            <div data-testid="header" className="mb-8 text-center">
              <h1 data-testid="title" className="text-4xl font-bold text-white mb-2">
                CHESS: Sistema Cultural de Xadrez
              </h1>
              <p data-testid="subtitle" className="text-emerald-100">
                Uma experiência única de xadrez com elementos culturais adaptativos
              </p>
              
              {/* ARKITECT Link */}
              <div className="mt-4">
                <a
                  href="/arkitect"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600/70 hover:bg-emerald-500 text-white font-medium rounded-lg transition-all duration-200 hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
                  style={{backgroundImage: 'url(/images/buttons/modern.png)'}}
                >
                  🧠 ARKITECT Dashboard
                </a>
              </div>
            </div>

            {/* Main Content */}
            <div data-testid="main-content" className="grid lg:grid-cols-3 gap-8">
              
              {/* Board Controls */}
              <div data-testid="board-controls" className="lg:col-span-2 space-y-8">
                
                {/* Controls Panel */}
                <div className="flex flex-col gap-4 p-6 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 shadow-xl">
                  <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">
                      ⚙️
                    </span>
                    Controles
                  </h2>
                  
                  <div className="flex flex-col gap-2">
                    <label className="text-emerald-100 text-sm">Estilo Cultural</label>
                    <select
                      data-testid="style-select"
                      value={selectedStyle}
                      onChange={(e) => setSelectedStyle(e.target.value as any)}
                      className="w-full bg-emerald-700/50 text-white border border-emerald-600/50 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-colors hover:bg-emerald-700/70"
                    >
                      <option value="medieval" data-testid="style-medieval">Medieval</option>
                      <option value="renaissance" data-testid="style-renaissance">Renaissance</option>
                      <option value="modern" data-testid="style-modern">Modern</option>
                      <option value="ancient" data-testid="style-ancient">Ancient</option>
                    </select>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      data-testid="new-game-btn"
                      onClick={handleNewGame}
                      className="bg-emerald-600/70 hover:bg-emerald-500 text-white font-medium rounded-lg px-4 py-3 transition-all duration-200 hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
                      style={{backgroundImage: 'url(/images/buttons/modern.png)'}}
                    >
                      Nova Partida
                    </button>
                    <button
                      data-testid="flip-board-btn"
                      onClick={handleFlipBoard}
                      className="bg-emerald-600/70 hover:bg-emerald-500 text-white font-medium rounded-lg px-4 py-3 transition-all duration-200 hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
                      style={{backgroundImage: 'url(/images/buttons/modern.png)'}}
                    >
                      Inverter Tabuleiro
                    </button>
                    <button
                      data-testid="undo-btn"
                      onClick={handleUndoMove}
                      disabled={moveHistory.length === 0}
                      className={`
                        col-span-2 
                        ${moveHistory.length === 0 
                          ? 'bg-emerald-800/50 cursor-not-allowed opacity-50' 
                          : 'bg-emerald-600/70 hover:bg-emerald-500'
                        }
                        text-white font-medium
                        rounded-lg px-4 py-3
                        transition-all duration-200
                      `}
                    >
                      Desfazer Jogada
                    </button>
                  </div>
                  
                  <div className="mt-2 text-center">
                    <p data-testid="game-status" data-state={gameStatus} className="text-emerald-100">
                      {getStatusText()}
                    </p>
                  </div>
                </div>

                {/* Chess Board */}
                <div data-testid="board-container" className="flex justify-center w-full max-w-[800px] h-[calc(100vh-12rem)] min-h-[280px] mx-auto">
                  <SimpleChessBoard />
                </div>
              </div>

              {/* Side Panel */}
              <div className="space-y-6">
                
                {/* Turn Indicator */}
                <div className="p-4 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50">
                  <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                    <span className="w-6 h-6 flex items-center justify-center rounded bg-emerald-500/20">
                      ⏰
                    </span>
                    Sua vez de jogar
                  </h3>
                  <div className="flex flex-wrap gap-1">
                    {['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'].map((piece, index) => (
                      <div key={index} className="text-2xl text-emerald-300">
                        {piece}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Evaluation */}
                <div className="p-4 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50">
                  <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                    <span className="w-6 h-6 flex items-center justify-center rounded bg-emerald-500/20">
                      📊
                    </span>
                    Avaliação
                  </h3>
                  <p className="text-emerald-100">
                    Posição atual: {evaluation > 0 ? '+' : ''}{evaluation}
                  </p>
                </div>

                {/* Selected Piece Info */}
                {selectedPiece && (
                  <div className="p-4 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50">
                    <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                      <span className="w-6 h-6 flex items-center justify-center rounded bg-emerald-500/20">
                        ♟️
                      </span>
                      Peça Selecionada
                    </h3>
                    <div className="text-emerald-100 space-y-1">
                      <p>Tipo: {selectedPiece.type}</p>
                      <p>Cor: {selectedPiece.color === 'white' ? 'Branca' : 'Preta'}</p>
                      <p>Posição: {selectedPiece.position}</p>
                    </div>
                  </div>
                )}

                {/* Narratives */}
                <div className="p-4 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50">
                  <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                    <span className="w-6 h-6 flex items-center justify-center rounded bg-emerald-500/20">
                      📚
                    </span>
                    Narrativas
                  </h3>
                  <p className="text-emerald-100 text-sm">
                    Sistema cultural adaptativo ativo
                  </p>
                </div>

                {/* Moves */}
                <div className="p-4 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50">
                  <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                    <span className="w-6 h-6 flex items-center justify-center rounded bg-emerald-500/20">
                      ♟️
                    </span>
                    Movimentos
                  </h3>
                  <div className="space-y-1 max-h-32 overflow-y-auto scrollbar-custom">
                    {moveHistory.length === 0 ? (
                      <p className="text-emerald-300 text-sm">Nenhum movimento ainda</p>
                    ) : (
                      moveHistory.map((move, index) => (
                        <div key={index} className="text-emerald-100 text-sm">
                          {Math.floor(index / 2) + 1}. {move}
                        </div>
                      ))
                    )}
                  </div>
                </div>

                {/* Events */}
                <div className="p-4 bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50">
                  <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                    <span className="w-6 h-6 flex items-center justify-center rounded bg-emerald-500/20">
                      👤
                    </span>
                    Eventos
                  </h3>
                  <p className="text-emerald-100">
                    {moveHistory.length + 6} eventos ativos
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
