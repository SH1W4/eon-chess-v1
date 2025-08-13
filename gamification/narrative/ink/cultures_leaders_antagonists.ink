# CHESS: Culturas, Líderes e Antagonistas Expandidos
# Sistema Completo de Personagens e Dinâmicas Culturais

// Culturas Expandidas
LIST all_cultures = Viking, Maia, Samurai, Azteca, Persian, Egyptian, Chinese, Greek, Roman, Celtic, Arabian, Mongol, Zulu, Inca

// Líderes Estratégicos por Cultura
LIST viking_leaders = Ragnar_Lothbrok, Harald_Hardrada, Erik_the_Red, Lagertha_Shieldmaiden
LIST maia_leaders = Itzamna_the_Wise, Kukulkan_Serpent, Ixchel_Moon, Hunab_Ku
LIST samurai_leaders = Miyamoto_Musashi, Oda_Nobunaga, Tomoe_Gozen, Minamoto_Yoritomo
LIST azteca_leaders = Montezuma_II, Tlacaelel_Advisor, Itzcoatl_Obsidian, Nezahualcoyotl
LIST persian_leaders = Cyrus_the_Great, Darius_I, Xerxes_I, Ardashir_I
LIST egyptian_leaders = Cleopatra_VII, Ramesses_II, Hatshepsut, Thutmose_III
LIST chinese_leaders = Sun_Tzu, Zhuge_Liang, Wu_Zetian, Qin_Shi_Huang
LIST greek_leaders = Alexander_Great, Leonidas_Sparta, Pericles_Athens, Odysseus_Cunning

// Antagonistas Universais
LIST universal_antagonists = Shadow_Master, Chaos_Weaver, Time_Thief, Mind_Breaker, Soul_Crusher, Pattern_Destroyer

// Tipos de Desafios Estratégicos
LIST strategic_challenges = berserker_rush, celestial_puzzle, honor_gambit, sacrifice_ritual, immortal_defense, divine_trap, art_of_war, phalanx_formation

// Estados de Rivalidade
LIST rivalry_states = neutral, challenged, respected, feared, allied, nemesis, legendary_rival

VAR current_culture = ""
VAR current_leader = ""
VAR current_antagonist = ""
VAR rivalry_level = 0
VAR cultural_synergy = 0
VAR leader_trust = 0
VAR antagonist_power = 0

=== culture_expansion_selection ===
# Escolha sua Civilização

Cada cultura traz milênios de sabedoria estratégica única. Qual legado você abraçará?

+ [🛡️ Viking - Fúria do Norte]
    -> select_viking_path
+ [🌟 Maia - Sabedoria Celestial]
    -> select_maia_path
+ [⚔️ Samurai - Caminho do Bushido]
    -> select_samurai_path
+ [🦅 Azteca - Império do Sol]
    -> select_azteca_path
+ [🏛️ Persa - Império Imortal]
    -> select_persian_path
+ [👁️ Egípcio - Mistérios do Nilo]
    -> select_egyptian_path
+ [🐉 Chinês - Reino do Meio]
    -> select_chinese_path
+ [⚡ Grego - Berço da Estratégia]
    -> select_greek_path
+ [Mais Culturas →]
    -> more_cultures_selection

=== select_viking_path ===
~ current_culture = "Viking"
~ cultural_synergy = 15

# A Saga Viking Começa

Os ventos gélidos do norte trazem o eco de mil batalhas. Você escolheu o caminho da fúria controlada e da conquista implacável.

Qual lendário líder Viking guiará sua jornada?

+ [Ragnar Lothbrok - O Conquistador Lendário]
    ~ current_leader = "Ragnar_Lothbrok"
    ~ leader_trust = 10
    "Por Odin! Você tem a coragem de um verdadeiro guerreiro. Juntos, conquistaremos o tabuleiro como conquistamos os mares!"
    -> viking_strategy_introduction
    
+ [Harald Hardrada - O Último Viking]
    ~ current_leader = "Harald_Hardrada"
    ~ leader_trust = 10
    "A era dos Vikings pode ter acabado no mundo, mas no tabuleiro, nossa lenda apenas começou!"
    -> viking_strategy_introduction
    
+ [Lagertha - A Guerreira Escudeira]
    ~ current_leader = "Lagertha_Shieldmaiden"
    ~ leader_trust = 15
    "Força não é apenas músculo, jovem guerreiro. É estratégia, timing e a coragem de sacrificar."
    -> viking_strategy_introduction

=== viking_strategy_introduction ===
# Estratégia Viking: Berserker Rush

{current_leader} se aproxima do tabuleiro com olhos ardentes.

"A estratégia Viking é como uma tempestade no mar - súbita, devastadora e imprevisível. Nosso estilo principal é o 'Berserker Rush'."

Características do Berserker Rush:
- Desenvolvimento ultra-agressivo de peças
- Sacrifícios táticos para abrir linhas de ataque
- Pressão constante sobre o rei inimigo
- Ignorar pequenas perdas materiais por iniciativa

"Mas cuidado," {current_leader} adverte, "há um inimigo que conhece nossos métodos..."

-> introduce_viking_antagonist

=== introduce_viking_antagonist ===
~ current_antagonist = "Fenrir_the_Bound"
~ antagonist_power = 20

# O Antagonista Surge: Fenrir, O Acorrentado

Uma sombra cobre o tabuleiro. {current_leader} se tensa.

"Fenrir... O lobo que devora estratégias. Ele foi um de nós, mas agora serve apenas ao caos. Ele conhece cada movimento Viking e os perverte."

Fenrir materializa-se do outro lado do tabuleiro, seus olhos brilhando com malícia antiga.

"Ah, {current_leader}... ainda ensinando os velhos truques? Deixe-me mostrar ao seu pupilo o que acontece quando a fúria Viking encontra a verdadeira selvageria!"

+ [Enfrentar Fenrir com coragem]
    ~ rivalry_level = 1
    -> viking_first_challenge
+ [Pedir orientação a {current_leader}]
    ~ leader_trust += 5
    -> viking_mentor_moment
+ [Estudar Fenrir cuidadosamente]
    ~ cultural_synergy += 5
    -> analyze_antagonist_style

=== select_maia_path ===
~ current_culture = "Maia"
~ cultural_synergy = 20

# O Calendário Maia se Alinha

As estrelas dançam em padrões antigos. Você escolheu o caminho da sabedoria celestial e dos ciclos eternos.

Qual sábio Maia interpretará os sinais para você?

+ [Itzamna - O Criador da Escrita]
    ~ current_leader = "Itzamna_the_Wise"
    ~ leader_trust = 15
    "Os glifos no tabuleiro contam histórias de vitórias ainda não escritas. Venha, jovem escriba, vamos decifrá-las juntos."
    -> maia_strategy_introduction
    
+ [Kukulkan - A Serpente Emplumada]
    ~ current_leader = "Kukulkan_Serpent"
    ~ leader_trust = 10
    "Como a serpente que sou, movo-me em padrões que o olho destreinado não consegue seguir. Aprenda a ver além do óbvio."
    -> maia_strategy_introduction
    
+ [Ixchel - Senhora da Lua]
    ~ current_leader = "Ixchel_Moon"
    ~ leader_trust = 20
    "A lua revela o que o sol esconde. No xadrez, como na vida, os movimentos mais poderosos acontecem nas sombras."
    -> maia_strategy_introduction

=== maia_strategy_introduction ===
# Estratégia Maia: Puzzle Celestial

{current_leader} traça padrões invisíveis sobre o tabuleiro.

"A estratégia Maia é como observar as estrelas - requer paciência, precisão e a capacidade de ver conexões onde outros veem apenas caos."

Características do Puzzle Celestial:
- Construção de estruturas de peões complexas
- Manobras de longo prazo (10+ movimentos)
- Sacrifícios posicionais profundos
- Harmonização de todas as peças

"Mas nem todos respeitam a ordem cósmica," {current_leader} sussurra.

-> introduce_maia_antagonist

=== introduce_maia_antagonist ===
~ current_antagonist = "Xibalba_Lord"
~ antagonist_power = 25

# O Senhor de Xibalba Desperta

O tabuleiro escurece. {current_leader} fecha os olhos em concentração.

"Xibalba... o submundo do xadrez. Seu senhor corrompeu nossa astronomia sagrada, transformando padrões em armadilhas."

Uma risada ecoa das profundezas:

"Bem-vindo ao meu reino, pequeno astrônomo. Seus padrões celestiais não significam nada nas trevas de Xibalba. Cada movimento que você faz alimenta meu caos!"

+ [Iluminar as trevas com sabedoria]
    ~ cultural_synergy += 10
    -> maia_light_challenge
+ [Aceitar o desafio das sombras]
    ~ rivalry_level = 2
    -> maia_shadow_duel
+ [Invocar a proteção ancestral]
    ~ leader_trust += 10
    -> maia_ancestral_wisdom

=== select_chinese_path ===
~ current_culture = "Chinese"
~ cultural_synergy = 25

# O Império do Meio Desperta

O tabuleiro se transforma em um campo de batalha onde a arte da guerra encontra a filosofia milenar.

Qual estrategista lendário comandará suas forças?

+ [Sun Tzu - O Mestre da Guerra]
    ~ current_leader = "Sun_Tzu"
    ~ leader_trust = 20
    "A suprema excelência consiste em quebrar a resistência do inimigo sem lutar. Observe e aprenda."
    -> chinese_strategy_introduction
    
+ [Zhuge Liang - O Dragão Adormecido]
    ~ current_leader = "Zhuge_Liang"
    ~ leader_trust = 15
    "Estratégia é como água - assume a forma necessária para a vitória. Seja fluido, seja imprevisível."
    -> chinese_strategy_introduction
    
+ [Wu Zetian - A Imperatriz de Ferro]
    ~ current_leader = "Wu_Zetian"
    ~ leader_trust = 15
    "O poder não é tomado, é cultivado. Cada peça é uma semente de vitória futura."
    -> chinese_strategy_introduction

=== chinese_strategy_introduction ===
# Estratégia Chinesa: A Arte da Guerra

{current_leader} contempla o tabuleiro como um general observa o campo de batalha.

"A estratégia chinesa abraça os ensinamentos de cinco mil anos. Não buscamos apenas vencer, mas vencer sem desperdiçar energia."

Princípios da Arte da Guerra:
- "Conheça o inimigo e conheça a si mesmo"
- Formações flexíveis que se adaptam
- Uso do tempo como arma
- Vitória através da posição, não da força

"Mas existe um que perverteu nossos ensinamentos..."

-> introduce_chinese_antagonist

=== introduce_chinese_antagonist ===
~ current_antagonist = "Mandate_Breaker"
~ antagonist_power = 30

# O Quebrador do Mandato Celestial

O tabuleiro treme. {current_leader} aperta os punhos.

"O Quebrador do Mandato... ele era um de nossos melhores, mas a ambição o consumiu. Agora usa nossa própria arte contra nós."

Uma figura sombria emerge, vestida em armadura negra com caracteres distorcidos:

"Sun Tzu? Zhuge Liang? Wu Zetian? Relíquias! Eu transcendi suas limitações. O Mandato Celestial é meu para quebrar e refazer!"

+ [Defender a tradição milenar]
    ~ cultural_synergy += 15
    -> chinese_tradition_defense
+ [Inovar dentro da tradição]
    ~ leader_trust += 15
    -> chinese_innovation_path
+ [Desafiar o Quebrador diretamente]
    ~ rivalry_level = 3
    -> chinese_direct_confrontation

=== persian_immortal_gambit ===
~ current_culture = "Persian"

# O Gambito Imortal Persa

O tabuleiro se transforma em Persépolis. Colunas douradas emergem nos cantos.

"A estratégia persa," explica Cyrus, "é a Defesa Imortal. Como nossos guardas elite, sacrificamos para renascer mais fortes."

Características:
- Sacrifícios que levam a contra-ataques devastadores
- Desenvolvimento assimétrico desconcertante
- Pressão psicológica constante
- Finais com material mínimo mas posição máxima

-> introduce_persian_antagonist

=== egyptian_divine_trap ===
~ current_culture = "Egyptian"

# A Armadilha Divina Egípcia

Hieróglifos brilham no tabuleiro. Cada casa conta uma história.

"O xadrez egípcio," Cleopatra sussurra, "é sobre sedução e armadilhas. Fazemos o oponente pensar que está vencendo..."

Elementos da Armadilha Divina:
- Aberturas que parecem passivas mas escondem veneno
- Sacrifícios de dama calculados
- Uso de zugzwang como arte
- Transformação de peões em momento crítico

-> egyptian_mystical_challenge

=== dynamic_rivalry_system ===
# Sistema de Rivalidade Dinâmica

{rivalry_level:
- 0: O antagonista apenas observa, estudando seus movimentos
- 1: Primeiros confrontos, testando forças
- 2: Batalhas intensas, aprendendo um com o outro  
- 3: Duelos épicos que definem destinos
- 4: Respeito mútuo emergindo do conflito
- 5: Transformação - inimigo se torna aliado ou nemesis eterno
}

{
- rivalry_level < 3:
    -> escalate_rivalry
- rivalry_level >= 3 && rivalry_level < 5:
    -> rivalry_climax  
- else:
    -> rivalry_resolution
}

=== cultural_synergy_effects ===
# Efeitos de Sinergia Cultural

{cultural_synergy:
- 0-25: Iniciante - Movimentos básicos da cultura
- 26-50: Adepto - Compreende filosofia cultural
- 51-75: Mestre - Canaliza força ancestral
- 76-99: Sábio - Cria novas variações
- 100: Transcendente - Torna-se lenda viva da cultura
}

{cultural_synergy > 50:
    Você sente a força de seus ancestrais fluindo através de cada movimento.
    
    + [Invocar poder ancestral]
        -> ancestral_power_surge
    + [Meditar sobre a sabedoria cultural]
        -> cultural_meditation
}

=== leader_relationship_dynamics ===
# Dinâmica com Líderes

{leader_trust:
- 0-20: Mentor distante - Ensina apenas o básico
- 21-40: Professor dedicado - Compartilha segredos
- 41-60: Aliado confiável - Luta ao seu lado
- 61-80: Amigo verdadeiro - Sacrifica-se por você
- 81-100: Sucessor escolhido - Passa o manto de liderança
}

{current_leader} observa seu progresso:

{leader_trust > 60:
    "Você superou minhas expectativas. Está pronto para aprender o segredo final de nossa cultura..."
    -> ultimate_cultural_secret
- else:
    "Continue praticando. A maestria requer paciência e dedicação."
    -> continue_training
}

=== multi_cultural_fusion ===
# Fusão Multicultural

Após dominar uma cultura, você pode aprender de outras:

+ [Combinar Viking + Samurai = "Fúria Disciplinada"]
    -> fusion_viking_samurai
+ [Mesclar Maia + Egípcio = "Mistérios Celestiais"]
    -> fusion_maia_egyptian
+ [Unir Chinês + Grego = "Estratégia Filosófica"]
    -> fusion_chinese_greek
+ [Criar sua própria fusão]
    -> custom_fusion_creation

=== antagonist_evolution_system ===
# Evolução dos Antagonistas

{antagonist_power:
- 0-30: Ameaça Emergente
- 31-60: Rival Perigoso
- 61-90: Nemesis Poderoso
- 91-120: Força Caótica
- 121+: Entidade Transcendente
}

O poder de {current_antagonist} cresce com cada confronto:

{antagonist_power > 90:
    # Transformação Final!
    
    {current_antagonist} transcende sua forma atual!
    
    "HAHAHAHA! Você me fez mais forte do que jamais imaginei! Agora, enfrente minha verdadeira forma!"
    
    -> antagonist_final_form
}

=== cultural_war_council ===
# Conselho de Guerra Cultural

Em momentos críticos, você pode convocar um conselho com todos os líderes que conheceu:

Os líderes se reúnem em círculo ao redor do tabuleiro:

{leader_trust > 40:
    - Ragnar: "Ataque frontal! Esmague-os!"
    - Sun Tzu: "Paciência. A vitória já está decidida."
    - Cleopatra: "Seduza-os para a armadilha."
    - Montezuma: "O sacrifício trará poder."
}

+ [Seguir conselho Viking] -> aggressive_strategy
+ [Adotar sabedoria Chinesa] -> patient_strategy
+ [Usar sedução Egípcia] -> deceptive_strategy
+ [Abraçar sacrifício Azteca] -> sacrificial_strategy
+ [Forjar seu próprio caminho] -> unique_strategy

=== legendary_transformation ===
# Transformação Lendária

{cultural_synergy >= 100 && leader_trust >= 80 && rivalry_level >= 5:
    
    # Ascensão à Lenda
    
    O tabuleiro brilha com energia antiga. Todos os líderes e até mesmo os antagonistas param para observar.
    
    {current_leader}: "Você não é mais um estudante. Você se tornou a própria encarnação de nossa cultura!"
    
    {current_antagonist}: "Impossível! Você... você transcendeu até mesmo minha oposição!"
    
    Você alcançou a Transformação Lendária!
    
    Novos poderes desbloqueados:
    - Invocar qualquer estratégia cultural à vontade
    - Converter antagonistas em aliados
    - Criar novas escolas de xadrez
    - Guiar outros jogadores como mentor universal
    
    -> legendary_epilogue
}

=== special_event_world_championship ===
# Evento Especial: Campeonato Mundial das Culturas

Um arauto anuncia:

"O Grande Torneio das Civilizações começará! Cada cultura enviará seu campeão!"

Participantes:
- Vikings: {leader_trust > 60: "Você é nosso campeão!" | "Ragnar representará os Vikings"}
- Maias: Kukulkan lidera as forças celestiais
- Samurais: Musashi empunha o tabuleiro como espada
- Aztecas: Montezuma traz sacrifícios estratégicos
- Persas: Ciro comanda os Imortais
- Egípcios: Cleópatra tece suas teias
- Chineses: Sun Tzu orquestra a vitória
- Gregos: Alexandre conquista quadrados

+ [Entrar no torneio] -> world_championship_begins
+ [Observar e aprender] -> spectator_wisdom
+ [Desafiar o sistema] -> rebel_against_tournament

=== create_your_legend ===
# Crie Sua Própria Lenda

Após dominar todas as culturas, você pode criar sua própria escola:

Nome da sua escola de xadrez: [Input do jogador]

Filosofia central:
+ [Agressão Calculada] -> found_aggressive_school
+ [Harmonia Posicional] -> found_positional_school  
+ [Caos Controlado] -> found_chaotic_school
+ [Transcendência Tática] -> found_tactical_school

Escolha seu símbolo:
+ [🦅 Águia - Visão Superior] -> eagle_symbol
+ [🐉 Dragão - Poder Antigo] -> dragon_symbol
+ [⚡ Raio - Velocidade Divina] -> lightning_symbol
+ [🌀 Espiral - Evolução Infinita] -> spiral_symbol

-> establish_new_tradition

=== universal_ending ===
# O Tabuleiro Infinito

Você transcendeu todas as culturas, derrotou e redimiu todos os antagonistas, ganhou a confiança de todos os líderes.

O tabuleiro se expande ao infinito. Cada casa conta uma história, cada peça carrega uma lenda.

{current_leader}: "Você não é mais jogador nem peça. Você é o próprio jogo."

{current_antagonist}: "Eu era sua sombra, mas agora somos luz juntos."

O que você fará com este poder?

+ [Ensinar outros] -> become_universal_mentor
+ [Explorar novas dimensões] -> explore_chess_multiverse
+ [Criar paz entre culturas] -> establish_chess_harmony
+ [Buscar desafio ainda maior] -> seek_ultimate_challenge

-> DONE
