#!/usr/bin/env python3
"""
Configurações do Sistema EcoRota Angola
======================================

Este módulo contém todas as configurações do sistema, incluindo:
- Parâmetros de ML
- Configurações de dados
- Configurações de interface
- Configurações de logging

Autor: Sistema EcoRota Angola
Data: 2024
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class DataConfig:
    """Configurações relacionadas aos dados."""
    
    # Caminhos dos arquivos
    data_dir: Path = Path("data")
    csv_file: str = "locais_ecoturismo_angola.csv"
    output_dir: Path = Path("outputs")
    
    # Configurações do dataset
    min_fragilidade: int = 1
    max_fragilidade: int = 5
    fragilidade_sustentavel: int = 4
    
    # Configurações de validação
    required_columns: List[str] = field(default_factory=lambda: [
        'nome', 'provincia', 'latitude', 'longitude', 
        'fragilidade', 'capacidade_diaria', 'taxa_aoa', 
        'tipo_ecosistema', 'descricao'
    ])
    
    # Coordenadas de referência (Luanda)
    luanda_coords: tuple = (-8.8390, 13.2894)


@dataclass
class MLConfig:
    """Configurações do sistema de Machine Learning."""
    
    # Configurações do modelo de rating
    rating_model_params: Dict[str, Any] = field(default_factory=lambda: {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 6,
        'random_state': 42,
        'n_jobs': -1
    })
    
    # Configurações de clustering
    clustering_params: Dict[str, Any] = field(default_factory=lambda: {
        'n_clusters': 6,
        'random_state': 42,
        'n_init': 10,
        'max_iter': 300
    })
    
    # Configurações de feature engineering
    feature_weights: Dict[str, float] = field(default_factory=lambda: {
        'sustentabilidade': 0.3,
        'capacidade': 0.2,
        'popularidade': 0.2,
        'acessibilidade': 0.2,
        'custo': 0.1
    })
    
    # Configurações de dados sintéticos
    synthetic_users: int = 1000
    min_visits_per_user: int = 3
    max_visits_per_user: int = 15
    
    # Configurações de treinamento
    test_size: float = 0.2
    cv_folds: int = 5
    random_state: int = 42
    
    # Configurações de persistência
    model_prefix: str = "ecorota_ml"
    save_models: bool = True


@dataclass
class RouteConfig:
    """Configurações para geração de rotas."""
    
    # Limites padrão
    default_max_budget: float = 20000.0
    default_max_locations: int = 6
    default_max_fragility: int = 4
    default_num_routes: int = 5
    
    # Configurações de otimização
    max_budget_per_location: float = 0.4  # 40% do orçamento por local
    min_route_score: float = 0.0
    max_route_score: float = 10.0
    
    # Configurações de score
    score_weights: Dict[str, float] = field(default_factory=lambda: {
        'fragilidade': 0.45,
        'distancia': 0.35,
        'custo': 0.20
    })
    
    # Configurações de clustering para rotas
    route_clustering: bool = True
    min_cluster_size: int = 2


@dataclass
class UIConfig:
    """Configurações da interface de usuário."""
    
    # Configurações do Streamlit
    page_title: str = "EcoRota Angola - Sistema Inteligente de Ecoturismo"
    page_icon: str = "🌍"
    layout: str = "wide"
    
    # Configurações do mapa
    default_zoom: int = 6
    map_center: tuple = (-12.5, 17.5)
    map_tiles: str = "OpenStreetMap"
    
    # Configurações de cores
    color_palette: List[str] = field(default_factory=lambda: [
        'red', 'blue', 'green', 'purple', 'orange', 
        'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen'
    ])
    
    # Configurações de visualização
    max_display_routes: int = 10
    chart_height: int = 400
    map_height: int = 600


@dataclass
class LoggingConfig:
    """Configurações de logging."""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "logs/ecorota.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


class Config:
    """Classe principal de configuração do sistema."""
    
    def __init__(self):
        """Inicializa todas as configurações."""
        self.data = DataConfig()
        self.ml = MLConfig()
        self.route = RouteConfig()
        self.ui = UIConfig()
        self.logging = LoggingConfig()
        
        # Criar diretórios necessários
        self._create_directories()
    
    def _create_directories(self):
        """Cria diretórios necessários se não existirem."""
        directories = [
            self.data.data_dir,
            self.data.output_dir,
            Path("logs"),
            Path("models"),
            Path("tests/outputs")
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_data_path(self) -> Path:
        """Retorna o caminho completo do arquivo de dados."""
        return self.data.data_dir / self.data.csv_file
    
    def get_output_path(self, filename: str) -> Path:
        """Retorna o caminho completo para arquivos de saída."""
        return self.data.output_dir / filename
    
    def get_model_path(self, model_name: str) -> Path:
        """Retorna o caminho completo para modelos salvos."""
        return Path("models") / f"{self.ml.model_prefix}_{model_name}.pkl"
    
    def validate_config(self) -> bool:
        """Valida se todas as configurações estão corretas."""
        try:
            # Verificar se arquivo de dados existe
            if not self.get_data_path().exists():
                raise FileNotFoundError(f"Arquivo de dados não encontrado: {self.get_data_path()}")
            
            # Verificar se diretórios existem
            if not self.data.data_dir.exists():
                raise FileNotFoundError(f"Diretório de dados não encontrado: {self.data.data_dir}")
            
            # Validar configurações de ML
            if self.ml.test_size <= 0 or self.ml.test_size >= 1:
                raise ValueError("test_size deve estar entre 0 e 1")
            
            if self.ml.cv_folds < 2:
                raise ValueError("cv_folds deve ser pelo menos 2")
            
            # Validar configurações de rota
            if self.route.default_max_budget <= 0:
                raise ValueError("default_max_budget deve ser positivo")
            
            if self.route.default_max_locations < 2:
                raise ValueError("default_max_locations deve ser pelo menos 2")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na validação da configuração: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte todas as configurações para dicionário."""
        return {
            'data': self.data.__dict__,
            'ml': self.ml.__dict__,
            'route': self.route.__dict__,
            'ui': self.ui.__dict__,
            'logging': self.logging.__dict__
        }
    
    def save_config(self, filename: str = "config.json"):
        """Salva configurações em arquivo JSON."""
        import json
        
        config_dict = self.to_dict()
        config_path = Path("config") / filename
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Configurações salvas em: {config_path}")
    
    def load_config(self, filename: str = "config.json"):
        """Carrega configurações de arquivo JSON."""
        import json
        
        config_path = Path("config") / filename
        
        if not config_path.exists():
            print(f"⚠️ Arquivo de configuração não encontrado: {config_path}")
            return False
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            # Atualizar configurações
            self.data.__dict__.update(config_dict.get('data', {}))
            self.ml.__dict__.update(config_dict.get('ml', {}))
            self.route.__dict__.update(config_dict.get('route', {}))
            self.ui.__dict__.update(config_dict.get('ui', {}))
            self.logging.__dict__.update(config_dict.get('logging', {}))
            
            print(f"✅ Configurações carregadas de: {config_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar configurações: {e}")
            return False


# Instância global de configuração
config = Config()


def get_config() -> Config:
    """Retorna a instância global de configuração."""
    return config


def validate_environment() -> bool:
    """Valida se o ambiente está configurado corretamente."""
    try:
        # Verificar se configuração é válida
        if not config.validate_config():
            return False
        
        # Verificar dependências Python
        required_packages = [
            'pandas', 'numpy', 'scikit-learn', 'folium', 
            'haversine', 'streamlit', 'plotly', 'joblib'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Pacotes Python faltando: {', '.join(missing_packages)}")
            print("💡 Execute: pip install -r requirements.txt")
            return False
        
        print("✅ Ambiente validado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na validação do ambiente: {e}")
        return False


if __name__ == "__main__":
    """Teste das configurações."""
    print("🔧 Testando configurações do EcoRota Angola...")
    
    if validate_environment():
        print("✅ Todas as configurações estão corretas!")
        config.save_config()
    else:
        print("❌ Problemas encontrados nas configurações.")
