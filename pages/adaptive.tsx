import React from 'react';
import Layout from '../components/Layout';
import CircularMetric from '../components/CircularMetric';
import EvolutionGraph from '../components/EvolutionGraph';
import useAdaptiveStore from '../src/stores/adaptiveStore';

const AdaptivePage = () =\u003e {
  const { metrics, phase, primaryCapabilities, secondaryCapabilities } = useAdaptiveStore();

  // Dados para o gráfico de evolução
  const evolutionPhases = [
    {
      name: 'Inicialização',
      status: phase === 'initialization' ? 'current' :
              phase === 'adaptation' || phase === 'evolution' || phase === 'autonomy' ? 'completed' : 'pending',
      metrics: [
        {
          label: 'Coesão Adaptativa',
          value: metrics.adaptiveCohesion,
          threshold: 0.8
        }
      ]
    },
    {
      name: 'Adaptação',
      status: phase === 'adaptation' ? 'current' :
              phase === 'evolution' || phase === 'autonomy' ? 'completed' : 'pending',
      metrics: [
        {
          label: 'Equilíbrio de Recursos',
          value: metrics.resourceBalance,
          threshold: 0.7
        }
      ]
    },
    {
      name: 'Evolução',
      status: phase === 'evolution' ? 'current' :
              phase === 'autonomy' ? 'completed' : 'pending',
      metrics: [
        {
          label: 'Estabilidade',
          value: metrics.evolutionStability,
          threshold: 0.9
        }
      ]
    },
    {
      name: 'Autonomia',
      status: phase === 'autonomy' ? 'current' : 'pending',
      metrics: [
        {
          label: 'Saúde do Sistema',
          value: (metrics.adaptiveCohesion + metrics.resourceBalance + metrics.evolutionStability) / 3,
          threshold: 0.85
        }
      ]
    }
  ];

  return (
    \u003cLayout\u003e
      \u003cdiv className="container mx-auto px-4 py-8"\u003e
        {/* Cabeçalho */}
        \u003csection className="mb-16"\u003e
          \u003ch1 className="text-4xl font-bold text-gray-900 mb-4"\u003e
            Sistema Adaptativo
          \u003c/h1\u003e
          \u003cp className="text-xl text-gray-600"\u003e
            Monitore e gerencie a evolução do sistema adaptativo
          \u003c/p\u003e
        \u003c/section\u003e

        {/* Métricas */}
        \u003csection className="mb-16"\u003e
          \u003ch2 className="text-2xl font-semibold text-gray-800 mb-8"\u003e
            Métricas em Tempo Real
          \u003c/h2\u003e
          \u003cdiv className="grid grid-cols-1 md:grid-cols-3 gap-8"\u003e
            \u003cCircularMetric
              label="Coesão Adaptativa"
              value={metrics.adaptiveCohesion}
              maxValue={1}
              size={180}
              thickness={10}
              color="#3B82F6"
            /\u003e
            \u003cCircularMetric
              label="Equilíbrio de Recursos"
              value={metrics.resourceBalance}
              maxValue={1}
              size={180}
              thickness={10}
              color="#10B981"
            /\u003e
            \u003cCircularMetric
              label="Estabilidade Evolutiva"
              value={metrics.evolutionStability}
              maxValue={1}
              size={180}
              thickness={10}
              color="#6366F1"
            /\u003e
          \u003c/div\u003e
        \u003c/section\u003e

        {/* Capacidades */}
        \u003csection className="mb-16"\u003e
          \u003ch2 className="text-2xl font-semibold text-gray-800 mb-8"\u003e
            Capacidades do Sistema
          \u003c/h2\u003e
          \u003cdiv className="grid grid-cols-1 md:grid-cols-2 gap-8"\u003e
            {/* Sistema Primário */}
            \u003cdiv className="bg-white rounded-lg shadow p-6"\u003e
              \u003ch3 className="text-xl font-medium text-gray-800 mb-4"\u003e
                Sistema Primário
              \u003c/h3\u003e
              \u003cdiv className="space-y-2"\u003e
                {primaryCapabilities.map(cap =\u003e (
                  \u003cdiv
                    key={cap}
                    className="flex items-center justify-between bg-blue-50 p-3 rounded"
                  \u003e
                    \u003cspan className="text-blue-800"\u003e{cap}\u003c/span\u003e
                    \u003cspan className="text-blue-600 text-sm"\u003eAtivo\u003c/span\u003e
                  \u003c/div\u003e
                ))}
              \u003c/div\u003e
            \u003c/div\u003e

            {/* Sistema Secundário */}
            \u003cdiv className="bg-white rounded-lg shadow p-6"\u003e
              \u003ch3 className="text-xl font-medium text-gray-800 mb-4"\u003e
                Sistema Secundário
              \u003c/h3\u003e
              \u003cdiv className="space-y-2"\u003e
                {secondaryCapabilities.map(cap =\u003e (
                  \u003cdiv
                    key={cap}
                    className="flex items-center justify-between bg-green-50 p-3 rounded"
                  \u003e
                    \u003cspan className="text-green-800"\u003e{cap}\u003c/span\u003e
                    \u003cspan className="text-green-600 text-sm"\u003eAtivo\u003c/span\u003e
                  \u003c/div\u003e
                ))}
              \u003c/div\u003e
            \u003c/div\u003e
          \u003c/div\u003e
        \u003c/section\u003e

        {/* Evolução */}
        \u003csection className="mb-16"\u003e
          \u003cEvolutionGraph phases={evolutionPhases} /\u003e
        \u003c/section\u003e
      \u003c/div\u003e
    \u003c/Layout\u003e
  );
};

export default AdaptivePage;
