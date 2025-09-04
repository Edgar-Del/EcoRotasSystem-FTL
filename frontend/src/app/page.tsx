'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  MapIcon, 
  SparklesIcon, 
  GlobeAltIcon,
  ChartBarIcon,
  LeafIcon,
  HeartIcon
} from '@heroicons/react/24/outline'
import { Header } from '@/components/layout/header'
import { Hero } from '@/components/sections/hero'
import { RouteGenerator } from '@/components/route-generator/route-generator'
import { SimpleMapView } from '@/components/map/simple-map-view'
import { StatsSection } from '@/components/sections/stats-section'
import { FeaturesSection } from '@/components/sections/features-section'
import { Footer } from '@/components/layout/footer'

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<'generator' | 'map' | 'stats'>('generator')
  const [generatedRoutes, setGeneratedRoutes] = useState<any[]>([])

  const handleRoutesGenerated = (routes: any[]) => {
    setGeneratedRoutes(routes)
    setActiveTab('map')
  }

  return (
    <div className="min-h-screen">
      <Header />
      
      <main>
        {/* Hero Section */}
        <Hero />
        
        {/* Main Content */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Tab Navigation */}
            <div className="flex justify-center mb-12">
              <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
                {[
                  { id: 'generator', label: 'Gerador de Rotas', icon: SparklesIcon },
                  { id: 'map', label: 'Mapa Interativo', icon: MapIcon },
                  { id: 'stats', label: 'Estatísticas', icon: ChartBarIcon },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all duration-200 ${
                      activeTab === tab.id
                        ? 'bg-white text-primary-600 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    <tab.icon className="w-5 h-5" />
                    <span className="font-medium">{tab.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Tab Content */}
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              {activeTab === 'generator' && (
                <RouteGenerator onRoutesGenerated={handleRoutesGenerated} />
              )}
              
              {activeTab === 'map' && (
                <SimpleMapView routes={generatedRoutes} />
              )}
              
              {activeTab === 'stats' && (
                <StatsSection />
              )}
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <FeaturesSection />
      </main>

      <Footer />
    </div>
  )
}
