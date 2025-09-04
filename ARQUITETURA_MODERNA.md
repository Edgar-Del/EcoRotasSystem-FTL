# 🌍 EcoRota Angola - Arquitetura Moderna

## 📋 Visão Geral

O Sistema EcoRota Angola foi modernizado com uma arquitetura de API REST + Frontend React, substituindo a interface Streamlit por uma solução mais escalável e moderna.

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Backend   │    │   Sistema Core  │
│   NextJS/React  │◄──►│   FastAPI       │◄──►│   Python        │
│   Port: 3000    │    │   Port: 8000    │    │   (Original)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Componentes

### 1. API Backend (FastAPI)
- **Localização**: `/api/`
- **Porta**: 8000
- **Documentação**: http://localhost:8000/docs
- **Funcionalidades**:
  - Endpoints REST para todas as operações
  - Validação de dados com Pydantic
  - CORS habilitado para frontend
  - Documentação automática (Swagger/ReDoc)
  - Sistema de autenticação JWT (básico)

### 2. Frontend (NextJS + React)
- **Localização**: `/frontend/`
- **Porta**: 3000
- **URL**: http://localhost:3000
- **Funcionalidades**:
  - Interface moderna e responsiva
  - Componentes interativos
  - Mapas com Leaflet
  - Gráficos com Recharts
  - Animações com Framer Motion
  - Formulários com validação

### 3. Sistema Core (Python)
- **Localização**: `/src/`
- **Funcionalidades**:
  - Algoritmos de recomendação
  - Machine Learning
  - Processamento de dados
  - Geração de mapas
  - Relatórios

## 🛠️ Tecnologias Utilizadas

### Backend (API)
- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI
- **Python 3.8+**: Linguagem principal

### Frontend
- **Next.js 14**: Framework React com App Router
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Framework CSS utilitário
- **Framer Motion**: Animações
- **React Query**: Gerenciamento de estado servidor
- **React Hook Form**: Formulários
- **Zod**: Validação de schemas
- **Leaflet**: Mapas interativos
- **Recharts**: Gráficos

## 📁 Estrutura de Arquivos

```
EcoRotasSystem-FTL/
├── api/                          # API FastAPI
│   ├── main.py                   # Aplicação principal
│   ├── run.py                    # Script de execução
│   └── requirements.txt          # Dependências Python
├── frontend/                     # Frontend NextJS
│   ├── src/
│   │   ├── app/                  # App Router
│   │   ├── components/           # Componentes React
│   │   ├── lib/                  # Utilitários
│   │   ├── types/                # Tipos TypeScript
│   │   └── utils/                # Funções auxiliares
│   ├── package.json              # Dependências Node.js
│   ├── tailwind.config.js        # Configuração Tailwind
│   └── next.config.js            # Configuração Next.js
├── src/                          # Sistema Core (original)
├── start.sh                      # Script de inicialização
└── ARQUITETURA_MODERNA.md        # Esta documentação
```

## 🔌 Endpoints da API

### Rotas
- `POST /routes/traditional` - Gerar rotas tradicionais
- `POST /routes/ml` - Gerar rotas com ML
- `GET /routes/export/csv` - Exportar CSV
- `GET /routes/export/json` - Exportar JSON

### Locais
- `GET /locations` - Listar todos os locais
- `GET /locations/{id}` - Obter local específico

### Sistema
- `GET /health` - Health check
- `GET /stats` - Estatísticas do sistema

## 🎨 Interface do Frontend

### Páginas Principais
1. **Home** (`/`) - Página principal com todas as funcionalidades
2. **Gerador de Rotas** - Formulários para gerar rotas
3. **Mapa Interativo** - Visualização das rotas
4. **Estatísticas** - Gráficos e métricas

### Componentes Principais
- `RouteGenerator` - Gerador de rotas (tradicional/ML)
- `MapView` - Mapa interativo com Leaflet
- `StatsSection` - Estatísticas e gráficos
- `Hero` - Seção principal
- `Header/Footer` - Layout

## 🚀 Como Executar

### Opção 1: Script Automático
```bash
./start.sh
```

### Opção 2: Manual

#### API Backend
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Configuração

### Variáveis de Ambiente

#### API
```env
# Configurações padrão do sistema original
```

#### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=EcoRota Angola
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## 📊 Funcionalidades Implementadas

### ✅ Completas
- [x] API REST completa
- [x] Frontend React moderno
- [x] Gerador de rotas (tradicional e ML)
- [x] Mapa interativo
- [x] Estatísticas e gráficos
- [x] Interface responsiva
- [x] Validação de formulários
- [x] Animações fluidas
- [x] Documentação automática

### 🔄 Melhorias Futuras
- [ ] Autenticação JWT completa
- [ ] Cache Redis
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Deploy em produção
- [ ] PWA (Progressive Web App)
- [ ] Notificações push

## 🎯 Benefícios da Nova Arquitetura

### Para Desenvolvedores
- **Separação de responsabilidades**: Frontend e backend independentes
- **Tecnologias modernas**: Stack atualizada e performática
- **Documentação automática**: API auto-documentada
- **Tipagem forte**: TypeScript + Pydantic
- **Desenvolvimento ágil**: Hot reload e ferramentas modernas

### Para Usuários
- **Interface moderna**: Design responsivo e intuitivo
- **Performance**: Carregamento rápido e interações fluidas
- **Experiência rica**: Animações e feedback visual
- **Acessibilidade**: Componentes acessíveis
- **Mobile-first**: Otimizado para dispositivos móveis

### Para o Sistema
- **Escalabilidade**: Arquitetura preparada para crescimento
- **Manutenibilidade**: Código organizado e documentado
- **Extensibilidade**: Fácil adição de novas funcionalidades
- **Monitoramento**: Logs estruturados e métricas
- **Deploy**: Preparado para ambientes de produção

## 🔍 Comparação: Antes vs Depois

| Aspecto | Streamlit (Antes) | React + API (Depois) |
|---------|-------------------|----------------------|
| **Interface** | Básica, limitada | Moderna, rica |
| **Performance** | Lenta, recarregamentos | Rápida, SPA |
| **Customização** | Limitada | Total flexibilidade |
| **Mobile** | Não responsivo | Mobile-first |
| **Escalabilidade** | Limitada | Alta |
| **Manutenção** | Monolítica | Modular |
| **Deploy** | Complexo | Simples |
| **Desenvolvimento** | Lento | Ágil |

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação da API: http://localhost:8000/docs
2. Verifique os logs do sistema
3. Execute o script de diagnóstico: `./start.sh`

---

**EcoRota Angola** - Arquitetura Moderna para Ecoturismo Sustentável 🇦🇴
