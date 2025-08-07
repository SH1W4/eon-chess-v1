import React, { useEffect } from 'react';
import Layout from '../components/Layout';
import CircularMetric from '../components/CircularMetric';
import EvolutionGraph from '../components/EvolutionGraph';
import SymbioticMetrics from '../components/SymbioticMetrics';
import AdaptiveInsights from '../components/AdaptiveInsights';
import EmergencePatterns from '../components/EmergencePatterns';
import useAdaptiveStore from '../src/stores/adaptiveStore';
import useSymbioticStore from '../src/stores/symbioticStore';

const AdaptivePage = () => {
  const { metrics, phase, primaryCapabilities, secondaryCapabilities } = useAdaptiveStore();
  const { 
    symbioticMetrics,
    emergencePatterns,
    updateSymbioticMetrics,
    analyzeEmergencePatterns 
  } = useSymbioticStore();

  useEffect(() => {
    // Atualiza métricas simbióticas periodicamente
    const interval = setInterval(() => {
      updateSymbioticMetrics();
      analyzeEmergencePatterns();
    }, 30000); // A cada 30 segundos

    return () => clearInterval(interval);
  }, []);

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
    <Layout>
      <div className="container mx-auto px-4 py-8">
        {/* Cabeçalho */}
        <section className="mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Sistema Adaptativo
          </h1>
          <p className="text-xl text-gray-600">
            Monitore e gerencie a evolução do sistema adaptativo
          </p>
        </section>

        {/* Métricas */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold text-gray-800 mb-8">
            Métricas em Tempo Real
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <CircularMetric
              label="Coesão Adaptativa"
              value={metrics.adaptiveCohesion}
              maxValue={1}
              size={180}
              thickness={10}
              color="#3B82F6"
            />
            <CircularMetric
              label="Equilíbrio de Recursos"
              value={metrics.resourceBalance}
              maxValue={1}
              size={180}
              thickness={10}
              color="#10B981"
            />
            <CircularMetric
              label="Estabilidade Evolutiva"
              value={metrics.evolutionStability}
              maxValue={1}
              size={180}
              thickness={10}
              color="#6366F1"
            />
          </div>
        </section>

        {/* Capacidades */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold text-gray-800 mb-8">
            Capacidades do Sistema
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Sistema Primário */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-medium text-gray-800 mb-4">
                Sistema Primário
              </h3>
              <div className="space-y-2">
                {primaryCapabilities.map(cap => (
                  <div
                    key={cap}
                    className="flex items-center justify-between bg-blue-50 p-3 rounded"
                  >
                    <span className="text-blue-800">{cap}</span>
                    <span className="text-blue-600 text-sm">Ativo</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Sistema Secundário */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-medium text-gray-800 mb-4">
                Sistema Secundário
              </h3>
              <div className="space-y-2">
                {secondaryCapabilities.map(cap => (
                  <div
                    key={cap}
                    className="flex items-center justify-between bg-green-50 p-3 rounded"
                  >
                    <span className="text-green-800">{cap}</span>
                    <span className="text-green-600 text-sm">Ativo</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Evolução */}
        <section className="mb-16">
          <EvolutionGraph phases={evolutionPhases} />
        </section>

        {/* Métricas Simbióticas */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold text-gray-800 mb-8">
            Integração Simbiótica
          </h2>
          <SymbioticMetrics metrics={symbioticMetrics} />
        </section>

        {/* Insights Adaptativos */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold text-gray-800 mb-8">
            Insights Adaptativos
          </h2>
          <AdaptiveInsights 
            phase={phase}
            metrics={metrics}
            symbioticMetrics={symbioticMetrics}
          />
        </section>

        {/* Padrões de Emergência */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold text-gray-800 mb-8">
            Padrões de Emergência
          </h2>
          <EmergencePatterns patterns={emergencePatterns} />
        </section>
      </div>
    </Layout>
  );
};

export default AdaptivePage;
