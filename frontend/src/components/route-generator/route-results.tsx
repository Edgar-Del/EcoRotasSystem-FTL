'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  MapIcon,
  CurrencyDollarIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  StarIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  MapPinIcon
} from '@heroicons/react/24/outline'

import { Route, RouteGeneratorMode } from '@/types'
import { formatCurrency, formatDistance, getFragilityColor, getFragilityLabel, getEcosystemIcon } from '@/lib/api'

interface RouteResultsProps {
  routes: Route[]
  mode: RouteGeneratorMode
}

export function RouteResults({ routes, mode }: RouteResultsProps) {
  const [expandedRoute, setExpandedRoute] = useState<number | null>(null)

  const toggleExpanded = (index: number) => {
    setExpandedRoute(expandedRoute === index ? null : index)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          {mode === 'traditional' ? 'Rotas Tradicionais Geradas' : 'Rotas Personalizadas com IA'}
        </h3>
        <p className="text-gray-600">
          {routes.length} rota{routes.length !== 1 ? 's' : ''} encontrada{routes.length !== 1 ? 's' : ''} com base nos seus critérios
        </p>
      </div>

      <div className="grid gap-6">
        {routes.map((route, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="card hover:shadow-lg transition-shadow duration-200"
          >
            {/* Header da Rota */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="flex items-center justify-center w-10 h-10 bg-primary-100 rounded-lg">
                  <span className="text-primary-600 font-bold text-lg">
                    {index + 1}
                  </span>
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-gray-900">
                    {route.nome}
                  </h4>
                  <p className="text-sm text-gray-500">
                    {route.num_locais} locais • {route.provincias.length} província{route.provincias.length !== 1 ? 's' : ''}
                  </p>
                </div>
              </div>
              
              <button
                onClick={() => toggleExpanded(index)}
                className="flex items-center space-x-2 text-gray-500 hover:text-gray-700 transition-colors"
              >
                <span className="text-sm font-medium">
                  {expandedRoute === index ? 'Menos detalhes' : 'Mais detalhes'}
                </span>
                {expandedRoute === index ? (
                  <ChevronUpIcon className="w-5 h-5" />
                ) : (
                  <ChevronDownIcon className="w-5 h-5" />
                )}
              </button>
            </div>

            {/* Métricas Principais */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div className="text-center">
                <div className="flex items-center justify-center w-8 h-8 bg-blue-100 rounded-lg mx-auto mb-2">
                  <MapIcon className="w-4 h-4 text-blue-600" />
                </div>
                <p className="text-sm text-gray-500">Distância</p>
                <p className="font-semibold text-gray-900">
                  {formatDistance(route.distancia_total_km)}
                </p>
              </div>

              <div className="text-center">
                <div className="flex items-center justify-center w-8 h-8 bg-green-100 rounded-lg mx-auto mb-2">
                  <CurrencyDollarIcon className="w-4 h-4 text-green-600" />
                </div>
                <p className="text-sm text-gray-500">Custo Total</p>
                <p className="font-semibold text-gray-900">
                  {formatCurrency(route.custo_total_aoa)}
                </p>
              </div>

              <div className="text-center">
                <div className="flex items-center justify-center w-8 h-8 bg-yellow-100 rounded-lg mx-auto mb-2">
                  <ExclamationTriangleIcon className="w-4 h-4 text-yellow-600" />
                </div>
                <p className="text-sm text-gray-500">Fragilidade</p>
                <p className="font-semibold text-gray-900">
                  {route.fragilidade_media.toFixed(1)}/5
                </p>
              </div>

              <div className="text-center">
                <div className="flex items-center justify-center w-8 h-8 bg-purple-100 rounded-lg mx-auto mb-2">
                  <StarIcon className="w-4 h-4 text-purple-600" />
                </div>
                <p className="text-sm text-gray-500">
                  {mode === 'traditional' ? 'Score' : 'Rating IA'}
                </p>
                <p className="font-semibold text-gray-900">
                  {mode === 'traditional' 
                    ? route.score?.toFixed(2) || 'N/A'
                    : route.rating_medio_previsto?.toFixed(2) || 'N/A'
                  }
                </p>
              </div>
            </div>

            {/* Detalhes Expandidos */}
            <AnimatePresence>
              {expandedRoute === index && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  className="border-t border-gray-200 pt-4"
                >
                  {/* Informações Gerais */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                      <h5 className="font-medium text-gray-900 mb-2">Províncias</h5>
                      <div className="flex flex-wrap gap-2">
                        {route.provincias.map((provincia, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                          >
                            {provincia}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h5 className="font-medium text-gray-900 mb-2">Ecossistemas</h5>
                      <div className="flex flex-wrap gap-2">
                        {route.tipos_ecosistema.map((ecosistema, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded-full flex items-center space-x-1"
                          >
                            <span>{getEcosystemIcon(ecosistema)}</span>
                            <span>{ecosistema}</span>
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Lista de Locais */}
                  <div>
                    <h5 className="font-medium text-gray-900 mb-3 flex items-center">
                      <MapPinIcon className="w-4 h-4 mr-2" />
                      Locais da Rota
                    </h5>
                    <div className="space-y-3">
                      {route.locais.map((local, idx) => (
                        <div
                          key={idx}
                          className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                        >
                          <div className="flex items-center space-x-3">
                            <div className="flex items-center justify-center w-6 h-6 bg-primary-100 rounded-full">
                              <span className="text-primary-600 font-medium text-sm">
                                {idx + 1}
                              </span>
                            </div>
                            <div>
                              <p className="font-medium text-gray-900">{local.nome}</p>
                              <p className="text-sm text-gray-500">{local.provincia}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-4 text-sm">
                            <div className="text-right">
                              <p className="text-gray-500">Custo</p>
                              <p className="font-medium text-gray-900">
                                {formatCurrency(local.taxa_aoa)}
                              </p>
                            </div>
                            <div className="text-right">
                              <p className="text-gray-500">Fragilidade</p>
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getFragilityColor(local.fragilidade)}`}>
                                {getFragilityLabel(local.fragilidade)}
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
      </div>

      {/* Ações */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button className="btn-primary flex items-center justify-center space-x-2">
          <MapIcon className="w-5 h-5" />
          <span>Ver no Mapa</span>
        </button>
        
        <button className="btn-secondary flex items-center justify-center space-x-2">
          <CurrencyDollarIcon className="w-5 h-5" />
          <span>Exportar Relatório</span>
        </button>
      </div>
    </motion.div>
  )
}
