import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './CulturalTheme.css';

interface Culture {
  id: string;
  name: string;
  description: string;
  icon: string;
  primaryColor: string;
  secondaryColor: string;
  traits: string[];
  strategies: string[];
  specialMoves?: string[];
}

interface CulturalThemeProps {
  culture: string;
  onThemeChange: (culture: string) => void;
  showDetails?: boolean;
}

const cultures: Culture[] = [
  {
    id: 'persian',
    name: 'Persa',
    description: 'Mestres da estratégia e poesia, combinando arte com guerra',
    icon: '🏛️',
    primaryColor: '#FF6B6B',
    secondaryColor: '#FFE5E5',
    traits: ['Poético', 'Estratégico', 'Filosófico'],
    strategies: ['Controle do centro', 'Sacrifícios calculados', 'Finais artísticos'],
    specialMoves: ['Gambito do Xá', 'Defesa Imortal']
  },
  {
    id: 'mongol',
    name: 'Mongol',
    description: 'Guerreiros nômades com táticas de cavalaria devastadoras',
    icon: '🏹',
    primaryColor: '#4ECDC4',
    secondaryColor: '#E0F7F6',
    traits: ['Agressivo', 'Móvel', 'Imprevisível'],
    strategies: ['Ataques rápidos', 'Flancos múltiplos', 'Pressão constante'],
    specialMoves: ['Carga da Horda', 'Cerco Relâmpago']
  },
  {
    id: 'chinese',
    name: 'Chinês',
    description: 'Sabedoria milenar e estratégias profundas como a Arte da Guerra',
    icon: '🏮',
    primaryColor: '#FFE66D',
    secondaryColor: '#FFF9E6',
    traits: ['Paciente', 'Calculista', 'Harmonioso'],
    strategies: ['Desenvolvimento lento', 'Armadilhas sutis', 'Equilíbrio de forças'],
    specialMoves: ['Dragão Adormecido', 'Muralha de Jade']
  },
  {
    id: 'indian',
    name: 'Indiano',
    description: 'Berço do xadrez, com movimentos que refletem filosofia profunda',
    icon: '🕉️',
    primaryColor: '#FF8B94',
    secondaryColor: '#FFE8EA',
    traits: ['Místico', 'Criativo', 'Contemplativo'],
    strategies: ['Desenvolvimento espiritual', 'Sacrifícios simbólicos', 'Transformação'],
    specialMoves: ['Dança de Shiva', 'Meditação do Elefante']
  },
  {
    id: 'arabic',
    name: 'Árabe',
    description: 'Matemáticos e astrônomos que elevaram o xadrez a uma ciência',
    icon: '🌙',
    primaryColor: '#A8E6CF',
    secondaryColor: '#E8F7F1',
    traits: ['Analítico', 'Preciso', 'Elegante'],
    strategies: ['Geometria do tabuleiro', 'Cálculos profundos', 'Beleza matemática'],
    specialMoves: ['Estrela de Al-Andalus', 'Crescente Dourado']
  },
  {
    id: 'japanese',
    name: 'Japonês',
    description: 'Disciplina samurai aplicada ao tabuleiro com honra e precisão',
    icon: '⛩️',
    primaryColor: '#C7CEEA',
    secondaryColor: '#F0F2FB',
    traits: ['Disciplinado', 'Honorável', 'Preciso'],
    strategies: ['Sacrifício honorável', 'Defesa impenetrável', 'Golpe decisivo'],
    specialMoves: ['Caminho do Bushido', 'Corte do Vento']
  },
  {
    id: 'viking',
    name: 'Viking',
    description: 'Guerreiros do norte com táticas brutais e coragem inabalável',
    icon: '⚔️',
    primaryColor: '#95A99C',
    secondaryColor: '#E5E9E7',
    traits: ['Feroz', 'Corajoso', 'Direto'],
    strategies: ['Ataque frontal', 'Sem recuo', 'Vitória ou Valhalla'],
    specialMoves: ['Fúria Berserker', 'Escudo de Parede']
  },
  {
    id: 'aztec',
    name: 'Asteca',
    description: 'Guerreiros-sacerdotes com rituais de batalha elaborados',
    icon: '🎭',
    primaryColor: '#FFDAC1',
    secondaryColor: '#FFF5EE',
    traits: ['Ritualístico', 'Feroz', 'Simbólico'],
    strategies: ['Sacrifícios rituais', 'Pressão psicológica', 'Dominância'],
    specialMoves: ['Águia Guerreira', 'Serpente Emplumada']
  },
  {
    id: 'mayan',
    name: 'Maia',
    description: 'Astrônomos e matemáticos com visão cósmica do jogo',
    icon: '🗿',
    primaryColor: '#B4A7D6',
    secondaryColor: '#F0EDFA',
    traits: ['Visionário', 'Matemático', 'Cósmico'],
    strategies: ['Padrões celestiais', 'Ciclos de poder', 'Previsão'],
    specialMoves: ['Calendário Sagrado', 'Eclipse Total']
  },
  {
    id: 'samurai',
    name: 'Samurai',
    description: 'Elite guerreira com código de honra e maestria técnica',
    icon: '🗾',
    primaryColor: '#D4A5A5',
    secondaryColor: '#F5EDED',
    traits: ['Leal', 'Técnico', 'Determinado'],
    strategies: ['Perfeição técnica', 'Lealdade absoluta', 'Morte antes da desonra'],
    specialMoves: ['Iaijutsu', 'Seppuku Honorável']
  }
];

export const CulturalTheme: React.FC<CulturalThemeProps> = ({
  culture,
  onThemeChange,
  showDetails = true
}) => {
  const [selectedCulture, setSelectedCulture] = useState<Culture | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [hoveredCulture, setHoveredCulture] = useState<string | null>(null);

  useEffect(() => {
    const found = cultures.find(c => c.id === culture);
    setSelectedCulture(found || cultures[0]);
  }, [culture]);

  const handleCultureSelect = (cultureId: string) => {
    const newCulture = cultures.find(c => c.id === cultureId);
    if (newCulture) {
      setSelectedCulture(newCulture);
      onThemeChange(cultureId);
      setIsOpen(false);
    }
  };

  if (!selectedCulture) return null;

  return (
    <div className="cultural-theme-container">
      <motion.div 
        className="culture-selector"
        style={{ 
          backgroundColor: selectedCulture.secondaryColor,
          borderColor: selectedCulture.primaryColor
        }}
      >
        <button
          className="culture-selector-button"
          onClick={() => setIsOpen(!isOpen)}
          style={{ color: selectedCulture.primaryColor }}
        >
          <span className="culture-icon">{selectedCulture.icon}</span>
          <span className="culture-name">{selectedCulture.name}</span>
          <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
        </button>

        <AnimatePresence>
          {isOpen && (
            <motion.div
              className="culture-dropdown"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {cultures.map((cult) => (
                <motion.button
                  key={cult.id}
                  className={`culture-option ${cult.id === selectedCulture.id ? 'selected' : ''}`}
                  onClick={() => handleCultureSelect(cult.id)}
                  onMouseEnter={() => setHoveredCulture(cult.id)}
                  onMouseLeave={() => setHoveredCulture(null)}
                  style={{
                    backgroundColor: cult.id === selectedCulture.id 
                      ? cult.primaryColor 
                      : hoveredCulture === cult.id 
                        ? cult.secondaryColor 
                        : 'transparent',
                    color: cult.id === selectedCulture.id ? 'white' : cult.primaryColor
                  }}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <span className="culture-icon">{cult.icon}</span>
                  <span className="culture-name">{cult.name}</span>
                </motion.button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {showDetails && (
        <motion.div 
          className="culture-details"
          key={selectedCulture.id}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          style={{ borderLeftColor: selectedCulture.primaryColor }}
        >
          <h4 style={{ color: selectedCulture.primaryColor }}>
            {selectedCulture.icon} {selectedCulture.name}
          </h4>
          <p className="culture-description">{selectedCulture.description}</p>
          
          <div className="culture-traits">
            <h5>Características:</h5>
            <div className="trait-list">
              {selectedCulture.traits.map((trait, index) => (
                <span 
                  key={index} 
                  className="trait-badge"
                  style={{ 
                    backgroundColor: selectedCulture.secondaryColor,
                    color: selectedCulture.primaryColor
                  }}
                >
                  {trait}
                </span>
              ))}
            </div>
          </div>

          <div className="culture-strategies">
            <h5>Estratégias:</h5>
            <ul>
              {selectedCulture.strategies.map((strategy, index) => (
                <li key={index}>{strategy}</li>
              ))}
            </ul>
          </div>

          {selectedCulture.specialMoves && selectedCulture.specialMoves.length > 0 && (
            <div className="culture-special-moves">
              <h5>Movimentos Especiais:</h5>
              <div className="special-moves-list">
                {selectedCulture.specialMoves.map((move, index) => (
                  <motion.div 
                    key={index}
                    className="special-move"
                    style={{ backgroundColor: selectedCulture.secondaryColor }}
                    whileHover={{ scale: 1.05 }}
                  >
                    ⚡ {move}
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default CulturalTheme;
