import React from 'react';
import { Line } from 'react-chartjs-2';

const SymbioticMetrics = ({ metrics }) => {
  const {
    symbioticCohesion,
    resourceBalance,
    emergenceStability,
    integrationHealth,
    adaptationEfficiency,
    evolutionProgress,
    history
  } = metrics;

  // Configuração do gráfico de tendências
  const trendData = {
    labels: history.map(h => h.timestamp),
    datasets: [
      {
        label: 'Coesão Simbiótica',
        data: history.map(h => h.symbioticCohesion),
        borderColor: '#3B82F6',
        fill: false
      },
      {
        label: 'Equilíbrio de Recursos',
        data: history.map(h => h.resourceBalance),
        borderColor: '#10B981',
        fill: false
      },
      {
        label: 'Estabilidade Emergente',
        data: history.map(h => h.emergenceStability),
        borderColor: '#6366F1',
        fill: false
      }
    ]
  };

  return (
    <div className="space-y-8">
      {/* Métricas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-800 mb-4">
            Saúde da Integração
          </h3>
          <div className="flex items-center justify-between">
            <span className="text-3xl font-bold text-blue-600">
              {(integrationHealth * 100).toFixed(1)}%
            </span>
            <div className={`px-3 py-1 rounded-full text-sm ${
              integrationHealth >= 0.8 ? 'bg-green-100 text-green-800' :
              integrationHealth >= 0.6 ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {integrationHealth >= 0.8 ? 'Saudável' :
               integrationHealth >= 0.6 ? 'Atenção' : 'Crítico'}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-800 mb-4">
            Eficiência de Adaptação
          </h3>
          <div className="flex items-center justify-between">
            <span className="text-3xl font-bold text-green-600">
              {(adaptationEfficiency * 100).toFixed(1)}%
            </span>
            <span className="text-sm text-gray-500">
              Taxa de Sucesso
            </span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-800 mb-4">
            Progresso Evolutivo
          </h3>
          <div className="flex items-center justify-between">
            <span className="text-3xl font-bold text-indigo-600">
              {(evolutionProgress * 100).toFixed(1)}%
            </span>
            <span className="text-sm text-gray-500">
              Avanço Total
            </span>
          </div>
        </div>
      </div>

      {/* Gráfico de Tendências */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-800 mb-4">
          Tendências Simbióticas
        </h3>
        <div className="h-80">
          <Line 
            data={trendData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                y: {
                  beginAtZero: true,
                  max: 1
                }
              }
            }}
          />
        </div>
      </div>

      {/* Detalhes das Métricas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h4 className="text-md font-medium text-gray-800 mb-2">
            Coesão Simbiótica
          </h4>
          <div className="flex items-center space-x-2">
            <div className="flex-1 bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${symbioticCohesion * 100}%` }}
              />
            </div>
            <span className="text-sm text-gray-600">
              {(symbioticCohesion * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h4 className="text-md font-medium text-gray-800 mb-2">
            Equilíbrio de Recursos
          </h4>
          <div className="flex items-center space-x-2">
            <div className="flex-1 bg-gray-200 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full"
                style={{ width: `${resourceBalance * 100}%` }}
              />
            </div>
            <span className="text-sm text-gray-600">
              {(resourceBalance * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h4 className="text-md font-medium text-gray-800 mb-2">
            Estabilidade Emergente
          </h4>
          <div className="flex items-center space-x-2">
            <div className="flex-1 bg-gray-200 rounded-full h-2">
              <div
                className="bg-indigo-600 h-2 rounded-full"
                style={{ width: `${emergenceStability * 100}%` }}
              />
            </div>
            <span className="text-sm text-gray-600">
              {(emergenceStability * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SymbioticMetrics;
