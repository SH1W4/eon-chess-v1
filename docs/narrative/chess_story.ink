VAR player_culture = "medieval"
VAR game_phase = "opening"
VAR game_style = "aggressive"

/* Métricas Culturais */
VAR honor = 0
VAR tradition = 0
VAR innovation = 0
VAR efficiency = 0

=== function update_cultural_values() ===
{player_culture == "medieval":
    ~ honor += 1
    ~ tradition += 1
- else:
    ~ innovation += 1
    ~ efficiency += 1
}

=== main ===
# title: ChessMaster - Uma Jornada Através do Tempo
# author: ChessMaster Team
# tags: chess, culture, storytelling

Na encruzilhada do tempo, duas visões do nobre jogo de xadrez emergem.

-> culture_choice

=== culture_choice ===
Qual caminho você escolherá?

* [Medieval: O Caminho da Honra]
    ~ player_culture = "medieval"
    Em um tempo de cavaleiros e castelos, o xadrez é mais que um jogo - é uma representação da própria nobreza.
    -> medieval_intro
* [Futurista: O Caminho da Inovação]
    ~ player_culture = "futuristic"
    No limiar do futuro, o xadrez transcende sua forma clássica, tornando-se uma dança de padrões e probabilidades.
    -> futuristic_intro

=== medieval_intro ===
{update_cultural_values()}
O ar carrega o peso da tradição. O tabuleiro diante de você não é apenas madeira e marfim - é um campo de batalha em miniatura, onde a honra e a estratégia dançam em perfeita harmonia.

* [Iniciar com Tradição]
    Os antigos mestres nos ensinaram o valor da posição e desenvolvimento.
    -> medieval_opening
* [Começar Ousadamente]
    Que os bardos cantem sobre nossa coragem!
    -> medieval_opening

=== futuristic_intro ===
{update_cultural_values()}
Hologramas dançam sobre o tabuleiro quântico, cada peça um nexo de possibilidades infinitas. Este não é apenas um jogo - é uma simulação de realidades paralelas.

* [Iniciar Análise Tática]
    Padrões emergem da matriz de possibilidades.
    -> futuristic_opening
* [Calibrar Estratégia]
    Otimizando parâmetros iniciais.
    -> futuristic_opening

=== medieval_opening ===
{game_phase = "opening"}
O campo de batalha aguarda seu primeiro comando. Como deseja conduzir suas forças?

* [Gambito do Rei]
    "Um sacrifício nobre pelo controle do centro!"
    Um peão avança, oferecendo-se em sacrifício pela glória do reino.
    -> medieval_development
* [Jogo Italiano]
    "Seguindo os passos dos grandes mestres!"
    Com precisão e tradição, suas peças assumem posições clássicas.
    -> medieval_development
* [Defesa Siciliana]
    "Uma defesa astuta e testada pelo tempo!"
    Como um castelo bem fortificado, sua posição promete segurança e contra-ataque.
    -> medieval_development

=== futuristic_opening ===
{game_phase = "opening"}
Matrizes de possibilidades se desdobram. Qual vetor de desenvolvimento você escolherá?

* [Variação Hiperacelerada]
    "Iniciando sequência de desenvolvimento otimizado."
    Suas peças dançam em padrões não-lineares, desafiando conceitos tradicionais.
    -> futuristic_development
* [Sistema Neural]
    "Ativando redes de desenvolvimento adaptativo."
    Cada peça se move em harmonia, criando sinergias posicionais complexas.
    -> futuristic_development
* [Configuração Quântica]
    "Estabelecendo superposição estratégica."
    Suas peças assumem estados múltiplos, mantendo máxima flexibilidade.
    -> futuristic_development

=== medieval_development ===
O campo de batalha ganha vida com o movimento das tropas.

* [Avançar com Bravura]
    Os cavaleiros marcham à frente, estandartes tremulando ao vento.
    -> medieval_middlegame
* [Fortificar Posições]
    Como um castelo bem defendido, cada peça protege sua posição.
    -> medieval_middlegame
* [Manobras Táticas]
    As peças se movem em formação, prontas para o embate.
    -> medieval_middlegame

=== futuristic_development ===
Padrões emergentes se cristalizam na matriz posicional.

* [Expansão Vetorial]
    Peças fluem através de linhas de força calculadas.
    -> futuristic_middlegame
* [Configuração Defensiva]
    Campos de energia posicional se entrelaçam.
    -> futuristic_middlegame
* [Otimização Tática]
    Algoritmos posicionais convergem para estados ideais.
    -> futuristic_middlegame

=== medieval_middlegame ===
{game_phase = "middlegame"}
O fragor da batalha ecoa pelo tabuleiro. Que manobra comandará?

* [Ataque Frontal]
    "Pela honra do reino!"
    -> medieval_tactics
* [Cerco Estratégico]
    "Vamos cercá-los com precisão e paciência."
    -> medieval_tactics
* [Manobra de Flanqueamento]
    "Que nossos cavaleiros circulem suas defesas!"
    -> medieval_tactics

=== futuristic_middlegame ===
{game_phase = "middlegame"}
Padrões táticos emergem da matriz posicional.

* [Ataque Multi-vetorial]
    "Iniciando sequências ofensivas paralelas."
    -> futuristic_tactics
* [Compressão Posicional]
    "Otimizando densidade estratégica."
    -> futuristic_tactics
* [Recalibração Dinâmica]
    "Ajustando vetores táticos."
    -> futuristic_tactics

=== medieval_tactics ===
O momento decisivo se aproxima.

* [Carga dos Cavaleiros]
    Suas peças avançam em formação heroica.
    -> medieval_endgame
* [Assalto ao Castelo]
    Torres e Bispos convergem para o ataque final.
    -> medieval_endgame
* [Manobra Real]
    A Rainha lidera um ataque devastador.
    -> medieval_endgame

=== futuristic_tactics ===
Convergência tática detectada.

* [Sobrecarga Sistêmica]
    Todas as linhas de força convergem para o ataque.
    -> futuristic_endgame
* [Colapso Posicional]
    Estruturas defensivas se desintegram sob pressão.
    -> futuristic_endgame
* [Sincronização Crítica]
    Peças atingem ressonância tática perfeita.
    -> futuristic_endgame

=== medieval_endgame ===
{game_phase = "endgame"}
O destino da batalha será decidido!

* [Pela Glória!]
    -> medieval_victory
* [Proposta de Paz]
    -> medieval_draw
* [Último Bastião]
    -> medieval_defeat

=== futuristic_endgame ===
{game_phase = "endgame"}
Fase final iniciada. Calculando resolução.

* [Execução Terminal]
    -> futuristic_victory
* [Equilíbrio Dinâmico]
    -> futuristic_draw
* [Reconfiguração Defensiva]
    -> futuristic_defeat

=== medieval_victory ===
Pela honra e glória, a vitória é vossa!
-> epilogue

=== medieval_draw ===
Um empate digno de ser cantado pelos bardos.
-> epilogue

=== medieval_defeat ===
Mesmo na derrota, a honra permanece intacta.
-> epilogue

=== futuristic_victory ===
Simulação concluída. Resultado: Vitória.
-> epilogue

=== futuristic_draw ===
Equilíbrio perfeito alcançado.
-> epilogue

=== futuristic_defeat ===
Recalibrando parâmetros para futuros encontros.
-> epilogue

=== epilogue ===
{player_culture == "medieval":
    Que os bardos cantem sobre esta partida por gerações!
- else:
    Análise completa. Padrões registrados para otimização futura.
}

* [Jogar Novamente]
    -> culture_choice
* [Encerrar Partida]
    -> END
