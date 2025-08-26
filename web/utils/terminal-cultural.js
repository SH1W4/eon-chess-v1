// AEON CHESS - Terminal Cultural Interativo
// Versão: 1.0 - Experiências Históricas e Narrativas

class AeonTerminal {
    constructor() {
        this.currentExperience = null;
        this.isRunning = false;
        this.outputElement = null;
        this.experiences = {
            fischer_spassky: {
                title: "Fischer vs Spassky (1972)",
                description: "O 'Match do Século' - Reykjavik, Islândia",
                moves: [{
                        move: "1.e4",
                        narration: "Fischer abre com e4, uma jogada clássica que controla o centro e libera o bispo e a dama."
                    },
                    {
                        move: "1...c5",
                        narration: "Spassky responde com a Defesa Siciliana, uma das mais populares contra e4."
                    },
                    {
                        move: "2.Nf3",
                        narration: "Fischer desenvolve o cavalo para f3, atacando o peão em e5 e preparando o roque."
                    },
                    {
                        move: "2...d6",
                        narration: "Spassky protege o peão c5 e prepara o desenvolvimento do bispo."
                    },
                    {
                        move: "3.d4",
                        narration: "Fischer abre o centro, criando tensão na posição."
                    },
                    {
                        move: "3...cxd4",
                        narration: "Spassky captura, abrindo a coluna c para suas peças."
                    },
                    {
                        move: "4.Nxd4",
                        narration: "Fischer recaptura com o cavalo, mantendo pressão no centro."
                    },
                    {
                        move: "4...Nf6",
                        narration: "Spassky desenvolve o cavalo, atacando o peão e4."
                    },
                    {
                        move: "5.Nc3",
                        narration: "Fischer protege o peão e4 e desenvolve o cavalo da dama."
                    },
                    {
                        move: "5...a6",
                        narration: "Spassky joga a6, preparando b5 para expandir no flanco da dama."
                    }
                ]
            },
            polgar_kasparov: {
                title: "Polgár vs Kasparov (2002)",
                description: "Judite Polgár desafia o campeão mundial",
                moves: [{
                        move: "1.d4",
                        narration: "Polgár abre com d4, controlando o centro e preparando o desenvolvimento."
                    },
                    {
                        move: "1...Nf6",
                        narration: "Kasparov responde com a Defesa Índia, flexível e sólida."
                    },
                    {
                        move: "2.c4",
                        narration: "Polgár expande no flanco da dama, controlando mais casas centrais."
                    },
                    {
                        move: "2...e6",
                        narration: "Kasparov prepara o desenvolvimento do bispo da dama."
                    },
                    {
                        move: "3.Nc3",
                        narration: "Polgár desenvolve o cavalo, atacando o centro."
                    },
                    {
                        move: "3...Bb4",
                        narration: "Kasparov pinça o cavalo, criando tensão na posição."
                    },
                    {
                        move: "4.Qc2",
                        narration: "Polgár protege o cavalo e prepara o desenvolvimento."
                    },
                    {
                        move: "4...O-O",
                        narration: "Kasparov faz o roque, protegendo o rei."
                    },
                    {
                        move: "5.a3",
                        narration: "Polgár força o bispo a se mover ou trocar."
                    },
                    {
                        move: "5...Bxc3+",
                        narration: "Kasparov troca, dobrando os peões de Polgár."
                    }
                ]
            }
        };
        this.init();
    }

    init() {
        this.outputElement = document.getElementById('terminal-output');
        if (this.outputElement) {
            this.outputElement.innerHTML = this.getWelcomeMessage();
        }
    }

    getWelcomeMessage() {
        return `
<span style="color: #00ff00;">aeon-chess@terminal:~$</span> <span style="color: #ffffff;">./aeon-chess --cultural-mode</span>

<span style="color: #00ffff;">╔══════════════════════════════════════════════════════════════╗</span>
<span style="color: #00ffff;">║                    AEON CHESS - TERMINAL CULTURAL             ║</span>
<span style="color: #00ffff;">║                                                              ║</span>
<span style="color: #00ffff;">║  Bem-vindo ao modo cultural do Aeon Chess!                  ║</span>
<span style="color: #00ffff;">║  Aqui você pode reviver as maiores partidas da história     ║</span>
<span style="color: #00ffff;">║  do xadrez com narração detalhada e contexto histórico.     ║</span>
<span style="color: #00ffff;">╚══════════════════════════════════════════════════════════════╝</span>

<span style="color: #ffff00;">Experiências disponíveis:</span>
<span style="color: #ffffff;">• fischer_spassky</span> - O "Match do Século" (1972)
<span style="color: #ffffff;">• polgar_kasparov</span> - Judite Polgár vs Kasparov (2002)

<span style="color: #00ff00;">aeon-chess@terminal:~$</span> <span style="color: #ffffff;">Digite 'start' para começar ou escolha uma experiência específica</span>

<span style="color: #00ff00;">aeon-chess@terminal:~$</span> <span style="color: #ffffff;">_</span>
        `;
    }

    startExperience(experienceName = null) {
        if (this.isRunning) return;

        const experience = experienceName ? this.experiences[experienceName] : this.experiences.fischer_spassky;
        if (!experience) {
            this.typeMessage("Experiência não encontrada. Use 'fischer_spassky' ou 'polgar_kasparov'");
            return;
        }

        this.currentExperience = experience;
        this.isRunning = true;
        this.outputElement.innerHTML = '';

        this.typeMessage(`<span style="color: #00ffff;">Iniciando experiência: ${experience.title}</span>`);
        this.typeMessage(`<span style="color: #ffff00;">${experience.description}</span>`);
        this.typeMessage("");
        this.typeMessage("<span style='color: #ffffff;'>Pressione ENTER para continuar...</span>");

        setTimeout(() => {
            this.playMoves(experience.moves, 0);
        }, 2000);
    }

    playMoves(moves, index) {
        if (index >= moves.length || !this.isRunning) {
            this.finishExperience();
            return;
        }

        const move = moves[index];
        this.typeMessage("");
        this.typeMessage(`<span style="color: #00ff00;">Movimento ${index + 1}:</span> <span style="color: #ffffff; font-weight: bold;">${move.move}</span>`);
        this.typeMessage(`<span style="color: #cccccc; font-style: italic;">${move.narration}</span>`);
        this.typeMessage("");

        setTimeout(() => {
            this.playMoves(moves, index + 1);
        }, 3000);
    }

    finishExperience() {
        this.isRunning = false;
        this.typeMessage("");
        this.typeMessage("<span style='color: #00ff00;'>Experiência concluída!</span>");
        this.typeMessage("<span style='color: #ffffff;'>Digite 'restart' para recomeçar ou escolha outra experiência.</span>");
    }

    typeMessage(message, delay = 100) {
        if (!this.outputElement) return;

        const messageElement = document.createElement('div');
        messageElement.innerHTML = message;
        this.outputElement.appendChild(messageElement);
        this.outputElement.scrollTop = this.outputElement.scrollHeight;

        setTimeout(() => {
            messageElement.style.opacity = '1';
        }, delay);
    }

    switchToExperience(experienceName) {
        if (this.experiences[experienceName]) {
            this.startExperience(experienceName);
        } else {
            this.typeMessage(`<span style="color: #ff0000;">Experiência '${experienceName}' não encontrada.</span>`);
        }
    }

    // Métodos públicos para integração
    startExperience() {
        this.startExperience();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.aeonTerminal = new AeonTerminal();
});