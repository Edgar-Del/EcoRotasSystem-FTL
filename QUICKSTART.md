# 🚀 Guia de Início Rápido - EcoRota Angola

## ⚡ Instalação e Execução em 3 Passos

### 1. Instalar Dependências
```bash
python install.py
```

### 2. Testar Sistema Básico
```bash
python demo.py
```

### 3. Testar Sistema com ML
```bash
python demo_ml.py
```

## 🌐 Interface Web

### Interface Tradicional
```bash
streamlit run app_streamlit.py
```

### Interface com ML
```bash
streamlit run app_ml_streamlit.py
```

## 📊 Arquivos Gerados

Após executar qualquer script, você encontrará:
- `mapa_ecoturismo_angola_*.html` - Mapa interativo
- `relatorio_rotas_*.csv` - Relatório CSV
- `relatorio_detalhado_*.json` - Relatório JSON
- `ml_models_*.pkl` - Modelos ML (se usar ML)

## 🎯 Exemplos de Uso

### Sistema Básico
```python
from ecoturismo_system import EcoTurismoSystem

sistema = EcoTurismoSystem()
sistema.carregar_dados()
rotas = sistema.gerar_rotas_recomendadas()
```

### Sistema com ML
```python
from ecoturismo_system import EcoTurismoSystem

sistema = EcoTurismoSystem(use_ml=True)
sistema.carregar_dados()

user_profile = {
    'idade': 30,
    'orcamento_max': 20000,
    'preferencia_sustentabilidade': 0.8,
    'preferencia_aventura': 0.6,
    'preferencia_cultura': 0.7
}

rotas = sistema.gerar_rotas_personalizadas_ml(user_profile)
```

## 🆘 Solução de Problemas

### Erro de Importação
```bash
pip install -r requirements.txt
```

### Erro de Arquivo CSV
Verifique se `locais_ecoturismo_angola.csv` está no diretório.

### Erro de Streamlit
```bash
pip install streamlit streamlit-folium
```

## 📞 Suporte

Para dúvidas ou problemas, consulte o README.md completo.
