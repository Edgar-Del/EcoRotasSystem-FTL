# EcoRota Angola - Frontend

Frontend moderno em React/NextJS para o Sistema de Ecoturismo Sustentável de Angola.

## 🚀 Tecnologias

- **Next.js 14** - Framework React com App Router
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização utilitária
- **Framer Motion** - Animações fluidas
- **React Query** - Gerenciamento de estado servidor
- **React Hook Form** - Formulários performáticos
- **Zod** - Validação de schemas
- **Leaflet** - Mapas interativos
- **Recharts** - Gráficos e visualizações
- **Heroicons** - Ícones modernos

## 📦 Instalação

```bash
# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env.local

# Executar em desenvolvimento
npm run dev
```

## 🛠️ Scripts Disponíveis

```bash
npm run dev          # Servidor de desenvolvimento
npm run build        # Build de produção
npm run start        # Servidor de produção
npm run lint         # Verificação de código
npm run type-check   # Verificação de tipos
```

## 🏗️ Estrutura do Projeto

```
src/
├── app/                 # App Router (Next.js 14)
│   ├── globals.css     # Estilos globais
│   ├── layout.tsx      # Layout principal
│   └── page.tsx        # Página inicial
├── components/         # Componentes React
│   ├── layout/         # Componentes de layout
│   ├── sections/       # Seções da página
│   ├── route-generator/ # Gerador de rotas
│   ├── map/           # Componentes de mapa
│   └── ui/            # Componentes de UI
├── lib/               # Utilitários e configurações
├── hooks/             # Custom hooks
├── types/             # Definições TypeScript
└── utils/             # Funções utilitárias
```

## 🎨 Design System

### Cores
- **Primary**: Verde (sustentabilidade)
- **Secondary**: Amarelo (sol angolano)
- **Accent**: Azul (água e céu)

### Componentes
- Cards com sombras suaves
- Botões com estados hover/focus
- Formulários com validação
- Animações fluidas
- Design responsivo

## 🔌 Integração com API

O frontend se conecta com a API FastAPI através de:
- **Base URL**: `http://localhost:8000`
- **Endpoints**: Documentados em `/docs`
- **Autenticação**: JWT (implementação básica)

## 📱 Funcionalidades

### 🎯 Gerador de Rotas
- **Modo Tradicional**: Algoritmo clássico
- **Modo IA**: Personalização com ML
- **Validação**: Formulários com Zod
- **Feedback**: Toast notifications

### 🗺️ Mapa Interativo
- **Leaflet**: Mapas responsivos
- **Marcadores**: Locais de ecoturismo
- **Rotas**: Linhas coloridas
- **Popups**: Informações detalhadas

### 📊 Estatísticas
- **Gráficos**: Recharts
- **Métricas**: Sistema em tempo real
- **Visualizações**: Interativas

## 🚀 Deploy

### Vercel (Recomendado)
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```bash
# Build da imagem
docker build -t ecorota-frontend .

# Executar container
docker run -p 3000:3000 ecorota-frontend
```

## 🔧 Configuração

### Variáveis de Ambiente
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=EcoRota Angola
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Tailwind CSS
- Configuração customizada
- Cores do design system
- Animações personalizadas
- Responsividade mobile-first

## 📈 Performance

- **Lazy Loading**: Componentes sob demanda
- **Image Optimization**: Next.js Image
- **Code Splitting**: Automático
- **Caching**: React Query
- **Bundle Analysis**: `npm run build`

## 🧪 Testes

```bash
# Executar testes
npm test

# Coverage
npm run test:coverage

# E2E
npm run test:e2e
```

## 📝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Suporte

Para suporte, entre em contato:
- **Email**: suporte@ecorota-angola.com
- **GitHub Issues**: [Abrir issue](https://github.com/ecorota-angola/frontend/issues)

---

**EcoRota Angola** - Promovendo Ecoturismo Sustentável 🇦🇴
