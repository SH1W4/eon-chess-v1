# 📘 Manual do Projeto: AEON CHESS

## 🏎️ A Analogia da Ferrari
Você perguntou o que significa "ter uma Ferrari" e por que é difícil entender o que foi criado. Aqui está a explicação sincera:

### 1. A Carroceria (Frontend) - **PRONTA E LINDA**
*   **O que é:** O que você vê na tela (Next.js, React, Design).
*   **Estado:** É uma Ferrari de exposição. Pintura impecável, bancos de couro, painel digital.
*   **Onde está:** `src/pages`, `src/components`.
*   **O que faz:** Mostra o tabuleiro, os menus, as animações. Parece um produto de milhões de dólares.

### 2. O Motor (Backend/IA) - **DESMONTADO NA GARAGEM**
*   **O que é:** A inteligência que deveria mover o carro (Python scripts, Lógica de Xadrez, Narrativa).
*   **Estado:** Você tem um motor V12 biturbo... mas ele está desmontado no chão da garagem. As peças (`storyteller.py`, `aeon-brain.js`) são incríveis, mas não estão ligadas umas às outras.
*   **Onde está:** `src/ai`, `src/cultural`, `src/core`.
*   **O que faz:** Atualmente? Nada sozinho. São scripts isolados esperando para serem chamados.

### 3. A Transmissão (Integração) - **FALTANDO**
*   **O que é:** O que conecta o Motor às Rodas.
*   **Estado:** Inexistente. Quando você clica em "Jogar" no site, o painel (Frontend) não manda sinal para o motor (Python). Ele apenas "finge" que mandou (usa dados simulados).
*   **O que falta:** Um servidor API (FastAPI) que receba os cliques do site e execute os scripts Python.

### 4. O Combustível (APIs Reais) - **TANQUE VAZIO**
*   **O que é:** As chaves de API (OpenAI, Anthropic) que dão vida à IA.
*   **Estado:** O sistema está rodando no "modo simulação". Ele não está gastando dinheiro (combustível), mas também não está indo a lugar nenhum de verdade.

---

## 🗺️ O Que Esse Projeto Faz (A Visão)
Quando estiver 100% montado, o **AEON CHESS** será:
1.  **Um Professor de Xadrez Vivo:** Não apenas analisa lances, mas conta uma *história* sobre eles (usando o `storyteller.py`).
2.  **Adaptativo:** Se você joga mal, ele muda a personalidade para "Professor". Se joga bem, vira "Militar" (usando o `aeon-brain`).
3.  **Visual:** Uma experiência de luxo, não apenas um tabuleiro 2D chato.

## 🛠️ Seu Fluxo de Trabalho Atual
É difícil entender porque você está trabalhando em **peças separadas**:
1.  Às vezes você polimento na lataria (Frontend/CSS).
2.  Às vezes você usina uma peça do motor (Python/IA).

**O problema:** Você nunca ligou a chave para ouvir o motor roncar de verdade, porque a fiação (API) não foi feita.

## 🚀 Próximos Passos (Para fazer o carro andar)
Para sair da "exposição" e ir para a "pista":
1.  **Criar a API:** Fazer um arquivo `server.py` que exponha o `storyteller.py` para a internet.
2.  **Conectar os Fios:** Fazer o Frontend chamar esse `server.py` em vez de usar dados falsos.
3.  **Abastecer:** Colocar sua chave da OpenAI/Anthropic.

**Resumo:** Você construiu algo incrível, mas ainda é um modelo estático. O próximo passo é dar vida a ele.
