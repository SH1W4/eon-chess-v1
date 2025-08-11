# 🎯 Guia do Usuário - AEON Chess

## Bem-vindo ao AEON Chess!

O AEON Chess é um sistema de xadrez revolucionário que combina inteligência artificial adaptativa com elementos culturais profundos, criando uma experiência única e imersiva de jogo.

## 📖 Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Começando a Jogar](#começando-a-jogar)
4. [Perfis Culturais](#perfis-culturais)
5. [Modos de Jogo](#modos-de-jogo)
6. [Interface do Jogo](#interface-do-jogo)
7. [Recursos Especiais](#recursos-especiais)
8. [Dicas e Estratégias](#dicas-e-estratégias)
9. [Solução de Problemas](#solução-de-problemas)

## 🚀 Introdução

O AEON Chess não é apenas mais um jogo de xadrez. É uma experiência que une:

- **IA Adaptativa**: Aprende seu estilo e se adapta para oferecer desafios equilibrados
- **Narrativas Culturais**: Cada movimento gera narrativas únicas baseadas em culturas históricas
- **Perfis Temáticos**: 10+ culturas diferentes, cada uma com estratégias e estilos únicos
- **Sistema Simbiótico**: O jogo evolui com você, criando uma experiência personalizada

## 💻 Instalação

### Requisitos do Sistema

- **Sistema Operacional**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 ou superior
- **Memória RAM**: Mínimo 4GB (8GB recomendado)
- **Espaço em Disco**: 500MB
- **Conexão Internet**: Para recursos online e atualizações

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/aeon-chess.git
cd aeon-chess

# Instale as dependências
pip install -r requirements.txt

# Execute o jogo
python main.py
```

### Instalação da Interface Web

```bash
# Entre no diretório web
cd src/web

# Instale dependências
npm install

# Inicie o servidor de desenvolvimento
npm start
```

O jogo estará disponível em `http://localhost:3000`

## 🎮 Começando a Jogar

### Primeiro Jogo

1. **Abra o jogo** através da interface web ou aplicativo desktop
2. **Escolha seu perfil cultural** (recomendamos começar com Persa ou Chinês)
3. **Selecione o nível de dificuldade**:
   - 🟢 **Iniciante**: Para quem está aprendendo xadrez
   - 🟡 **Intermediário**: Para jogadores casuais
   - 🔴 **Avançado**: Para jogadores experientes
   - 🟣 **Adaptativo**: A IA ajusta a dificuldade dinamicamente

4. **Faça seu primeiro movimento** clicando na peça e depois no destino

### Controles Básicos

- **Mover Peça**: Clique na peça → Clique no destino
- **Desfazer**: `Ctrl+Z` ou botão ↩️
- **Refazer**: `Ctrl+Y` ou botão ↪️
- **Nova Partida**: `Ctrl+N` ou botão 🔄
- **Pausar**: `Space` ou botão ⏸️

## 🌍 Perfis Culturais

Cada cultura oferece uma experiência única:

### 🏛️ **Persa**
- **Estilo**: Estratégico e poético
- **Características**: Controle do centro, sacrifícios calculados
- **Ideal para**: Jogadores que apreciam beleza e estratégia

### 🏹 **Mongol**
- **Estilo**: Agressivo e móvel
- **Características**: Ataques rápidos, pressão constante
- **Ideal para**: Jogadores que gostam de ação intensa

### 🏮 **Chinês**
- **Estilo**: Paciente e calculista
- **Características**: Desenvolvimento lento, armadilhas sutis
- **Ideal para**: Jogadores estratégicos de longo prazo

### 🕉️ **Indiano**
- **Estilo**: Místico e criativo
- **Características**: Movimentos não convencionais, transformação
- **Ideal para**: Jogadores que pensam fora da caixa

### 🌙 **Árabe**
- **Estilo**: Matemático e preciso
- **Características**: Cálculos profundos, geometria do tabuleiro
- **Ideal para**: Jogadores analíticos

### ⛩️ **Japonês**
- **Estilo**: Disciplinado e honorável
- **Características**: Defesa sólida, golpes decisivos
- **Ideal para**: Jogadores metódicos

### ⚔️ **Viking**
- **Estilo**: Feroz e direto
- **Características**: Ataque frontal, sem recuo
- **Ideal para**: Jogadores corajosos

### 🎭 **Asteca**
- **Estilo**: Ritualístico e simbólico
- **Características**: Sacrifícios estratégicos, pressão psicológica
- **Ideal para**: Jogadores táticos

### 🗿 **Maia**
- **Estilo**: Visionário e cósmico
- **Características**: Padrões complexos, previsão
- **Ideal para**: Jogadores que veem o quadro geral

### 🗾 **Samurai**
- **Estilo**: Técnico e determinado
- **Características**: Perfeição técnica, lealdade às peças
- **Ideal para**: Jogadores perfeccionistas

## 🎯 Modos de Jogo

### Jogo Rápido
- Partida padrão contra a IA
- Configurações rápidas
- Ideal para sessões casuais

### Campanha Cultural
- Jogue através de todas as culturas
- Desbloqueie narrativas especiais
- Ganhe conquistas culturais

### Modo História
- Reviva batalhas históricas famosas
- Aprenda sobre xadrez em diferentes culturas
- Narrativas expandidas e cinemáticas

### Modo Análise
- Analise suas partidas
- Veja sugestões da IA
- Aprenda com seus erros

### Multiplayer Online
- Jogue contra outros jogadores
- Torneios temáticos
- Rankings por cultura

## 🖥️ Interface do Jogo

### Tabuleiro Principal
- **Peças**: Clique para ver movimentos válidos
- **Destaque**: Quadrados válidos aparecem em verde
- **Última Jogada**: Destacada em amarelo
- **Xeque**: Rei em perigo aparece em vermelho

### Painel de Narrativa
- **Narrativas em Tempo Real**: Histórias geradas para cada movimento
- **Contexto Cultural**: Explicações sobre estratégias culturais
- **Momentos Épicos**: Destaques de jogadas importantes

### Controles do Jogo
- **Timer**: Mostra tempo restante de cada jogador
- **Histórico**: Lista de movimentos realizados
- **Análise**: Avaliação da posição atual
- **Configurações**: Ajuste som, tema visual, etc.

## ✨ Recursos Especiais

### Sistema de Narrativa Dinâmica
Cada movimento gera uma narrativa única baseada em:
- Cultura escolhida
- Contexto da partida
- Importância do movimento
- Fase do jogo (abertura, meio-jogo, final)

### IA Adaptativa
A inteligência artificial:
- Aprende seu estilo de jogo
- Ajusta a dificuldade dinamicamente
- Oferece desafios personalizados
- Evolui com cada partida

### Movimentos Especiais Culturais
Algumas culturas têm interpretações únicas:
- **Gambito do Xá** (Persa): Sacrifício poético de peão
- **Carga da Horda** (Mongol): Avanço coordenado de peões
- **Muralha de Jade** (Chinês): Formação defensiva sólida

## 💡 Dicas e Estratégias

### Para Iniciantes
1. **Comece com o básico**: Pratique no modo Iniciante
2. **Leia as narrativas**: Elas explicam conceitos importantes
3. **Use o modo análise**: Aprenda com cada partida
4. **Experimente culturas diferentes**: Cada uma ensina algo novo

### Para Intermediários
1. **Domine uma cultura**: Especialize-se antes de diversificar
2. **Estude os padrões**: Cada cultura tem aberturas preferidas
3. **Use a pausa estratégica**: Analise posições complexas
4. **Participe de torneios culturais**: Teste suas habilidades

### Para Avançados
1. **Modo Adaptativo**: Deixe a IA desafiar você ao máximo
2. **Combine estilos**: Misture estratégias de diferentes culturas
3. **Crie suas narrativas**: Compartilhe partidas épicas
4. **Contribua com a comunidade**: Sugira melhorias e novos recursos

## 🔧 Solução de Problemas

### Problemas Comuns

**O jogo não inicia**
- Verifique se Python 3.8+ está instalado
- Execute `pip install -r requirements.txt` novamente
- Confira mensagens de erro no console

**Interface web não carrega**
- Verifique se a porta 3000 está livre
- Execute `npm install` no diretório web
- Limpe o cache do navegador

**IA demora para responder**
- Normal em posições complexas
- Reduza a profundidade de análise nas configurações
- Considere usar modo "Resposta Rápida"

**Narrativas não aparecem**
- Verifique se o módulo narrativo está ativo
- Recarregue a página
- Verifique configurações de idioma

### Suporte

- **Discord**: [discord.gg/aeonchess](https://discord.gg/aeonchess)
- **Email**: support@aeonchess.com
- **GitHub Issues**: Para bugs e sugestões
- **Wiki**: [wiki.aeonchess.com](https://wiki.aeonchess.com)

## 🎉 Conclusão

O AEON Chess é mais que um jogo - é uma jornada através de culturas e estratégias. Cada partida é única, cada movimento conta uma história, e cada vitória é uma conquista cultural.

**Que suas partidas sejam épicas e suas narrativas, lendárias!**

---

*"No AEON Chess, você não apenas joga xadrez - você vive a história do jogo através dos olhos de grandes civilizações."*
