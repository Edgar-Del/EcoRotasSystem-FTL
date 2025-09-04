#!/usr/bin/env python3
"""
Processador de Dados para EcoRota Angola
=======================================

Este módulo contém a classe DataProcessor responsável por:
- Carregamento e validação de dados
- Limpeza e transformação de dados
- Criação de features derivadas
- Validação de integridade dos dados

Autor: Sistema EcoRota Angola
Data: 2024
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import logging

from ..utils.validators import DataValidator
from ..utils.geographic import GeographicCalculator
from config.settings import get_config

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Classe responsável pelo processamento e validação de dados do sistema.
    
    Esta classe implementa o padrão de design Strategy para diferentes tipos
    de processamento de dados, garantindo flexibilidade e extensibilidade.
    
    Atributos:
        config: Configurações do sistema
        validator: Validador de dados
        geo_calc: Calculadora geográfica
        df: DataFrame principal com os dados processados
    """
    
    def __init__(self, config=None):
        """
        Inicializa o processador de dados.
        
        Args:
            config: Instância de configuração. Se None, usa configuração global.
        """
        self.config = config or get_config()
        self.validator = DataValidator(self.config)
        self.geo_calc = GeographicCalculator(self.config.data.luanda_coords)
        self.df: Optional[pd.DataFrame] = None
        
        logger.info("DataProcessor inicializado")
    
    def load_data(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """
        Carrega dados do arquivo CSV especificado.
        
        Este método implementa carregamento robusto com:
        - Validação de existência do arquivo
        - Tratamento de erros de encoding
        - Validação de estrutura dos dados
        - Logging detalhado do processo
        
        Args:
            file_path: Caminho para o arquivo CSV. Se None, usa configuração padrão.
            
        Returns:
            DataFrame com os dados carregados
            
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            ValueError: Se os dados não passarem na validação
            Exception: Para outros erros de carregamento
            
        Example:
            >>> processor = DataProcessor()
            >>> df = processor.load_data()
            >>> print(f"Dados carregados: {len(df)} registros")
        """
        try:
            # Determinar caminho do arquivo
            if file_path is None:
                file_path = self.config.get_data_path()
            
            logger.info(f"Carregando dados de: {file_path}")
            
            # Verificar se arquivo existe
            if not file_path.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
            # Carregar dados com tratamento de encoding
            try:
                self.df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                logger.warning("Tentando carregar com encoding latin-1")
                self.df = pd.read_csv(file_path, encoding='latin-1')
            
            logger.info(f"Dados carregados: {len(self.df)} registros, {len(self.df.columns)} colunas")
            
            # Validar estrutura dos dados
            if not self.validator.validate_dataframe_structure(self.df):
                raise ValueError("Estrutura dos dados inválida")
            
            # Validar conteúdo dos dados
            if not self.validator.validate_data_content(self.df):
                raise ValueError("Conteúdo dos dados inválido")
            
            # Processar dados
            self._process_loaded_data()
            
            logger.info("Dados carregados e processados com sucesso")
            return self.df
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def _process_loaded_data(self) -> None:
        """
        Processa dados após carregamento.
        
        Este método privado executa:
        - Limpeza de dados
        - Criação de features derivadas
        - Validação de integridade
        - Otimização de tipos de dados
        """
        try:
            logger.info("Iniciando processamento dos dados...")
            
            # Limpar dados
            self._clean_data()
            
            # Criar features derivadas
            self._create_derived_features()
            
            # Otimizar tipos de dados
            self._optimize_data_types()
            
            # Validação final
            self._validate_processed_data()
            
            logger.info("Processamento dos dados concluído")
            
        except Exception as e:
            logger.error(f"Erro no processamento dos dados: {e}")
            raise
    
    def _clean_data(self) -> None:
        """
        Limpa e normaliza os dados carregados.
        
        Operações de limpeza:
        - Remoção de espaços em branco
        - Normalização de strings
        - Tratamento de valores nulos
        - Validação de tipos de dados
        """
        try:
            logger.debug("Limpando dados...")
            
            # Remover espaços em branco de strings
            string_columns = self.df.select_dtypes(include=['object']).columns
            for col in string_columns:
                self.df[col] = self.df[col].astype(str).str.strip()
            
            # Normalizar nomes (primeira letra maiúscula)
            if 'nome' in self.df.columns:
                self.df['nome'] = self.df['nome'].str.title()
            
            if 'provincia' in self.df.columns:
                self.df['provincia'] = self.df['provincia'].str.title()
            
            # Tratamento de valores nulos
            self._handle_missing_values()
            
            logger.debug("Limpeza dos dados concluída")
            
        except Exception as e:
            logger.error(f"Erro na limpeza dos dados: {e}")
            raise
    
    def _handle_missing_values(self) -> None:
        """
        Trata valores nulos nos dados.
        
        Estratégias de tratamento:
        - Valores numéricos: preenchimento com mediana
        - Valores categóricos: preenchimento com moda
        - Coordenadas: remoção de registros inválidos
        """
        try:
            logger.debug("Tratando valores nulos...")
            
            # Verificar valores nulos
            null_counts = self.df.isnull().sum()
            if null_counts.sum() > 0:
                logger.warning(f"Valores nulos encontrados: {null_counts[null_counts > 0].to_dict()}")
                
                # Tratar valores nulos em colunas numéricas
                numeric_columns = self.df.select_dtypes(include=[np.number]).columns
                for col in numeric_columns:
                    if self.df[col].isnull().sum() > 0:
                        median_value = self.df[col].median()
                        self.df[col].fillna(median_value, inplace=True)
                        logger.debug(f"Preenchido {col} com mediana: {median_value}")
                
                # Tratar valores nulos em colunas categóricas
                categorical_columns = self.df.select_dtypes(include=['object']).columns
                for col in categorical_columns:
                    if self.df[col].isnull().sum() > 0:
                        mode_value = self.df[col].mode().iloc[0] if not self.df[col].mode().empty else 'Desconhecido'
                        self.df[col].fillna(mode_value, inplace=True)
                        logger.debug(f"Preenchido {col} com moda: {mode_value}")
            
            logger.debug("Tratamento de valores nulos concluído")
            
        except Exception as e:
            logger.error(f"Erro no tratamento de valores nulos: {e}")
            raise
    
    def _create_derived_features(self) -> None:
        """
        Cria features derivadas dos dados originais.
        
        Features criadas:
        - Distância de Luanda
        - Score de sustentabilidade
        - Capacidade relativa
        - Custo relativo
        - Score de acessibilidade
        - Score de atratividade composta
        """
        try:
            logger.debug("Criando features derivadas...")
            
            # Distância de Luanda
            self.df['distancia_luanda'] = self.df.apply(
                lambda row: self.geo_calc.calculate_distance_from_reference(
                    (row['latitude'], row['longitude'])
                ), axis=1
            )
            
            # Score de sustentabilidade (inversão da fragilidade)
            self.df['sustentabilidade_score'] = (
                self.config.data.max_fragilidade - self.df['fragilidade'] + 1
            )
            
            # Capacidade relativa
            max_capacidade = self.df['capacidade_diaria'].max()
            self.df['capacidade_relativa'] = self.df['capacidade_diaria'] / max_capacidade
            
            # Custo relativo
            max_custo = self.df['taxa_aoa'].max()
            self.df['custo_relativo'] = self.df['taxa_aoa'] / max_custo
            
            # Score de acessibilidade (inversão da distância)
            max_distancia = self.df['distancia_luanda'].max()
            self.df['acessibilidade_score'] = 1 - (self.df['distancia_luanda'] / max_distancia)
            
            # Score de atratividade composta
            weights = self.config.ml.feature_weights
            self.df['atratividade_score'] = (
                weights['sustentabilidade'] * self.df['sustentabilidade_score'] +
                weights['capacidade'] * self.df['capacidade_relativa'] +
                weights['acessibilidade'] * self.df['acessibilidade_score'] +
                weights['custo'] * (1 - self.df['custo_relativo'])
            )
            
            logger.debug("Features derivadas criadas com sucesso")
            
        except Exception as e:
            logger.error(f"Erro na criação de features derivadas: {e}")
            raise
    
    def _optimize_data_types(self) -> None:
        """
        Otimiza tipos de dados para melhor performance.
        
        Otimizações:
        - Conversão de floats para tipos menores quando possível
        - Uso de categorias para strings repetitivas
        - Otimização de índices
        """
        try:
            logger.debug("Otimizando tipos de dados...")
            
            # Converter colunas categóricas
            categorical_columns = ['provincia', 'tipo_ecosistema']
            for col in categorical_columns:
                if col in self.df.columns:
                    self.df[col] = self.df[col].astype('category')
            
            # Otimizar tipos numéricos
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                if self.df[col].dtype == 'float64':
                    # Tentar converter para float32 se possível
                    if self.df[col].min() >= np.finfo(np.float32).min and \
                       self.df[col].max() <= np.finfo(np.float32).max:
                        self.df[col] = self.df[col].astype('float32')
            
            logger.debug("Otimização de tipos concluída")
            
        except Exception as e:
            logger.error(f"Erro na otimização de tipos: {e}")
            raise
    
    def _validate_processed_data(self) -> None:
        """
        Valida dados após processamento.
        
        Validações:
        - Integridade dos dados
        - Ranges de valores
        - Consistência das features derivadas
        """
        try:
            logger.debug("Validando dados processados...")
            
            # Validar ranges de valores
            if not self.validator.validate_value_ranges(self.df):
                raise ValueError("Ranges de valores inválidos")
            
            # Validar consistência das features
            if not self.validator.validate_derived_features(self.df):
                raise ValueError("Features derivadas inconsistentes")
            
            logger.debug("Validação dos dados processados concluída")
            
        except Exception as e:
            logger.error(f"Erro na validação dos dados processados: {e}")
            raise
    
    def get_sustainable_locations(self, max_fragility: Optional[int] = None) -> pd.DataFrame:
        """
        Filtra locais sustentáveis baseado na fragilidade.
        
        Args:
            max_fragility: Fragilidade máxima permitida. Se None, usa configuração.
            
        Returns:
            DataFrame filtrado com locais sustentáveis
        """
        try:
            if max_fragility is None:
                max_fragility = self.config.data.fragilidade_sustentavel
            
            sustainable_df = self.df[self.df['fragilidade'] <= max_fragility].copy()
            
            logger.info(f"Locais sustentáveis (fragilidade <= {max_fragility}): {len(sustainable_df)}")
            return sustainable_df
            
        except Exception as e:
            logger.error(f"Erro ao filtrar locais sustentáveis: {e}")
            raise
    
    def get_locations_by_budget(self, max_budget: float) -> pd.DataFrame:
        """
        Filtra locais baseado no orçamento máximo.
        
        Args:
            max_budget: Orçamento máximo em AOA
            
        Returns:
            DataFrame filtrado por orçamento
        """
        try:
            budget_df = self.df[self.df['taxa_aoa'] <= max_budget].copy()
            
            logger.info(f"Locais dentro do orçamento (<= {max_budget} AOA): {len(budget_df)}")
            return budget_df
            
        except Exception as e:
            logger.error(f"Erro ao filtrar por orçamento: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas dos dados processados.
        
        Returns:
            Dicionário com estatísticas dos dados
        """
        try:
            if self.df is None:
                raise ValueError("Dados não carregados")
            
            stats = {
                'total_locations': len(self.df),
                'provinces': self.df['provincia'].nunique(),
                'ecosystems': self.df['tipo_ecosistema'].nunique(),
                'avg_fragility': self.df['fragilidade'].mean(),
                'avg_cost': self.df['taxa_aoa'].mean(),
                'avg_capacity': self.df['capacidade_diaria'].mean(),
                'fragility_distribution': self.df['fragilidade'].value_counts().to_dict(),
                'province_distribution': self.df['provincia'].value_counts().to_dict(),
                'ecosystem_distribution': self.df['tipo_ecosistema'].value_counts().to_dict()
            }
            
            logger.info("Estatísticas calculadas com sucesso")
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            raise
    
    def export_processed_data(self, output_path: Optional[Path] = None) -> Path:
        """
        Exporta dados processados para arquivo CSV.
        
        Args:
            output_path: Caminho de saída. Se None, usa configuração padrão.
            
        Returns:
            Caminho do arquivo exportado
        """
        try:
            if self.df is None:
                raise ValueError("Dados não carregados")
            
            if output_path is None:
                output_path = self.config.get_output_path("dados_processados.csv")
            
            self.df.to_csv(output_path, index=False, encoding='utf-8')
            
            logger.info(f"Dados processados exportados para: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao exportar dados: {e}")
            raise


if __name__ == "__main__":
    """Teste do processador de dados."""
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Teste básico
    processor = DataProcessor()
    
    try:
        # Carregar dados
        df = processor.load_data()
        print(f"✅ Dados carregados: {len(df)} registros")
        
        # Obter estatísticas
        stats = processor.get_statistics()
        print(f"📊 Estatísticas: {stats['total_locations']} locais, {stats['provinces']} províncias")
        
        # Filtrar locais sustentáveis
        sustainable = processor.get_sustainable_locations()
        print(f"🌱 Locais sustentáveis: {len(sustainable)}")
        
        print("✅ Teste do processador concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
