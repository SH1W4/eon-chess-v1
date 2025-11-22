// AEON CHESS - Análise Narrativa de Jogos Históricos
// Versão: 1.0 - Sistema Completo de Análise

class NarrativeAnalysis {
    constructor() {
        this.currentGame = null;
        this.currentMoveIndex = 0;
        this.gameHistory = [];
        this.chess = null;
        this.board = null;
        this.isAutoPlaying = false;
        this.autoPlayInterval = null;

        this.games = {
            'fischer-spassky': {
                title: 'Fischer vs Spassky',
                subtitle: 'O "Match do Século" - Reykjavik, Islândia',
                year: 1972,
                players: {
                    white: 'Bobby Fischer',
                    black: 'Boris Spassky'
                },
                context: 'Este foi o match pelo Campeonato Mundial de Xadrez de 1972, disputado em Reykjavik, Islândia. Fischer, representando os EUA, enfrentou o campeão mundial Spassky, da URSS, em plena Guerra Fria. O match teve enorme significado político e cultural.',
                moves: [{
                        move: '1.e4',
                        algebraic: 'e4',
                        narrative: 'Fischer abre com e4, uma jogada clássica que controla o centro e libera o bispo e a dama. Esta é uma das aberturas mais populares e agressivas do xadrez.',
                        evaluation: 0.2,
                        context: 'Fischer era conhecido por suas aberturas agressivas e este movimento estabelece controle imediato do centro.'
                    },
                    {
                        move: '1...c5',
                        algebraic: 'c5',
                        narrative: 'Spassky responde com a Defesa Siciliana, uma das mais populares e dinâmicas contra e4. Esta abertura leva a posições complexas e táticas.',
                        evaluation: 0.1,
                        context: 'A Siciliana é uma escolha sólida que Spassky dominava profundamente.'
                    },
                    {
                        move: '2.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'Fischer desenvolve o cavalo para f3, atacando o peão em e5 e preparando o roque. Esta é a continuação mais natural e forte.',
                        evaluation: 0.3,
                        context: 'O desenvolvimento natural do cavalo mantém a pressão no centro.'
                    },
                    {
                        move: '2...d6',
                        algebraic: 'd6',
                        narrative: 'Spassky protege o peão c5 e prepara o desenvolvimento do bispo. Esta é uma continuação sólida da Siciliana.',
                        evaluation: 0.2,
                        context: 'A proteção do peão c5 é essencial para a estrutura da Siciliana.'
                    },
                    {
                        move: '3.d4',
                        algebraic: 'd4',
                        narrative: 'Fischer abre o centro, criando tensão na posição. Esta é uma jogada tática que força o adversário a tomar uma decisão.',
                        evaluation: 0.4,
                        context: 'A abertura do centro é típica das posições da Siciliana e leva a jogo dinâmico.'
                    },
                    {
                        move: '3...cxd4',
                        algebraic: 'cxd4',
                        narrative: 'Spassky captura, abrindo a coluna c para suas peças. Esta é a resposta mais comum e correta.',
                        evaluation: 0.3,
                        context: 'A captura é forçada e mantém a igualdade na posição.'
                    },
                    {
                        move: '4.Nxd4',
                        algebraic: 'Nxd4',
                        narrative: 'Fischer recaptura com o cavalo, mantendo pressão no centro. O cavalo em d4 é uma peça forte.',
                        evaluation: 0.5,
                        context: 'O cavalo em d4 controla importantes casas centrais e pode atacar em várias direções.'
                    },
                    {
                        move: '4...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'Spassky desenvolve o cavalo, atacando o peão e4. Esta é uma continuação natural e forte.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo para f6 é uma das principais ideias da Siciliana.'
                    },
                    {
                        move: '5.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'Fischer protege o peão e4 e desenvolve o cavalo da dama. A posição está se tornando mais complexa.',
                        evaluation: 0.6,
                        context: 'O desenvolvimento do cavalo para c3 protege o peão e4 e prepara o roque.'
                    },
                    {
                        move: '5...a6',
                        algebraic: 'a6',
                        narrative: 'Spassky joga a6, preparando b5 para expandir no flanco da dama. Esta é uma ideia típica da Siciliana.',
                        evaluation: 0.5,
                        context: 'A jogada a6 prepara a expansão no flanco da dama com b5, uma ideia fundamental da Siciliana.'
                    }
                ]
            },
            'kasparov-deepblue': {
                title: 'Kasparov vs Deep Blue',
                subtitle: 'O homem contra a máquina - Nova York',
                year: 1997,
                players: {
                    white: 'Garry Kasparov',
                    black: 'Deep Blue (IBM)'
                },
                context: 'Este foi o match histórico entre o campeão mundial Garry Kasparov e o supercomputador Deep Blue da IBM. A vitória da máquina marcou um momento crucial na história da IA e do xadrez.',
                moves: [{
                        move: '1.e4',
                        algebraic: 'e4',
                        narrative: 'Kasparov abre com e4, controlando o centro. Uma escolha clássica e agressiva.',
                        evaluation: 0.2,
                        context: 'Kasparov era conhecido por seu jogo agressivo e e4 é uma abertura que permite iniciativa.'
                    },
                    {
                        move: '1...c6',
                        algebraic: 'c6',
                        narrative: 'Deep Blue escolhe a Defesa Caro-Kann, uma abertura sólida e defensiva.',
                        evaluation: 0.1,
                        context: 'A Caro-Kann é uma abertura sólida que evita posições táticas complexas.'
                    },
                    {
                        move: '2.d4',
                        algebraic: 'd4',
                        narrative: 'Kasparov expande no centro, criando tensão na posição.',
                        evaluation: 0.3,
                        context: 'A expansão no centro é natural e forte contra a Caro-Kann.'
                    },
                    {
                        move: '2...d5',
                        algebraic: 'd5',
                        narrative: 'Deep Blue contesta o centro, criando uma posição de peões fixos.',
                        evaluation: 0.2,
                        context: 'A contestação do centro é a ideia principal da Caro-Kann.'
                    },
                    {
                        move: '3.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'Kasparov desenvolve o cavalo, atacando o peão d5.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo para c3 é a continuação mais agressiva.'
                    },
                    {
                        move: '3...dxe4',
                        algebraic: 'dxe4',
                        narrative: 'Deep Blue captura, simplificando a posição.',
                        evaluation: 0.3,
                        context: 'A captura é forçada e leva a uma posição mais simples.'
                    },
                    {
                        move: '4.Nxe4',
                        algebraic: 'Nxe4',
                        narrative: 'Kasparov recaptura, mantendo pressão no centro.',
                        evaluation: 0.5,
                        context: 'O cavalo em e4 é uma peça forte que controla importantes casas.'
                    },
                    {
                        move: '4...Bf5',
                        algebraic: 'Bf5',
                        narrative: 'Deep Blue desenvolve o bispo, atacando o cavalo.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do bispo para f5 é uma ideia típica da Caro-Kann.'
                    },
                    {
                        move: '5.Ng3',
                        algebraic: 'Ng3',
                        narrative: 'Kasparov recua o cavalo, mantendo a estrutura.',
                        evaluation: 0.6,
                        context: 'O recuo do cavalo mantém a pressão e prepara o desenvolvimento.'
                    },
                    {
                        move: '5...Bg6',
                        algebraic: 'Bg6',
                        narrative: 'Deep Blue recua o bispo, mantendo a proteção.',
                        evaluation: 0.5,
                        context: 'O recuo do bispo mantém a proteção e prepara o roque.'
                    }
                ]
            },
            'morphy-duke': {
                title: 'Morphy vs Duke & Count',
                subtitle: 'A "Opera House Game" - Paris',
                year: 1858,
                players: {
                    white: 'Paul Morphy',
                    black: 'Duke Karl & Count Isouard'
                },
                context: 'Este é um dos jogos mais famosos da história do xadrez. Morphy jogou contra dois adversários simultaneamente em uma ópera de Paris, demonstrando genialidade tática.',
                moves: [{
                        move: '1.e4',
                        algebraic: 'e4',
                        narrative: 'Morphy abre com e4, controlando o centro. Uma abertura clássica e agressiva.',
                        evaluation: 0.2,
                        context: 'Morphy era conhecido por seu jogo agressivo e tático.'
                    },
                    {
                        move: '1...e5',
                        algebraic: 'e5',
                        narrative: 'Os adversários respondem simetricamente, controlando o centro.',
                        evaluation: 0.1,
                        context: 'A resposta simétrica é natural e mantém a igualdade.'
                    },
                    {
                        move: '2.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'Morphy desenvolve o cavalo, atacando o peão e5.',
                        evaluation: 0.3,
                        context: 'O desenvolvimento do cavalo para f3 é natural e forte.'
                    },
                    {
                        move: '2...d6',
                        algebraic: 'd6',
                        narrative: 'Os adversários protegem o peão e5, mas bloqueiam o bispo.',
                        evaluation: 0.0,
                        context: 'Esta jogada protege o peão mas limita o desenvolvimento.'
                    },
                    {
                        move: '3.d4',
                        algebraic: 'd4',
                        narrative: 'Morphy abre o centro, criando tensão.',
                        evaluation: 0.5,
                        context: 'A abertura do centro dá iniciativa às brancas.'
                    },
                    {
                        move: '3...Bg4',
                        algebraic: 'Bg4',
                        narrative: 'Os adversários desenvolvem o bispo, pinçando o cavalo.',
                        evaluation: 0.2,
                        context: 'O pin do cavalo é uma ideia tática, mas pode ser perigoso.'
                    },
                    {
                        move: '4.dxe5',
                        algebraic: 'dxe5',
                        narrative: 'Morphy captura, abrindo a posição.',
                        evaluation: 0.7,
                        context: 'A captura abre a posição e dá vantagem às brancas.'
                    },
                    {
                        move: '4...Bxf3',
                        algebraic: 'Bxf3',
                        narrative: 'Os adversários capturam o cavalo, mas perdem tempo.',
                        evaluation: 0.9,
                        context: 'A captura do cavalo perde tempo e dá vantagem às brancas.'
                    },
                    {
                        move: '5.Qxf3',
                        algebraic: 'Qxf3',
                        narrative: 'Morphy recaptura com a dama, mantendo pressão.',
                        evaluation: 1.2,
                        context: 'A dama em f3 é muito forte e ameaça o rei adversário.'
                    },
                    {
                        move: '5...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'Os adversários desenvolvem o cavalo, mas a posição está difícil.',
                        evaluation: 1.0,
                        context: 'O desenvolvimento do cavalo é necessário mas insuficiente.'
                    }
                ]
            },
            'polgar-kasparov': {
                title: 'Polgár vs Kasparov',
                subtitle: 'Judite Polgár desafia o campeão mundial',
                year: 2002,
                players: {
                    white: 'Judite Polgár',
                    black: 'Garry Kasparov'
                },
                context: 'Judite Polgár, uma das maiores jogadoras da história, enfrentou o campeão mundial Garry Kasparov em 2002. Este jogo demonstrou o alto nível técnico de Polgár e sua capacidade de competir com os melhores.',
                moves: [{
                        move: '1.d4',
                        algebraic: 'd4',
                        narrative: 'Polgár abre com d4, controlando o centro e preparando o desenvolvimento. Esta é uma abertura sólida e posicional.',
                        evaluation: 0.2,
                        context: 'Polgár era conhecida por seu jogo sólido e posicional, e d4 reflete esse estilo.'
                    },
                    {
                        move: '1...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'Kasparov responde com a Defesa Índia, flexível e sólida. Esta abertura permite jogo dinâmico.',
                        evaluation: 0.1,
                        context: 'Kasparov era mestre em posições dinâmicas e a Defesa Índia oferece muitas possibilidades.'
                    },
                    {
                        move: '2.c4',
                        algebraic: 'c4',
                        narrative: 'Polgár expande no flanco da dama, controlando mais casas centrais. Esta é uma continuação natural.',
                        evaluation: 0.3,
                        context: 'A expansão no flanco da dama é típica das aberturas indianas.'
                    },
                    {
                        move: '2...e6',
                        algebraic: 'e6',
                        narrative: 'Kasparov prepara o desenvolvimento do bispo da dama. Esta é uma continuação sólida.',
                        evaluation: 0.2,
                        context: 'A preparação do desenvolvimento do bispo é fundamental na Defesa Índia.'
                    },
                    {
                        move: '3.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'Polgár desenvolve o cavalo, atacando o centro. A posição está se tornando mais complexa.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo para c3 é natural e forte.'
                    },
                    {
                        move: '3...Bb4',
                        algebraic: 'Bb4',
                        narrative: 'Kasparov pinça o cavalo, criando tensão na posição. Esta é uma ideia tática importante.',
                        evaluation: 0.3,
                        context: 'O pin do cavalo é uma ideia tática fundamental na Defesa Índia.'
                    },
                    {
                        move: '4.Qc2',
                        algebraic: 'Qc2',
                        narrative: 'Polgár protege o cavalo e prepara o desenvolvimento. Esta é uma resposta sólida.',
                        evaluation: 0.5,
                        context: 'A proteção do cavalo é essencial para manter a estrutura da posição.'
                    },
                    {
                        move: '4...O-O',
                        algebraic: 'O-O',
                        narrative: 'Kasparov faz o roque, protegendo o rei. Esta é uma jogada de segurança importante.',
                        evaluation: 0.4,
                        context: 'O roque é fundamental para a segurança do rei em posições abertas.'
                    },
                    {
                        move: '5.a3',
                        algebraic: 'a3',
                        narrative: 'Polgár força o bispo a se mover ou trocar. Esta é uma jogada tática.',
                        evaluation: 0.6,
                        context: 'A jogada a3 força o bispo a tomar uma decisão, criando tensão na posição.'
                    },
                    {
                        move: '5...Bxc3+',
                        algebraic: 'Bxc3+',
                        narrative: 'Kasparov troca, dobrando os peões de Polgár. Esta é uma continuação tática.',
                        evaluation: 0.5,
                        context: 'A troca do bispo pelo cavalo é uma ideia tática que dobra os peões adversários.'
                    }
                ]
            },
            'capablanca-alekhine': {
                title: 'Capablanca vs Alekhine',
                subtitle: 'O fim de uma era - Buenos Aires',
                year: 1927,
                players: {
                    white: 'José Capablanca',
                    black: 'Alexander Alekhine'
                },
                context: 'Este foi o match pelo Campeonato Mundial de Xadrez de 1927, disputado em Buenos Aires. Capablanca, o campeão mundial, enfrentou o desafiante Alekhine. O match marcou o fim do reinado de Capablanca.',
                moves: [{
                        move: '1.d4',
                        algebraic: 'd4',
                        narrative: 'Capablanca abre com d4, controlando o centro. Esta é uma abertura sólida e posicional.',
                        evaluation: 0.2,
                        context: 'Capablanca era conhecido por seu jogo posicional e d4 reflete esse estilo.'
                    },
                    {
                        move: '1...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'Alekhine responde com a Defesa Índia, flexível e dinâmica. Esta abertura permite jogo complexo.',
                        evaluation: 0.1,
                        context: 'Alekhine era mestre em posições complexas e a Defesa Índia oferece muitas possibilidades.'
                    },
                    {
                        move: '2.c4',
                        algebraic: 'c4',
                        narrative: 'Capablanca expande no flanco da dama, controlando mais casas centrais. Esta é uma continuação natural.',
                        evaluation: 0.3,
                        context: 'A expansão no flanco da dama é típica das aberturas indianas.'
                    },
                    {
                        move: '2...e6',
                        algebraic: 'e6',
                        narrative: 'Alekhine prepara o desenvolvimento do bispo da dama. Esta é uma continuação sólida.',
                        evaluation: 0.2,
                        context: 'A preparação do desenvolvimento do bispo é fundamental na Defesa Índia.'
                    },
                    {
                        move: '3.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'Capablanca desenvolve o cavalo, atacando o centro. A posição está se tornando mais complexa.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo para c3 é natural e forte.'
                    },
                    {
                        move: '3...Bb4',
                        algebraic: 'Bb4',
                        narrative: 'Alekhine pinça o cavalo, criando tensão na posição. Esta é uma ideia tática importante.',
                        evaluation: 0.3,
                        context: 'O pin do cavalo é uma ideia tática fundamental na Defesa Índia.'
                    },
                    {
                        move: '4.Qc2',
                        algebraic: 'Qc2',
                        narrative: 'Capablanca protege o cavalo e prepara o desenvolvimento. Esta é uma resposta sólida.',
                        evaluation: 0.5,
                        context: 'A proteção do cavalo é essencial para manter a estrutura da posição.'
                    },
                    {
                        move: '4...O-O',
                        algebraic: 'O-O',
                        narrative: 'Alekhine faz o roque, protegendo o rei. Esta é uma jogada de segurança importante.',
                        evaluation: 0.4,
                        context: 'O roque é fundamental para a segurança do rei em posições abertas.'
                    },
                    {
                        move: '5.a3',
                        algebraic: 'a3',
                        narrative: 'Capablanca força o bispo a se mover ou trocar. Esta é uma jogada tática.',
                        evaluation: 0.6,
                        context: 'A jogada a3 força o bispo a tomar uma decisão, criando tensão na posição.'
                    },
                    {
                        move: '5...Bxc3+',
                        algebraic: 'Bxc3+',
                        narrative: 'Alekhine troca, dobrando os peões de Capablanca. Esta é uma continuação tática.',
                        evaluation: 0.5,
                        context: 'A troca do bispo pelo cavalo é uma ideia tática que dobra os peões adversários.'
                    }
                ]
            },
            'magnus-carlsen': {
                title: 'Magnus Carlsen vs Anand',
                subtitle: 'O novo rei do xadrez - Chennai',
                year: 2013,
                players: {
                    white: 'Magnus Carlsen',
                    black: 'Viswanathan Anand'
                },
                context: 'Este foi o match pelo Campeonato Mundial de Xadrez de 2013, onde o jovem Magnus Carlsen, com apenas 22 anos, derrotou o campeão Viswanathan Anand, marcando o início de uma nova era no xadrez.',
                moves: [{
                        move: '1.e4',
                        algebraic: 'e4',
                        narrative: 'Carlsen abre com e4, controlando o centro. Uma escolha clássica e agressiva.',
                        evaluation: 0.2,
                        context: 'Carlsen é conhecido por seu jogo universal e e4 é uma abertura que permite muitas possibilidades.'
                    },
                    {
                        move: '1...e5',
                        algebraic: 'e5',
                        narrative: 'Anand responde simetricamente, controlando o centro.',
                        evaluation: 0.1,
                        context: 'A resposta simétrica é natural e mantém a igualdade na posição.'
                    },
                    {
                        move: '2.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'Carlsen desenvolve o cavalo, atacando o peão e5.',
                        evaluation: 0.3,
                        context: 'O desenvolvimento do cavalo para f3 é natural e forte.'
                    },
                    {
                        move: '2...Nc6',
                        algebraic: 'Nc6',
                        narrative: 'Anand protege o peão e5 com o cavalo, preparando o desenvolvimento.',
                        evaluation: 0.2,
                        context: 'A proteção do peão com o cavalo é uma continuação natural.'
                    },
                    {
                        move: '3.Bb5',
                        algebraic: 'Bb5',
                        narrative: 'Carlsen desenvolve o bispo, pinçando o cavalo. Esta é a Abertura Ruy Lopez.',
                        evaluation: 0.4,
                        context: 'A Ruy Lopez é uma das aberturas mais antigas e respeitadas do xadrez.'
                    },
                    {
                        move: '3...a6',
                        algebraic: 'a6',
                        narrative: 'Anand força o bispo a se mover, preparando b5.',
                        evaluation: 0.3,
                        context: 'A jogada a6 é uma continuação típica da Ruy Lopez.'
                    },
                    {
                        move: '4.Ba4',
                        algebraic: 'Ba4',
                        narrative: 'Carlsen recua o bispo, mantendo o pin.',
                        evaluation: 0.5,
                        context: 'O recuo do bispo mantém a pressão sobre o cavalo.'
                    },
                    {
                        move: '4...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'Anand desenvolve o cavalo, atacando o peão e4.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo para f6 é natural e forte.'
                    },
                    {
                        move: '5.O-O',
                        algebraic: 'O-O',
                        narrative: 'Carlsen faz o roque, protegendo o rei.',
                        evaluation: 0.6,
                        context: 'O roque é fundamental para a segurança do rei.'
                    },
                    {
                        move: '5...Be7',
                        algebraic: 'Be7',
                        narrative: 'Anand desenvolve o bispo, preparando o roque.',
                        evaluation: 0.5,
                        context: 'O desenvolvimento do bispo para e7 prepara o roque.'
                    }
                ]
            },
            'tal-botvinnik': {
                title: 'Tal vs Botvinnik',
                subtitle: 'O mago de Riga - Moscou',
                year: 1960,
                players: {
                    white: 'Mikhail Tal',
                    black: 'Mikhail Botvinnik'
                },
                context: 'Este foi o match pelo Campeonato Mundial de Xadrez de 1960, onde o jovem Mikhail Tal, conhecido como "O Mago de Riga", derrotou o campeão Botvinnik com seu jogo tático e agressivo.',
                moves: [{
                        move: '1.d4',
                        algebraic: 'd4',
                        narrative: 'Tal abre com d4, controlando o centro. Uma escolha sólida.',
                        evaluation: 0.2,
                        context: 'Tal era conhecido por seu jogo tático, mas também sabia jogar posicionalmente.'
                    },
                    {
                        move: '1...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'Botvinnik responde com a Defesa Índia, flexível e sólida.',
                        evaluation: 0.1,
                        context: 'Botvinnik era mestre em posições sólidas e a Defesa Índia reflete seu estilo.'
                    },
                    {
                        move: '2.c4',
                        algebraic: 'c4',
                        narrative: 'Tal expande no flanco da dama, controlando mais casas centrais.',
                        evaluation: 0.3,
                        context: 'A expansão no flanco da dama é típica das aberturas indianas.'
                    },
                    {
                        move: '2...g6',
                        algebraic: 'g6',
                        narrative: 'Botvinnik prepara o fianchetto do bispo, criando uma posição sólida.',
                        evaluation: 0.2,
                        context: 'O fianchetto do bispo é uma ideia fundamental da Defesa Índia.'
                    },
                    {
                        move: '3.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'Tal desenvolve o cavalo, atacando o centro.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo para c3 é natural e forte.'
                    },
                    {
                        move: '3...Bg7',
                        algebraic: 'Bg7',
                        narrative: 'Botvinnik completa o fianchetto, criando uma posição sólida.',
                        evaluation: 0.3,
                        context: 'O fianchetto do bispo cria uma posição sólida e flexível.'
                    },
                    {
                        move: '4.e4',
                        algebraic: 'e4',
                        narrative: 'Tal expande no centro, criando uma posição dinâmica.',
                        evaluation: 0.5,
                        context: 'A expansão no centro dá iniciativa às brancas.'
                    },
                    {
                        move: '4...d6',
                        algebraic: 'd6',
                        narrative: 'Botvinnik protege o peão e5, mantendo a estrutura.',
                        evaluation: 0.4,
                        context: 'A proteção do peão e5 é necessária para manter a estrutura.'
                    },
                    {
                        move: '5.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'Tal desenvolve o cavalo, preparando o roque.',
                        evaluation: 0.6,
                        context: 'O desenvolvimento do cavalo para f3 prepara o roque.'
                    },
                    {
                        move: '5...O-O',
                        algebraic: 'O-O',
                        narrative: 'Botvinnik faz o roque, protegendo o rei.',
                        evaluation: 0.5,
                        context: 'O roque é fundamental para a segurança do rei.'
                    }
                ]
            },

            // === PERSONAGENS E CULTURAS LENDÁRIAS ===
            'alexandria-ptolemaic': {
                title: 'Alexandria Ptolomaica',
                subtitle: 'A Biblioteca do Conhecimento - Egito Antigo',
                year: -300,
                players: {
                    white: 'Sábio Ptolomaico',
                    black: 'Estrategista Macedônico'
                },
                context: 'Na lendária Biblioteca de Alexandria, onde o conhecimento do mundo antigo era preservado, mestres do xadrez desenvolviam estratégias que combinavam matemática, filosofia e arte da guerra. Este jogo representa a síntese do conhecimento helenístico.',
                moves: [{
                        move: '1.e4',
                        algebraic: 'e4',
                        narrative: 'O Sábio Ptolomaico abre com e4, simbolizando a expansão do conhecimento e a busca pela verdade. Esta jogada representa a abertura da mente para novas possibilidades.',
                        evaluation: 0.2,
                        context: 'Na Alexandria antiga, e4 era visto como a "jogada da sabedoria", abrindo caminhos para o desenvolvimento harmonioso.'
                    },
                    {
                        move: '1...e5',
                        algebraic: 'e5',
                        narrative: 'O Estrategista Macedônico responde simetricamente, honrando a tradição militar de Alexandre. Esta é a resposta da experiência e da disciplina.',
                        evaluation: 0.1,
                        context: 'A resposta simétrica reflete o equilíbrio entre conhecimento teórico e experiência prática.'
                    },
                    {
                        move: '2.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'O cavalo avança como um guardião do conhecimento, protegendo o centro e preparando o desenvolvimento. Esta é a jogada do pensador estratégico.',
                        evaluation: 0.3,
                        context: 'O cavalo em f3 representa a proteção do conhecimento acumulado na biblioteca.'
                    },
                    {
                        move: '2...Nc6',
                        algebraic: 'Nc6',
                        narrative: 'O cavalo adversário se posiciona para defender, mostrando a importância da proteção e da preparação. Esta é a resposta do estrategista experiente.',
                        evaluation: 0.2,
                        context: 'A proteção do peão central é fundamental na filosofia militar macedônica.'
                    },
                    {
                        move: '3.Bb5',
                        algebraic: 'Bb5',
                        narrative: 'O bispo se desenvolve, pinçando o cavalo e criando tensão. Esta é a "Abertura Espanhola", que simboliza a influência cultural e intelectual.',
                        evaluation: 0.4,
                        context: 'O pin do cavalo representa a pressão intelectual e cultural exercida por Alexandria.'
                    },
                    {
                        move: '3...a6',
                        algebraic: 'a6',
                        narrative: 'A jogada a6 força o bispo a se mover, criando uma posição dinâmica. Esta é a resposta prática do estrategista.',
                        evaluation: 0.3,
                        context: 'A jogada a6 prepara a expansão no flanco da dama, uma ideia estratégica fundamental.'
                    },
                    {
                        move: '4.Ba4',
                        algebraic: 'Ba4',
                        narrative: 'O bispo recua, mantendo a pressão sobre o cavalo. Esta é a continuação natural que preserva a tensão na posição.',
                        evaluation: 0.5,
                        context: 'O recuo do bispo mantém a pressão intelectual e estratégica.'
                    },
                    {
                        move: '4...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'O cavalo se desenvolve, atacando o peão e4. Esta é a resposta ativa que busca iniciativa.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento ativo do cavalo reflete a filosofia militar agressiva.'
                    },
                    {
                        move: '5.O-O',
                        algebraic: 'O-O',
                        narrative: 'O roque protege o rei e conecta as torres. Esta é a jogada da segurança e da preparação para o meio-jogo.',
                        evaluation: 0.6,
                        context: 'O roque representa a proteção do conhecimento e da sabedoria acumulada.'
                    },
                    {
                        move: '5...Be7',
                        algebraic: 'Be7',
                        narrative: 'O bispo se desenvolve, preparando o roque. Esta é a continuação natural que busca segurança.',
                        evaluation: 0.5,
                        context: 'O desenvolvimento do bispo prepara a proteção do rei e a conexão das torres.'
                    }
                ]
            },

            'samurai-shogun': {
                title: 'Samurai vs Shogun',
                subtitle: 'A Arte da Guerra - Japão Feudal',
                year: 1600,
                players: {
                    white: 'Samurai Ronin',
                    black: 'Shogun Tokugawa'
                },
                context: 'No Japão feudal, durante o período Edo, um samurai ronin (sem mestre) desafia o próprio Shogun em uma partida que simboliza a tensão entre honra individual e poder centralizado. O xadrez aqui representa a estratégia militar e o código bushido.',
                moves: [{
                        move: '1.d4',
                        algebraic: 'd4',
                        narrative: 'O Samurai Ronin abre com d4, controlando o centro com determinação. Esta jogada representa a busca pela honra e pela verdade, mesmo em face do poder.',
                        evaluation: 0.2,
                        context: 'A jogada d4 simboliza a determinação do ronin em manter sua honra e princípios.'
                    },
                    {
                        move: '1...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'O Shogun responde com a Defesa Índia, flexível e poderosa. Esta é a resposta do poder estabelecido, que busca controlar sem se comprometer.',
                        evaluation: 0.1,
                        context: 'A Defesa Índia representa a flexibilidade e o poder do sistema shogunal.'
                    },
                    {
                        move: '2.c4',
                        algebraic: 'c4',
                        narrative: 'O Samurai expande no flanco da dama, mostrando sua determinação em lutar por seus ideais. Esta é a jogada da coragem e da convicção.',
                        evaluation: 0.3,
                        context: 'A expansão no flanco da dama representa a expansão dos ideais do bushido.'
                    },
                    {
                        move: '2...e6',
                        algebraic: 'e6',
                        narrative: 'O Shogun prepara o desenvolvimento, mantendo a flexibilidade. Esta é a resposta calculada do poder centralizado.',
                        evaluation: 0.2,
                        context: 'A preparação do desenvolvimento reflete a estratégia cuidadosa do shogunato.'
                    },
                    {
                        move: '3.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'O cavalo se desenvolve, atacando o centro. Esta é a jogada do guerreiro que busca iniciativa e honra.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo representa a busca pela iniciativa no campo de batalha.'
                    },
                    {
                        move: '3...Bb4',
                        algebraic: 'Bb4',
                        narrative: 'O bispo pinça o cavalo, criando tensão. Esta é a resposta tática do poder estabelecido.',
                        evaluation: 0.3,
                        context: 'O pin do cavalo representa a pressão exercida pelo sistema sobre o indivíduo.'
                    },
                    {
                        move: '4.Qc2',
                        algebraic: 'Qc2',
                        narrative: 'A dama protege o cavalo, mostrando a importância da proteção mútua. Esta é a jogada da lealdade e da honra.',
                        evaluation: 0.5,
                        context: 'A proteção do cavalo simboliza a proteção dos ideais e da honra.'
                    },
                    {
                        move: '4...O-O',
                        algebraic: 'O-O',
                        narrative: 'O Shogun faz o roque, protegendo seu rei. Esta é a jogada da segurança e da estabilidade.',
                        evaluation: 0.4,
                        context: 'O roque representa a proteção do poder centralizado e da estabilidade.'
                    },
                    {
                        move: '5.a3',
                        algebraic: 'a3',
                        narrative: 'O Samurai força o bispo a se mover, criando tensão. Esta é a jogada da coragem que desafia o poder.',
                        evaluation: 0.6,
                        context: 'A jogada a3 força uma decisão, representando o desafio direto ao poder estabelecido.'
                    },
                    {
                        move: '5...Bxc3+',
                        algebraic: 'Bxc3+',
                        narrative: 'O Shogun troca, dobrando os peões do Samurai. Esta é a resposta tática que busca vantagem material.',
                        evaluation: 0.5,
                        context: 'A troca representa o conflito entre poder centralizado e liberdade individual.'
                    }
                ]
            },

            'viking-king': {
                title: 'Viking vs Rei Cristão',
                subtitle: 'Conquista e Resistência - Norte da Europa',
                year: 900,
                players: {
                    white: 'Jarl Viking',
                    black: 'Rei Cristão'
                },
                context: 'Durante a Era Viking, um poderoso Jarl (nobre viking) enfrenta um rei cristão em uma partida que simboliza o conflito entre a cultura nórdica pagã e a nova ordem cristã. O xadrez aqui representa a estratégia de conquista e resistência.',
                moves: [{
                        move: '1.e4',
                        algebraic: 'e4',
                        narrative: 'O Jarl Viking abre com e4, controlando o centro com agressividade. Esta jogada representa a expansão viking e a busca por novos territórios.',
                        evaluation: 0.2,
                        context: 'A jogada e4 simboliza a expansão territorial e a agressividade viking.'
                    },
                    {
                        move: '1...e5',
                        algebraic: 'e5',
                        narrative: 'O Rei Cristão responde simetricamente, defendendo seu território. Esta é a resposta da resistência e da defesa da fé.',
                        evaluation: 0.1,
                        context: 'A resposta simétrica representa a defesa do território e da nova ordem cristã.'
                    },
                    {
                        move: '2.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'O cavalo viking se desenvolve, atacando o peão adversário. Esta é a jogada do guerreiro que busca iniciativa.',
                        evaluation: 0.3,
                        context: 'O desenvolvimento do cavalo representa a iniciativa militar viking.'
                    },
                    {
                        move: '2...Nc6',
                        algebraic: 'Nc6',
                        narrative: 'O cavalo cristão protege o peão, mostrando a importância da defesa. Esta é a resposta da resistência organizada.',
                        evaluation: 0.2,
                        context: 'A proteção do peão representa a defesa organizada contra a invasão.'
                    },
                    {
                        move: '3.Bc4',
                        algebraic: 'Bc4',
                        narrative: 'O bispo viking se desenvolve, atacando o ponto fraco f7. Esta é a "Abertura Italiana", que busca ataque rápido.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do bispo representa a estratégia de ataque rápido viking.'
                    },
                    {
                        move: '3...Bc5',
                        algebraic: 'Bc5',
                        narrative: 'O bispo cristão se desenvolve simetricamente, defendendo e contra-atacando. Esta é a resposta equilibrada.',
                        evaluation: 0.3,
                        context: 'O desenvolvimento simétrico representa a defesa equilibrada e organizada.'
                    },
                    {
                        move: '4.c3',
                        algebraic: 'c3',
                        narrative: 'O Viking prepara d4, criando uma posição dinâmica. Esta é a jogada da preparação para o ataque.',
                        evaluation: 0.5,
                        context: 'A preparação de d4 representa a preparação para o ataque decisivo.'
                    },
                    {
                        move: '4...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'O cavalo cristão se desenvolve, atacando o peão e4. Esta é a resposta ativa que busca contra-jogo.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento ativo representa a busca por contra-jogo e iniciativa.'
                    },
                    {
                        move: '5.d4',
                        algebraic: 'd4',
                        narrative: 'O Viking abre o centro, criando tensão. Esta é a jogada que força o confronto decisivo.',
                        evaluation: 0.6,
                        context: 'A abertura do centro representa o confronto direto entre as duas forças.'
                    },
                    {
                        move: '5...exd4',
                        algebraic: 'exd4',
                        narrative: 'O Rei Cristão captura, aceitando o desafio. Esta é a resposta que aceita o confronto.',
                        evaluation: 0.5,
                        context: 'A captura aceita o desafio e prepara o contra-ataque.'
                    }
                ]
            },

            'maya-aztec': {
                title: 'Sacerdote Maya vs Imperador Asteca',
                subtitle: 'Sabedoria Ancestral - Mesoamérica',
                year: 1400,
                players: {
                    white: 'Sacerdote Maya',
                    black: 'Imperador Asteca'
                },
                context: 'Na Mesoamérica pré-colombiana, um sacerdote maia enfrenta um imperador asteca em uma partida que simboliza o conflito entre sabedoria ancestral e poder imperial. O xadrez aqui representa a estratégia ritual e a busca pelo conhecimento cósmico.',
                moves: [{
                        move: '1.d4',
                        algebraic: 'd4',
                        narrative: 'O Sacerdote Maya abre com d4, controlando o centro com sabedoria ancestral. Esta jogada representa a busca pelo conhecimento cósmico e pela verdade.',
                        evaluation: 0.2,
                        context: 'A jogada d4 simboliza a busca pela sabedoria ancestral e pelo conhecimento cósmico.'
                    },
                    {
                        move: '1...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'O Imperador Asteca responde com a Defesa Índia, flexível e poderosa. Esta é a resposta do poder imperial que busca controle.',
                        evaluation: 0.1,
                        context: 'A Defesa Índia representa a flexibilidade e o poder do império asteca.'
                    },
                    {
                        move: '2.c4',
                        algebraic: 'c4',
                        narrative: 'O Sacerdote expande no flanco da dama, mostrando sua determinação em preservar a sabedoria. Esta é a jogada da expansão do conhecimento.',
                        evaluation: 0.3,
                        context: 'A expansão no flanco representa a expansão do conhecimento e da sabedoria.'
                    },
                    {
                        move: '2...g6',
                        algebraic: 'g6',
                        narrative: 'O Imperador prepara o fianchetto, criando uma posição sólida. Esta é a resposta da estabilidade imperial.',
                        evaluation: 0.2,
                        context: 'O fianchetto representa a estabilidade e a solidez do império.'
                    },
                    {
                        move: '3.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'O cavalo se desenvolve, atacando o centro. Esta é a jogada do conhecimento que busca iniciativa.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento do cavalo representa a busca pela iniciativa no conhecimento.'
                    },
                    {
                        move: '3...Bg7',
                        algebraic: 'Bg7',
                        narrative: 'O bispo completa o fianchetto, criando uma posição sólida. Esta é a resposta da estabilidade imperial.',
                        evaluation: 0.3,
                        context: 'O fianchetto completo representa a estabilidade e a proteção do império.'
                    },
                    {
                        move: '4.e4',
                        algebraic: 'e4',
                        narrative: 'O Sacerdote expande no centro, criando uma posição dinâmica. Esta é a jogada da expansão do conhecimento.',
                        evaluation: 0.5,
                        context: 'A expansão no centro representa a expansão do conhecimento e da sabedoria.'
                    },
                    {
                        move: '4...d6',
                        algebraic: 'd6',
                        narrative: 'O Imperador protege o peão e5, mantendo a estrutura. Esta é a resposta da proteção imperial.',
                        evaluation: 0.4,
                        context: 'A proteção do peão representa a proteção da estrutura imperial.'
                    },
                    {
                        move: '5.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'O cavalo se desenvolve, preparando o roque. Esta é a jogada da preparação para o conhecimento.',
                        evaluation: 0.6,
                        context: 'O desenvolvimento do cavalo prepara a proteção do conhecimento.'
                    },
                    {
                        move: '5...O-O',
                        algebraic: 'O-O',
                        narrative: 'O Imperador faz o roque, protegendo seu rei. Esta é a jogada da segurança imperial.',
                        evaluation: 0.5,
                        context: 'O roque representa a proteção do poder imperial e da estabilidade.'
                    }
                ]
            },

            'mongol-khan': {
                title: 'Mongol vs Khan',
                subtitle: 'A Horda Dourada - Estepe Asiática',
                year: 1200,
                players: {
                    white: 'Guerreiro Mongol',
                    black: 'Khan da Horda'
                },
                context: 'Nas vastas estepes da Ásia Central, um guerreiro mongol enfrenta seu próprio Khan em uma partida que simboliza a hierarquia militar e a estratégia de conquista. O xadrez aqui representa a tática de cavalaria e a disciplina militar.',
                moves: [{
                        move: '1.e4',
                        algebraic: 'e4',
                        narrative: 'O Guerreiro Mongol abre com e4, controlando o centro com agressividade. Esta jogada representa a velocidade e a iniciativa da cavalaria mongol.',
                        evaluation: 0.2,
                        context: 'A jogada e4 simboliza a velocidade e a agressividade da cavalaria mongol.'
                    },
                    {
                        move: '1...c5',
                        algebraic: 'c5',
                        narrative: 'O Khan responde com a Defesa Siciliana, dinâmica e tática. Esta é a resposta do líder que busca contra-jogo.',
                        evaluation: 0.1,
                        context: 'A Siciliana representa a dinâmica e a tática da estratégia mongol.'
                    },
                    {
                        move: '2.Nf3',
                        algebraic: 'Nf3',
                        narrative: 'O cavalo se desenvolve, atacando o peão c5. Esta é a jogada da cavalaria que busca iniciativa.',
                        evaluation: 0.3,
                        context: 'O desenvolvimento do cavalo representa a iniciativa da cavalaria mongol.'
                    },
                    {
                        move: '2...d6',
                        algebraic: 'd6',
                        narrative: 'O Khan protege o peão c5, mantendo a estrutura. Esta é a resposta da disciplina militar.',
                        evaluation: 0.2,
                        context: 'A proteção do peão representa a disciplina e a organização militar.'
                    },
                    {
                        move: '3.d4',
                        algebraic: 'd4',
                        narrative: 'O Mongol abre o centro, criando tensão. Esta é a jogada que força o confronto decisivo.',
                        evaluation: 0.4,
                        context: 'A abertura do centro representa o confronto direto entre as forças.'
                    },
                    {
                        move: '3...cxd4',
                        algebraic: 'cxd4',
                        narrative: 'O Khan captura, aceitando o desafio. Esta é a resposta que aceita o confronto.',
                        evaluation: 0.3,
                        context: 'A captura aceita o desafio e prepara o contra-ataque.'
                    },
                    {
                        move: '4.Nxd4',
                        algebraic: 'Nxd4',
                        narrative: 'O cavalo recaptura, mantendo pressão no centro. Esta é a jogada da pressão contínua.',
                        evaluation: 0.5,
                        context: 'O cavalo em d4 mantém a pressão e controla o centro.'
                    },
                    {
                        move: '4...Nf6',
                        algebraic: 'Nf6',
                        narrative: 'O cavalo do Khan se desenvolve, atacando o peão e4. Esta é a resposta ativa que busca contra-jogo.',
                        evaluation: 0.4,
                        context: 'O desenvolvimento ativo representa a busca por contra-jogo.'
                    },
                    {
                        move: '5.Nc3',
                        algebraic: 'Nc3',
                        narrative: 'O cavalo se desenvolve, protegendo o peão e4. Esta é a jogada da proteção e do desenvolvimento.',
                        evaluation: 0.6,
                        context: 'O desenvolvimento do cavalo protege o peão e prepara o ataque.'
                    },
                    {
                        move: '5...a6',
                        algebraic: 'a6',
                        narrative: 'O Khan prepara b5, expandindo no flanco. Esta é a resposta que busca expansão.',
                        evaluation: 0.5,
                        context: 'A preparação de b5 representa a expansão e o contra-ataque.'
                    }
                ]
            }
        };

        this.init();
    }

    init() {
        this.chess = new Chess();
        this.board = document.getElementById('narrative-board');

        this.setupEventListeners();
        this.updateUI();
    }

    setupEventListeners() {
        // Game selection
        document.querySelectorAll('.game-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const gameId = card.dataset.game;
                this.loadGame(gameId);
            });
        });

        // Navigation controls
        const prevBtn = document.getElementById('prev-move');
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                this.previousMove();
            });
        }

        const nextBtn = document.getElementById('next-move');
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.nextMove();
            });
        }

        // Game controls
        const playBtn = document.getElementById('play-game');
        if (playBtn) {
            playBtn.addEventListener('click', () => {
                this.playSequence();
            });
        }

        const resetBtn = document.getElementById('reset-game');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetGame();
            });
        }

        const autoPlayBtn = document.getElementById('auto-play');
        if (autoPlayBtn) {
            autoPlayBtn.addEventListener('click', () => {
                this.toggleAutoPlay();
            });
        }
    }

    loadGame(gameId) {
        this.currentGame = this.games[gameId];
        this.currentMoveIndex = 0;
        this.gameHistory = [];

        // Reset chess position
        this.chess.reset();

        // Update UI
        this.updateGameInfo();
        this.updateBoard();
        this.updateMoveList();
        this.updateNarrative();
        this.updateEvaluation();
        this.updateHistoricalContext();

        // Highlight selected game card
        document.querySelectorAll('.game-card').forEach(card => {
            card.classList.remove('selected');
        });
        document.querySelector(`[data-game="${gameId}"]`).classList.add('selected');
    }

    updateGameInfo() {
        if (!this.currentGame) return;

        document.getElementById('move-counter').textContent = 'Movimento 1';
    }

    updateBoard() {
        if (this.board && this.board.setPosition) {
            try {
                this.board.setPosition(this.chess.fen());
            } catch (error) {
                console.log('Board update:', this.chess.fen());
            }
        } else if (this.board && this.board.position) {
            // Alternative method for chessboard-element
            try {
                this.board.position = this.chess.fen();
            } catch (error) {
                console.log('Board position update:', this.chess.fen());
            }
        }
    }

    updateMoveList() {
        const moveList = document.getElementById('move-list');
        if (!moveList) return;

        let html = '';
        this.currentGame.moves.forEach((move, index) => {
            const moveNumber = Math.floor(index / 2) + 1;
            const isWhiteMove = index % 2 === 0;

            if (isWhiteMove) {
                html += `<div class="flex justify-between items-center py-1 ${index === this.currentMoveIndex ? 'bg-blue-500/20 rounded px-2' : ''}">`;
                html += `<span class="text-gray-500">${moveNumber}.</span>`;
                html += `<span class="text-white">${move.algebraic}</span>`;
            } else {
                html += `<span class="text-white ml-4">${move.algebraic}</span>`;
                html += `</div>`;
            }
        });

        moveList.innerHTML = html;
    }

    updateNarrative() {
        const narrativeText = document.getElementById('narrative-text');
        if (!narrativeText || !this.currentGame) return;

        if (this.currentMoveIndex < this.currentGame.moves.length) {
            const move = this.currentGame.moves[this.currentMoveIndex];
            narrativeText.innerHTML = `
                <div class="mb-4">
                    <h5 class="font-semibold text-white mb-2">${move.move}</h5>
                    <p class="mb-3">${move.narrative}</p>
                    <div class="bg-gray-800 rounded-lg p-3">
                        <p class="text-sm text-gray-400"><strong>Contexto:</strong> ${move.context}</p>
                    </div>
                </div>
            `;
        } else {
            narrativeText.innerHTML = `
                <p class="text-gray-400 italic">Jogo concluído. Selecione outro jogo ou reinicie para continuar a análise.</p>
            `;
        }
    }

    updateEvaluation() {
        const evalScore = document.getElementById('eval-score');
        const evalBar = document.getElementById('eval-bar');

        if (!this.currentGame || this.currentMoveIndex >= this.currentGame.moves.length) {
            evalScore.textContent = '=';
            evalBar.style.width = '50%';
            return;
        }

        const move = this.currentGame.moves[this.currentMoveIndex];
        const evaluation = move.evaluation;

        // Update score display
        if (evaluation > 0) {
            evalScore.textContent = `+${evaluation.toFixed(1)}`;
            evalScore.className = 'text-lg font-bold text-blue-400';
        } else if (evaluation < 0) {
            evalScore.textContent = `${evaluation.toFixed(1)}`;
            evalScore.className = 'text-lg font-bold text-purple-400';
        } else {
            evalScore.textContent = '=';
            evalScore.className = 'text-lg font-bold text-gray-400';
        }

        // Update evaluation bar
        const percentage = 50 + (evaluation * 25); // Convert to percentage
        evalBar.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
    }

    updateHistoricalContext() {
        const historicalContext = document.getElementById('historical-context');
        if (!historicalContext || !this.currentGame) return;

        historicalContext.innerHTML = `
            <p class="mb-3"><strong>${this.currentGame.year}</strong> - ${this.currentGame.subtitle}</p>
            <p class="mb-3"><strong>Brancas:</strong> ${this.currentGame.players.white}</p>
            <p class="mb-3"><strong>Pretas:</strong> ${this.currentGame.players.black}</p>
            <p>${this.currentGame.context}</p>
        `;
    }

    nextMove() {
        if (!this.currentGame || this.currentMoveIndex >= this.currentGame.moves.length) return;

        const move = this.currentGame.moves[this.currentMoveIndex];

        // Make the move
        try {
            this.chess.move(move.algebraic);
            this.gameHistory.push(move);
            this.currentMoveIndex++;

            // Update UI
            this.updateBoard();
            this.updateMoveList();
            this.updateNarrative();
            this.updateEvaluation();
            document.getElementById('move-counter').textContent = `Movimento ${this.currentMoveIndex}`;
        } catch (error) {
            console.error('Invalid move:', error);
        }
    }

    previousMove() {
        if (this.currentMoveIndex <= 0) return;

        // Undo the last move
        this.chess.undo();
        this.gameHistory.pop();
        this.currentMoveIndex--;

        // Update UI
        this.updateBoard();
        this.updateMoveList();
        this.updateNarrative();
        this.updateEvaluation();
        document.getElementById('move-counter').textContent = `Movimento ${this.currentMoveIndex}`;
    }

    playSequence() {
        this.resetGame();
        this.autoPlaySequence();
    }

    autoPlaySequence() {
        if (this.isAutoPlaying) return;

        this.isAutoPlaying = true;
        document.getElementById('auto-play').textContent = 'Parar Auto-Play';

        this.autoPlayInterval = setInterval(() => {
            if (this.currentMoveIndex >= this.currentGame.moves.length) {
                this.stopAutoPlay();
                return;
            }

            this.nextMove();
        }, 2000); // 2 seconds per move
    }

    stopAutoPlay() {
        this.isAutoPlaying = false;
        clearInterval(this.autoPlayInterval);
        document.getElementById('auto-play').textContent = 'Auto-Play';
    }

    toggleAutoPlay() {
        if (this.isAutoPlaying) {
            this.stopAutoPlay();
        } else {
            this.autoPlaySequence();
        }
    }

    resetGame() {
        this.stopAutoPlay();
        this.currentMoveIndex = 0;
        this.gameHistory = [];
        this.chess.reset();

        this.updateBoard();
        this.updateMoveList();
        this.updateNarrative();
        this.updateEvaluation();
        document.getElementById('move-counter').textContent = 'Movimento 1';
    }

    updateUI() {
        // Initial state
        document.getElementById('narrative-text').innerHTML = `
            <p class="text-gray-400 italic">Selecione um jogo para começar a análise...</p>
        `;

        document.getElementById('historical-context').innerHTML = `
            <p class="text-gray-400 italic">Contexto histórico será exibido aqui...</p>
        `;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.narrativeAnalysis = new NarrativeAnalysis();
});