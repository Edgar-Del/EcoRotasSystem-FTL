'use client'

import { motion } from 'framer-motion'
import { 
  SparklesIcon,
  MapIcon,
  GlobeAltIcon,
  CpuChipIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  CurrencyDollarIcon,
  ClockIcon,
  HeartIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'

export function FeaturesSection() {
  const features = [
    {
      icon: SparklesIcon,
      title: 'IA Personalizada',
      description: 'Algoritmos de machine learning que personalizam recomendações baseadas no seu perfil e preferências.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: MapIcon,
      title: 'Rotas Otimizadas',
      description: 'Algoritmo do vizinho mais próximo para minimizar distâncias e maximizar a experiência.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: GlobeAltIcon,
      title: 'Sustentabilidade',
      description: 'Prioriza locais com baixa fragilidade ambiental para preservar o ecossistema.',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: CpuChipIcon,
      title: 'Algoritmo Tradicional',
      description: 'Sistema clássico de recomendação baseado em critérios de sustentabilidade e custo.',
      color: 'from-orange-500 to-red-500'
    },
    {
      icon: ChartBarIcon,
      title: 'Análise Avançada',
      description: 'Estatísticas detalhadas e visualizações interativas para análise de rotas.',
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Critérios Rigorosos',
      description: 'Validação de fragilidade ambiental, capacidade de carga e impacto sustentável.',
      color: 'from-teal-500 to-green-500'
    }
  ]

  const benefits = [
    {
      icon: CurrencyDollarIcon,
      title: 'Custo-Benefício',
      description: 'Otimização de orçamento com máxima experiência'
    },
    {
      icon: ClockIcon,
      title: 'Eficiência',
      description: 'Rotas otimizadas para minimizar tempo de deslocamento'
    },
    {
      icon: HeartIcon,
      title: 'Preservação',
      description: 'Foco na conservação ambiental e turismo responsável'
    },
    {
      icon: LightBulbIcon,
      title: 'Inovação',
      description: 'Tecnologia de ponta para ecoturismo sustentável'
    }
  ]

  return (
    <section id="features" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Funcionalidades Avançadas
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Tecnologia de ponta combinada com expertise em sustentabilidade 
              para criar a melhor experiência de ecoturismo em Angola.
            </p>
          </motion.div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group"
            >
              <div className="card hover:shadow-xl transition-all duration-300 h-full">
                <div className="flex items-center mb-4">
                  <div className={`flex items-center justify-center w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <feature.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Benefits Section */}
        <div className="bg-white rounded-2xl shadow-soft p-8 md:p-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
              Por que escolher o EcoRota Angola?
            </h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Combinamos tecnologia avançada com conhecimento local para 
              oferecer a melhor experiência de ecoturismo sustentável.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="flex items-center justify-center w-16 h-16 bg-primary-100 rounded-2xl mx-auto mb-4">
                  <benefit.icon className="w-8 h-8 text-primary-600" />
                </div>
                
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  {benefit.title}
                </h4>
                
                <p className="text-gray-600 text-sm">
                  {benefit.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mt-16"
        >
          <div className="bg-gradient-to-r from-primary-600 to-accent-600 rounded-2xl p-8 md:p-12 text-white">
            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Pronto para explorar Angola de forma sustentável?
            </h3>
            <p className="text-lg mb-8 opacity-90 max-w-2xl mx-auto">
              Comece sua jornada de ecoturismo hoje mesmo. Gere rotas personalizadas 
              e descubra as maravilhas naturais de Angola.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-white text-primary-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-50 transition-colors duration-200 flex items-center justify-center space-x-2"
              >
                <SparklesIcon className="w-5 h-5" />
                <span>Começar Agora</span>
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white hover:text-primary-600 transition-colors duration-200 flex items-center justify-center space-x-2"
              >
                <MapIcon className="w-5 h-5" />
                <span>Ver Mapa</span>
              </motion.button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
