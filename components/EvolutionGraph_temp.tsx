import React from 'react';

interface EvolutionPhase {
  name: string;
  status: 'completed' | 'current' | 'pending';
  metrics: {
    label: string;
    value: number;
    threshold: number;
  }[];
}

interface EvolutionGraphProps {
  phases: EvolutionPhase[];
}

const EvolutionGraph: React.FC<EvolutionGraphProps> = ({ phases }) => {
  return (
    <div>
      <h2>Evolução do Sistema Adaptativo</h2>
      <div>
        {phases.map((phase) => (
          <div key={phase.name}>
            <h3>{phase.name}</h3>
            <div>
              {phase.metrics.map((metric) => (
                <div key={metric.label}>
                  <p>{metric.label}</p>
                  <p>{(metric.value * 100).toFixed(0)}%</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EvolutionGraph;
