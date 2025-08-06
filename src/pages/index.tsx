import React, { useState, useCallback } from 'react';
import { MemoizedChessBoard } from '../web/components/board/ChessBoard';
import { MemoizedGameControls } from '../web/components/controls/GameControls';
import { MemoizedGameInfo } from '../web/components/info/GameInfo';
import { ChessPosition, ChessMove } from '../shared/types/chess';
import { CulturalChessEngine } from '../shared/engine/CulturalChessEngine';
import { CULTURAL_STYLES } from '../shared/constants/game';

const [engine] = useState(() => new CulturalChessEngine());
const [gameHistory, setGameHistory] = useState<ChessMove[]>([]);
const [canUndo, setCanUndo] = useState(false);

export default function Home() {
  const [orientation, setOrientation] = useState<'white' | 'black'>('white');
  const [culturalStyle, setCulturalStyle] = useState('modern');
  const [narratives, setNarratives] = useState<string[]>([]);
  const [evaluation, setEvaluation] = useState(0);
  const [events, setEvents] = useState<Array<{
    type: string;
    description: string;
    timestamp: number;
  }>>([]);

const handleMove = useCallback((from: ChessPosition, to: ChessPosition) => {
    const success = engine.makeMove(from, to);
    if (success) {
      const analysis = engine.getStyleBasedEvaluation();
      const newNarratives = engine.getCulturalNarrative();
      const newEvents = engine.getCulturalEventHistory();
      
      setNarratives(newNarratives);
      setEvaluation(analysis.evaluation);
      setEvents(newEvents);
      setGameHistory(prev => [...prev, { from, to, piece: engine.getPieceAt(to)! }]);
      setCanUndo(true);
    }
  }, []);

  const handleGameEnd = useCallback((result: string) => {
    alert(`Jogo finalizado! Resultado: ${result}`);
  }, []);

const handleStyleChange = useCallback((style: string) => {
    if (style in CULTURAL_STYLES) {
      setCulturalStyle(style);
      engine.setCulturalStyle(style);
      const analysis = engine.getStyleBasedEvaluation();
      setEvaluation(analysis.evaluation);
    }
  }, []);

  const handleNewGame = useCallback(() => {
    engine.reset();
    setGameHistory([]);
    setNarratives([]);
    setEvents([]);
    setEvaluation(0);
    setCanUndo(false);
  }, []);

  const handleUndo = useCallback(() => {
    if (canUndo) {
      engine.undoLastMove();
      setGameHistory(prev => prev.slice(0, -1));
      setCanUndo(gameHistory.length > 1);
      
      const analysis = engine.getStyleBasedEvaluation();
      const newNarratives = engine.getCulturalNarrative();
      const newEvents = engine.getCulturalEventHistory();
      
      setEvaluation(analysis.evaluation);
      setNarratives(newNarratives);
      setEvents(newEvents);
    }
  }, [canUndo, gameHistory.length]);

  const handleFlipBoard = useCallback(() => {
    setOrientation(prev => prev === 'white' ? 'black' : 'white');
  }, []);

return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700 py-8">
      <div className="max-w-7xl mx-auto px-4 flex flex-col gap-8">
        {/* Cabeçalho */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-white mb-2">
            CHESS: Sistema Cultural de Xadrez
          </h1>
          <p className="text-emerald-100">
            Uma experiência única de xadrez com elementos culturais adaptativos
          </p>
        </div>

        {/* Área principal */}
        <div className="grid lg:grid-cols-3 gap-8">

        {/* Área principal */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Controles e Tabuleiro */}
          <div className="lg:col-span-2 space-y-8">
            <MemoizedGameControls
              culturalStyle={culturalStyle}
              onStyleChange={handleStyleChange}
              onFlipBoard={handleFlipBoard}
              onNewGame={handleNewGame}
              onUndo={handleUndo}
              canUndo={canUndo}
              isPlayerTurn={true} // TODO: Implementar lógica de turno
            />
            
            <div className="flex justify-center">
              <MemoizedChessBoard
                orientation={orientation}
                culturalStyle={culturalStyle}
                showCoordinates={true}
                onMove={handleMove}
                onGameEnd={handleGameEnd}
              />
            </div>
          </div>

          {/* Painel de Informações */}
          <div>
            <MemoizedGameInfo
              culturalStyle={culturalStyle}
              moves={gameHistory}
              evaluation={evaluation}
              narratives={narratives}
              events={events}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
