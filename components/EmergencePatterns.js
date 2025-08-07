import React from 'react';

const EmergencePatterns = ({ patterns }) => {
  // Função para determinar a cor do padrão baseado no tipo
  const getPatternColor = (type) => {
    switch (type) {
      case 'resource_optimization':
        return 'bg-blue-50 border-blue-200 text-blue-800';
      case 'state_synchronization':
        return 'bg-green-50 border-green-200 text-green-800';
      case 'event_harmonization':
        return 'bg-purple-50 border-purple-200 text-purple-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  // Função para obter ícone do padrão
  const getPatternIcon = (type) => {
    switch (type) {
      case 'resource_optimization':
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        );
      case 'state_synchronization':
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        );
      case 'event_harmonization':
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        );
      default:
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Sumário de Padrões */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-800 mb-4">
          Sumário de Padrões Emergentes
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 rounded-lg p-4">
            <span className="text-blue-800 font-medium">
              Padrões Ativos
            </span>
            <p className="text-2xl font-bold text-blue-600">
              {patterns.length}
            </p>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <span className="text-green-800 font-medium">
              Taxa de Sucesso
            </span>
            <p className="text-2xl font-bold text-green-600">
              {((patterns.filter(p => p.success).length / patterns.length) * 100).toFixed(1)}%
            </p>
          </div>
          <div className="bg-purple-50 rounded-lg p-4">
            <span className="text-purple-800 font-medium">
              Eficiência Média
            </span>
            <p className="text-2xl font-bold text-purple-600">
              {(patterns.reduce((acc, p) => acc + p.efficiency, 0) / patterns.length * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      </div>

      {/* Lista de Padrões */}
      <div className="space-y-4">
        {patterns.map((pattern, index) => (
          <div
            key={index}
            className={`border rounded-lg p-6 ${getPatternColor(pattern.type)}`}
          >
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                {getPatternIcon(pattern.type)}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-lg font-medium">
                    {pattern.name}
                  </h4>
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    pattern.success ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {pattern.success ? 'Ativo' : 'Em Adaptação'}
                  </span>
                </div>
                <p className="text-sm mb-4">
                  {pattern.description}
                </p>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-sm font-medium">Eficiência</span>
                    <div className="mt-1 flex items-center space-x-2">
                      <div className="flex-1 bg-white rounded-full h-2">
                        <div
                          className="bg-current h-2 rounded-full"
                          style={{ width: `${pattern.efficiency * 100}%` }}
                        />
                      </div>
                      <span className="text-sm">
                        {(pattern.efficiency * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                  <div>
                    <span className="text-sm font-medium">Frequência</span>
                    <div className="mt-1 flex items-center space-x-2">
                      <div className="flex-1 bg-white rounded-full h-2">
                        <div
                          className="bg-current h-2 rounded-full"
                          style={{ width: `${pattern.frequency * 100}%` }}
                        />
                      </div>
                      <span className="text-sm">
                        {(pattern.frequency * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmergencePatterns;
