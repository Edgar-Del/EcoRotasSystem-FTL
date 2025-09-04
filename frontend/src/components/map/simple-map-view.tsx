'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  MapIcon,
  ExclamationTriangleIcon,
  CurrencyDollarIcon,
  MapPinIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'

import { Route } from '@/types'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

interface SimpleMapViewProps {
  routes: Route[]
}

export function SimpleMapView({ routes }: SimpleMapViewProps) {
  const [isLoading, setIsLoading] = useState(false)

  const handleRefresh = () => {
    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
    }, 1000)
  }

  if (routes.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="card text-center py-16"
      >
        <div className="flex flex-col items-center space-y-4">
          <div className="flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full">
            <MapIcon className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900">
            Nenhuma Rota Disponível
          </h3>
          <p className="text-gray-600 max-w-md">
            Gere algumas rotas primeiro para visualizá-las no mapa interativo. 
            Use o gerador de rotas para começar sua jornada de ecoturismo.
          </p>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Header do Mapa */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            Mapa Interativo das Rotas
          </h3>
          <p className="text-gray-600">
            Visualize as {routes.length} rota{routes.length !== 1 ? 's' : ''} gerada{routes.length !== 1 ? 's' : ''} no mapa de Angola
          </p>
        </div>
        
        <button
          onClick={handleRefresh}
          disabled={isLoading}
          className="btn-secondary flex items-center space-x-2"
        >
          {isLoading ? (
            <LoadingSpinner size="sm" />
          ) : (
            <ArrowPathIcon className="w-5 h-5" />
          )}
          <span>Atualizar</span>
        </button>
      </div>

      {/* Mapa Placeholder */}
      <div className="card p-0 overflow-hidden">
        <div className="h-96 w-full bg-gradient-to-br from-green-100 to-blue-100 flex items-center justify-center">
          <div className="text-center">
            <MapIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h4 className="text-lg font-semibold text-gray-700 mb-2">
              Mapa Interativo
            </h4>
            <p className="text-gray-500">
              {routes.length} rota{routes.length !== 1 ? 's' : ''} disponível{routes.length !== 1 ? 'is' : ''}
            </p>
          </div>
        </div>
      </div>

      {/* Lista de Rotas */}
      <div className="grid gap-4">
        {routes.map((route, index) => (
          <div key={index} className="card">
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
            </div>

            {/* Métricas */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="flex items-center justify-center w-8 h-8 bg-blue-100 rounded-lg mx-auto mb-2">
                  <MapIcon className="w-4 h-4 text-blue-600" />
                </div>
                <p className="text-sm text-gray-500">Distância</p>
                <p className="font-semibold text-gray-900">
                  {route.distancia_total_km.toFixed(1)} km
                </p>
              </div>

              <div className="text-center">
                <div className="flex items-center justify-center w-8 h-8 bg-green-100 rounded-lg mx-auto mb-2">
                  <CurrencyDollarIcon className="w-4 h-4 text-green-600" />
                </div>
                <p className="text-sm text-gray-500">Custo Total</p>
                <p className="font-semibold text-gray-900">
                  {route.custo_total_aoa.toLocaleString()} AOA
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
                  <MapPinIcon className="w-4 h-4 text-purple-600" />
                </div>
                <p className="text-sm text-gray-500">Locais</p>
                <p className="font-semibold text-gray-900">
                  {route.num_locais}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}
