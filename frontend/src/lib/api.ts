import axios from 'axios'
import { 
  RouteResponse, 
  SystemStats, 
  RouteRequest, 
  MLRouteRequest,
  Location,
  ApiResponse 
} from '@/types'

// Configuração da API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Endpoints da API
export const apiEndpoints = {
  // Health check
  health: () => api.get('/health'),
  
  // Estatísticas do sistema
  stats: () => api.get<SystemStats>('/stats'),
  
  // Rotas
  generateTraditionalRoutes: (data: RouteRequest) => 
    api.post<RouteResponse>('/routes/traditional', data),
  
  generateMLRoutes: (data: MLRouteRequest) => 
    api.post<RouteResponse>('/routes/ml', data),
  
  // Locais
  getLocations: () => api.get<ApiResponse<Location[]>>('/locations'),
  getLocation: (id: number) => api.get<ApiResponse<Location>>(`/locations/${id}`),
  
  // Exportação
  exportCSV: () => api.get('/routes/export/csv'),
  exportJSON: () => api.get('/routes/export/json'),
}

// Funções auxiliares
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('pt-AO', {
    style: 'currency',
    currency: 'AOA',
    minimumFractionDigits: 0,
  }).format(amount)
}

export const formatDistance = (distance: number): string => {
  return `${distance.toFixed(1)} km`
}

export const getFragilityColor = (fragility: number): string => {
  if (fragility <= 2) return 'text-green-600 bg-green-100'
  if (fragility === 3) return 'text-yellow-600 bg-yellow-100'
  return 'text-red-600 bg-red-100'
}

export const getFragilityLabel = (fragility: number): string => {
  const labels = {
    1: 'Muito Baixa',
    2: 'Baixa',
    3: 'Média',
    4: 'Alta',
    5: 'Muito Alta'
  }
  return labels[fragility as keyof typeof labels] || 'Desconhecida'
}

export const getEcosystemIcon = (ecosystem: string): string => {
  const icons = {
    'Floresta': '🌲',
    'Savana': '🌾',
    'Deserto': '🏜️',
    'Costa': '🏖️',
    'Montanha': '⛰️',
    'Rio': '🏞️',
    'Lago': '🏞️'
  }
  return icons[ecosystem as keyof typeof icons] || '🌍'
}

// Validação de dados
export const validateRouteRequest = (data: Partial<RouteRequest>): string[] => {
  const errors: string[] = []
  
  if (!data.max_budget || data.max_budget <= 0) {
    errors.push('Orçamento deve ser maior que zero')
  }
  
  if (!data.max_locations || data.max_locations < 2 || data.max_locations > 10) {
    errors.push('Número de locais deve estar entre 2 e 10')
  }
  
  if (!data.max_fragility || data.max_fragility < 1 || data.max_fragility > 5) {
    errors.push('Fragilidade deve estar entre 1 e 5')
  }
  
  if (!data.num_routes || data.num_routes < 1 || data.num_routes > 10) {
    errors.push('Número de rotas deve estar entre 1 e 10')
  }
  
  return errors
}

export const validateMLRouteRequest = (data: Partial<MLRouteRequest>): string[] => {
  const errors: string[] = []
  
  if (!data.user_profile) {
    errors.push('Perfil do usuário é obrigatório')
    return errors
  }
  
  const { user_profile } = data
  
  if (!user_profile.idade || user_profile.idade < 18 || user_profile.idade > 100) {
    errors.push('Idade deve estar entre 18 e 100 anos')
  }
  
  if (!user_profile.orcamento_max || user_profile.orcamento_max <= 0) {
    errors.push('Orçamento deve ser maior que zero')
  }
  
  const preferences = [
    user_profile.preferencia_sustentabilidade,
    user_profile.preferencia_aventura,
    user_profile.preferencia_cultura
  ]
  
  for (const pref of preferences) {
    if (pref < 0 || pref > 1) {
      errors.push('Preferências devem estar entre 0 e 1')
      break
    }
  }
  
  return errors
}

export default api
