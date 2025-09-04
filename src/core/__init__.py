"""
Módulo Core do EcoRota Angola
============================

Este módulo contém as classes principais do sistema:
- EcoTurismoSystem: Sistema principal de recomendação
- RouteOptimizer: Otimizador de rotas
- DataProcessor: Processador de dados

Autor: Sistema EcoRota Angola
Data: 2024
"""

from .ecoturismo_system import EcoTurismoSystem
from .route_optimizer import RouteOptimizer
from .data_processor import DataProcessor

__all__ = [
    'EcoTurismoSystem',
    'RouteOptimizer',
    'DataProcessor'
]
