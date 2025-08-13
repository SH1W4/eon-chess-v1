import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface ARKITECTMetrics {
  overall_score: number;
  quality_gate: boolean;
  performance_score: number;
  security_score: number;
  architecture_score: number;
  last_analysis: string;
  status: 'healthy' | 'warning' | 'critical';
}

interface ARKITECTSystem {
  name: string;
  status: 'operational' | 'degraded' | 'down';
  uptime: number;
  response_time: number;
  last_check: string;
}

const ARKITECTDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<ARKITECTMetrics | null>(null);
  const [systems, setSystems] = useState<ARKITECTSystem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'analysis' | 'monitoring' | 'optimization'>('overview');

  useEffect(() => {
    // Simular carregamento de métricas do ARKITECT
    const loadARKITECTData = async () => {
      try {
        // Em produção, isso seria uma chamada real para a API do ARKITECT
        const mockMetrics: ARKITECTMetrics = {
          overall_score: 9.2,
          quality_gate: true,
          performance_score: 9.5,
          security_score: 9.8,
          architecture_score: 9.1,
          last_analysis: new Date().toISOString(),
          status: 'healthy'
        };

        const mockSystems: ARKITECTSystem[] = [
          {
            name: 'ARKITECT Core',
            status: 'operational',
            uptime: 99.98,
            response_time: 12,
            last_check: new Date().toISOString()
          },
          {
            name: 'TaskMash Super Scope',
            status: 'operational',
            uptime: 99.95,
            response_time: 45,
            last_check: new Date().toISOString()
          },
          {
            name: 'Quality Gate',
            status: 'operational',
            uptime: 99.99,
            response_time: 8,
            last_check: new Date().toISOString()
          },
          {
            name: 'Performance Monitor',
            status: 'operational',
            uptime: 99.97,
            response_time: 15,
            last_check: new Date().toISOString()
          }
        ];

        setMetrics(mockMetrics);
        setSystems(mockSystems);
      } catch (error) {
        console.error('Erro ao carregar dados do ARKITECT:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadARKITECTData();
    const interval = setInterval(loadARKITECTData, 30000); // Atualizar a cada 30s

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational':
      case 'healthy':
        return 'text-green-500';
      case 'degraded':
      case 'warning':
        return 'text-yellow-500';
      case 'down':
      case 'critical':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'operational':
      case 'healthy':
        return '🟢';
      case 'degraded':
      case 'warning':
        return '🟡';
      case 'down':
      case 'critical':
        return '🔴';
      default:
        return '⚪';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-900 to-emerald-700 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-white mb-2">
            🧠 ARKITECT Dashboard
          </h1>
          <p className="text-emerald-100 text-lg">
            Sistema de Controle de Complexidade Arquitetural
          </p>
        </motion.div>

        {/* Navigation Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-2 mb-6"
        >
          <div className="flex space-x-2">
            {[
              { id: 'overview', label: 'Visão Geral', icon: '📊' },
              { id: 'analysis', label: 'Análise', icon: '🔍' },
              { id: 'monitoring', label: 'Monitoramento', icon: '📈' },
              { id: 'optimization', label: 'Otimização', icon: '⚡' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-emerald-600 text-white shadow-lg'
                    : 'text-emerald-100 hover:bg-emerald-700/50'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Content */}
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="grid lg:grid-cols-2 gap-6"
            >
              {/* Overall Metrics */}
              <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                  <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">
                    📊
                  </span>
                  Métricas Gerais
                </h2>
                {metrics && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-emerald-100">Score Geral</span>
                      <span className={`text-2xl font-bold ${getStatusColor(metrics.status)}`}>
                        {metrics.overall_score}/10
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-emerald-100">Quality Gate</span>
                      <span className={getStatusColor(metrics.quality_gate ? 'healthy' : 'critical')}>
                        {metrics.quality_gate ? '✅ PASSED' : '❌ FAILED'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-emerald-100">Performance</span>
                      <span className="text-emerald-300">{metrics.performance_score}/10</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-emerald-100">Segurança</span>
                      <span className="text-emerald-300">{metrics.security_score}/10</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-emerald-100">Arquitetura</span>
                      <span className="text-emerald-300">{metrics.architecture_score}/10</span>
                    </div>
                  </div>
                )}
              </div>

              {/* System Status */}
              <div className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                  <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">
                    🖥️
                  </span>
                  Status dos Sistemas
                </h2>
                <div className="space-y-3">
                  {systems.map((system) => (
                    <div key={system.name} className="flex items-center justify-between p-3 bg-emerald-700/20 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <span className="text-lg">{getStatusIcon(system.status)}</span>
                        <span className="text-emerald-100 font-medium">{system.name}</span>
                      </div>
                      <div className="text-right">
                        <div className={`text-sm ${getStatusColor(system.status)}`}>
                          {system.status === 'operational' ? 'Operacional' : 
                           system.status === 'degraded' ? 'Degradado' : 'Indisponível'}
                        </div>
                        <div className="text-xs text-emerald-300">
                          Uptime: {system.uptime}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'analysis' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6"
            >
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">
                  🔍
                </span>
                Análise ARKITECT
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-emerald-200">Análise de Arquitetura</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-emerald-100">Modularidade</span>
                      <span className="text-emerald-300">9.2/10</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-100">Coesão</span>
                      <span className="text-emerald-300">8.8/10</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-100">Complexidade</span>
                      <span className="text-emerald-300">7.5/10</span>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-emerald-200">Qualidade do Código</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-emerald-100">Cobertura de Testes</span>
                      <span className="text-emerald-300">92%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-100">Duplicação</span>
                      <span className="text-emerald-300">1.2%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-emerald-100">Complexidade Ciclomática</span>
                      <span className="text-emerald-300">3.1</span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'monitoring' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6"
            >
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">
                  📈
                </span>
                Monitoramento em Tempo Real
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center p-4 bg-emerald-700/20 rounded-lg">
                  <div className="text-3xl font-bold text-emerald-300 mb-2">99.98%</div>
                  <div className="text-emerald-100">Uptime</div>
                </div>
                <div className="text-center p-4 bg-emerald-700/20 rounded-lg">
                  <div className="text-3xl font-bold text-emerald-300 mb-2">12ms</div>
                  <div className="text-emerald-100">Response Time</div>
                </div>
                <div className="text-center p-4 bg-emerald-700/20 rounded-lg">
                  <div className="text-3xl font-bold text-emerald-300 mb-2">1.2M</div>
                  <div className="text-emerald-100">Requests/min</div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'optimization' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-emerald-800/30 backdrop-blur-sm rounded-xl border border-emerald-600/50 p-6"
            >
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="w-8 h-8 flex items-center justify-center rounded-lg bg-emerald-500/20">
                  ⚡
                </span>
                Otimizações Automáticas
              </h2>
              <div className="space-y-4">
                <div className="p-4 bg-emerald-700/20 rounded-lg">
                  <h3 className="text-lg font-semibold text-emerald-200 mb-2">Bundle Optimization</h3>
                  <div className="flex justify-between items-center">
                    <span className="text-emerald-100">Status</span>
                    <span className="text-green-400">✅ Ativo</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-emerald-100">Redução</span>
                    <span className="text-emerald-300">27%</span>
                  </div>
                </div>
                <div className="p-4 bg-emerald-700/20 rounded-lg">
                  <h3 className="text-lg font-semibold text-emerald-200 mb-2">Code Splitting</h3>
                  <div className="flex justify-between items-center">
                    <span className="text-emerald-100">Status</span>
                    <span className="text-green-400">✅ Ativo</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-emerald-100">Chunks</span>
                    <span className="text-emerald-300">6-8 (otimizado)</span>
                  </div>
                </div>
                <div className="p-4 bg-emerald-700/20 rounded-lg">
                  <h3 className="text-lg font-semibold text-emerald-200 mb-2">Tree Shaking</h3>
                  <div className="flex justify-between items-center">
                    <span className="text-emerald-100">Status</span>
                    <span className="text-green-400">✅ Ativo</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-emerald-100">Código Morto</span>
                    <span className="text-emerald-300">Removido</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mt-8 text-emerald-300 text-sm"
        >
          <p>ARKITECT Dashboard - Sistema de Controle de Complexidade</p>
          <p>Última atualização: {new Date().toLocaleString('pt-BR')}</p>
        </motion.div>
      </div>
    </div>
  );
};

export default ARKITECTDashboard;
