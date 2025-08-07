import Layout from '../components/Layout';
import Link from 'next/link';

const IndexPage = () => {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        {/* Banner Principal */}
        <div className="text-center mb-12 p-8 bg-gray-900 rounded-lg shadow-xl border-2 border-blue-500">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
            ♞ AEON CHESS
          </h1>
          <p className="text-xl text-gray-300">
            Sistema de Xadrez com Inteligência Cultural
          </p>
        </div>

        {/* Seções de Destaque */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 hover:border-blue-500 transition-colors">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Arquitetura Simbiótica</h2>
            <p className="text-gray-600 mb-4">
              Explore nossa arquitetura única que combina IA avançada com adaptação cultural em tempo real.
            </p>
            <Link 
              href="/architecture" 
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              Ver Arquitetura →
            </Link>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 hover:border-blue-500 transition-colors">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Sistema Cultural</h2>
            <p className="text-gray-600 mb-4">
              Conheça como nossa IA aprende e se adapta aos diferentes estilos de jogo.
            </p>
            <Link 
              href="/culture" 
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              Explorar Sistema →
            </Link>
          </div>
        </div>

        {/* Métricas */}
        <div className="bg-gray-100 p-8 rounded-lg shadow-inner">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Métricas do Sistema</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">1.2M+</div>
              <div className="text-sm text-gray-600">Partidas Jogadas</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">850+</div>
              <div className="text-sm text-gray-600">Perfis Culturais</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">98%</div>
              <div className="text-sm text-gray-600">Precisão</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">24/7</div>
              <div className="text-sm text-gray-600">Disponibilidade</div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default IndexPage;
