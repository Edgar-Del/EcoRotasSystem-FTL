'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon,
  MapIcon,
  GlobeAltIcon,
  CpuChipIcon,
  ExclamationTriangleIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import toast from 'react-hot-toast'

import { SystemStats } from '@/types'
import { apiEndpoints } from '@/lib/api'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

export function StatsSection() {
  const [stats, setStats] = useState<SystemStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiEndpoints.stats()
        setStats(response.data.stats)
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
        toast.error('Erro ao carregar estatísticas do sistema')
      } finally {
        setIsLoading(false)
      }
    }

    fetchStats()
  }, [])

  // Dados mockados para demonstração (quando a API não estiver disponível)
  const mockData = {
    data_loaded: true,
    ml_enabled: true,
    routes_generated: 0,
    map_created: false,
    total_locations: 25,
    provinces: 8,
    ecosystems: 7,
    ml_model_trained: true,
    ml_features: 12
  }

  const currentStats = stats || mockData

  // Dados para gráficos
  const fragilityData = [
    { name: 'Muito Baixa', value: 5, color: '#10B981' },
    { name: 'Baixa', value: 8, color: '#34D399' },
    { name: 'Média', value: 7, color: '#FBBF24' },
    { name: 'Alta', value: 4, color: '#F59E0B' },
    { name: 'Muito Alta', value: 1, color: '#EF4444' }
  ]

  const ecosystemData = [
    { name: 'Floresta', value: 8, color: '#059669' },
    { name: 'Savana', value: 6, color: '#D97706' },
    { name: 'Costa', value: 4, color: '#0284C7' },
    { name: 'Montanha', value: 3, color: '#7C3AED' },
    { name: 'Rio', value: 2, color: '#0891B2' },
    { name: 'Deserto', value: 1, color: '#DC2626' },
    { name: 'Lago', value: 1, color: '#0EA5E9' }
  ]

  const provinceData = [
    { name: 'Luanda', locations: 5 },
    { name: 'Benguela', locations: 4 },
    { name: 'Huíla', locations: 3 },
    { name: 'Cabinda', locations: 3 },
    { name: 'Malanje', locations: 2 },
    { name: 'Uíge', locations: 2 },
    { name: 'Kwanza Sul', locations: 3 },
    { name: 'Namibe', locations: 3 }
  ]

  if (isLoading) {
    return (
      <div className="card text-center py-16">
        <LoadingSpinner size="lg" />
        <p className="text-gray-600 mt-4">Carregando estatísticas...</p>
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-8"
    >
      {/* Header */}
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Estatísticas do Sistema
        </h3>
        <p className="text-gray-600">
          Dados e métricas sobre o sistema EcoRota Angola
        </p>
      </div>

      {/* Cards de Estatísticas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card text-center"
        >
          <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mx-auto mb-4">
            <MapIcon className="w-6 h-6 text-blue-600" />
          </div>
          <h4 className="text-2xl font-bold text-gray-900 mb-1">
            {currentStats.total_locations || 0}
          </h4>
          <p className="text-gray-600">Locais de Ecoturismo</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card text-center"
        >
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mx-auto mb-4">
            <GlobeAltIcon className="w-6 h-6 text-green-600" />
          </div>
          <h4 className="text-2xl font-bold text-gray-900 mb-1">
            {currentStats.provinces || 0}
          </h4>
          <p className="text-gray-600">Províncias</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card text-center"
        >
          <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mx-auto mb-4">
            <ChartBarIcon className="w-6 h-6 text-purple-600" />
          </div>
          <h4 className="text-2xl font-bold text-gray-900 mb-1">
            {currentStats.ecosystems || 0}
          </h4>
          <p className="text-gray-600">Tipos de Ecossistema</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card text-center"
        >
          <div className="flex items-center justify-center w-12 h-12 bg-yellow-100 rounded-lg mx-auto mb-4">
            <CpuChipIcon className="w-6 h-6 text-yellow-600" />
          </div>
          <h4 className="text-2xl font-bold text-gray-900 mb-1">
            {currentStats.ml_features || 0}
          </h4>
          <p className="text-gray-600">Features de ML</p>
        </motion.div>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Gráfico de Fragilidade */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="card"
        >
          <h4 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
            <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600 mr-2" />
            Distribuição por Fragilidade
          </h4>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={fragilityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {fragilityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Gráfico de Ecossistemas */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="card"
        >
          <h4 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
            <GlobeAltIcon className="w-5 h-5 text-green-600 mr-2" />
            Tipos de Ecossistema
          </h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ecosystemData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Gráfico de Províncias */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="card"
      >
        <h4 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
          <MapIcon className="w-5 h-5 text-blue-600 mr-2" />
          Locais por Província
        </h4>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={provinceData} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="name" type="category" width={100} />
            <Tooltip />
            <Bar dataKey="locations" fill="#3B82F6" />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Status do Sistema */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="card"
      >
        <h4 className="text-lg font-semibold text-gray-900 mb-6">
          Status do Sistema
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Dados Carregados</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                currentStats.data_loaded 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {currentStats.data_loaded ? 'Ativo' : 'Inativo'}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Sistema ML</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                currentStats.ml_enabled 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {currentStats.ml_enabled ? 'Habilitado' : 'Desabilitado'}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Modelo Treinado</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                currentStats.ml_model_trained 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {currentStats.ml_model_trained ? 'Sim' : 'Não'}
              </span>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Rotas Geradas</span>
              <span className="text-gray-900 font-medium">
                {currentStats.routes_generated}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Mapa Criado</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                currentStats.map_created 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {currentStats.map_created ? 'Sim' : 'Não'}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Features ML</span>
              <span className="text-gray-900 font-medium">
                {currentStats.ml_features || 0}
              </span>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}
