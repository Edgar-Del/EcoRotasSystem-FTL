'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { 
  SparklesIcon,
  CpuChipIcon,
  MapIcon,
  CurrencyDollarIcon,
  MapPinIcon,
  ExclamationTriangleIcon,
  UserIcon
} from '@heroicons/react/24/outline'

import { RouteRequest, MLRouteRequest, Route } from '@/types'
import { apiEndpoints, validateRouteRequest, validateMLRouteRequest } from '@/lib/api'
import { RouteResults } from './route-results'
import { LoadingSpinner } from '@/components/ui/loading-spinner'

// Schema de validação para rota tradicional
const traditionalRouteSchema = z.object({
  maxBudget: z.number().min(1000, 'Orçamento mínimo: 1.000 AOA').max(100000, 'Orçamento máximo: 100.000 AOA'),
  maxLocations: z.number().min(2, 'Mínimo 2 locais').max(10, 'Máximo 10 locais'),
  maxFragility: z.number().min(1, 'Fragilidade mínima: 1').max(5, 'Fragilidade máxima: 5'),
  numRoutes: z.number().min(1, 'Mínimo 1 rota').max(10, 'Máximo 10 rotas'),
})

// Schema de validação para rota ML
const mlRouteSchema = z.object({
  userAge: z.number().min(18, 'Idade mínima: 18 anos').max(100, 'Idade máxima: 100 anos'),
  maxBudget: z.number().min(1000, 'Orçamento mínimo: 1.000 AOA').max(100000, 'Orçamento máximo: 100.000 AOA'),
  sustainabilityPreference: z.number().min(0, 'Preferência mínima: 0').max(1, 'Preferência máxima: 1'),
  adventurePreference: z.number().min(0, 'Preferência mínima: 0').max(1, 'Preferência máxima: 1'),
  culturePreference: z.number().min(0, 'Preferência mínima: 0').max(1, 'Preferência máxima: 1'),
  maxLocations: z.number().min(2, 'Mínimo 2 locais').max(10, 'Máximo 10 locais'),
  numRoutes: z.number().min(1, 'Mínimo 1 rota').max(10, 'Máximo 10 rotas'),
})

type TraditionalFormData = z.infer<typeof traditionalRouteSchema>
type MLFormData = z.infer<typeof mlRouteSchema>

interface RouteGeneratorProps {
  onRoutesGenerated: (routes: Route[]) => void
}

export function RouteGenerator({ onRoutesGenerated }: RouteGeneratorProps) {
  const [mode, setMode] = useState<'traditional' | 'ml'>('traditional')
  const [isLoading, setIsLoading] = useState(false)
  const [generatedRoutes, setGeneratedRoutes] = useState<Route[]>([])

  // Formulário para rota tradicional
  const traditionalForm = useForm<TraditionalFormData>({
    resolver: zodResolver(traditionalRouteSchema),
    defaultValues: {
      maxBudget: 20000,
      maxLocations: 5,
      maxFragility: 4,
      numRoutes: 3,
    }
  })

  // Formulário para rota ML
  const mlForm = useForm<MLFormData>({
    resolver: zodResolver(mlRouteSchema),
    defaultValues: {
      userAge: 30,
      maxBudget: 20000,
      sustainabilityPreference: 0.8,
      adventurePreference: 0.6,
      culturePreference: 0.7,
      maxLocations: 5,
      numRoutes: 3,
    }
  })

  const handleTraditionalSubmit = async (data: TraditionalFormData) => {
    setIsLoading(true)
    try {
      const request: RouteRequest = {
        max_budget: data.maxBudget,
        max_locations: data.maxLocations,
        max_fragility: data.maxFragility,
        num_routes: data.numRoutes,
      }

      const response = await apiEndpoints.generateTraditionalRoutes(request)
      
      if (response.data.success) {
        setGeneratedRoutes(response.data.routes)
        onRoutesGenerated(response.data.routes)
        toast.success(`Geradas ${response.data.routes.length} rotas tradicionais!`)
      } else {
        toast.error(response.data.message)
      }
    } catch (error) {
      console.error('Erro ao gerar rotas tradicionais:', error)
      toast.error('Erro ao gerar rotas. Tente novamente.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleMLSubmit = async (data: MLFormData) => {
    setIsLoading(true)
    try {
      const request: MLRouteRequest = {
        user_profile: {
          idade: data.userAge,
          orcamento_max: data.maxBudget,
          preferencia_sustentabilidade: data.sustainabilityPreference,
          preferencia_aventura: data.adventurePreference,
          preferencia_cultura: data.culturePreference,
        },
        max_locations: data.maxLocations,
        num_routes: data.numRoutes,
      }

      const response = await apiEndpoints.generateMLRoutes(request)
      
      if (response.data.success) {
        setGeneratedRoutes(response.data.routes)
        onRoutesGenerated(response.data.routes)
        toast.success(`Geradas ${response.data.routes.length} rotas personalizadas!`)
      } else {
        toast.error(response.data.message)
      }
    } catch (error) {
      console.error('Erro ao gerar rotas ML:', error)
      toast.error('Erro ao gerar rotas. Tente novamente.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Gerador de Rotas Inteligentes
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Escolha entre algoritmo tradicional ou personalização com IA para gerar 
          as melhores rotas de ecoturismo sustentável em Angola.
        </p>
      </div>

      {/* Mode Selector */}
      <div className="flex justify-center">
        <div className="flex bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setMode('traditional')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-md transition-all duration-200 ${
              mode === 'traditional'
                ? 'bg-white text-primary-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <CpuChipIcon className="w-5 h-5" />
            <span className="font-medium">Tradicional</span>
          </button>
          <button
            onClick={() => setMode('ml')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-md transition-all duration-200 ${
              mode === 'ml'
                ? 'bg-white text-primary-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <SparklesIcon className="w-5 h-5" />
            <span className="font-medium">IA Personalizada</span>
          </button>
        </div>
      </div>

      {/* Forms */}
      <AnimatePresence mode="wait">
        {mode === 'traditional' ? (
          <motion.div
            key="traditional"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
          >
            <form onSubmit={traditionalForm.handleSubmit(handleTraditionalSubmit)} className="space-y-6">
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                  <CpuChipIcon className="w-6 h-6 text-primary-600 mr-2" />
                  Parâmetros da Rota Tradicional
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Orçamento */}
                  <div>
                    <label className="label">
                      <CurrencyDollarIcon className="w-4 h-4 inline mr-1" />
                      Orçamento Máximo (AOA)
                    </label>
                    <input
                      type="number"
                      {...traditionalForm.register('maxBudget', { valueAsNumber: true })}
                      className="input-field"
                      placeholder="20000"
                    />
                    {traditionalForm.formState.errors.maxBudget && (
                      <p className="text-red-500 text-sm mt-1">
                        {traditionalForm.formState.errors.maxBudget.message}
                      </p>
                    )}
                  </div>

                  {/* Número de Locais */}
                  <div>
                    <label className="label">
                      <MapPinIcon className="w-4 h-4 inline mr-1" />
                      Número Máximo de Locais
                    </label>
                    <input
                      type="number"
                      {...traditionalForm.register('maxLocations', { valueAsNumber: true })}
                      className="input-field"
                      placeholder="5"
                    />
                    {traditionalForm.formState.errors.maxLocations && (
                      <p className="text-red-500 text-sm mt-1">
                        {traditionalForm.formState.errors.maxLocations.message}
                      </p>
                    )}
                  </div>

                  {/* Fragilidade */}
                  <div>
                    <label className="label">
                      <ExclamationTriangleIcon className="w-4 h-4 inline mr-1" />
                      Fragilidade Máxima
                    </label>
                    <select
                      {...traditionalForm.register('maxFragility', { valueAsNumber: true })}
                      className="input-field"
                    >
                      <option value={1}>1 - Muito Baixa</option>
                      <option value={2}>2 - Baixa</option>
                      <option value={3}>3 - Média</option>
                      <option value={4}>4 - Alta</option>
                      <option value={5}>5 - Muito Alta</option>
                    </select>
                    {traditionalForm.formState.errors.maxFragility && (
                      <p className="text-red-500 text-sm mt-1">
                        {traditionalForm.formState.errors.maxFragility.message}
                      </p>
                    )}
                  </div>

                  {/* Número de Rotas */}
                  <div>
                    <label className="label">
                      <MapIcon className="w-4 h-4 inline mr-1" />
                      Número de Rotas
                    </label>
                    <input
                      type="number"
                      {...traditionalForm.register('numRoutes', { valueAsNumber: true })}
                      className="input-field"
                      placeholder="3"
                    />
                    {traditionalForm.formState.errors.numRoutes && (
                      <p className="text-red-500 text-sm mt-1">
                        {traditionalForm.formState.errors.numRoutes.message}
                      </p>
                    )}
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="btn-primary w-full mt-6 flex items-center justify-center space-x-2"
                >
                  {isLoading ? (
                    <LoadingSpinner size="sm" />
                  ) : (
                    <CpuChipIcon className="w-5 h-5" />
                  )}
                  <span>{isLoading ? 'Gerando Rotas...' : 'Gerar Rotas Tradicionais'}</span>
                </button>
              </div>
            </form>
          </motion.div>
        ) : (
          <motion.div
            key="ml"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.3 }}
          >
            <form onSubmit={mlForm.handleSubmit(handleMLSubmit)} className="space-y-6">
              <div className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                  <SparklesIcon className="w-6 h-6 text-primary-600 mr-2" />
                  Perfil Personalizado com IA
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Idade */}
                  <div>
                    <label className="label">
                      <UserIcon className="w-4 h-4 inline mr-1" />
                      Sua Idade
                    </label>
                    <input
                      type="number"
                      {...mlForm.register('userAge', { valueAsNumber: true })}
                      className="input-field"
                      placeholder="30"
                    />
                    {mlForm.formState.errors.userAge && (
                      <p className="text-red-500 text-sm mt-1">
                        {mlForm.formState.errors.userAge.message}
                      </p>
                    )}
                  </div>

                  {/* Orçamento */}
                  <div>
                    <label className="label">
                      <CurrencyDollarIcon className="w-4 h-4 inline mr-1" />
                      Orçamento Máximo (AOA)
                    </label>
                    <input
                      type="number"
                      {...mlForm.register('maxBudget', { valueAsNumber: true })}
                      className="input-field"
                      placeholder="20000"
                    />
                    {mlForm.formState.errors.maxBudget && (
                      <p className="text-red-500 text-sm mt-1">
                        {mlForm.formState.errors.maxBudget.message}
                      </p>
                    )}
                  </div>

                  {/* Preferências */}
                  <div>
                    <label className="label">
                      🌱 Preferência por Sustentabilidade
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      {...mlForm.register('sustainabilityPreference', { valueAsNumber: true })}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-gray-500 mt-1">
                      <span>Baixa</span>
                      <span>{mlForm.watch('sustainabilityPreference')?.toFixed(1) || '0.8'}</span>
                      <span>Alta</span>
                    </div>
                  </div>

                  <div>
                    <label className="label">
                      🏔️ Preferência por Aventura
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      {...mlForm.register('adventurePreference', { valueAsNumber: true })}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-gray-500 mt-1">
                      <span>Baixa</span>
                      <span>{mlForm.watch('adventurePreference')?.toFixed(1) || '0.6'}</span>
                      <span>Alta</span>
                    </div>
                  </div>

                  <div>
                    <label className="label">
                      🎭 Preferência por Cultura
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      {...mlForm.register('culturePreference', { valueAsNumber: true })}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-gray-500 mt-1">
                      <span>Baixa</span>
                      <span>{mlForm.watch('culturePreference')?.toFixed(1) || '0.7'}</span>
                      <span>Alta</span>
                    </div>
                  </div>

                  {/* Número de Locais */}
                  <div>
                    <label className="label">
                      <MapPinIcon className="w-4 h-4 inline mr-1" />
                      Número Máximo de Locais
                    </label>
                    <input
                      type="number"
                      {...mlForm.register('maxLocations', { valueAsNumber: true })}
                      className="input-field"
                      placeholder="5"
                    />
                    {mlForm.formState.errors.maxLocations && (
                      <p className="text-red-500 text-sm mt-1">
                        {mlForm.formState.errors.maxLocations.message}
                      </p>
                    )}
                  </div>

                  {/* Número de Rotas */}
                  <div>
                    <label className="label">
                      <MapIcon className="w-4 h-4 inline mr-1" />
                      Número de Rotas
                    </label>
                    <input
                      type="number"
                      {...mlForm.register('numRoutes', { valueAsNumber: true })}
                      className="input-field"
                      placeholder="3"
                    />
                    {mlForm.formState.errors.numRoutes && (
                      <p className="text-red-500 text-sm mt-1">
                        {mlForm.formState.errors.numRoutes.message}
                      </p>
                    )}
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="btn-primary w-full mt-6 flex items-center justify-center space-x-2"
                >
                  {isLoading ? (
                    <LoadingSpinner size="sm" />
                  ) : (
                    <SparklesIcon className="w-5 h-5" />
                  )}
                  <span>{isLoading ? 'Gerando Rotas...' : 'Gerar Rotas Personalizadas'}</span>
                </button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results */}
      {generatedRoutes.length > 0 && (
        <RouteResults routes={generatedRoutes} mode={mode} />
      )}
    </div>
  )
}
