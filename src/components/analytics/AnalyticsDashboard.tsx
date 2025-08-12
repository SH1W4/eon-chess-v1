
import React, { useState, useEffect } from 'react';
import { performanceMonitor } from '../../monitoring/performance-monitor';

interface AnalyticsData {
  pageViews: number;
  uniqueUsers: number;
  averageSessionTime: number;
  bounceRate: number;
  topPages: Array<{ path: string; views: number }>;
}

export const AnalyticsDashboard: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadAnalyticsData();
  }, []);
  
  const loadAnalyticsData = async () => {
    try {
      // Simular carregamento de dados
      const mockData: AnalyticsData = {
        pageViews: 15420,
        uniqueUsers: 3247,
        averageSessionTime: 8.5,
        bounceRate: 23.4,
        topPages: [
          { path: '/', views: 5234 },
          { path: '/game', views: 3120 },
          { path: '/analysis', views: 1890 },
          { path: '/learn', views: 1456 }
        ]
      };
      
      setData(mockData);
    } catch (error) {
      console.error('Erro ao carregar analytics:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }
  
  if (!data) {
    return (
      <div className="p-8 text-center text-gray-500">
        Nenhum dado disponível
      </div>
    );
  }
  
  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Dashboard de Analytics</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-blue-600">Visualizações</h3>
          <p className="text-2xl font-bold text-blue-800">{data.pageViews.toLocaleString()}</p>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-green-600">Usuários Únicos</h3>
          <p className="text-2xl font-bold text-green-800">{data.uniqueUsers.toLocaleString()}</p>
        </div>
        
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-yellow-600">Tempo Médio</h3>
          <p className="text-2xl font-bold text-yellow-800">{data.averageSessionTime}min</p>
        </div>
        
        <div className="bg-red-50 p-4 rounded-lg">
          <h3 className="text-sm font-medium text-red-600">Taxa de Rejeição</h3>
          <p className="text-2xl font-bold text-red-800">{data.bounceRate}%</p>
        </div>
      </div>
      
      <div className="bg-gray-50 p-4 rounded-lg">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Páginas Mais Visitadas</h3>
        <div className="space-y-2">
          {data.topPages.map((page, index) => (
            <div key={page.path} className="flex justify-between items-center">
              <span className="text-gray-600">{page.path}</span>
              <span className="font-medium text-gray-800">{page.views.toLocaleString()} views</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
