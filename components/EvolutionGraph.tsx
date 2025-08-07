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

const EvolutionGraph: React.FC\u003cEvolutionGraphProps\u003e = ({ phases }) =\u003e {
  return (
    \u003cdiv className="w-full max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-lg"\u003e
      \u003ch2 className="text-2xl font-bold text-gray-900 mb-8"\u003e
        Evolução do Sistema Adaptativo
      \u003c/h2\u003e
      
      \u003cdiv className="relative"\u003e
        {/* Linha do tempo */}
        \u003cdiv 
          className="absolute left-8 top-0 bottom-0 w-1 bg-gray-200"
          style={{ transform: 'translateX(-50%)' }}
        /\u003e

        {/* Fases */}
        \u003cdiv className="space-y-8"\u003e
          {phases.map((phase, index) =\u003e (
            \u003cdiv key={phase.name} className="relative pl-20"\u003e
              {/* Indicador de fase */}
              \u003cdiv 
                className={`
                  absolute left-8 w-4 h-4 rounded-full
                  transform -translate-x-1/2
                  ${phase.status === 'completed' ? 'bg-green-500' :
                    phase.status === 'current' ? 'bg-blue-500' :
                    'bg-gray-300'}
                `}
                style={{ top: '50%', marginTop: '-0.5rem' }}
              /\u003e

              {/* Conteúdo da fase */}
              \u003cdiv className="bg-gray-50 p-6 rounded-lg"\u003e
                \u003ch3 className="text-xl font-bold text-gray-800 mb-4"
                  style={{ 
                    color: phase.status === 'completed' ? '#059669' :
                           phase.status === 'current' ? '#2563EB' :
                           '#6B7280'
                  }}
                \u003e
                  {phase.name}
                \u003c/h3\u003e

                {/* Métricas */}
                \u003cdiv className="grid grid-cols-1 md:grid-cols-3 gap-4"\u003e
                  {phase.metrics.map(metric =\u003e (
                    \u003cdiv key={metric.label} className="text-center"\u003e
                      \u003cp className="text-sm text-gray-600 mb-1"\u003e{metric.label}\u003c/p\u003e
                      \u003cdiv className="relative pt-1"\u003e
                        \u003cdiv className="flex mb-2 items-center justify-between"\u003e
                          \u003cdiv\u003e
                            \u003cspan className="text-xs font-semibold inline-block text-gray-600"\u003e
                              {(metric.value * 100).toFixed(0)}%
                            \u003c/span\u003e
                          \u003c/div\u003e
                          \u003cdiv\u003e
                            \u003cspan className="text-xs font-semibold inline-block text-gray-600"\u003e
                              Meta: {(metric.threshold * 100).toFixed(0)}%
                            \u003c/span\u003e
                          \u003c/div\u003e
                        \u003c/div\u003e
                        \u003cdiv className="overflow-hidden h-2 text-xs flex rounded bg-gray-200"\u003e
                          \u003cdiv
                            style={{ width: `${(metric.value * 100)}%` }}
                            className={`
                              shadow-none flex flex-col text-center whitespace-nowrap
                              text-white justify-center
                              ${metric.value \u003e= metric.threshold ? 'bg-green-500' : 'bg-blue-500'}
                            `}
                          \u003e\u003c/div\u003e
                          {/* Indicador de threshold */}
                          \u003cdiv 
                            className="absolute top-0 bottom-0 w-0.5 bg-red-500"
                            style={{ left: `${metric.threshold * 100}%` }}
                          /\u003e
                        \u003c/div\u003e
                      \u003c/div\u003e
                    \u003c/div\u003e
                  ))}\u003c/div\u003e
              \u003c/div\u003e
            \u003c/div\u003e
          ))}\u003c/div\u003e
      \u003c/div\u003e
    \u003c/div\u003e
  );
};

export default EvolutionGraph;
