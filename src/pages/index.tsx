import React, { useState, useCallback } from 'react';
import { MemoizedChessBoard } from '../web/components/board/ChessBoard';
import { ChessPosition, ChessMove } from '../shared/types/chess';
import { CulturalChessEngine } from '../shared/engine/CulturalChessEngine';
import { CULTURAL_STYLES } from '../shared/constants/game';

const engine = new CulturalChessEngine();

export default function Home() {
  const [orientation, setOrientation] = useState<'white' | 'black'>('white');
  const [culturalStyle, setCulturalStyle] = useState('modern');
  const [narratives, setNarratives] = useState<string[]>([]);

  const handleMove = useCallback((from: ChessPosition, to: ChessPosition) => {
    const success = engine.makeMove(from, to);
    if (success) {
      const analysis = engine.getStyleBasedEvaluation();
      const newNarratives = engine.getCulturalNarrative();
      setNarratives(newNarratives);
    }
  }, []);

  const handleGameEnd = useCallback((result: string) => {
    alert(`Jogo finalizado! Resultado: ${result}`);
  }, []);

  const handleStyleChange = useCallback((style: string) => {
    if (style in CULTURAL_STYLES) {
      setCulturalStyle(style);
      engine.setCulturalStyle(style);
    }
  }, []);

  const handleFlipBoard = useCallback(() => {
    setOrientation(prev => prev === 'white' ? 'black' : 'white');
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Cabeçalho */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-white mb-2">
            CHESS: Sistema Cultural de Xadrez
          </h1>
          <p className="text-emerald-100">
            Uma experiência única de xadrez com elementos culturais adaptativos
          </p>
        </div>

        {/* Controles */}
        <div className="mb-8 flex justify-center space-x-4">
          <select
            value={culturalStyle}
            onChange={(e) => handleStyleChange(e.target.value)}
            className="bg-emerald-800 text-white border border-emerald-600 rounded px-4 py-2"
          >
            {Object.entries(CULTURAL_STYLES).map(([key, value]) => (
              <option key={key} value={value}>
                Estilo {value}
              </option>
            ))}
          </select>

          <button
            onClick={handleFlipBoard}
            className="bg-emerald-800 text-white border border-emerald-600 rounded px-4 py-2 hover:bg-emerald-700"
          >
            Inverter Tabuleiro
          </button>
        </div>

        {/* Área principal */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Tabuleiro */}
          <div className="lg:col-span-2 flex justify-center">
            <MemoizedChessBoard
              orientation={orientation}
              culturalStyle={culturalStyle}
              showCoordinates={true}
              onMove={handleMove}
              onGameEnd={handleGameEnd}
            />
          </div>

          {/* Painel lateral */}
          <div className="space-y-4">
            {/* Narrativas culturais */}
            <div className="bg-emerald-800/50 border border-emerald-600 rounded-lg p-4">
              <h2 className="text-xl font-bold text-white mb-4">
                Narrativas Culturais
              </h2>
              <div className="space-y-2">
                {narratives.map((narrative, index) => (
                  <p key={index} className="text-emerald-100">
                    {narrative}
                  </p>
                ))}
              </div>
            </div>

            {/* Avaliação */}
            <div className="bg-emerald-800/50 border border-emerald-600 rounded-lg p-4">
              <h2 className="text-xl font-bold text-white mb-4">
                Análise da Posição
              </h2>
              <div className="space-y-2">
                {engine.getStyleBasedEvaluation().explanation.split('\n').map((line, index) => (
                  <p key={index} className="text-emerald-100">
                    {line}
                  </p>
                ))}
              </div>
            </div>

            {/* Histórico de eventos */}
            <div className="bg-emerald-800/50 border border-emerald-600 rounded-lg p-4">
              <h2 className="text-xl font-bold text-white mb-4">
                Eventos Culturais
              </h2>
              <div className="space-y-2">
                {engine.getCulturalEventHistory().map((event, index) => (
                  <div key={index} className="text-emerald-100">
                    <span className="text-emerald-400">
                      {new Date(event.timestamp).toLocaleTimeString()}:
                    </span>{' '}
                    {event.description}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
