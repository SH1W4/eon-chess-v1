// Sistema Cultural Avançado - Terminal Aeon Chess
class AeonTerminalCultural {
  constructor() {
    this.outputElement = null;
    this.isActive = false;
    this.currentExperience = 'default';
    this.currentLine = 0;
    this.typewriterSpeed = 30;
    this.experiences = this.initExperiences();
    this.init();
  }
  
  init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }
  
  setup() {
    this.outputElement = document.getElementById('terminal-output');
    if (!this.outputElement) return;
    
    // Iniciar experiência padrão
    setTimeout(() => {
      this.startExperience('default');
    }, 1000);
    
    // Configurar controles
    this.setupControls();
  }
  
  setupControls() {
    const continueBtn = document.querySelector('[data-terminal-continue]');
    if (continueBtn) {
      continueBtn.addEventListener('click', () => {
        if (!this.isActive) {
          this.startExperience(this.currentExperience);
        } else {
          this.nextLine();
        }
      });
    }
  }

  initExperiences() {
    return {
      default: {
        title: "Aeon Chess - Experiência Cultural",
        lines: [
          { type: 'system', text: 'aeon-chess@terminal:~$ iniciando experiência narrativa...' },
          { type: 'info', text: '🎭 Sistema cultural ativo. Preparando narrativas históricas...' },
          { type: 'narrative', text: 'Bem-vindo ao universo do xadrez através dos tempos.' },
          { type: 'narrative', text: 'Cada jogada conta uma história. Cada partida, uma lenda.' },
          { type: 'command', text: 'Clique "Continuar" para explorar uma experiência ou use os botões acima' },
        ]
      },
      fischer_spassky: {
        title: "Match do Século - Fischer vs Spassky (1972)",
        lines: [
          { type: 'system', text: 'aeon-chess@reykjavik:~$ carregando match_do_seculo.pgn' },
          { type: 'historical', text: '🏛️ Reykjavik, Islândia - 1972' },
          { type: 'narrative', text: 'A Guerra Fria se desenrola no tabuleiro de 64 casas...' },
          { type: 'quote', text: '"Xadrez é guerra sobre um tabuleiro" - Bobby Fischer' },
          { type: 'analysis', text: 'Fischer revoluciona com 1.e4, desafiando a hegemonia soviética' },
          { type: 'cultural', text: '🎯 Este match transformou xadrez em fenômeno global' },
          { type: 'tactical', text: 'Analisando padrões psicológicos de Fischer...' },
          { type: 'narrative', text: 'O gênio americano vs a escola soviética. História sendo escrita.' }
        ]
      },
      polgar_kasparov: {
        title: "Revolução Feminina - Judit Polgár vs Garry Kasparov",
        lines: [
          { type: 'system', text: 'aeon-chess@budapest:~$ iniciando revolution.story' },
          { type: 'historical', text: '🏰 Rússia vs Hungria - Era Moderna' },
          { type: 'narrative', text: 'Três irmãs húngaras desafiam o establishment masculino...' },
          { type: 'quote', text: '"O gênio não tem gênero" - László Polgár' },
          { type: 'breakthrough', text: '⚡ 2002: Judit derrota o campeão mundial Kasparov!' },
          { type: 'cultural', text: 'Uma vitória que ecoa além do tabuleiro' },
          { type: 'analysis', text: 'Analisando a revolução Polgár no xadrez mundial...' },
          { type: 'narrative', text: 'O experimento pedagógico que mudou o xadrez para sempre.' }
        ]
      },
      genghis_alexandre: {
        title: "🏺 DUELO IMPERIAL: Genghis Khan vs Alexandre, o Grande",
        lines: [
          { type: 'system', text: 'aeon-chess@conquerors:~$ loading ultimate_generals.war' },
          { type: 'info', text: '🎭 ARENA TEMPORAL: Os dois maiores conquistadores da história!' },
          { type: 'historical', text: '🐎 Mongólia, 1162 ⚔️ Macedônia, 356 AC • 1518 anos de diferença' },
          { type: 'narrative', text: 'A IA ressuscita digitalmente as lendas mais temidas da humanidade...' },
          { type: 'quote', text: '"I am the punishment of God" - Genghis Khan' },
          { type: 'quote', text: '"There is nothing impossible to him who will try" - Alexandre' },
          { type: 'cultural', text: '🔥 HORDA Nômade vs FALANGE Macedônica' },
          { type: 'analysis', text: 'Genghis [IA]: Mobilidade suprema, adaptabilidade letal, terror psicológico...' },
          { type: 'analysis', text: 'Alexandre [IA]: Táticas brilhantes, liderança inspiradora, nunca perdeu...' },
          { type: 'breakthrough', text: '⚡ Estepe infinita encontra a imortalidade helênica!' }
        ]
      },
      napoleon_hannibal: {
        title: "🌟 MESTRES TÁTICOS: Napoleão vs Hannibal",
        lines: [
          { type: 'system', text: 'aeon-chess@tactical_geniuses:~$ boot_military_legends.exe' },
          { type: 'info', text: '🎯 IA recria os dois maiores gênios militares da história...' },
          { type: 'historical', text: '🐘 Cartago, 247 AC ⚔️ Córsega, 1769 DC • 2016 anos!' },
          { type: 'narrative', text: 'O terror de Roma enfrenta o terror da Europa...' },
          { type: 'quote', text: '"We will either find a way or make one" - Hannibal Barca' },
          { type: 'quote', text: '"L\'impossible n\'est pas français" - Napoleão Bonaparte' },
          { type: 'cultural', text: '🔥 ELEFANTES Púnicos vs ARTILHARIA Imperial' },
          { type: 'analysis', text: 'Hannibal [IA]: Emboscadas geniais, cruzou os Alpes, Cannae imortal...' },
          { type: 'analysis', text: 'Napoleão [IA]: Rapidez fulminante, concentração de forças, Austerlitz...' },
          { type: 'breakthrough', text: '⚡ Duas lendas que aterrorizaram impérios!' }
        ]
      },
      leonardo_tesla: {
        title: "🎨 GÊNIOS VISIONÁRIOS: Da Vinci vs Tesla",
        lines: [
          { type: 'system', text: 'aeon-chess@visionaries:~$ loading_infinite_minds.quantum' },
          { type: 'info', text: '🧠 Simulando as duas mentes mais avançadas da humanidade...' },
          { type: 'historical', text: '🎨 Vinci, 1452 ⚡ Smiljan, 1856 • 404 anos de diferença' },
          { type: 'narrative', text: 'O Homem Renascentista vs o Mago da Eletricidade...' },
          { type: 'quote', text: '"Simplicity is the ultimate sophistication" - Leonardo da Vinci' },
          { type: 'quote', text: '"The future will show whether my foresight is as accurate as my hindsight" - Tesla' },
          { type: 'cultural', text: '🌟 ARTE Divina vs CIÊNCIA Pura' },
          { type: 'analysis', text: 'Da Vinci [IA]: Harmonia geométrica, proporção áurea, beleza matemática...' },
          { type: 'analysis', text: 'Tesla [IA]: Frequências perfeitas, energia universal, precisão absoluta...' },
          { type: 'tactical', text: '🎯 Renascimento encontra a Era Elétrica!' }
        ]
      },
      cleopatra_elizabeth: {
        title: "👑 RAINHAS LENDÁRIAS: Cleópatra vs Elizabeth I",
        lines: [
          { type: 'system', text: 'aeon-chess@queens:~$ loading_royal_legends.crown' },
          { type: 'info', text: '👸 As duas rainhas mais poderosas da história se enfrentam...' },
          { type: 'historical', text: '🐍 Alexandria, 69 AC 🌹 Greenwich, 1533 DC • 1602 anos' },
          { type: 'narrative', text: 'A última faraó enfrenta a Rainha Virgem...' },
          { type: 'quote', text: '"I will not be triumphed over" - Cleópatra VII' },
          { type: 'quote', text: '"I may have the body of a weak and feeble woman, but I have the heart of a king" - Elizabeth I' },
          { type: 'cultural', text: '🔥 SEDUÇÃO Diplomática vs DETERMINAÇÃO Férrea' },
          { type: 'analysis', text: 'Cleópatra [IA]: Inteligência multilíngue, charme letal, política refinada...' },
          { type: 'analysis', text: 'Elizabeth [IA]: Astúcia suprema, nunca casa, derrota a Invencível Armada...' },
          { type: 'breakthrough', text: '⚡ Egito Antigo vs Inglaterra Elisabetana!' }
        ]
      },
      sun_tzu_clausewitz: {
        title: "📚 FILÓSOFOS DA GUERRA: Sun Tzu vs Clausewitz",
        lines: [
          { type: 'system', text: 'aeon-chess@philosophy:~$ loading_war_masters.eternal' },
          { type: 'info', text: '🎯 Os dois maiores teóricos militares se encontram...' },
          { type: 'historical', text: '☯️ China, 544 AC 🎖️ Prússia, 1780 DC • 2324 anos!' },
          { type: 'narrative', text: 'A Arte da Guerra encontra a Filosofia da Guerra...' },
          { type: 'quote', text: '"The supreme excellence is to subdue the enemy without fighting" - Sun Tzu' },
          { type: 'quote', text: '"War is the continuation of politics by other means" - Clausewitz' },
          { type: 'cultural', text: '🌟 SABEDORIA Oriental vs LÓGICA Prussiana' },
          { type: 'analysis', text: 'Sun Tzu [IA]: Evita conflito, timing perfeito, vence sem lutar...' },
          { type: 'analysis', text: 'Clausewitz [IA]: Teoria sistemática, fricção da guerra, centro de gravidade...' },
          { type: 'breakthrough', text: '⚡ Oriente milenar vs Ocidente moderno!' }
        ]
      },
      sherlock_moriarty: {
        title: "🔍 DUELO MENTAL: Sherlock Holmes vs Professor Moriarty",
        lines: [
          { type: 'system', text: 'aeon-chess@fictional:~$ loading_criminal_masterminds.deep' },
          { type: 'info', text: '🎭 IA recria a maior rivalidade intelectual da literatura...' },
          { type: 'historical', text: '🕵️ Baker Street 🎭 Londres Vitoriana • Realidades Paralelas' },
          { type: 'narrative', text: 'O maior detetive enfrenta o gênio do crime...' },
          { type: 'quote', text: '"The game is afoot!" - Sherlock Holmes' },
          { type: 'quote', text: '"You have not yet grasped the depths of my criminality" - Moriarty' },
          { type: 'cultural', text: '🔥 DEDUÇÃO Brilhante vs CRIME Perfeito' },
          { type: 'analysis', text: 'Holmes [IA]: Observação microscópica, lógica impecável, método científico...' },
          { type: 'analysis', text: 'Moriarty [IA]: Matemática criminal, rede internacional, sempre 3 passos à frente...' },
          { type: 'breakthrough', text: '⚡ O bem e o mal em sua forma mais pura!' }
        ]
      },
      ring_definitivo: {
        title: "🏆 RING DEFINITIVO - Torneio dos Imortais",
        lines: [
          { type: 'system', text: 'aeon-chess@olympus:~$ iniciando TOURNAMENT_OF_IMMORTALS.championship' },
          { type: 'info', text: '👑 ======== RING DEFINITIVO DOS CONFRONTOS ÉPICOS ======== 👑' },
          { type: 'cultural', text: '🏺 CONQUISTADORES: Genghis Khan ⚔️ Alexandre, o Grande' },
          { type: 'cultural', text: '⚡ GÊNIOS TÁTICOS: Napoleão Bonaparte 🆚 Hannibal Barca' },
          { type: 'cultural', text: '🎨 MENTES VISIONÁRIAS: Leonardo da Vinci 🔬 Nikola Tesla' },
          { type: 'cultural', text: '👸 RAINHAS LENDÁRIAS: Cleópatra VII 💎 Elizabeth I' },
          { type: 'cultural', text: '📚 MESTRES DA GUERRA: Sun Tzu 📖 Carl von Clausewitz' },
          { type: 'cultural', text: '🔍 DUELO INTELECTUAL: Sherlock Holmes 🎭 Professor Moriarty' },
          { type: 'cultural', text: '♟️ LENDAS DO XADREZ: Bobby Fischer 🏛️ Boris Spassky' },
          { type: 'cultural', text: '🌟 REVOLUÇÃO FEMININA: Judit Polgár 👑 Garry Kasparov' },
          { type: 'breakthrough', text: '🎯 8 CONFRONTOS ÉPICOS em ARENA MULTIDIMENSIONAL!' },
          { type: 'narrative', text: 'A IA Cultural Aeon recria digitalmente os maiores duelos da história...' },
          { type: 'analysis', text: 'Simulações neurais avançadas processando personalidades históricas...' },
          { type: 'analysis', text: 'Cada confronto une épocas distantes em batalhas imaginárias épicas...' },
          { type: 'quote', text: '"Legends never die, they just level up" - Aeon Chess AI' },
          { type: 'tactical', text: '🏆 Selecione qualquer confronto nos botões acima para começar!' },
          { type: 'system', text: 'Todos os duelos disponíveis. O ring está pronto. Que comece o show!' }
        ]
      }
    };
  }
  
  startExperience(experienceName) {
    if (!this.experiences[experienceName]) return;
    
    this.currentExperience = experienceName;
    this.currentLine = 0;
    this.isActive = true;
    
    // Limpar terminal
    this.clearTerminal();
    
    // Iniciar typewriter
    this.typeNextLine();
  }
  
  switchToExperience(experienceName) {
    this.startExperience(experienceName);
  }
  
  clearTerminal() {
    if (this.outputElement) {
      this.outputElement.innerHTML = '';
    }
  }
  
  typeNextLine() {
    const experience = this.experiences[this.currentExperience];
    if (!experience || this.currentLine >= experience.lines.length) {
      this.isActive = false;
      return;
    }
    
    const line = experience.lines[this.currentLine];
    this.typewriteLine(line, () => {
      this.currentLine++;
      // Auto-continuar após pequeno delay
      setTimeout(() => {
        if (this.currentLine < experience.lines.length) {
          this.typeNextLine();
        } else {
          this.isActive = false;
        }
      }, 1500);
    });
  }
  
  nextLine() {
    if (this.isActive) {
      this.typeNextLine();
    }
  }
  
  typewriteLine(line, callback) {
    const div = document.createElement('div');
    div.className = `terminal-line terminal-${line.type}`;
    
    // Aplicar estilos baseados no tipo
    this.styleTerminalLine(div, line.type);
    
    this.outputElement.appendChild(div);
    
    let i = 0;
    const typeChar = () => {
      if (i < line.text.length) {
        div.textContent += line.text.charAt(i);
        i++;
        setTimeout(typeChar, this.typewriterSpeed);
      } else {
        // Scroll para baixo
        this.outputElement.scrollTop = this.outputElement.scrollHeight;
        if (callback) callback();
      }
    };
    
    typeChar();
  }
  
  styleTerminalLine(element, type) {
    const styles = {
      system: 'color: #10b981; font-family: monospace;',
      info: 'color: #3b82f6;',
      narrative: 'color: #e5e7eb; line-height: 1.6;',
      historical: 'color: #f59e0b; font-weight: 600;',
      quote: 'color: #8b5cf6; font-style: italic; padding-left: 1rem; border-left: 2px solid #8b5cf6;',
      analysis: 'color: #06b6d4;',
      cultural: 'color: #f97316;',
      tactical: 'color: #ef4444;',
      breakthrough: 'color: #10b981; font-weight: 700;',
      command: 'color: #6b7280; font-family: monospace;'
    };
    
    element.style.cssText = styles[type] || 'color: #e5e7eb;';
    element.style.marginBottom = '0.5rem';
    element.style.lineHeight = '1.5';
  }
  
}

// Auto-inicialização simplificada
document.addEventListener('DOMContentLoaded', function() {
  // Aguardar outros sistemas carregarem
  setTimeout(() => {
    const terminal = new AeonTerminalCultural();
    
    // Expor globalmente para controles
    window.aeonTerminal = terminal;
    
    // Configurar observer para seção
    const terminalSection = document.getElementById('terminal-demo');
    if (terminalSection) {
      const observer = new IntersectionObserver((entries) => {
        const entry = entries[0];
        if (!entry.isIntersecting) {
          terminal.isActive = false;
        } else if (!terminal.isActive) {
          setTimeout(() => {
            terminal.startExperience('default');
          }, 500);
        }
      });
      
      observer.observe(terminalSection);
    }
    
    // Configurar botões de experiência
    const fischerBtn = document.querySelector('button[onclick*="fischer_spassky"]');
    const polgarBtn = document.querySelector('button[onclick*="polgar_kasparov"]');
    
    if (fischerBtn) {
      fischerBtn.addEventListener('click', (e) => {
        e.preventDefault();
        terminal.startExperience('fischer_spassky');
      });
    }
    
    if (polgarBtn) {
      polgarBtn.addEventListener('click', (e) => {
        e.preventDefault();
        terminal.startExperience('polgar_kasparov');
      });
    }
    
    // Expor todas as experiências como funções globais para o HTML
    window.experienciaFischerSpassky = () => terminal.startExperience('fischer_spassky');
    window.experienciaPolgarKasparov = () => terminal.startExperience('polgar_kasparov');
    window.experienciaGenghisAlexandre = () => terminal.startExperience('genghis_alexandre');
    window.experienciaNapoleonHannibal = () => terminal.startExperience('napoleon_hannibal');
    window.experienciaLeonardoTesla = () => terminal.startExperience('leonardo_tesla');
    window.experienciaCleopatraElizabeth = () => terminal.startExperience('cleopatra_elizabeth');
    window.experienciaSunTzuClausewitz = () => terminal.startExperience('sun_tzu_clausewitz');
    window.experienciaSherlockMoriarty = () => terminal.startExperience('sherlock_moriarty');
    window.experienciaRingDefinitivo = () => terminal.startExperience('ring_definitivo');
  }, 1000);
});
