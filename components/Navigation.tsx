import Link from 'next/link';
import { useRouter } from 'next/router';

const Navigation = () => {
  const router = useRouter();
  
  const navItems = [
    { href: '/', label: 'Início' },
    { href: '/play', label: 'Jogar' },
    { href: '/architecture', label: 'Arquitetura' },
    { href: '/symbiotic', label: 'Ecossistema' },
    { href: '/culture', label: 'Sistema Cultural' },
    { href: '/metrics', label: 'Métricas' },
  ];

  return (
    <nav className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo e título */}
          <div className="flex items-center space-x-4">
            <Link href="/" className="text-xl font-bold tracking-wider">
              ♞ AEON CHESS
            </Link>
          </div>

          {/* Links de navegação */}
          <div className="hidden md:flex space-x-6">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  px-3 py-2 rounded-md text-sm font-medium
                  transition-colors duration-200
                  ${router.pathname === item.href
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }
                `}
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* Botão de menu mobile */}
          <div className="md:hidden">
            <button className="text-gray-300 hover:text-white">
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>

          {/* Seção direita - botão de ação */}
          <div className="hidden md:flex items-center space-x-4">
            <Link 
              href="/play"
              className="
                px-4 py-2 rounded-md text-sm font-medium
                bg-blue-600 hover:bg-blue-700
                transition-colors duration-200
              "
            >
              Iniciar Jogo
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
