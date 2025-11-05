# CHESS - Cultural Heritage Enhanced Strategic System

An experimental chess platform that combines traditional chess gameplay with cultural narratives, adaptive AI, and gamification elements.

## 🚧 Project Status: In Active Development

This project is currently in experimental phase. Many features are under development and the API/architecture may change.

## 🎯 Project Overview

CHESS aims to create an innovative chess experience by integrating:
- **Cultural Narratives**: Dynamic storytelling based on chess pieces representing different cultures
- **Adaptive AI**: Machine learning-powered opponent that adapts to player style
- **Gamification System**: Comprehensive progression, achievements, and virtual economy
- **Educational Elements**: Learn about world cultures through gameplay

### 🌟 Project Vision

#### 🎯 Short-term (2026)
Check out our [Vision 2026 document](docs/VISAO_2026.md) for immediate goals:
- AI system optimization (95%+ accuracy)
- Enhanced user experience (NPS > 85)
- Cultural system expansion (20+ cultures)
- Performance improvements (< 50ms latency)

#### 🔮 Long-term (2035)
Check out our [Vision 2035 document](docs/VISAO_2035.md) to understand where we're headed:
- Advanced neural architectures
- Quantum-classical hybrid processing
- Neural interfaces and holographic visualization
- Sustainable and ethical AI development
- Global cultural preservation and evolution

## 🔧 Technology Stack

### Core Technologies
- **Frontend**: Next.js, React, TypeScript
- **Backend**: FastAPI (Python)
- **AI/ML**: TensorFlow, Chess engine integration
- **Narrative**: Ink narrative scripting language
- **Database**: PostgreSQL (planned)
- **Real-time**: WebSockets for multiplayer (planned)

### Integration Layer
- **MCP (Model Context Protocol)**:
  - [Specification](docs/MCP_SPECIFICATION.md) - Especificação técnica detalhada
  - [Implementation Superscope](docs/TASKMASH_MCP_SUPERSCOPE.md) - Plano de implementação
  - [ARKITECT Workflow](.arkitect/workflows/mcp_superscope.yaml) - Integração com ARKITECT
  - Features:
    - Multi-model orchestration
    - Context sharing and synchronization
    - Symbiotic evolution
    - Cultural integration

## 📁 Project Structure

```
CHESS/
├── src/
│   ├── api/          # FastAPI backend
│   ├── frontend/     # Next.js application
│   └── shared/       # Shared utilities
├── gamification/     # Gamification system
├── landing-page/     # Static landing page
├── docs/            # GitHub Pages documentation
└── out/             # Build outputs
```

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- Python 3.9+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NEO-SH1W4/eon-chess-v1.git
cd eon-chess-v1
```

2. Install frontend dependencies:
```bash
cd src/frontend
npm install
```

3. Install backend dependencies:
```bash
cd ../api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Development Server

1. Start the API server:
```bash
cd src/api
python main.py
```

2. Start the frontend:
```bash
cd src/frontend
npm run dev
```

3. (Optional) Serve the landing page:
```bash
cd landing-page
python -m http.server 8000
```

## 🎮 Features

### Implemented
- ✅ Basic chess gameplay with AI
- ✅ Landing page with project information
- ✅ Initial gamification system structure
- ✅ Virtual economy framework

### In Development
- 🔧 Cultural narrative integration
- 🔧 Adaptive AI opponents
- 🔧 Achievement system
- 🔧 Player progression
- 🔧 Tournament system

### Planned
- 📋 Multiplayer support
- 📋 Mobile applications
- 📋 Advanced analytics
- 📋 Community features

## 🤝 Contributing

We welcome contributions! Please note:
- This is an experimental project
- Code quality and documentation are priorities
- All contributions should align with the cultural education mission

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Acknowledgments

- Chess.js library for chess logic
- Ink narrative language for storytelling
- The open-source community

## 📧 Contact

For questions or collaboration opportunities, please open an issue on GitHub.

---

**Note**: This is an experimental project in active development. Features, APIs, and documentation are subject to change.
