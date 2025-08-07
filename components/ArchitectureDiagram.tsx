import { useEffect } from 'react';
import mermaid from 'mermaid';

// Configuração do tema Mermaid com cores que combinam com sua interface
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#1d3557',
    primaryTextColor: '#f1faee',
    primaryBorderColor: '#457b9d',
    lineColor: '#a8dadc',
    secondaryColor: '#e63946',
    tertiaryColor: '#2a9d8f'
  },
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'basis'
  }
});

const diagram = `
graph TB
    %% Interface Layer
    subgraph Interface["Interface Layer"]
        WebUI["Web UI"]
        Mobile["Mobile"]
        Desktop["Desktop"]
        WebUI --- Mobile
        Mobile --- Desktop
    end

    %% Symbiotic Core
    subgraph Core["Symbiotic Core"]
        ARQUIMAX["ARQUIMAX"]
        NEXUS["NEXUS"]
        CHESS["CHESS Engine"]
        ARQUIMAX <--> NEXUS
        NEXUS <--> CHESS
    end

    %% Neural Network Layer
    subgraph Neural["Neural Network Layer"]
        Cultural["Cultural Engine"]
        AI["AI Engine"]
        Cultural <--> AI
    end

    %% Data Layer
    subgraph Data["Data & Learning Layer"]
        CulturalDB["Cultural DB"]
        NeuralDB["Neural DB & Cache"]
        CulturalDB <--> NeuralDB
    end

    %% Connections between layers
    Interface --> Core
    Core --> Neural
    Neural --> Data

    %% Style definitions
    classDef interface fill:#1d3557,stroke:#a8dadc,stroke-width:2px,color:#f1faee
    classDef core fill:#e63946,stroke:#a8dadc,stroke-width:2px,color:#f1faee
    classDef neural fill:#457b9d,stroke:#a8dadc,stroke-width:2px,color:#f1faee
    classDef data fill:#2a9d8f,stroke:#a8dadc,stroke-width:2px,color:#f1faee

    %% Apply styles
    class WebUI,Mobile,Desktop interface
    class ARQUIMAX,NEXUS,CHESS core
    class Cultural,AI neural
    class CulturalDB,NeuralDB data
`;

interface Props {
  className?: string;
}

export const ArchitectureDiagram: React.FC<Props> = ({ className = '' }) => {
  useEffect(() => {
    // Renderiza o diagrama quando o componente montar
    mermaid.contentLoaded();
  }, []);

  return (
    <div className={`architecture-diagram ${className}`}>
      <style jsx>{`
        .architecture-diagram {
          background: transparent;
          padding: 1rem;
          border-radius: 0.5rem;
          width: 100%;
          max-width: 1200px;
          margin: 0 auto;
        }
        :global(.mermaid) {
          display: flex;
          justify-content: center;
          align-items: center;
          background: transparent;
        }
        :global(.mermaid svg) {
          max-width: 100%;
          height: auto;
        }
      `}</style>
      <div className="mermaid">
        {diagram}
      </div>
    </div>
  );
};

export default ArchitectureDiagram;
