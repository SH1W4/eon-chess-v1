import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './NarrativeDisplay.css';

interface NarrativeDisplayProps {
  narrative: string;
  culture: string;
  moveNumber?: number;
  isImportant?: boolean;
}

interface NarrativeEntry {
  id: string;
  text: string;
  culture: string;
  timestamp: Date;
  isImportant: boolean;
  moveNumber: number;
}

export const NarrativeDisplay: React.FC<NarrativeDisplayProps> = ({
  narrative,
  culture,
  moveNumber = 0,
  isImportant = false
}) => {
  const [narrativeHistory, setNarrativeHistory] = useState<NarrativeEntry[]>([]);
  const [isExpanded, setIsExpanded] = useState(true);
  const [autoScroll, setAutoScroll] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Adicionar nova narrativa ao histórico
  useEffect(() => {
    if (narrative) {
      const newEntry: NarrativeEntry = {
        id: `${Date.now()}-${moveNumber}`,
        text: narrative,
        culture,
        timestamp: new Date(),
        isImportant,
        moveNumber
      };

      setNarrativeHistory(prev => [...prev, newEntry]);
    }
  }, [narrative, culture, moveNumber, isImportant]);

  // Auto-scroll quando nova narrativa é adicionada
  useEffect(() => {
    if (autoScroll && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [narrativeHistory, autoScroll]);

  // Obter ícone cultural
  const getCultureIcon = (cultureName: string): string => {
    const icons: Record<string, string> = {
      persian: '🏛️',
      mongol: '🏹',
      chinese: '🏮',
      indian: '🕉️',
      arabic: '🌙',
      japanese: '⛩️',
      viking: '⚔️',
      aztec: '🎭',
      mayan: '🗿',
      samurai: '🗾',
      default: '♟️'
    };
    return icons[cultureName.toLowerCase()] || icons.default;
  };

  // Obter estilo de cor cultural
  const getCultureColor = (cultureName: string): string => {
    const colors: Record<string, string> = {
      persian: '#FF6B6B',
      mongol: '#4ECDC4',
      chinese: '#FFE66D',
      indian: '#FF8B94',
      arabic: '#A8E6CF',
      japanese: '#C7CEEA',
      viking: '#95A99C',
      aztec: '#FFDAC1',
      mayan: '#B4A7D6',
      samurai: '#D4A5A5',
      default: '#6C757D'
    };
    return colors[cultureName.toLowerCase()] || colors.default;
  };

  // Formatar tempo relativo
  const formatTimeAgo = (date: Date): string => {
    const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
    
    if (seconds < 60) return 'agora';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m atrás`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h atrás`;
    return `${Math.floor(seconds / 86400)}d atrás`;
  };

  // Limpar histórico
  const clearHistory = () => {
    setNarrativeHistory([]);
  };

  // Exportar narrativas
  const exportNarratives = () => {
    const narrativeText = narrativeHistory
      .map(entry => `[Movimento ${entry.moveNumber}] ${entry.text}`)
      .join('\n\n');
    
    const blob = new Blob([narrativeText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `aeon_chess_narrative_${new Date().toISOString()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <motion.div 
      className="narrative-display"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="narrative-header">
        <h3>
          <span className="culture-icon">{getCultureIcon(culture)}</span>
          Narrativa {culture.charAt(0).toUpperCase() + culture.slice(1)}
        </h3>
        <div className="narrative-controls">
          <button 
            className="control-btn"
            onClick={() => setAutoScroll(!autoScroll)}
            title={autoScroll ? "Desativar auto-scroll" : "Ativar auto-scroll"}
          >
            {autoScroll ? '📜' : '📄'}
          </button>
          <button 
            className="control-btn"
            onClick={() => setIsExpanded(!isExpanded)}
            title={isExpanded ? "Minimizar" : "Expandir"}
          >
            {isExpanded ? '−' : '+'}
          </button>
          <button 
            className="control-btn"
            onClick={exportNarratives}
            title="Exportar narrativas"
            disabled={narrativeHistory.length === 0}
          >
            💾
          </button>
          <button 
            className="control-btn"
            onClick={clearHistory}
            title="Limpar histórico"
            disabled={narrativeHistory.length === 0}
          >
            🗑️
          </button>
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div 
            className="narrative-content"
            ref={scrollRef}
            initial={{ height: 0 }}
            animate={{ height: 'auto' }}
            exit={{ height: 0 }}
            transition={{ duration: 0.3 }}
          >
            {narrativeHistory.length === 0 ? (
              <div className="narrative-empty">
                <p>As narrativas aparecerão aqui conforme o jogo progride...</p>
              </div>
            ) : (
              <div className="narrative-list">
                {narrativeHistory.map((entry, index) => (
                  <motion.div
                    key={entry.id}
                    className={`narrative-entry ${entry.isImportant ? 'important' : ''}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    style={{ borderLeftColor: getCultureColor(entry.culture) }}
                  >
                    <div className="entry-header">
                      <span className="move-number">
                        Movimento {entry.moveNumber}
                      </span>
                      <span className="timestamp">
                        {formatTimeAgo(entry.timestamp)}
                      </span>
                    </div>
                    <div className="entry-text">
                      {entry.text}
                    </div>
                    {entry.isImportant && (
                      <div className="important-marker">
                        ⚡ Momento Crucial
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {!isExpanded && narrativeHistory.length > 0 && (
        <div className="narrative-minimized">
          <p className="latest-narrative">
            {narrativeHistory[narrativeHistory.length - 1].text}
          </p>
        </div>
      )}
    </motion.div>
  );
};

export default NarrativeDisplay;
