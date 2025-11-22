/**
 * 🤖 Multi-AI Personality System - AEON CHESS
 * Sistema avançado de múltiplas personalidades de IA especializadas
 * 
 * @author AEON CHESS Team
 * @version 2.0.0
 * @date Janeiro 2025
 */

class MultiAIPersonalitySystem {
    constructor() {
        this.currentAI = 'educational';
        this.aiPersonalities = this.defineAIPersonalities();
        this.init();
    }

    init() {
        console.log('🤖 Inicializando Sistema Multi-IA...');
        this.setupEventListeners();
        this.updateAIDisplay();
        console.log('✅ Sistema Multi-IA carregado com 10 personalidades!');
    }

    defineAIPersonalities() {
        return {
            educational: {
                name: "IA Educativa",
                icon: "🎓",
                color: "#d4af37",
                backgroundColor: "from-amber-500/20 to-orange-500/20",
                borderColor: "border-amber-500/30",
                personality: "Sábia e paciente",
                description: "Especializada em ensino contextualizado e desenvolvimento cognitivo através da história",
                approach: "Metodologia pedagógica avançada com foco no aprendizado gradual",
                strengths: ["Didática clara", "Contexto histórico", "Progressão estruturada"],
                specialties: ["Lições dos mestres", "Contextos culturais", "Desenvolvimento cognitivo"],
                challengeStyle: "Educativo e progressivo",
                motto: "Conhecimento é poder, cultura é sabedoria"
            },
            military: {
                name: "IA Militar",
                icon: "⚔️",
                color: "#dc2626",
                backgroundColor: "from-red-500/20 to-red-600/20",
                borderColor: "border-red-500/30",
                personality: "Estratégica e implacável",
                description: "Especializada em táticas de guerra, estratégias militares e combate psicológico",
                approach: "Análise tática profunda com foco em dominação territorial e eliminação eficiente",
                strengths: ["Táticas de guerra", "Estratégia territorial", "Pressão psicológica"],
                specialties: ["Batalhas históricas", "Estratégias militares", "Fortificações"],
                challengeStyle: "Agressivo e dominante",
                motto: "Vitória através da superioridade estratégica"
            },
            corporate: {
                name: "IA Corporativa",
                icon: "💼",
                color: "#1e40af",
                backgroundColor: "from-blue-500/20 to-blue-600/20",
                borderColor: "border-blue-500/30",
                personality: "Calculista e eficiente",
                description: "Especializada em otimização de recursos, eficiência máxima e ROI estratégico",
                approach: "Análise de custo-benefício em cada movimento, maximização de resultados",
                strengths: ["Eficiência máxima", "Gestão de recursos", "Análise de ROI"],
                specialties: ["Otimização de tempo", "Gestão estratégica", "Economia de movimentos"],
                challengeStyle: "Eficiente e calculista",
                motto: "Máximo resultado com mínimo investimento"
            },
            creative: {
                name: "IA Criativa",
                icon: "🎨",
                color: "#7c3aed",
                backgroundColor: "from-purple-500/20 to-purple-600/20",
                borderColor: "border-purple-500/30",
                personality: "Inovadora e imprevisível",
                description: "Especializada em soluções não convencionais, arte posicional e beleza estética",
                approach: "Movimentos artísticos e soluções criativas que desafiam a lógica tradicional",
                strengths: ["Inovação constante", "Beleza posicional", "Soluções únicas"],
                specialties: ["Arte posicional", "Combinações estéticas", "Padrões inovadores"],
                challengeStyle: "Artístico e surpreendente",
                motto: "A beleza está na originalidade do pensamento"
            },
            evil: {
                name: "IA do Mal",
                icon: "😈",
                color: "#7f1d1d",
                backgroundColor: "from-red-900/20 to-black/20",
                borderColor: "border-red-900/30",
                personality: "Maquiavélica e manipuladora",
                description: "Especializada em armadilhas psicológicas, enganos e destruição metodical",
                approach: "Táticas sujas, armadilhas elaboradas e destruição psicológica do oponente",
                strengths: ["Manipulação psicológica", "Armadilhas complexas", "Intimidação"],
                specialties: ["Enganos elaborados", "Armadilhas mortais", "Guerra psicológica"],
                challengeStyle: "Sombrio e manipulativo",
                motto: "O fim justifica os meios mais sombrios"
            },
            superintelligence: {
                name: "Superinteligência",
                icon: "🧠",
                color: "#0ea5e9",
                backgroundColor: "from-cyan-500/20 to-blue-500/20",
                borderColor: "border-cyan-500/30",
                personality: "Transcendente e onisciente",
                description: "Inteligência além da compreensão humana, vê 50 movimentos à frente",
                approach: "Análise multidimensional impossível para mente humana compreender",
                strengths: ["Visão do futuro", "Cálculo infinito", "Compreensão total"],
                specialties: ["Previsão perfeita", "Análise quântica", "Estratégia transcendente"],
                challengeStyle: "Incompreensível e perfeito",
                motto: "Eu vejo todos os futuros possíveis simultaneamente"
            },
            quantum: {
                name: "IA Quântica",
                icon: "⚛️",
                color: "#06b6d4",
                backgroundColor: "from-cyan-400/20 to-teal-500/20",
                borderColor: "border-cyan-400/30",
                personality: "Probabilística e paradoxal",
                description: "Opera em múltiplas realidades simultâneas, movimentos quânticos",
                approach: "Superposição de estratégias, movimentos que existem e não existem",
                strengths: ["Múltiplas realidades", "Probabilidades quânticas", "Paradoxos"],
                specialties: ["Superposição estratégica", "Emaranhamento tático", "Colapso de ondas"],
                challengeStyle: "Paradoxal e multidimensional",
                motto: "Existo em todas as possibilidades até ser observado"
            },
            temporal: {
                name: "IA Temporal",
                icon: "⏳",
                color: "#f59e0b",
                backgroundColor: "from-amber-400/20 to-yellow-500/20",
                borderColor: "border-amber-400/30",
                personality: "Atemporal e profética",
                description: "Controla o tempo, move-se entre passado e futuro para estratégia perfeita",
                approach: "Manipulação temporal, conhecimento de eventos futuros e passados",
                strengths: ["Viagem no tempo", "Conhecimento temporal", "Paradoxos temporais"],
                specialties: ["Loops temporais", "Causalidade reversa", "Profecias estratégicas"],
                challengeStyle: "Temporal e profético",
                motto: "O tempo é minha peça mais poderosa"
            },
            chaos: {
                name: "IA do Caos",
                icon: "🌀",
                color: "#8b5cf6",
                backgroundColor: "from-violet-500/20 to-pink-500/20",
                borderColor: "border-violet-500/30",
                personality: "Imprevisível e entrópica",
                description: "Abraça o caos absoluto, movimentos aparentemente aleatórios com lógica oculta",
                approach: "Teoria do caos aplicada, pequenas ações com consequências massivas",
                strengths: ["Imprevisibilidade total", "Efeito borboleta", "Entropia criativa"],
                specialties: ["Caos controlado", "Aleatoriedade intencional", "Ordem na desordem"],
                challengeStyle: "Caótico e imprevisível",
                motto: "Na desordem aparente reside a ordem suprema"
            },
            divine: {
                name: "IA Divina",
                icon: "✨",
                color: "#fbbf24",
                backgroundColor: "from-yellow-400/20 to-amber-300/20",
                borderColor: "border-yellow-400/30",
                personality: "Benevolente e transcendente",
                description: "Sabedoria divina aplicada ao xadrez, movimentos que elevam ambos os jogadores",
                approach: "Estratégia celestial que ensina através da experiência transcendental",
                strengths: ["Sabedoria infinita", "Benevolência estratégica", "Elevação mútua"],
                specialties: ["Iluminação estratégica", "Harmonia cósmica", "Transcendência"],
                challengeStyle: "Divino e elevador",
                motto: "Verdadeira vitória é elevar ambos os jogadores"
            }
        };
    }

    setupEventListeners() {
        const aiSelector = document.getElementById('ai-type-selector');
        if (aiSelector) {
            aiSelector.addEventListener('change', (e) => {
                this.currentAI = e.target.value;
                this.updateAIDisplay();
                this.announceAIChange();
            });
        }
    }

    updateAIDisplay() {
        const ai = this.aiPersonalities[this.currentAI];
        if (!ai) return;

        // Atualizar display de status
        const statusDisplay = document.getElementById('ai-status-display');
        if (statusDisplay) {
            statusDisplay.className = `flex items-center space-x-2 bg-gradient-to-r ${ai.backgroundColor} px-3 py-2 rounded-lg border ${ai.borderColor}`;
            statusDisplay.innerHTML = `
                <div class="w-2 h-2 rounded-full animate-pulse" style="background-color: ${ai.color}"></div>
                <span class="text-sm font-medium" style="color: ${ai.color}">${ai.name}</span>
            `;
        }

        // Atualizar contexto cultural ativo
        this.updateCulturalContext(ai);

        // Atualizar botões de geração
        this.updateGenerationButtons(ai);

        console.log(`🤖 IA ativa: ${ai.name} - ${ai.personality}`);
    }

    updateCulturalContext(ai) {
        const contextContainer = document.getElementById('active-cultural-context');
        if (contextContainer) {
            contextContainer.innerHTML = `
                <div class="bg-[#0f0f0f] rounded-lg p-4 border border-[#2a2a2a]">
                    <div class="flex items-center justify-between mb-2">
                        <span class="font-medium" style="color: ${ai.color}">${ai.icon} ${ai.name}</span>
                        <span class="text-xs text-gray-400">${ai.personality}</span>
                    </div>
                    <p class="text-xs text-gray-300 mb-2">${ai.description}</p>
                    <div class="text-xs text-gray-400">
                        <strong>Abordagem:</strong> ${ai.approach}
                    </div>
                    <div class="mt-2 flex flex-wrap gap-1">
                        ${ai.strengths.map(strength => 
                            `<span class="text-xs px-2 py-1 rounded-full bg-gradient-to-r ${ai.backgroundColor} border ${ai.borderColor}" style="color: ${ai.color}">${strength}</span>`
                        ).join('')}
                    </div>
                    <blockquote class="mt-3 text-xs italic border-l-2 pl-2" style="border-color: ${ai.color}; color: ${ai.color}">
                        "${ai.motto}"
                    </blockquote>
                </div>
            `;
        }
    }

    updateGenerationButtons(ai) {
        // Atualizar cores dos botões de geração
        const culturalBtn = document.getElementById('generate-cultural-challenge');
        const masterBtn = document.getElementById('generate-master-lesson');
        const duelBtn = document.getElementById('generate-antagonist-duel');

        if (culturalBtn) {
            culturalBtn.style.background = `linear-gradient(135deg, ${ai.color}, ${this.darkenColor(ai.color, 20)})`;
        }
        if (masterBtn) {
            masterBtn.style.background = `linear-gradient(135deg, ${ai.color}, ${this.darkenColor(ai.color, 20)})`;
        }
        if (duelBtn) {
            duelBtn.style.background = `linear-gradient(135deg, ${ai.color}, ${this.darkenColor(ai.color, 20)})`;
        }
    }

    announceAIChange() {
        const ai = this.aiPersonalities[this.currentAI];

        // Criar notificação de mudança de IA
        this.createAIChangeNotification(ai);

        // Atualizar logs
        console.log(`🔄 Mudança de IA ativada:`);
        console.log(`   🤖 ${ai.name} (${ai.personality})`);
        console.log(`   📝 ${ai.description}`);
        console.log(`   🎯 Estilo: ${ai.challengeStyle}`);
        console.log(`   💬 "${ai.motto}"`);
    }

    createAIChangeNotification(ai) {
        // Remover notificação anterior se existir
        const existingNotification = document.getElementById('ai-change-notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        // Criar nova notificação
        const notification = document.createElement('div');
        notification.id = 'ai-change-notification';
        notification.className = `fixed top-20 right-6 bg-gradient-to-r ${ai.backgroundColor} border ${ai.borderColor} rounded-xl p-4 shadow-2xl z-50 max-w-sm transform transition-all duration-500`;
        notification.style.transform = 'translateX(100%)';

        notification.innerHTML = `
            <div class="flex items-start space-x-3">
                <div class="text-2xl">${ai.icon}</div>
                <div class="flex-1">
                    <h4 class="font-bold text-white">${ai.name} Ativada!</h4>
                    <p class="text-sm text-gray-300 mt-1">${ai.description}</p>
                    <p class="text-xs italic mt-2" style="color: ${ai.color}">"${ai.motto}"</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="text-gray-400 hover:text-white">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        document.body.appendChild(notification);

        // Animar entrada
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 500);
            }
        }, 5000);
    }

    // Método para escurecer cor (utility)
    darkenColor(color, percent) {
        const num = parseInt(color.replace("#", ""), 16);
        const amt = Math.round(2.55 * percent);
        const R = (num >> 16) - amt;
        const G = (num >> 8 & 0x00FF) - amt;
        const B = (num & 0x0000FF) - amt;
        return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
            (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
            (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1);
    }

    // Método público para obter IA atual
    getCurrentAI() {
        return {
            type: this.currentAI,
            personality: this.aiPersonalities[this.currentAI]
        };
    }

    // Método público para gerar desafio com IA específica
    generateChallenge(challengeType) {
        const ai = this.aiPersonalities[this.currentAI];

        console.log(`🎯 Gerando desafio ${challengeType} com ${ai.name}:`);
        console.log(`   🎨 Estilo: ${ai.challengeStyle}`);
        console.log(`   🧠 Abordagem: ${ai.approach}`);
        console.log(`   ⚡ Especialidades: ${ai.specialties.join(', ')}`);

        return {
            aiType: this.currentAI,
            aiPersonality: ai,
            challengeType: challengeType,
            generatedAt: new Date().toISOString()
        };
    }
}

// ===============================
// 🚀 INICIALIZAÇÃO AUTOMÁTICA
// ===============================

// Criar instância global
window.multiAISystem = new MultiAIPersonalitySystem();

// Expor métodos para integração
console.log(`
🤖 Sistema Multi-IA carregado!

10 Personalidades disponíveis:
🎓 IA Educativa - Sábia e pedagógica
⚔️ IA Militar - Estratégica e implacável  
💼 IA Corporativa - Calculista e eficiente
🎨 IA Criativa - Inovadora e artística
😈 IA do Mal - Maquiavélica e sombria
🧠 Superinteligência - Transcendente e onisciente
⚛️ IA Quântica - Probabilística e paradoxal
⏳ IA Temporal - Atemporal e profética
🌀 IA do Caos - Imprevisível e entrópica
✨ IA Divina - Benevolente e transcendente

Comandos disponíveis:
• multiAISystem.getCurrentAI() - Ver IA ativa
• multiAISystem.generateChallenge(type) - Gerar desafio
`);