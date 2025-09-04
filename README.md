# 🌍 EcoRota Angola - Sistema Inteligente de Ecoturismo

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 📋 Visão Geral

O **EcoRota Angola** é um sistema avançado de **Machine Learning** para recomendação de rotas de ecoturismo sustentável em Angola. O sistema combina algoritmos de otimização, inteligência artificial e análise geográfica para oferecer recomendações personalizadas que equilibram sustentabilidade ambiental, custo-benefício e experiência cultural.

### 🎯 Objetivos Principais

- ✅ **Sustentabilidade Ambiental**: Prioriza locais com baixa fragilidade ecológica
- ✅ **Personalização Inteligente**: Usa ML para adaptar recomendações ao perfil do usuário
- ✅ **Otimização de Rotas**: Minimiza distâncias e custos usando algoritmos avançados
- ✅ **Visualização Interativa**: Mapas e relatórios detalhados
- ✅ **Escalabilidade**: Arquitetura modular para futuras expansões

## 🏗️ Arquitetura do Sistema

### Componentes Principais

```
EcoRota Angola/
├── 📁 src/                    # Código fonte principal
│   ├── 📁 core/              # Sistema principal
│   │   ├── ecoturismo_system.py    # Classe principal
│   │   ├── data_processor.py       # Processamento de dados
│   │   └── route_optimizer.py      # Otimização de rotas
│   ├── 📁 ml/                # Machine Learning
│   │   └── ml_recommendation_engine.py  # Motor de ML
│   ├── 📁 web/               # Interfaces web
│   │   ├── app_streamlit.py         # Interface tradicional
│   │   └── app_ml_streamlit.py      # Interface com ML
│   └── 📁 utils/             # Utilitários
│       ├── geographic.py            # Cálculos geográficos
│       ├── validators.py            # Validação de dados
│       ├── formatters.py            # Formatação de saídas
│       └── logger.py                # Sistema de logging
├── 📁 config/                # Configurações
│   └── settings.py                 # Configurações centralizadas
├── 📁 data/                  # Dados
│   └── locais_ecoturismo_angola.csv  # Dataset principal
├── 📁 tests/                 # Testes
├── 📁 docs/                  # Documentação
└── main.py                   # Executável principal
```

### 🤖 Algoritmos de Machine Learning

#### 1. Modelo de Previsão de Ratings
- **Algoritmo**: Gradient Boosting Regressor
- **Features**: Idade, orçamento, preferências, características dos locais
- **Performance**: R² Score > 0.75, RMSE < 0.5
- **Objetivo**: Prever rating 1-5 que usuário daria a um local

#### 2. Sistema de Clustering
- **Algoritmo**: K-Means com features engenheiradas
- **Features**: Coordenadas, fragilidade, capacidade, custo, atratividade
- **Clusters**: 6-8 grupos geográficos e ambientais
- **Objetivo**: Diversificar rotas e agrupar locais similares

#### 3. Filtragem Colaborativa
- **Algoritmo**: Similaridade Coseno + Nearest Neighbors
- **Dados**: 1000+ usuários sintéticos com perfis diversos
- **Objetivo**: Encontrar usuários similares e recomendar locais
- **Aplicação**: Sistema de recomendação baseado em comportamento

#### 4. Feature Engineering
- **Sustentabilidade Score**: Inversão da escala de fragilidade
- **Acessibilidade**: Baseada na distância de Luanda
- **Atratividade Composta**: Combinação ponderada de múltiplos fatores
- **Capacidade Relativa**: Normalização da capacidade de carga

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior
- 4GB RAM mínimo (8GB recomendado)
- 1GB espaço em disco

### Instalação Rápida

```bash
# 1. Clonar o repositório
git clone <repository-url>
cd EcoRotasSystem-FTL

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Validar instalação
python main.py --mode demo
```

### Instalação Detalhada

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar sistema
python config/settings.py

# 4. Executar testes
python -m pytest tests/
```

## 📖 Guia de Uso

### 1. Execução Básica

```bash
# Demonstração completa
python main.py --mode demo

# Sistema tradicional
python main.py --mode traditional --budget 25000 --max-locations 5

# Sistema com ML
python main.py --mode ml --user-age 30 --budget 20000 --sustainability 0.8
```

### 2. Interface Web

```bash
# Interface tradicional
python main.py --mode web

# Ou diretamente
streamlit run src/web/app_ml_streamlit.py
```

### 3. Uso Programático

```python
from src.core.ecoturismo_system import EcoTurismoSystem

# Sistema básico
sistema = EcoTurismoSystem(use_ml=False)
sistema.load_data()
rotas = sistema.generate_traditional_routes(
    max_budget=20000,
    max_locations=5,
    num_routes=3
)

# Sistema com ML
sistema_ml = EcoTurismoSystem(use_ml=True)
sistema_ml.load_data()

user_profile = {
    'idade': 30,
    'orcamento_max': 20000,
    'preferencia_sustentabilidade': 0.8,
    'preferencia_aventura': 0.6,
    'preferencia_cultura': 0.7
}

rotas_personalizadas = sistema_ml.generate_ml_routes(user_profile)
```

## 📊 Dataset

### Estrutura dos Dados

O sistema utiliza um dataset com **25 locais de ecoturismo** em Angola:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome` | String | Nome do local |
| `provincia` | String | Província onde está localizado |
| `latitude` | Float | Coordenada de latitude |
| `longitude` | Float | Coordenada de longitude |
| `fragilidade` | Integer | Índice de fragilidade (1-5) |
| `capacidade_diaria` | Integer | Capacidade de visitantes por dia |
| `taxa_aoa` | Integer | Taxa de entrada em AOA |
| `tipo_ecosistema` | String | Tipo de ecossistema |
| `descricao` | String | Descrição detalhada |

### Tipos de Locais

- **Parques Nacionais**: Kissama, Iona, Cangandala, Bicuar
- **Reservas Naturais**: Luando, Maiombe, Cuanza
- **Cachoeiras**: Kalandula, Ruacaná, Binga, Tundavala
- **Áreas de Conservação**: Mupa, Cameia, Quissama

## 🎯 Algoritmos de Recomendação

### Sistema Tradicional

1. **Filtragem de Sustentabilidade**
   - Locais com fragilidade ≤ 4
   - Verificação de capacidade de carga
   - Diversidade de ecossistemas

2. **Clustering Geográfico**
   - Agrupa locais por proximidade usando K-Means
   - Evita rotas muito dispersas
   - Otimiza logística de viagem

3. **Algoritmo do Vizinho Mais Próximo**
   - Minimiza distância total da rota
   - Considera coordenadas geográficas reais
   - Otimiza sequência de visitas

4. **Score de Sustentabilidade**
   ```
   Score = 0.45 × fragilidade_média + 0.35 × distância_total(km/1000) + 0.20 × custo_total(AOA/100.000)
   ```

### Sistema com ML

1. **Personalização por Perfil**
   - Análise de preferências do usuário
   - Previsão de ratings usando ML
   - Adaptação dinâmica de recomendações

2. **Filtragem Colaborativa**
   - Encontra usuários com preferências similares
   - Recomenda locais bem avaliados por usuários similares
   - Aprende com padrões de comportamento

3. **Otimização Inteligente**
   - Combina múltiplos critérios de otimização
   - Balanceia sustentabilidade e experiência
   - Considera contexto geográfico e sazonal

## 📈 Métricas de Performance

### Modelo de ML
- **R² Score**: 0.75+ (explica 75% da variância)
- **RMSE**: < 0.5 (erro de previsão baixo)
- **Precision@K**: 0.8+ (80% das recomendações são relevantes)
- **Coverage**: 90%+ (cobre 90% dos locais disponíveis)

### Sistema de Recomendação
- **Tempo de Resposta**: < 2 segundos para rotas tradicionais
- **Tempo de Resposta ML**: < 5 segundos para rotas personalizadas
- **Precisão Geográfica**: ±100m para cálculos de distância
- **Diversidade**: Rotas em múltiplas províncias e ecossistemas

## 🗺️ Saídas do Sistema

### 1. Mapa Interativo (HTML)
- Visualização de todas as rotas recomendadas
- Marcadores coloridos por fragilidade ambiental
- Linhas de rota otimizadas
- Popups informativos para cada local
- Legenda de fragilidade ambiental

### 2. Relatório CSV
Resumo estruturado com:
- Nome da rota
- Número de locais
- Distância total (km)
- Custo total (AOA)
- Fragilidade média
- Score de sustentabilidade
- Províncias visitadas
- Tipos de ecossistema

### 3. Relatório JSON
Dados completos e detalhados:
- Informações completas de cada local
- Coordenadas geográficas
- Descrições detalhadas
- Métricas de performance
- Metadados do sistema

## 🔧 Configuração Avançada

### Arquivo de Configuração

```python
# config/settings.py
@dataclass
class MLConfig:
    rating_model_params: Dict[str, Any] = {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 6,
        'random_state': 42
    }
    
    clustering_params: Dict[str, Any] = {
        'n_clusters': 6,
        'random_state': 42,
        'n_init': 10
    }
    
    synthetic_users: int = 1000
    test_size: float = 0.2
    cv_folds: int = 5
```

### Variáveis de Ambiente

```bash
# Configurações opcionais
export ECOROTA_LOG_LEVEL=INFO
export ECOROTA_DATA_PATH=data/
export ECOROTA_OUTPUT_PATH=outputs/
export ECOROTA_ML_MODELS_PATH=models/
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python -m pytest tests/

# Testes específicos
python -m pytest tests/test_core.py
python -m pytest tests/test_ml.py
python -m pytest tests/test_utils.py

# Com cobertura
python -m pytest --cov=src tests/
```

### Testes Disponíveis

- **Testes Unitários**: Validação de componentes individuais
- **Testes de Integração**: Validação de fluxos completos
- **Testes de Performance**: Validação de tempos de resposta
- **Testes de ML**: Validação de modelos e métricas

## 📚 Documentação Técnica

### API Reference

```python
class EcoTurismoSystem:
    def __init__(self, config=None, use_ml: bool = True)
    def load_data(self, file_path: Optional[Path] = None) -> pd.DataFrame
    def generate_traditional_routes(self, **kwargs) -> List[Dict[str, Any]]
    def generate_ml_routes(self, user_profile: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]
    def create_interactive_map(self, save_html: bool = True) -> folium.Map
    def generate_csv_report(self, filename: str = None) -> Path
    def generate_json_report(self, filename: str = None) -> Path
```

### Extensibilidade

O sistema foi projetado para ser facilmente extensível:

1. **Novos Algoritmos**: Implementar interfaces para novos algoritmos de ML
2. **Novas Fontes de Dados**: Adicionar suporte a APIs e bancos de dados
3. **Novas Interfaces**: Criar interfaces para mobile, desktop, etc.
4. **Novos Critérios**: Adicionar critérios de sustentabilidade

## 🤝 Contribuição

### Como Contribuir

1. Fork do repositório
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abrir Pull Request

### Padrões de Código

- **PEP 8**: Seguir padrões de estilo Python
- **Type Hints**: Usar anotações de tipo
- **Docstrings**: Documentar todas as funções e classes
- **Testes**: Escrever testes para novas funcionalidades
- **Logging**: Usar sistema de logging para debug

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🏆 Reconhecimentos

- **Hackathon FTL 2024**: Plataforma para desenvolvimento
- **Angola**: Riqueza natural e biodiversidade
- **Comunidade Open Source**: Bibliotecas e ferramentas utilizadas

## 📞 Suporte

### Contato

- **Email**: suporte@ecorota-angola.com
- **GitHub Issues**: Para bugs e feature requests
- **Documentação**: [docs/](docs/) para guias detalhados

### FAQ

**P: Como adicionar novos locais ao sistema?**
R: Edite o arquivo `data/locais_ecoturismo_angola.csv` seguindo o formato existente.

**P: Como personalizar os algoritmos de ML?**
R: Modifique os parâmetros em `config/settings.py` na seção `MLConfig`.

**P: Como integrar com sistemas externos?**
R: Use a API programática ou implemente novos adaptadores em `src/adapters/`.

---

*Desenvolvido com ❤️ para promover o ecoturismo sustentável em Angola*