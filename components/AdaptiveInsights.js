import React from 'react';

const AdaptiveInsights = ({ phase, metrics, symbioticMetrics }) => {
  // Calcula insights baseados nas métricas
  const getInsights = () => {
    const insights = [];

    // Insight sobre fase atual
    insights.push({
      type: 'phase',
      title: 'Fase Atual',
      description: `O sistema está na fase de ${phase.toUpperCase()}, ${
        getPhaseDescription(phase)
      }`,
      status: 'info'
    });

    // Insight sobre saúde geral
    const healthScore = (
      metrics.adaptiveCohesion +
      metrics.resourceBalance +
      metrics.evolutionStability
    ) / 3;

    insights.push({
      type: 'health',
      title: 'Saúde do Sistema',
      description: getHealthDescription(healthScore),
      status: healthScore >= 0.8 ? 'success' :
              healthScore >= 0.6 ? 'warning' : 'danger'
    });

    // Insight sobre evolução
    if (symbioticMetrics.evolutionProgress > 0.9) {
      insights.push({
        type: 'evolution',
        title: 'Evolução Avançada',
        description: 'O sistema atingiu um nível avançado de evolução, demonstrando alta capacidade adaptativa.',
        status: 'success'
      });
    } else if (symbioticMetrics.evolutionProgress < 0.3) {
      insights.push({
        type: 'evolution',
        title: 'Evolução Inicial',
        description: 'O sistema está em estágios iniciais de evolução, requerendo mais tempo para adaptação.',
        status: 'info'
      });
    }

    // Insight sobre recursos
    if (metrics.resourceBalance < 0.5) {
      insights.push({
        type: 'resources',
        title: 'Otimização de Recursos',
        description: 'O sistema pode se beneficiar de uma melhor distribuição de recursos.',
        status: 'warning'
      });
    }

    // Insight sobre coesão
    if (symbioticMetrics.symbioticCohesion > 0.85) {
      insights.push({
        type: 'cohesion',
        title: 'Alta Coesão',
        description: 'O sistema demonstra excelente coesão entre seus componentes.',
        status: 'success'
      });
    }

    return insights;
  };

  const getPhaseDescription = (phase) => {
    switch (phase) {
      case 'initialization':
        return 'estabelecendo bases fundamentais e calibrando sistemas';
      case 'adaptation':
        return 'ajustando-se ativamente ao ambiente e padrões de uso';
      case 'evolution':
        return 'desenvolvendo novas capacidades e otimizando existentes';
      case 'autonomy':
        return 'operando com alto grau de independência e auto-otimização';
      default:
        return '';
    }
  };

  const getHealthDescription = (score) => {
    if (score >= 0.8) {
      return 'O sistema está operando em condições ótimas, com alta eficiência e estabilidade.';
    } else if (score >= 0.6) {
      return 'O sistema está funcionando adequadamente, mas há espaço para melhorias em alguns aspectos.';
    } else {
      return 'O sistema requer atenção para melhorar seu desempenho e estabilidade.';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'bg-green-50 text-green-800 border-green-200';
      case 'warning':
        return 'bg-yellow-50 text-yellow-800 border-yellow-200';
      case 'danger':
        return 'bg-red-50 text-red-800 border-red-200';
      case 'info':
      default:
        return 'bg-blue-50 text-blue-800 border-blue-200';
    }
  };

  const insights = getInsights();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {insights.map((insight, index) => (
        <div
          key={index}
          className={`rounded-lg border p-6 ${getStatusColor(insight.status)}`}
        >
          <h3 className="text-lg font-medium mb-2">
            {insight.title}
          </h3>
          <p className="text-sm">
            {insight.description}
          </p>
        </div>
      ))}
    </div>
  );
};

export default AdaptiveInsights;
