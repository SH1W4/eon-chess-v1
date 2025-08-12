import Layout from '../components/Layout';

const SymbioticPage = () => {
  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Cabeçalho */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Ecossistema Simbiótico
          </h1>
          <p className="text-xl text-gray-600">
            Uma arquitetura adaptativa que evolui com seu projeto
          </p>
        </div>

        {/* Fases */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Fases do Sistema</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-emerald-600 mb-4">Nucleação</h3>
              <p className="text-gray-600">
                Fase inicial onde o núcleo simbiótico é estabelecido e a análise de compatibilidade é realizada.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-blue-600 mb-4">Simbiogênese</h3>
              <p className="text-gray-600">
                Estabelecimento das pontes de integração e início da cooperação entre sistemas.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-purple-600 mb-4">Emergência</h3>
              <p className="text-gray-600">
                Desenvolvimento de comportamentos emergentes e evolução do sistema.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-red-600 mb-4">Homeostase</h3>
              <p className="text-gray-600">
                Manutenção do equilíbrio e monitoramento contínuo do sistema.
              </p>
            </div>
          </div>
        </section>

        {/* Capacidades */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Capacidades do Sistema</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Sistema Hospedeiro</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-center">
                  <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                  Gerenciamento de Recursos
                </li>
                <li className="flex items-center">
                  <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                  Monitoramento de Estado
                </li>
                <li className="flex items-center">
                  <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                  Propagação de Eventos
                </li>
              </ul>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Sistema Convidado</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-center">
                  <span className="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
                  Consumo de Recursos
                </li>
                <li className="flex items-center">
                  <span className="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
                  Reflexão de Estado
                </li>
                <li className="flex items-center">
                  <span className="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
                  Manipulação de Eventos
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Métricas */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Métricas Vitais</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Coesão Simbiótica</h3>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Limite: 0.7</span>
                <div className="w-24 h-24 relative">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-2xl font-bold text-emerald-600">0.85</span>
                  </div>
                  <div className="w-full h-full border-4 border-emerald-200 rounded-full">
                    <div 
                      className="h-full w-full border-4 border-emerald-600 rounded-full"
                      style={{ clipPath: 'inset(15% 15% 15% 15% round 100%)' }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Equilíbrio de Recursos</h3>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Limite: 0.6</span>
                <div className="w-24 h-24 relative">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-2xl font-bold text-blue-600">0.75</span>
                  </div>
                  <div className="w-full h-full border-4 border-blue-200 rounded-full">
                    <div 
                      className="h-full w-full border-4 border-blue-600 rounded-full"
                      style={{ clipPath: 'inset(25% 25% 25% 25% round 100%)' }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Estabilidade Emergente</h3>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Limite: 0.8</span>
                <div className="w-24 h-24 relative">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-2xl font-bold text-purple-600">0.92</span>
                  </div>
                  <div className="w-full h-full border-4 border-purple-200 rounded-full">
                    <div 
                      className="h-full w-full border-4 border-purple-600 rounded-full"
                      style={{ clipPath: 'inset(8% 8% 8% 8% round 100%)' }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Integrações */}
        <section>
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Tipos de Integração</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Monolítico</h3>
              <h4 className="font-semibold text-gray-700 mb-2">Capacidades Requeridas:</h4>
              <ul className="list-disc list-inside text-gray-600 mb-4">
                <li>Gerenciamento de Recursos</li>
                <li>Monitoramento de Estado</li>
              </ul>
              <h4 className="font-semibold text-gray-700 mb-2">Capacidades Opcionais:</h4>
              <ul className="list-disc list-inside text-gray-600">
                <li>Propagação de Eventos</li>
              </ul>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Microsserviços</h3>
              <h4 className="font-semibold text-gray-700 mb-2">Capacidades Requeridas:</h4>
              <ul className="list-disc list-inside text-gray-600 mb-4">
                <li>Propagação de Eventos</li>
                <li>Reflexão de Estado</li>
              </ul>
              <h4 className="font-semibold text-gray-700 mb-2">Capacidades Opcionais:</h4>
              <ul className="list-disc list-inside text-gray-600">
                <li>Gerenciamento de Recursos</li>
              </ul>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Serverless</h3>
              <h4 className="font-semibold text-gray-700 mb-2">Capacidades Requeridas:</h4>
              <ul className="list-disc list-inside text-gray-600 mb-4">
                <li>Manipulação de Eventos</li>
                <li>Consumo de Recursos</li>
              </ul>
              <h4 className="font-semibold text-gray-700 mb-2">Capacidades Opcionais:</h4>
              <ul className="list-disc list-inside text-gray-600">
                <li>Reflexão de Estado</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default SymbioticPage;
