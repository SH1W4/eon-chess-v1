import { ArchitectureDiagram } from '../components/ArchitectureDiagram';
import Layout from '../components/Layout';

const ArchitecturePage = () => {
  return (
    <Layout>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Seção do diagrama */}
        <div className="w-full">
          <ArchitectureDiagram />
        </div>
        
        {/* Seção de detalhes */}
        <div className="w-full space-y-6">
          <h2 className="text-2xl font-bold text-gray-800">
            Detalhes da Arquitetura
          </h2>
          <div className="space-y-4">
            <div className="p-4 bg-blue-100 rounded-lg">
              <h3 className="font-bold text-blue-800">Interface Layer</h3>
              <p className="text-blue-700">
                Camada de interação com usuário, suportando múltiplas plataformas.
              </p>
            </div>
            <div className="p-4 bg-red-100 rounded-lg">
              <h3 className="font-bold text-red-800">Symbiotic Core</h3>
              <p className="text-red-700">
                Núcleo do sistema com integração ARQUIMAX e motor CHESS.
              </p>
            </div>
            <div className="p-4 bg-green-100 rounded-lg">
              <h3 className="font-bold text-green-800">Neural Network Layer</h3>
              <p className="text-green-700">
                Processamento de IA e adaptação cultural em tempo real.
              </p>
            </div>
            <div className="p-4 bg-teal-100 rounded-lg">
              <h3 className="font-bold text-teal-800">Data Layer</h3>
              <p className="text-teal-700">
                Armazenamento e cache de dados culturais e neurais.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ArchitecturePage;
