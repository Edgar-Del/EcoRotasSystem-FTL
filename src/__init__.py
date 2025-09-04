"""
EcoRota Angola - Sistema Inteligente de Ecoturismo
=================================================

Este pacote contém o sistema completo de recomendação de rotas
de ecoturismo sustentável em Angola, incluindo:

- Sistema principal de recomendação
- Motor de Machine Learning
- Utilitários e ferramentas
- Interfaces web

Autor: Sistema EcoRota Angola
Data: 2024
Versão: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Sistema EcoRota Angola"
__email__ = "suporte@ecorota-angola.com"
__description__ = "Sistema Inteligente de Recomendação de Rotas de Ecoturismo Sustentável"

# Imports principais
from .core.ecoturismo_system import EcoTurismoSystem
from .core.data_processor import DataProcessor
from .core.route_optimizer import RouteOptimizer
from .ml.ml_recommendation_engine import MLRecommendationEngine

# Utilitários
from .utils.geographic import GeographicCalculator
from .utils.validators import DataValidator
from .utils.formatters import DataFormatter
from .utils.logger import setup_logger, EcoRotaLogger

__all__ = [
    # Sistema principal
    'EcoTurismoSystem',
    'DataProcessor', 
    'RouteOptimizer',
    'MLRecommendationEngine',
    
    # Utilitários
    'GeographicCalculator',
    'DataValidator',
    'DataFormatter',
    'setup_logger',
    'EcoRotaLogger',
    
    # Metadados
    '__version__',
    '__author__',
    '__email__',
    '__description__'
]
