'use client'

import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet'
import { Icon } from 'leaflet'
import { motion } from 'framer-motion'
import { 
  MapIcon,
  ExclamationTriangleIcon,
  CurrencyDollarIcon,
  MapPinIcon,
  RefreshIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

import { Route, Location } from '@/types'
import { formatCurrency, getFragilityColor, getFragilityLabel, getEcosystemIcon } from '@/lib/api'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

// Importar CSS do Leaflet
import 'leaflet/dist/leaflet.css'

// Configurar ícones padrão do Leaflet
delete (Icon.Default.prototype as any)._getIconUrl
Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

interface MapViewProps {
  routes: Route[]
}

// Componente para ajustar a visualização do mapa
function MapController({ routes }: { routes: Route[] }) {
  const map = useMap()
  
  useEffect(() => {
    if (routes.length > 0) {
      // Calcular bounds para incluir todos os locais
      const allLocations = routes.flatMap(route => route.locais)
      if (allLocations.length > 0) {
        const bounds = allLocations.map(location => [location.latitude, location.longitude] as [number, number])
        map.fitBounds(bounds, { padding: [20, 20] })
      }
    } else {
      // Centralizar em Angola se não há rotas
      map.setView([-8.8390, 13.2894], 6)
    }
  }, [map, routes])

  return null
}

export function MapView({ routes }: MapViewProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [selectedRoute, setSelectedRoute] = useState<number | null>(null)

  // Cores para as rotas
  const routeColors = [
    '#3B82F6', // Azul
    '#EF4444', // Vermelho
    '#10B981', // Verde
    '#F59E0B', // Amarelo
    '#8B5CF6', // Roxo
    '#EC4899', // Rosa
    '#06B6D4', // Ciano
    '#84CC16', // Lima
  ]

  const handleRefresh = () => {
    setIsLoading(true)
    // Simular refresh
    setTimeout(() => {
      setIsLoading(false)
      toast.success('Mapa atualizado!')
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
            <RefreshIcon className="w-5 h-5" />
          )}
          <span>Atualizar</span>
        </button>
      </div>

      {/* Controles de Rota */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setSelectedRoute(null)}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            selectedRoute === null
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Todas as Rotas
        </button>
        {routes.map((route, index) => (
          <button
            key={index}
            onClick={() => setSelectedRoute(index)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedRoute === index
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Rota {index + 1}
          </button>
        ))}
      </div>

      {/* Mapa */}
      <div className="card p-0 overflow-hidden">
        <div className="h-96 w-full">
          <MapContainer
            center={[-8.8390, 13.2894]} // Centro de Angola
            zoom={6}
            style={{ height: '100%', width: '100%' }}
            className="rounded-lg"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            <MapController routes={routes} />
            
            {/* Renderizar rotas */}
            {(selectedRoute === null ? routes : [routes[selectedRoute]]).map((route, routeIndex) => {
              const actualIndex = selectedRoute === null ? routeIndex : selectedRoute
              const color = routeColors[actualIndex % routeColors.length]
              
              return (
                <div key={actualIndex}>
                  {/* Linha da rota */}
                  <Polyline
                    positions={route.locais.map(location => [location.latitude, location.longitude])}
                    color={color}
                    weight={4}
                    opacity={0.8}
                  />
                  
                  {/* Marcadores dos locais */}
                  {route.locais.map((location, locationIndex) => (
                    <Marker
                      key={`${actualIndex}-${locationIndex}`}
                      position={[location.latitude, location.longitude]}
                      icon={new Icon({
                        iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color.replace('#', '')}.png`,
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                      })}
                    >
                      <Popup maxWidth={300} className="custom-popup">
                        <div className="p-2">
                          <h4 className="font-semibold text-gray-900 mb-2">
                            {location.nome}
                          </h4>
                          
                          <div className="space-y-2 text-sm">
                            <div className="flex items-center space-x-2">
                              <MapPinIcon className="w-4 h-4 text-gray-500" />
                              <span className="text-gray-600">{location.provincia}</span>
                            </div>
                            
                            <div className="flex items-center space-x-2">
                              <CurrencyDollarIcon className="w-4 h-4 text-gray-500" />
                              <span className="text-gray-600">
                                {formatCurrency(location.taxa_aoa)}
                              </span>
                            </div>
                            
                            <div className="flex items-center space-x-2">
                              <ExclamationTriangleIcon className="w-4 h-4 text-gray-500" />
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getFragilityColor(location.fragilidade)}`}>
                                {getFragilityLabel(location.fragilidade)}
                              </span>
                            </div>
                            
                            <div className="flex items-center space-x-2">
                              <span className="text-gray-500">🌍</span>
                              <span className="text-gray-600">{location.tipo_ecosistema}</span>
                            </div>
                            
                            {location.descricao && (
                              <p className="text-gray-600 text-xs mt-2">
                                {location.descricao}
                              </p>
                            )}
                          </div>
                        </div>
                      </Popup>
                    </Marker>
                  ))}
                </div>
              )
            })}
          </MapContainer>
        </div>
      </div>

      {/* Legenda */}
      <div className="card">
        <h4 className="font-semibold text-gray-900 mb-4">Legenda</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h5 className="font-medium text-gray-700 mb-2">Níveis de Fragilidade</h5>
            <div className="space-y-1">
              {[1, 2, 3, 4, 5].map(level => (
                <div key={level} className="flex items-center space-x-2">
                  <span className={`w-3 h-3 rounded-full ${
                    level <= 2 ? 'bg-green-500' : 
                    level === 3 ? 'bg-yellow-500' : 'bg-red-500'
                  }`} />
                  <span className="text-sm text-gray-600">
                    {level} - {getFragilityLabel(level)}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h5 className="font-medium text-gray-700 mb-2">Informações da Rota</h5>
            <div className="space-y-1 text-sm text-gray-600">
              <p>• <strong>Linhas coloridas:</strong> Trajeto da rota</p>
              <p>• <strong>Marcadores:</strong> Locais de ecoturismo</p>
              <p>• <strong>Clique no marcador:</strong> Ver detalhes</p>
              <p>• <strong>Zoom:</strong> Explorar região</p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
