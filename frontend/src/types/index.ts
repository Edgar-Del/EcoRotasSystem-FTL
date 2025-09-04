// Tipos para o sistema EcoRota Angola

export interface Location {
  id: number
  nome: string
  provincia: string
  latitude: number
  longitude: number
  fragilidade: number
  taxa_aoa: number
  capacidade_diaria: number
  tipo_ecosistema: string
  descricao: string
  distancia_luanda_km?: number
}

export interface Route {
  nome: string
  locais: Location[]
  distancia_total_km: number
  custo_total_aoa: number
  fragilidade_media: number
  num_locais: number
  provincias: string[]
  tipos_ecosistema: string[]
  score?: number
  rating_medio_previsto?: number
}

export interface UserProfile {
  idade: number
  orcamento_max: number
  preferencia_sustentabilidade: number
  preferencia_aventura: number
  preferencia_cultura: number
}

export interface RouteRequest {
  max_budget: number
  max_locations: number
  max_fragility: number
  num_routes: number
}

export interface MLRouteRequest {
  user_profile: UserProfile
  max_locations: number
  num_routes: number
}

export interface RouteResponse {
  success: boolean
  message: string
  routes: Route[]
  metadata: {
    request: RouteRequest | MLRouteRequest
    total_routes: number
    map_created: boolean
    timestamp: string
  }
}

export interface SystemStats {
  data_loaded: boolean
  ml_enabled: boolean
  routes_generated: number
  map_created: boolean
  total_locations?: number
  provinces?: number
  ecosystems?: number
  ml_model_trained?: boolean
  ml_features?: number
}

export interface ApiResponse<T> {
  success: boolean
  message: string
  data?: T
  error?: string
}

// Tipos para componentes
export interface MapMarker {
  id: number
  position: [number, number]
  title: string
  description: string
  fragility: number
  cost: number
}

export interface RouteLine {
  id: string
  coordinates: [number, number][]
  color: string
  route: Route
}

// Enums
export enum RouteType {
  TRADITIONAL = 'traditional',
  ML = 'ml'
}

export enum FragilityLevel {
  LOW = 1,
  MEDIUM_LOW = 2,
  MEDIUM = 3,
  MEDIUM_HIGH = 4,
  HIGH = 5
}

export enum EcosystemType {
  FLORESTA = 'Floresta',
  SAVANA = 'Savana',
  DESERTO = 'Deserto',
  COSTA = 'Costa',
  MONTANHA = 'Montanha',
  RIO = 'Rio',
  LAGO = 'Lago'
}

// Utilitários de tipo
export type RouteGeneratorMode = 'traditional' | 'ml'

export interface FormData {
  // Dados para rota tradicional
  maxBudget: number
  maxLocations: number
  maxFragility: number
  numRoutes: number
  
  // Dados para rota ML
  userAge: number
  sustainabilityPreference: number
  adventurePreference: number
  culturePreference: number
}
