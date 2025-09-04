#!/usr/bin/env python3
"""
Validadores de Dados para EcoRota Angola
=======================================

Este módulo contém classes e funções para validação de dados:
- Validação de estrutura de DataFrames
- Validação de conteúdo e tipos
- Validação de ranges e consistência
- Validação de integridade referencial

Autor: Sistema EcoRota Angola
Data: 2024
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Classe para validação de dados do sistema EcoRota Angola.
    
    Esta classe implementa validações robustas para garantir
    a qualidade e integridade dos dados em todas as etapas
    do processamento.
    """
    
    def __init__(self, config):
        """
        Inicializa o validador de dados.
        
        Args:
            config: Instância de configuração do sistema
        """
        self.config = config
        self.required_columns = config.data.required_columns
        self.min_fragilidade = config.data.min_fragilidade
        self.max_fragilidade = config.data.max_fragilidade
        
        logger.info("DataValidator inicializado")
    
    def validate_dataframe_structure(self, df: pd.DataFrame) -> bool:
        """
        Valida a estrutura básica do DataFrame.
        
        Validações realizadas:
        - Presença de colunas obrigatórias
        - Tipos de dados básicos
        - Não vazio
        
        Args:
            df: DataFrame a ser validado
            
        Returns:
            True se válido, False caso contrário
            
        Example:
            >>> validator = DataValidator(config)
            >>> is_valid = validator.validate_dataframe_structure(df)
            >>> print(f"DataFrame válido: {is_valid}")
        """
        try:
            logger.debug("Validando estrutura do DataFrame...")
            
            # Verificar se DataFrame não está vazio
            if df.empty:
                logger.error("DataFrame está vazio")
                return False
            
            # Verificar colunas obrigatórias
            missing_columns = set(self.required_columns) - set(df.columns)
            if missing_columns:
                logger.error(f"Colunas obrigatórias faltando: {missing_columns}")
                return False
            
            # Verificar se há dados suficientes
            if len(df) < 1:
                logger.error("DataFrame deve ter pelo menos 1 registro")
                return False
            
            logger.debug("Estrutura do DataFrame válida")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação da estrutura: {e}")
            return False
    
    def validate_data_content(self, df: pd.DataFrame) -> bool:
        """
        Valida o conteúdo dos dados.
        
        Validações realizadas:
        - Ranges de valores
        - Tipos de dados
        - Valores nulos críticos
        - Consistência básica
        
        Args:
            df: DataFrame a ser validado
            
        Returns:
            True se válido, False caso contrário
        """
        try:
            logger.debug("Validando conteúdo dos dados...")
            
            # Validar ranges de valores
            if not self.validate_value_ranges(df):
                return False
            
            # Validar tipos de dados
            if not self.validate_data_types(df):
                return False
            
            # Validar valores nulos críticos
            if not self.validate_critical_nulls(df):
                return False
            
            # Validar consistência geográfica
            if not self.validate_geographic_consistency(df):
                return False
            
            logger.debug("Conteúdo dos dados válido")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação do conteúdo: {e}")
            return False
    
    def validate_value_ranges(self, df: pd.DataFrame) -> bool:
        """
        Valida ranges de valores para colunas numéricas.
        
        Args:
            df: DataFrame a ser validado
            
        Returns:
            True se todos os valores estão em ranges válidos
        """
        try:
            logger.debug("Validando ranges de valores...")
            
            # Validar fragilidade
            if 'fragilidade' in df.columns:
                invalid_fragility = df[
                    (df['fragilidade'] < self.min_fragilidade) | 
                    (df['fragilidade'] > self.max_fragilidade)
                ]
                if not invalid_fragility.empty:
                    logger.error(f"Valores de fragilidade inválidos: {invalid_fragility['fragilidade'].tolist()}")
                    return False
            
            # Validar coordenadas
            if 'latitude' in df.columns:
                invalid_lat = df[
                    (df['latitude'] < -90) | (df['latitude'] > 90)
                ]
                if not invalid_lat.empty:
                    logger.error(f"Valores de latitude inválidos: {invalid_lat['latitude'].tolist()}")
                    return False
            
            if 'longitude' in df.columns:
                invalid_lon = df[
                    (df['longitude'] < -180) | (df['longitude'] > 180)
                ]
                if not invalid_lon.empty:
                    logger.error(f"Valores de longitude inválidos: {invalid_lon['longitude'].tolist()}")
                    return False
            
            # Validar valores positivos
            positive_columns = ['capacidade_diaria', 'taxa_aoa']
            for col in positive_columns:
                if col in df.columns:
                    negative_values = df[df[col] <= 0]
                    if not negative_values.empty:
                        logger.error(f"Valores negativos ou zero em {col}: {negative_values[col].tolist()}")
                        return False
            
            logger.debug("Ranges de valores válidos")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação de ranges: {e}")
            return False
    
    def validate_data_types(self, df: pd.DataFrame) -> bool:
        """
        Valida tipos de dados das colunas.
        
        Args:
            df: DataFrame a ser validado
            
        Returns:
            True se tipos estão corretos
        """
        try:
            logger.debug("Validando tipos de dados...")
            
            # Validar colunas numéricas
            numeric_columns = ['latitude', 'longitude', 'fragilidade', 'capacidade_diaria', 'taxa_aoa']
            for col in numeric_columns:
                if col in df.columns:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        logger.error(f"Coluna {col} deve ser numérica")
                        return False
            
            # Validar colunas de texto
            text_columns = ['nome', 'provincia', 'tipo_ecosistema', 'descricao']
            for col in text_columns:
                if col in df.columns:
                    if not pd.api.types.is_string_dtype(df[col]):
                        logger.error(f"Coluna {col} deve ser texto")
                        return False
            
            logger.debug("Tipos de dados válidos")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação de tipos: {e}")
            return False
    
    def validate_critical_nulls(self, df: pd.DataFrame) -> bool:
        """
        Valida valores nulos em colunas críticas.
        
        Args:
            df: DataFrame a ser validado
            
        Returns:
            True se não há valores nulos críticos
        """
        try:
            logger.debug("Validando valores nulos críticos...")
            
            # Colunas que não podem ter valores nulos
            critical_columns = ['nome', 'provincia', 'latitude', 'longitude', 'fragilidade']
            
            for col in critical_columns:
                if col in df.columns:
                    null_count = df[col].isnull().sum()
                    if null_count > 0:
                        logger.error(f"Valores nulos em coluna crítica {col}: {null_count}")
                        return False
            
            logger.debug("Valores nulos críticos validados")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação de valores nulos: {e}")
            return False
    
    def validate_geographic_consistency(self, df: pd.DataFrame) -> bool:
        """
        Valida consistência geográfica dos dados.
        
        Args:
            df: DataFrame a ser validado
            
        Returns:
            True se dados geográficos são consistentes
        """
        try:
            logger.debug("Validando consistência geográfica...")
            
            # Verificar se coordenadas estão dentro de Angola
            if 'latitude' in df.columns and 'longitude' in df.columns:
                # Aproximadamente limites de Angola
                angola_bounds = {
                    'lat_min': -18.0,
                    'lat_max': -4.0,
                    'lon_min': 11.0,
                    'lon_max': 24.0
                }
                
                outside_angola = df[
                    (df['latitude'] < angola_bounds['lat_min']) |
                    (df['latitude'] > angola_bounds['lat_max']) |
                    (df['longitude'] < angola_bounds['lon_min']) |
                    (df['longitude'] > angola_bounds['lon_max'])
                ]
                
                if not outside_angola.empty:
                    logger.warning(f"Coordenadas fora dos limites de Angola: {len(outside_angola)} registros")
                    # Não retorna False, apenas avisa
            
            logger.debug("Consistência geográfica validada")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação geográfica: {e}")
            return False
    
    def validate_derived_features(self, df: pd.DataFrame) -> bool:
        """
        Valida features derivadas criadas durante o processamento.
        
        Args:
            df: DataFrame com features derivadas
            
        Returns:
            True se features derivadas são válidas
        """
        try:
            logger.debug("Validando features derivadas...")
            
            # Validar score de sustentabilidade
            if 'sustentabilidade_score' in df.columns:
                invalid_sustainability = df[
                    (df['sustentabilidade_score'] < 0) | 
                    (df['sustentabilidade_score'] > self.max_fragilidade)
                ]
                if not invalid_sustainability.empty:
                    logger.error("Score de sustentabilidade inválido")
                    return False
            
            # Validar scores relativos
            relative_columns = ['capacidade_relativa', 'custo_relativo', 'acessibilidade_score']
            for col in relative_columns:
                if col in df.columns:
                    invalid_relative = df[
                        (df[col] < 0) | (df[col] > 1)
                    ]
                    if not invalid_relative.empty:
                        logger.error(f"Score relativo inválido em {col}")
                        return False
            
            # Validar score de atratividade
            if 'atratividade_score' in df.columns:
                invalid_attractiveness = df[
                    (df['atratividade_score'] < 0) | (df['atratividade_score'] > 1)
                ]
                if not invalid_attractiveness.empty:
                    logger.error("Score de atratividade inválido")
                    return False
            
            logger.debug("Features derivadas válidas")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação de features derivadas: {e}")
            return False
    
    def validate_route_data(self, route_data: List[Dict[str, Any]]) -> bool:
        """
        Valida dados de uma rota gerada.
        
        Args:
            route_data: Lista de dicionários com dados da rota
            
        Returns:
            True se dados da rota são válidos
        """
        try:
            logger.debug("Validando dados da rota...")
            
            if not route_data:
                logger.error("Dados da rota estão vazios")
                return False
            
            # Validar estrutura de cada local na rota
            required_route_fields = ['nome', 'provincia', 'latitude', 'longitude', 'fragilidade', 'taxa_aoa']
            
            for i, location in enumerate(route_data):
                missing_fields = set(required_route_fields) - set(location.keys())
                if missing_fields:
                    logger.error(f"Campos obrigatórios faltando no local {i}: {missing_fields}")
                    return False
                
                # Validar tipos de dados
                if not isinstance(location['latitude'], (int, float)):
                    logger.error(f"Latitude inválida no local {i}")
                    return False
                
                if not isinstance(location['longitude'], (int, float)):
                    logger.error(f"Longitude inválida no local {i}")
                    return False
                
                if not isinstance(location['fragilidade'], (int, float)):
                    logger.error(f"Fragilidade inválida no local {i}")
                    return False
            
            logger.debug("Dados da rota válidos")
            return True
            
        except Exception as e:
            logger.error(f"Erro na validação dos dados da rota: {e}")
            return False
    
    def get_validation_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Gera relatório detalhado de validação.
        
        Args:
            df: DataFrame a ser analisado
            
        Returns:
            Dicionário com relatório de validação
        """
        try:
            logger.debug("Gerando relatório de validação...")
            
            report = {
                'total_records': len(df),
                'total_columns': len(df.columns),
                'missing_columns': list(set(self.required_columns) - set(df.columns)),
                'null_counts': df.isnull().sum().to_dict(),
                'data_types': df.dtypes.to_dict(),
                'value_ranges': {},
                'validation_results': {}
            }
            
            # Calcular ranges de valores
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                report['value_ranges'][col] = {
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'mean': df[col].mean(),
                    'std': df[col].std()
                }
            
            # Resultados de validação
            report['validation_results'] = {
                'structure_valid': self.validate_dataframe_structure(df),
                'content_valid': self.validate_data_content(df),
                'value_ranges_valid': self.validate_value_ranges(df),
                'data_types_valid': self.validate_data_types(df),
                'critical_nulls_valid': self.validate_critical_nulls(df),
                'geographic_consistent': self.validate_geographic_consistency(df)
            }
            
            logger.debug("Relatório de validação gerado")
            return report
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de validação: {e}")
            return {}


def validate_user_profile(profile: Dict[str, Any]) -> bool:
    """
    Valida perfil de usuário para sistema de ML.
    
    Args:
        profile: Dicionário com perfil do usuário
        
    Returns:
        True se perfil é válido
    """
    try:
        required_fields = ['idade', 'orcamento_max', 'preferencia_sustentabilidade', 
                          'preferencia_aventura', 'preferencia_cultura']
        
        # Verificar campos obrigatórios
        missing_fields = set(required_fields) - set(profile.keys())
        if missing_fields:
            logger.error(f"Campos obrigatórios faltando no perfil: {missing_fields}")
            return False
        
        # Validar ranges
        if not (18 <= profile['idade'] <= 100):
            logger.error(f"Idade inválida: {profile['idade']}")
            return False
        
        if profile['orcamento_max'] <= 0:
            logger.error(f"Orçamento inválido: {profile['orcamento_max']}")
            return False
        
        # Validar preferências (0-1)
        preference_fields = ['preferencia_sustentabilidade', 'preferencia_aventura', 'preferencia_cultura']
        for field in preference_fields:
            if not (0 <= profile[field] <= 1):
                logger.error(f"Preferência inválida {field}: {profile[field]}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na validação do perfil: {e}")
        return False


if __name__ == "__main__":
    """Teste dos validadores."""
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Criar dados de teste
    test_data = {
        'nome': ['Parque Nacional da Kissama', 'Cascatas de Kalandula'],
        'provincia': ['Luanda', 'Malange'],
        'latitude': [-8.7500, -9.0833],
        'longitude': [13.2500, 16.0167],
        'fragilidade': [3, 2],
        'capacidade_diaria': [150, 200],
        'taxa_aoa': [25000, 15000],
        'tipo_ecosistema': ['savana', 'floresta'],
        'descricao': ['Reserva natural', 'Cachoeiras espetaculares']
    }
    
    df = pd.DataFrame(test_data)
    
    # Teste básico
    from config.settings import get_config
    config = get_config()
    validator = DataValidator(config)
    
    print("🧪 Testando validadores...")
    
    # Teste de estrutura
    is_valid = validator.validate_dataframe_structure(df)
    print(f"Estrutura válida: {is_valid}")
    
    # Teste de conteúdo
    is_valid = validator.validate_data_content(df)
    print(f"Conteúdo válido: {is_valid}")
    
    # Teste de perfil
    test_profile = {
        'idade': 30,
        'orcamento_max': 20000,
        'preferencia_sustentabilidade': 0.8,
        'preferencia_aventura': 0.6,
        'preferencia_cultura': 0.7
    }
    
    profile_valid = validate_user_profile(test_profile)
    print(f"Perfil válido: {profile_valid}")
    
    # Relatório de validação
    report = validator.get_validation_report(df)
    print(f"Relatório gerado: {len(report)} seções")
    
    print("✅ Testes dos validadores concluídos!")
