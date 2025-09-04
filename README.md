# 🌍 EcoRota Angola - Sistema de Roteiro Inteligente de Ecoturismo

## 📋 Visão Geral

O **EcoRota Angola** é um sistema inteligente de recomendação de rotas de ecoturismo que equilibra **sustentabilidade ambiental**, **custo-benefício** e **experiência cultural** para promover o turismo responsável em Angola.

## 🎯 Objetivos

- ✅ Sugerir rotas de ecoturismo sustentável baseadas em critérios ambientais
- ✅ Otimizar custos e distâncias usando algoritmos inteligentes
- ✅ Visualizar rotas em mapas interativos
- ✅ Gerar relatórios detalhados para turistas e operadores
- ✅ Promover o ecoturismo como motor de desenvolvimento sustentável

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** - Linguagem principal
- **Pandas** - Manipulação e análise de dados
- **Folium** - Criação de mapas interativos
- **Scikit-learn** - Algoritmos de clustering, ML e otimização
- **Haversine** - Cálculo de distâncias geográficas
- **Streamlit** - Interface web interativa (opcional)
- **Plotly** - Visualizações avançadas
- **Joblib** - Persistência de modelos ML
- **NumPy** - Computação numérica e arrays

## 📊 Dataset

O sistema utiliza um dataset com **25 locais de ecoturismo** em Angola, incluindo:

- **Parques Nacionais**: Kissama, Iona, Cangandala, Bicuar, etc.
- **Reservas Naturais**: Luando, Maiombe, Cuanza, etc.
- **Cachoeiras**: Kalandula, Ruacaná, Binga, Tundavala, etc.
- **Áreas de Conservação**: Mupa, Cameia, Quissama, etc.

### Estrutura dos Dados

Cada local possui:
- **Coordenadas geográficas** (latitude, longitude)
- **Índice de fragilidade ambiental** (1-5, onde 5 é mais frágil)
- **Capacidade diária** de visitantes
- **Taxa de entrada** em AOA
- **Tipo de ecossistema** (savana, floresta, deserto, montanha)
- **Descrição detalhada** do local

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd EcoRotasSystem-FTL
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Sistema

#### Modo Console (Recomendado para demonstração)

```bash
python ecoturismo_system.py
```

#### Demonstração com Machine Learning

```bash
python demo_ml.py
```

#### Interface Web Tradicional (Streamlit)

```bash
streamlit run app_streamlit.py
```

#### Interface Web com ML (Streamlit)

```bash
streamlit run app_ml_streamlit.py
```

## 📖 Como Usar

### 1. Execução Básica

O sistema irá automaticamente:
- Carregar o dataset de locais de ecoturismo
- Aplicar filtros de sustentabilidade (fragilidade ≤ 4)
- Gerar 5 rotas recomendadas usando clustering geográfico
- Criar mapa interativo HTML
- Gerar relatórios CSV e JSON

### 2. Parâmetros Configuráveis

```python
# Exemplo de uso personalizado
sistema = EcoTurismoSystem()
sistema.carregar_dados()

rotas = sistema.gerar_rotas_recomendadas(
    orcamento_max=25000,      # Orçamento máximo em AOA
    max_locais=5,             # Máximo de locais por rota
    fragilidade_max=3,        # Fragilidade máxima permitida
    num_rotas=3               # Número de rotas a gerar
)
```

### 3. Interface Web (Streamlit)

A interface web permite:
- Ajustar parâmetros em tempo real
- Visualizar mapas interativos
- Analisar dados com gráficos
- Exportar relatórios personalizados

## 🔬 Algoritmo de Recomendação

### 1. Filtragem de Sustentabilidade

- Locais com fragilidade ≤ 4
- Verificação de capacidade de carga
- Diversidade de ecossistemas

### 2. Clustering Geográfico

- Agrupa locais por proximidade usando K-Means
- Evita rotas muito dispersas
- Otimiza logística de viagem

### 3. Algoritmo do Vizinho Mais Próximo

- Minimiza distância total da rota
- Considera coordenadas geográficas reais
- Otimiza sequência de visitas

### 4. Score de Sustentabilidade

```
Score = 0.45 × fragilidade_média + 0.35 × distância_total(km/1000) + 0.20 × custo_total(AOA/100.000)
```

**Menor score = Melhor rota**

## 🤖 Sistema de Machine Learning

### 1. Modelo de Previsão de Ratings

- **Algoritmo**: Gradient Boosting Regressor
- **Features**: Idade, orçamento, preferências, características dos locais
- **Objetivo**: Prever rating que usuário daria a um local (1-5)
- **Performance**: R² Score > 0.7, RMSE < 0.5

### 2. Sistema de Clustering Avançado

- **Algoritmo**: K-Means com features engenheiradas
- **Features**: Coordenadas, fragilidade, capacidade, custo, atratividade
- **Objetivo**: Agrupar locais similares para diversificar rotas
- **Clusters**: 6-8 grupos baseados em características geográficas e ambientais

### 3. Filtragem Colaborativa

- **Algoritmo**: Similaridade Coseno + Nearest Neighbors
- **Dados**: Perfis de usuários sintéticos (1000+ usuários)
- **Objetivo**: Encontrar usuários com preferências similares
- **Aplicação**: Recomendar locais bem avaliados por usuários similares

### 4. Feature Engineering

- **Sustentabilidade Score**: Inversão da escala de fragilidade
- **Acessibilidade**: Baseada na distância de Luanda
- **Atratividade Composta**: Combinação ponderada de múltiplos fatores
- **Capacidade Relativa**: Normalização da capacidade de carga

### 5. Personalização Inteligente

O sistema aprende com:
- **Preferências explícitas**: Sustentabilidade, aventura, cultura
- **Comportamento implícito**: Padrões de escolha, ratings históricos
- **Contexto geográfico**: Proximidade, acessibilidade, clima
- **Características demográficas**: Idade, orçamento, experiência

## 📁 Estrutura do Projeto

```
EcoRotasSystem-FTL/
├── ecoturismo_system.py          # Sistema principal
├── ml_recommendation_engine.py   # Motor de ML
├── app_streamlit.py              # Interface web tradicional
├── app_ml_streamlit.py           # Interface web com ML
├── demo.py                       # Demonstração básica
├── demo_ml.py                    # Demonstração com ML
├── locais_ecoturismo_angola.csv  # Dataset dos locais
├── requirements.txt              # Dependências Python
├── README.md                     # Documentação
└── outputs/                      # Arquivos gerados
    ├── mapa_ecoturismo_*.html    # Mapas interativos
    ├── relatorio_rotas_*.csv     # Relatórios CSV
    ├── relatorio_detalhado_*.json # Relatórios JSON
    └── ml_models_*.pkl           # Modelos ML salvos
```

## 📊 Saídas do Sistema

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

## 🌱 Critérios de Sustentabilidade

### 1. Fragilidade Ambiental

- **1-2**: Baixa fragilidade (verde) - Ideal para turismo
- **3**: Fragilidade média (laranja) - Requer cuidado
- **4**: Alta fragilidade (vermelho) - Limite máximo
- **5**: Muito frágil - Excluído do sistema

### 2. Capacidade de Carga

- Considera limite diário de visitantes
- Evita sobrecarga em locais sensíveis
- Promove distribuição equilibrada

### 3. Diversidade Ecológica

- Inclui diferentes tipos de ecossistemas
- Promove educação ambiental
- Maximiza experiência do turista

### 4. Distribuição Geográfica

- Evita concentração em uma região
- Promove desenvolvimento regional
- Otimiza logística de transporte

## 📈 Exemplos de Rotas Geradas

### Rota 1: Circuito das Cachoeiras
- **Locais**: Kalandula, Ruacaná, Binga, Tundavala
- **Distância**: 1,247 km
- **Custo**: 54,000 AOA
- **Fragilidade**: 2.0/5
- **Score**: 2.847

### Rota 2: Parques do Sul
- **Locais**: Iona, Bicuar, Mupa, Caconda
- **Distância**: 892 km
- **Custo**: 95,000 AOA
- **Fragilidade**: 3.25/5
- **Score**: 3.421

## 🎯 Impacto Esperado

### Para Turistas
- Rotas otimizadas e sustentáveis
- Informações detalhadas sobre cada local
- Planejamento eficiente de viagem
- Consciência ambiental

### Para Operadores
- Planejamento logístico otimizado
- Redução de custos operacionais
- Diferenciação no mercado
- Responsabilidade social

### Para Comunidades Locais
- Turismo que preserva o meio ambiente
- Desenvolvimento econômico sustentável
- Preservação cultural
- Geração de empregos

### Para Angola
- Promoção do ecoturismo
- Diversificação da economia
- Preservação da biodiversidade
- Posicionamento internacional

## 🔮 Funcionalidades Futuras

### Fase 2 (Opcional)
- [ ] Integração com APIs de clima
- [ ] Sistema de reservas online
- [ ] Estimativa de pegada de carbono
- [ ] Relatórios em PDF
- [ ] App mobile

### Fase 3 (Expansão)
- [ ] Dados em tempo real
- [ ] IA para personalização
- [ ] Integração com transporte público
- [ ] Sistema de avaliações
- [ ] Marketplace de serviços

## 🤝 Contribuição

Este projeto foi desenvolvido para o **Hackathon FTL 2024** com o objetivo de demonstrar como a tecnologia pode apoiar o ecoturismo sustentável em Angola.

### Como Contribuir

1. Fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Contato

**Sistema EcoRota Angola**
- Desenvolvido para Hackathon FTL 2024
- Promovendo Ecoturismo Sustentável em Angola
- Equilibrando Preservação Ambiental e Desenvolvimento

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

*"Mostrando como a tecnologia pode apoiar o ecoturismo sustentável em Angola, equilibrando preservação ambiental, inclusão comunitária e experiência inesquecível para o turista."*
