import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'EcoRota Angola - Sistema de Ecoturismo Sustentável',
  description: 'Sistema inteligente de recomendação de rotas de ecoturismo sustentável em Angola',
  keywords: ['ecoturismo', 'angola', 'sustentabilidade', 'rotas', 'turismo'],
  authors: [{ name: 'Sistema EcoRota Angola' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#16a34a',
  openGraph: {
    title: 'EcoRota Angola',
    description: 'Sistema inteligente de recomendação de rotas de ecoturismo sustentável',
    type: 'website',
    locale: 'pt_AO',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt" className="h-full">
      <body className={`${inter.className} h-full antialiased`}>
        <Providers>
          <div className="min-h-full bg-gradient-to-br from-green-50 via-blue-50 to-yellow-50">
            {children}
          </div>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#22c55e',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 5000,
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </Providers>
      </body>
    </html>
  )
}
