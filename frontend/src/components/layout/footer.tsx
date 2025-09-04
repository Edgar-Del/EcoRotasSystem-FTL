'use client'

import { 
  GlobeAltIcon,
  HeartIcon,
  MapIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo e Descrição */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl">
                <GlobeAltIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold">EcoRota Angola</h3>
                <p className="text-sm text-gray-400">Ecoturismo Sustentável</p>
              </div>
            </div>
            <p className="text-gray-300 mb-6 max-w-md">
              Sistema inteligente de recomendação de rotas de ecoturismo sustentável 
              que equilibra preservação ambiental, custo-benefício e experiência cultural 
              para promover o turismo responsável em Angola.
            </p>
            <div className="flex items-center space-x-2 text-sm text-gray-400">
              <HeartIcon className="w-4 h-4 text-red-500" />
              <span>Feito com amor para Angola</span>
            </div>
          </div>

          {/* Links Rápidos */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Links Rápidos</h4>
            <ul className="space-y-2">
              <li>
                <a href="#home" className="text-gray-300 hover:text-white transition-colors">
                  Início
                </a>
              </li>
              <li>
                <a href="#about" className="text-gray-300 hover:text-white transition-colors">
                  Sobre o Sistema
                </a>
              </li>
              <li>
                <a href="#features" className="text-gray-300 hover:text-white transition-colors">
                  Funcionalidades
                </a>
              </li>
              <li>
                <a href="#contact" className="text-gray-300 hover:text-white transition-colors">
                  Contato
                </a>
              </li>
            </ul>
          </div>

          {/* Funcionalidades */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Funcionalidades</h4>
            <ul className="space-y-2">
              <li className="flex items-center space-x-2 text-gray-300">
                <SparklesIcon className="w-4 h-4 text-primary-400" />
                <span>Rotas Inteligentes</span>
              </li>
              <li className="flex items-center space-x-2 text-gray-300">
                <MapIcon className="w-4 h-4 text-accent-400" />
                <span>Mapas Interativos</span>
              </li>
              <li className="flex items-center space-x-2 text-gray-300">
                <GlobeAltIcon className="w-4 h-4 text-green-400" />
                <span>Sustentabilidade</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Linha Divisória */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-400 mb-4 md:mb-0">
              © 2024 EcoRota Angola. Todos os direitos reservados.
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-400">
              <span>Desenvolvido para o Hackathon FTL 2024</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
