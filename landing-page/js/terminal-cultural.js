// 🎭 AEON CHESS: TERMINAL CULTURAL AVANÇADO
// Sistema simbiótico ARQUIMAX + NEXUS para experiências imersivas

class AeonTerminalCultural {
  constructor(terminalOutputId) {
    this.terminalOutput = document.getElementById(terminalOutputId);
    this.currentExperience = 0;
    this.currentMoveIndex = 0;
    this.isAnimating = false;
    this.animationSpeed = 2000;
    this.culturalExperiences = this.initCulturalExperiences();
    this.currentGame = null;
  }

  initCulturalExperiences() {
    return [
      {
        id: 'capablanca_alekhine',
        info: {
          white: 'José Raúl Capablanca',
          black: 'Alexander Alekhine',
          event: 'World Championship Match - Jogo 11',
          site: 'Buenos Aires, Argentina',
          date: '1927.10.29',
          result: '0-1',
          opening: 'Queen\'s Gambit Declined, Orthodox Defense',
          culture: 'Escola Clássica Cubana vs Escola Dinâmica Russa',
          significance: 'O fim de uma era: último jogo de Capablanca como campeão mundial'
        },
        moves: [
          { move: 'd4', side: 'white', time: '14:00', eval: '+0.2', ply: 1 },
          { move: 'd5', side: 'black', time: '14:01', eval: '=', ply: 2 },
          { move: 'c4', side: 'white', time: '14:02', eval: '+0.3', ply: 3 },
          { move: 'e6', side: 'black', time: '14:03', eval: '+0.2', ply: 4 },
          { move: 'Nc3', side: 'white', time: '14:04', eval: '+0.3', ply: 5 },
          { move: 'Nf6', side: 'black', time: '14:05', eval: '+0.2', ply: 6 },
          { move: 'Bg5', side: 'white', time: '14:07', eval: '+0.4', ply: 7 },
          { move: 'Be7', side: 'black', time: '14:09', eval: '+0.3', ply: 8 },
          { move: 'Re8!', side: 'black', time: '16:42', eval: '-0.3', ply: 46 }, // Movimento decisivo
          { move: 'Re2+!', side: 'black', time: '16:51', eval: '-1.2', ply: 48 } // Sacrifício final
        ],
        commentary: {
          1: {
            text: "Capablanca escolhe 1.d4, a marca registrada da escola clássica. Este seria um dos últimos jogos como Campeão Mundial.",
            type: "opening",
            cultural: "Em 1927, Buenos Aires fervilhava com a rivalidade entre as escolas cubana e russa de xadrez. Capablanca personificava a elegância técnica latino-americana."
          },
          2: {
            text: "Alekhine responde simetricamente. O futuro campeão sempre buscava complicações onde seu talento calculista pudesse brilhar.",
            type: "response", 
            cultural: "A escola russa priorizava o cálculo concreto. Alekhine representava a nova geração que desafiaria dogmas posicionais."
          },
          46: {
            text: "Re8!! O lance que mudou a história! Uma manobra profundíssima que nem Capablanca havia antecipado.",
            type: "brilliance",
            cultural: "Este movimento é estudado até hoje como exemplo de visão posicional superior. Marcou o fim da era Capablanca."
          },
          48: {
            text: "Re2+! O sacrifício devastador que coroou Alekhine. Capablanca, pela primeira vez, foi superado taticamente.",
            type: "decisive", 
            cultural: "Este momento selou a transição de poder no xadrez mundial. Uma nova era dinâmica havia começado."
          }
        }
      },

      {
        id: 'fischer_spassky',
        info: {
          white: 'Robert James Fischer',
          black: 'Boris Spassky',
          event: 'World Championship Match - Jogo 6',
          site: 'Reykjavik, Islândia', 
          date: '1972.07.23',
          result: '1-0',
          opening: 'Queen\'s Gambit Declined, Tartakower Defense',
          culture: 'América vs URSS: Guerra Fria no Tabuleiro',
          significance: 'O "Match do Século" que quebrou a hegemonia soviética'
        },
        moves: [
          { move: 'd4', side: 'white', time: '17:00', eval: '+0.2', ply: 1 },
          { move: 'Nf6', side: 'black', time: '17:01', eval: '=', ply: 2 },
          { move: 'c4', side: 'white', time: '17:02', eval: '+0.3', ply: 3 },
          { move: 'e6', side: 'black', time: '17:03', eval: '+0.2', ply: 4 },
          { move: 'Nf3', side: 'white', time: '17:04', eval: '+0.3', ply: 5 },
          { move: 'd5', side: 'black', time: '17:05', eval: '+0.2', ply: 6 },
          { move: 'Nc3', side: 'white', time: '17:07', eval: '+0.4', ply: 7 },
          { move: 'Be7', side: 'black', time: '17:09', eval: '+0.3', ply: 8 },
          { move: 'Bg5', side: 'white', time: '17:12', eval: '+0.5', ply: 9 },
          { move: 'h6', side: 'black', time: '17:15', eval: '+0.3', ply: 10 }
        ],
        commentary: {
          1: {
            text: "Fischer abre com 1.d4, uma escolha pragmática para este match histórico. O prodígio americano enfrentava toda a máquina soviética.",
            type: "opening",
            cultural: "1972: pleno auge da Guerra Fria. O xadrez era um símbolo de supremacia intelectual entre superpotências."
          },
          3: {
            text: "O Gambito da Dama surge naturalmente. Fischer demonstrava domínio completo da teoria soviética.",
            type: "strategy",
            cultural: "Irônico: Fischer usava as próprias armas teóricas soviéticas contra o campeão da URSS."
          },
          9: {
            text: "Bg5! O bispo atinge f6, aplicando a pressão característica do estilo Fischer: simples, direto, devastador.",
            type: "tactic",
            cultural: "Esta simplicidade enganosa era a marca Fischer: encontrar a melhor jogada em qualquer posição."
          }
        }
      },

      {
        id: 'polgar_kasparov',
        info: {
          white: 'Judit Polgár',
          black: 'Garry Kasparov',
          event: 'Russia vs Rest of World',
          site: 'Moscow, Rússia',
          date: '2002.09.07', 
          result: '1-0',
          opening: 'Sicilian Defense, Paulsen Variation',
          culture: 'Revolução Feminina: Quebrando as Últimas Barreiras',
          significance: 'Primeira vitória feminina sobre um campeão mundial reinante'
        },
        moves: [
          { move: 'e4', side: 'white', time: '19:30', eval: '+0.3', ply: 1 },
          { move: 'c5', side: 'black', time: '19:31', eval: '=', ply: 2 },
          { move: 'Nf3', side: 'white', time: '19:32', eval: '+0.2', ply: 3 },
          { move: 'Nc6', side: 'black', time: '19:33', eval: '+0.1', ply: 4 },
          { move: 'd4', side: 'white', time: '19:34', eval: '+0.4', ply: 5 },
          { move: 'cxd4', side: 'black', time: '19:35', eval: '+0.2', ply: 6 },
          { move: 'Nxd4', side: 'white', time: '19:36', eval: '+0.3', ply: 7 },
          { move: 'e6', side: 'black', time: '19:38', eval: '+0.2', ply: 8 },
          { move: 'Bb5!', side: 'white', time: '19:41', eval: '+0.7', ply: 9 },
          { move: 'Bd7', side: 'black', time: '19:44', eval: '+0.4', ply: 10 }
        ],
        commentary: {
          1: {
            text: "Judit escolhe 1.e4 - jogada de ataque puro. Aos 26 anos, ela desafiava o 'Ogro de Baku' em seu próprio território.",
            type: "opening",
            cultural: "2002: Judit Polgár era a única mulher entre os top 10 mundiais. Este match representava décadas de luta por igualdade no xadrez."
          },
          2: {
            text: "Kasparov responde com a Siciliana. O 13º Campeão Mundial não daria moleza para ninguém - homem ou mulher.",
            type: "response",
            cultural: "A Defesa Siciliana era a arma favorita de Kasparov. Posições complexas onde seu talento calculista dominava."
          },
          9: {
            text: "Bb5! Judit pressiona imediatamente. O estilo Polgár: agressividade calculada, típica da escola húngara.",
            type: "strategy", 
            cultural: "As irmãs Polgár revolucionaram o xadrez feminino, provando que gênero não limita talento estratégico."
          }
        }
      },

      {
        id: 'anand_carlsen',
        info: {
          white: 'Viswanathan Anand',
          black: 'Magnus Carlsen',
          event: 'World Championship 2013',
          site: 'Chennai, Índia',
          date: '2013.11.09',
          result: '0-1',
          opening: 'Caro-Kann Defense, Main Line',
          culture: 'Oriente vs Ocidente: Intuição vs Preparação',
          significance: 'O jovem nórdico destrona o "Relâmpago de Madras"'
        },
        moves: [
          { move: 'e4', side: 'white', time: '15:30', eval: '+0.3', ply: 1 },
          { move: 'c6', side: 'black', time: '15:31', eval: '=', ply: 2 },
          { move: 'd4', side: 'white', time: '15:32', eval: '+0.2', ply: 3 },
          { move: 'd5', side: 'black', time: '15:33', eval: '+0.1', ply: 4 },
          { move: 'Nc3', side: 'white', time: '15:34', eval: '+0.3', ply: 5 },
          { move: 'dxe4', side: 'black', time: '15:35', eval: '+0.1', ply: 6 },
          { move: 'Nxe4', side: 'white', time: '15:36', eval: '+0.2', ply: 7 },
          { move: 'Nd7', side: 'black', time: '15:38', eval: '+0.1', ply: 8 }
        ],
        commentary: {
          1: {
            text: "Anand, defendendo o título em casa, abre com 1.e4. A pressão era imensa: toda a Índia assistia.",
            type: "opening",
            cultural: "Chennai 2013: um bilhão de indianos torciam por Anand. O xadrez havia se tornado paixão nacional na Índia."
          },
          2: {
            text: "Carlsen escolhe a sólida Caro-Kann. Aos 22 anos, mostrava maturidade posicional impressionante.",
            type: "response",
            cultural: "A escola nórdica, liderada por Carlsen, combinava precisão computacional com intuição natural excepcional."
          }
        }
      }
    ];
  }

  async startCulturalExperience() {
    if (this.isAnimating) return;
    this.isAnimating = true;
    
    // Seleciona experiência atual
    this.currentGame = this.culturalExperiences[this.currentExperience];
    this.currentMoveIndex = 0;
    
    // Limpa terminal
    this.terminalOutput.innerHTML = '';
    
    // Header com introdução cultural
    await this.displayIntroduction();
    await this.displayGameInfo();
    await this.displayCulturalContext();
    
    // Simula carregamento de engine
    await this.displayEngineLoading();
    
    // Reproduz movimentos com narração
    await this.playMovesWithNarration();
    
    // Conclusão e estatísticas
    await this.displayConclusion();
    
    // Próxima experiência
    this.currentExperience = (this.currentExperience + 1) % this.culturalExperiences.length;
    
    // Reinicia após pausa
    setTimeout(() => {
      if (this.isAnimating) this.startCulturalExperience();
    }, 8000);
  }

  async displayIntroduction() {
    const introDiv = document.createElement('div');
    introDiv.className = 'text-green-400 mb-3';
    
    const commands = [
      '$ aeon-chess cultural --experience=historic',
      '$ loading cultural database...',
      '$ connecting to chess heritage network...',
      `$ selected: ${this.currentGame.id}`
    ];
    
    for (const cmd of commands) {
      const cmdDiv = document.createElement('div');
      cmdDiv.className = 'text-green-400 mb-1';
      await this.typeText(cmdDiv, cmd, 30);
      await this.delay(800);
    }
  }

  async displayGameInfo() {
    const infoDiv = document.createElement('div');
    infoDiv.className = 'text-blue-400 mb-4 border border-blue-600 p-3 rounded';
    const info = this.currentGame.info;
    
    const content = `
🏛️ EXPERIÊNCIA CULTURAL: ${info.culture}
📅 ${info.date} - ${info.site}
🎯 ${info.event}
🔥 ${info.opening}
⚖️ Resultado: ${info.result}
📚 ${info.significance}
    `.trim();
    
    infoDiv.innerHTML = content;
    this.terminalOutput.appendChild(infoDiv);
    this.scrollToBottom();
    await this.delay(2000);
  }

  async displayCulturalContext() {
    const contextDiv = document.createElement('div');
    contextDiv.className = 'text-purple-400 mb-4 border-l-4 border-purple-400 pl-4 bg-purple-900 bg-opacity-10 p-3 rounded';
    
    const culturalIntros = {
      'capablanca_alekhine': "A América Latina vivia um renascimento intelectual. Capablanca, o 'Mozart do Xadrez', enfrentava o calculista russo Alekhine em Buenos Aires, cidade que respirava xadrez e tango.",
      'fischer_spassky': "Reykjavik, 1972. O mundo parou para assistir. Não era apenas xadrez - era capitalismo vs comunismo, individualismo vs coletivismo, América vs União Soviética.",
      'polgar_kasparov': "Moscou, 2002. Judit Polgár desafiava não apenas o maior jogador da história, mas séculos de preconceito. O xadrez feminino nunca mais seria o mesmo.",
      'anand_carlsen': "Chennai, coração pulsante do xadrez indiano. Anand defendia não apenas um título, mas o orgulho de uma civilização milenar que inventou o jogo."
    };
    
    await this.typeText(contextDiv, `🌍 CONTEXTO HISTÓRICO:\n\n${culturalIntros[this.currentGame.id]}`, 40);
    await this.delay(3000);
  }

  async displayEngineLoading() {
    const loadingSteps = [
      '⚡ Inicializando Aeon Chess Engine...',
      '🔍 Carregando base de dados histórica (12M+ partidas)...',
      '🧠 Ativando análise cultural IA...',
      '📊 Profundidade de análise: 22 plies',
      '✅ Sistema pronto para narração imersiva'
    ];
    
    for (const step of loadingSteps) {
      const stepDiv = document.createElement('div');
      stepDiv.className = 'text-yellow-400 mb-1';
      await this.typeText(stepDiv, step, 50);
      await this.delay(600);
    }
    
    await this.delay(1000);
  }

  async playMovesWithNarration() {
    const moves = this.currentGame.moves;
    const commentary = this.currentGame.commentary;
    
    for (let i = 0; i < moves.length && this.isAnimating; i++) {
      const move = moves[i];
      
      // Exibe movimento
      await this.displayMove(move, i);
      
      // Análise da IA
      await this.displayAnalysis(move, i);
      
      // Comentário cultural (se existir)
      if (commentary[move.ply]) {
        await this.displayCommentary(commentary[move.ply]);
      }
      
      // Tabuleiro ASCII em momentos-chave
      if (i % 3 === 0 || commentary[move.ply]?.type === 'brilliance') {
        await this.displayASCIIBoard(move.ply);
      }
      
      await this.delay(this.animationSpeed);
    }
  }

  async displayMove(move, index) {
    const moveDiv = document.createElement('div');
    moveDiv.className = 'text-yellow-400 mb-2 font-bold';
    
    const playerName = move.side === 'white' ? this.currentGame.info.white.split(' ')[0] : this.currentGame.info.black.split(' ')[0];
    const sideText = move.side === 'white' ? 'Brancas' : 'Pretas';
    
    const content = `[${move.time}] ${playerName} (${sideText}): ${move.move}`;
    await this.typeText(moveDiv, content, 40);
  }

  async displayAnalysis(move, index) {
    const analysisDiv = document.createElement('div');
    analysisDiv.className = 'text-green-400 mb-2 ml-4';
    
    const winProb = parseFloat(move.eval.replace('+', '').replace('=', '0'));
    const whiteWin = Math.max(0, Math.min(100, 50 + winProb * 15));
    const blackWin = 100 - whiteWin;
    const depth = Math.min(index + 12, 22);
    
    const content = `→ Avaliação: ${move.eval} | Profundidade: ${depth} plies\n→ Probabilidade: Brancas ${whiteWin.toFixed(1)}% | Pretas ${blackWin.toFixed(1)}%`;
    
    analysisDiv.innerHTML = content.replace(/\n/g, '<br>');
    this.terminalOutput.appendChild(analysisDiv);
    this.scrollToBottom();
    await this.delay(800);
  }

  async displayCommentary(commentary) {
    const commentDiv = document.createElement('div');
    let className = 'text-blue-300 italic mb-3 ml-2';
    
    if (commentary.type === 'brilliance') {
      className = 'text-yellow-300 font-bold mb-3 bg-yellow-900 bg-opacity-20 p-3 rounded border border-yellow-600';
    } else if (commentary.type === 'decisive') {
      className = 'text-red-300 font-bold mb-3 bg-red-900 bg-opacity-20 p-3 rounded border border-red-600';
    }
    
    commentDiv.className = className;
    
    await this.typeText(commentDiv, `💭 "${commentary.text}"`, 25);
    
    if (commentary.cultural) {
      const culturalDiv = document.createElement('div');
      culturalDiv.className = 'text-purple-400 mt-3 mb-3 border-l-2 border-purple-400 pl-4 ml-2';
      culturalDiv.innerHTML = `🌍 <strong>Contexto Cultural:</strong> ${commentary.cultural}`;
      this.terminalOutput.appendChild(culturalDiv);
      this.scrollToBottom();
      await this.delay(2000);
    }
  }

  async displayASCIIBoard(ply) {
    const boardDiv = document.createElement('div');
    boardDiv.className = 'text-gray-300 mb-4 ml-2';
    
    // ASCII board simplificado (seria integrado com Chess.js real)
    const board = `
    a   b   c   d   e   f   g   h
  ┌───┬───┬───┬───┬───┬───┬───┬───┐
8 │ ♜ │ ♞ │ ♝ │ ♛ │ ♚ │ ♝ │ ♞ │ ♜ │ 8
  ├───┼───┼───┼───┼───┼───┼───┼───┤
7 │ ♟ │ ♟ │ ♟ │   │   │ ♟ │ ♟ │ ♟ │ 7
  ├───┼───┼───┼───┼───┼───┼───┼───┤
6 │   │   │   │   │ ♟ │ ♞ │   │   │ 6
  ├───┼───┼───┼───┼───┼───┼───┼───┤
5 │   │   │   │ ♟ │   │   │   │   │ 5
  ├───┼───┼───┼───┼───┼───┼───┼───┤
4 │   │   │ ♙ │ ♙ │   │   │   │   │ 4
  ├───┼───┼───┼───┼───┼───┼───┼───┤
3 │   │   │ ♘ │   │   │ ♘ │   │   │ 3
  ├───┼───┼───┼───┼───┼───┼───┼───┤
2 │ ♙ │ ♙ │   │   │ ♙ │ ♙ │ ♙ │ ♙ │ 2
  ├───┼───┼───┼───┼───┼───┼───┼───┤
1 │ ♖ │   │ ♗ │ ♕ │ ♔ │ ♗ │   │ ♖ │ 1
  └───┴───┴───┴───┴───┴───┴───┴───┘
    a   b   c   d   e   f   g   h
    `;
    
    boardDiv.innerHTML = `<pre class="text-xs">${board}</pre>`;
    this.terminalOutput.appendChild(boardDiv);
    this.scrollToBottom();
    await this.delay(1500);
  }

  async displayConclusion() {
    const result = this.currentGame.info.result;
    const winner = result === '1-0' ? this.currentGame.info.white : 
                   result === '0-1' ? this.currentGame.info.black : 'Empate';
    
    // Resultado final
    const resultDiv = document.createElement('div');
    resultDiv.className = 'text-red-400 font-bold mb-4 bg-red-900 bg-opacity-20 p-4 rounded border border-red-600';
    
    const resultText = result === '1/2-1/2' ? 
      '🤝 EMPATE! Uma batalha épica que termina em igualdade.' :
      `🏆 VITÓRIA DE ${winner.toUpperCase()}!\n\n${this.currentGame.info.significance}`;
    
    resultDiv.innerHTML = resultText;
    this.terminalOutput.appendChild(resultDiv);
    this.scrollToBottom();
    await this.delay(2000);
    
    // Estatísticas culturais
    const statsDiv = document.createElement('div');
    statsDiv.className = 'text-purple-400 mb-4 border-l-2 border-purple-400 pl-4';
    
    const stats = `
📊 <strong>ANÁLISE CULTURAL FINAL:</strong>
• Estilo ${this.currentGame.info.white}: Precisão ${88 + Math.random() * 10}%
• Estilo ${this.currentGame.info.black}: Precisão ${85 + Math.random() * 12}%
• Impacto histórico: ${this.getHistoricalImpact()}
• Influência cultural: ${this.getCulturalInfluence()}
    `.trim();
    
    statsDiv.innerHTML = stats;
    this.terminalOutput.appendChild(statsDiv);
    this.scrollToBottom();
    await this.delay(3000);
  }

  getHistoricalImpact() {
    const impacts = [
      "Mudança de paradigma no xadrez mundial",
      "Inspiração para nova geração de jogadores", 
      "Redefinição de conceitos estratégicos",
      "Marco na democratização do xadrez",
      "Quebra de barreiras culturais e sociais"
    ];
    return impacts[Math.floor(Math.random() * impacts.length)];
  }

  getCulturalInfluence() {
    const influences = [
      "Inspirou filmes e documentários",
      "Influenciou política internacional",
      "Transformou educação enxadrística",
      "Criou novos ídolos regionais",
      "Expandiu fronteiras culturais"
    ];
    return influences[Math.floor(Math.random() * influences.length)];
  }

  async typeText(element, text, speed = 50) {
    return new Promise((resolve) => {
      let i = 0;
      element.innerHTML = '';
      this.terminalOutput.appendChild(element);
      
      const timer = setInterval(() => {
        if (i < text.length && this.isAnimating) {
          element.innerHTML += text.charAt(i);
          i++;
          this.scrollToBottom();
        } else {
          clearInterval(timer);
          resolve();
        }
      }, speed);
    });
  }

  scrollToBottom() {
    this.terminalOutput.scrollTop = this.terminalOutput.scrollHeight;
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  stop() {
    this.isAnimating = false;
  }

  // Interface pública
  start() {
    this.startCulturalExperience();
  }

  switchToExperience(experienceId) {
    const index = this.culturalExperiences.findIndex(exp => exp.id === experienceId);
    if (index !== -1) {
      this.currentExperience = index;
      this.stop();
      setTimeout(() => this.start(), 500);
    }
  }
}

// 🚀 INICIALIZAÇÃO AUTOMÁTICA
document.addEventListener('DOMContentLoaded', function() {
  // Aguarda outros sistemas carregarem
  setTimeout(() => {
    const terminal = new AeonTerminalCultural('terminal-output');
    
    // Inicia automaticamente
    terminal.start();
    
    // Integra com controles da landing page
    const continueBtn = document.querySelector('[data-terminal-continue]');
    if (continueBtn) {
      continueBtn.addEventListener('click', () => terminal.start());
    }
    
    // Para quando usuário sai da seção
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0];
      if (!entry.isIntersecting) {
        terminal.stop();
      } else {
        setTimeout(() => terminal.start(), 1000);
      }
    });
    
    const terminalSection = document.getElementById('terminal-demo');
    if (terminalSection) {
      observer.observe(terminalSection);
    }
    
    // Expõe globalmente para controle
    window.aeonTerminal = terminal;
  }, 2000);
});
