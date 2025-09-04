#!/usr/bin/env python3
"""
Sistema Principal EcoRota Angola
===============================

Este módulo contém a classe principal do sistema de recomendação de rotas
de ecoturismo sustentável, integrando todos os componentes do sistema:
- Processamento de dados
- Otimização de rotas
- Sistema de ML
- Geração de visualizações

Autor: Sistema EcoRota Angola
Data: 2024
"""

import pandas as pd
import numpy as np
import folium
import json
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime
import logging

from .data_processor import DataProcessor
from .route_optimizer import RouteOptimizer
from ..ml.ml_recommendation_engine import MLRecommendationEngine
from ..utils.geographic import GeographicCalculator
from ..utils.formatters import DataFormatter
from config.settings import get_config

logger = logging.getLogger(__name__)


class EcoTurismoSystem:
    """
    Sistema principal para recomendação de rotas de ecoturismo sustentável.
    
    Esta classe orquestra todos os componentes do sistema:
    - Carregamento e processamento de dados
    - Geração de rotas otimizadas
    - Sistema de ML para personalização
    - Criação de visualizações e relatórios
    
    Atributos:
        config: Configurações do sistema
        data_processor: Processador de dados
        route_optimizer: Otimizador de rotas
        ml_engine: Motor de ML (opcional)
        geo_calc: Calculadora geográfica
        formatter: Formatador de dados
        df: DataFrame principal com dados processados
        recommended_routes: Lista de rotas recomendadas
    """
    
    def __init__(self, config=None, use_ml: bool = True):
        """
        Inicializa o sistema de ecoturismo.
        
        Args:
            config: Instância de configuração. Se None, usa configuração global.
            use_ml: Se deve usar sistema de ML para recomendações personalizadas.
            
        Example:
            >>> # Sistema básico
            >>> sistema = EcoTurismoSystem(use_ml=False)
            >>> 
            >>> # Sistema com ML
            >>> sistema = EcoTurismoSystem(use_ml=True)
        """
        self.config = config or get_config()
        self.use_ml = use_ml
        
        # Inicializar componentes
        self.data_processor = DataProcessor(self.config)
        self.route_optimizer = RouteOptimizer(self.config)
        self.geo_calc = GeographicCalculator(self.config.data.luanda_coords)
        self.formatter = DataFormatter(self.config)
        
        # Sistema de ML (opcional)
        self.ml_engine = None
        if self.use_ml:
            self.ml_engine = MLRecommendationEngine(self.config)
            logger.info("Sistema de ML habilitado")
        
        # Estado do sistema
        self.df: Optional[pd.DataFrame] = None
        self.recommended_routes: List[Dict[str, Any]] = []
        self.map_base: Optional[folium.Map] = None
        
        logger.info("EcoTurismoSystem inicializado")
    
    def load_data(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """
        Carrega e processa dados dos locais de ecoturismo.
        
        Este método executa o pipeline completo de carregamento:
        1. Carregamento do arquivo CSV
        2. Validação de dados
        3. Limpeza e normalização
        4. Criação de features derivadas
        5. Otimização de tipos de dados
        
        Args:
            file_path: Caminho para o arquivo CSV. Se None, usa configuração padrão.
        
        Returns:
            DataFrame com os dados processados
            
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            ValueError: Se os dados não passarem na validação
            Exception: Para outros erros de processamento
            
        Example:
            >>> sistema = EcoTurismoSystem()
            >>> df = sistema.load_data()
            >>> print(f"Dados carregados: {len(df)} locais")
        """
        try:
            logger.info("Iniciando carregamento de dados...")
            
            # Carregar dados usando o processador
            self.df = self.data_processor.load_data(file_path)
            
            # Inicializar ML engine se habilitado
            if self.use_ml and self.ml_engine:
                self.ml_engine.load_data()
                logger.info("Dados carregados no motor de ML")
            
            # Log de estatísticas
            stats = self.data_processor.get_statistics()
            logger.info(f"Dados carregados: {stats['total_locations']} locais, "
                       f"{stats['provinces']} províncias, {stats['ecosystems']} ecossistemas")
            
            return self.df
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def generate_traditional_routes(self, 
                                  max_budget: float = None,
                                  max_locations: int = None,
                                  max_fragility: int = None,
                                  num_routes: int = None) -> List[Dict[str, Any]]:
        """
        Gera rotas recomendadas usando algoritmo tradicional.
        
        Este método implementa o algoritmo original de recomendação:
        1. Filtragem por critérios de sustentabilidade
        2. Clustering geográfico de locais
        3. Otimização de rotas com algoritmo do vizinho mais próximo
        4. Cálculo de scores de sustentabilidade
        5. Seleção das melhores rotas
        
        Args:
            max_budget: Orçamento máximo em AOA. Se None, usa configuração padrão.
            max_locations: Número máximo de locais por rota. Se None, usa configuração.
            max_fragility: Fragilidade máxima permitida. Se None, usa configuração.
            num_routes: Número de rotas a gerar. Se None, usa configuração.
            
        Returns:
            Lista de dicionários com informações das rotas recomendadas
            
        Example:
            >>> sistema = EcoTurismoSystem()
            >>> sistema.load_data()
            >>> rotas = sistema.generate_traditional_routes(
            ...     max_budget=25000,
            ...     max_locations=5,
            ...     num_routes=3
            ... )
            >>> print(f"Geradas {len(rotas)} rotas")
        """
        try:
            if self.df is None:
                raise ValueError("Dados não carregados. Execute load_data() primeiro.")
            
            # Usar valores padrão se não especificados
            max_budget = max_budget or self.config.route.default_max_budget
            max_locations = max_locations or self.config.route.default_max_locations
            max_fragility = max_fragility or self.config.route.default_max_fragility
            num_routes = num_routes or self.config.route.default_num_routes
            
            logger.info(f"Gerando rotas tradicionais: orçamento={max_budget}, "
                       f"locais={max_locations}, fragilidade={max_fragility}, rotas={num_routes}")
            
            # Filtrar locais sustentáveis
            sustainable_df = self.data_processor.get_sustainable_locations(max_fragility)
            if sustainable_df.empty:
                logger.warning("Nenhum local sustentável encontrado")
                return []
            
            # Filtrar por orçamento
            budget_df = self.data_processor.get_locations_by_budget(max_budget)
            if budget_df.empty:
                logger.warning("Nenhum local dentro do orçamento encontrado")
                return []
            
            # Intersecção dos filtros
            filtered_df = pd.merge(sustainable_df, budget_df, how='inner')
            if filtered_df.empty:
                logger.warning("Nenhum local atende aos critérios combinados")
                return []
            
            logger.info(f"Locais filtrados: {len(filtered_df)}")
            
            # Gerar rotas usando o otimizador
            routes = self.route_optimizer.generate_routes(
                df=filtered_df,
                max_locations=max_locations,
                num_routes=num_routes,
                max_budget=max_budget
            )
            
            # Armazenar rotas recomendadas
            self.recommended_routes = routes
            
            logger.info(f"Rotas tradicionais geradas: {len(routes)}")
            return routes
            
        except Exception as e:
            logger.error(f"Erro ao gerar rotas tradicionais: {e}")
            raise
    
    def generate_ml_routes(self, 
                          user_profile: Dict[str, Any],
                          max_budget: float = None,
                          max_locations: int = None,
                          num_routes: int = None) -> List[Dict[str, Any]]:
        """
        Gera rotas personalizadas usando Machine Learning.
        
        Este método utiliza o sistema de ML para personalizar recomendações:
        1. Validação do perfil do usuário
        2. Treinamento do modelo (se necessário)
        3. Previsão de ratings para locais
        4. Geração de rotas personalizadas
        5. Otimização baseada em preferências
        
        Args:
            user_profile: Dicionário com perfil do usuário
            max_budget: Orçamento máximo em AOA. Se None, usa perfil do usuário.
            max_locations: Número máximo de locais por rota. Se None, usa configuração.
            num_routes: Número de rotas a gerar. Se None, usa configuração.
            
        Returns:
            Lista de dicionários com rotas personalizadas
            
        Raises:
            ValueError: Se sistema de ML não estiver habilitado
            ValueError: Se perfil do usuário for inválido
            
        Example:
            >>> user_profile = {
            ...     'idade': 30,
            ...     'orcamento_max': 20000,
            ...     'preferencia_sustentabilidade': 0.8,
            ...     'preferencia_aventura': 0.6,
            ...     'preferencia_cultura': 0.7
            ... }
            >>> rotas = sistema.generate_ml_routes(user_profile)
        """
        try:
        if not self.use_ml or not self.ml_engine:
                raise ValueError("Sistema de ML não habilitado. Use use_ml=True na inicialização.")
        
        if self.df is None:
                raise ValueError("Dados não carregados. Execute load_data() primeiro.")
            
            # Validar perfil do usuário
            from ..utils.validators import validate_user_profile
            if not validate_user_profile(user_profile):
                raise ValueError("Perfil do usuário inválido")
            
            # Usar valores do perfil se não especificados
            max_budget = max_budget or user_profile.get('orcamento_max', self.config.route.default_max_budget)
            max_locations = max_locations or self.config.route.default_max_locations
            num_routes = num_routes or self.config.route.default_num_routes
            
            logger.info(f"Gerando rotas ML: perfil={user_profile['idade']} anos, "
                       f"orçamento={max_budget}, locais={max_locations}")
        
        # Treinar modelo se necessário
        if self.ml_engine.rating_model is None:
                logger.info("Treinando modelo de ML...")
                self._train_ml_model()
        
        # Gerar rotas personalizadas
            routes = self.ml_engine.generate_personalized_routes(
            user_profile=user_profile,
                max_budget=max_budget,
                max_locations=max_locations,
                num_routes=num_routes
            )
            
            # Armazenar rotas recomendadas
            self.recommended_routes = routes
            
            logger.info(f"Rotas ML geradas: {len(routes)}")
            return routes
            
        except Exception as e:
            logger.error(f"Erro ao gerar rotas ML: {e}")
            raise
    
    def _train_ml_model(self) -> None:
        """
        Treina o modelo de ML se necessário.
        
        Este método privado executa o treinamento completo:
        1. Criação de features engenheiradas
        2. Geração de dados sintéticos de usuários
        3. Treinamento do modelo de rating
        4. Criação de clusters de locais
        """
        try:
            logger.info("Iniciando treinamento do modelo ML...")
            
            # Criar features
            df_features = self.ml_engine.create_features_engineering()
            
            # Criar dados sintéticos
            df_users = self.ml_engine.create_synthetic_users(
                n_users=self.config.ml.synthetic_users
            )
            
            # Treinar modelo
            metrics = self.ml_engine.train_rating_model(df_users)
            logger.info(f"Modelo treinado - R²: {metrics['r2_score']:.3f}")
            
            # Criar clusters
            cluster_info = self.ml_engine.create_location_clusters(df_features)
            logger.info(f"Clusters criados: {len(cluster_info)}")
            
            # Salvar modelos se configurado
            if self.config.ml.save_models:
                self.ml_engine.save_models()
            
        except Exception as e:
            logger.error(f"Erro no treinamento do modelo ML: {e}")
            raise
    
    def create_interactive_map(self, save_html: bool = True) -> folium.Map:
        """
        Cria mapa interativo com as rotas recomendadas.
        
        Este método gera um mapa Folium com:
        - Marcadores para cada local (coloridos por fragilidade)
        - Linhas de rota otimizadas
        - Popups informativos
        - Legenda de fragilidade
        - Controles interativos
        
        Args:
            save_html: Se deve salvar o mapa como arquivo HTML
            
        Returns:
            Mapa Folium interativo
            
        Raises:
            ValueError: Se não há rotas recomendadas
        """
        try:
            if not self.recommended_routes:
                raise ValueError("Nenhuma rota recomendada. Execute generate_traditional_routes() ou generate_ml_routes() primeiro.")
            
            logger.info("Criando mapa interativo...")
        
        # Criar mapa base
            self.map_base = folium.Map(
                location=self.config.ui.map_center,
                zoom_start=self.config.ui.default_zoom,
                tiles=self.config.ui.map_tiles
            )
        
        # Adicionar cada rota ao mapa
            colors = self.config.ui.color_palette
            
            for idx, route in enumerate(self.recommended_routes):
                color = colors[idx % len(colors)]
                
                # Adicionar marcadores para cada local
                self._add_location_markers(route['locais'])
                
                # Adicionar linha da rota
                self._add_route_line(route, color)
            
            # Adicionar legenda
            self._add_legend()
            
            # Salvar mapa se solicitado
            if save_html:
                filename = f"mapa_ecoturismo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                output_path = self.config.get_output_path(filename)
                self.map_base.save(str(output_path))
                logger.info(f"Mapa salvo em: {output_path}")
            
            return self.map_base
            
        except Exception as e:
            logger.error(f"Erro ao criar mapa interativo: {e}")
            raise
    
    def _add_location_markers(self, locations: List[Dict[str, Any]]) -> None:
        """
        Adiciona marcadores de locais ao mapa.
        
        Args:
            locations: Lista de dicionários com dados dos locais
        """
        for location in locations:
            # Determinar cor do ícone baseado na fragilidade
            fragility = location['fragilidade']
            if fragility <= 2:
                icon_color = 'green'
            elif fragility == 3:
                icon_color = 'orange'
            else:
                icon_color = 'red'
            
            # Criar popup com informações
            popup_text = self.formatter.format_location_popup(location)
            
            # Adicionar marcador
            folium.Marker(
                [location['latitude'], location['longitude']],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"{location['nome']} (Fragilidade: {fragility})",
                icon=folium.Icon(color=icon_color, icon='leaf', prefix='fa')
            ).add_to(self.map_base)
    
    def _add_route_line(self, route: Dict[str, Any], color: str) -> None:
        """
        Adiciona linha de rota ao mapa.
        
        Args:
            route: Dicionário com dados da rota
            color: Cor da linha
        """
        coordinates = [[loc['latitude'], loc['longitude']] for loc in route['locais']]
        
        popup_text = self.formatter.format_route_popup(route)
        
            folium.PolyLine(
            coordinates,
            color=color,
                weight=3,
                opacity=0.8,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(self.map_base)
    
    def _add_legend(self) -> None:
        """
        Adiciona legenda de fragilidade ao mapa.
        """
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p><b>Legenda:</b></p>
        <p><i class="fa fa-leaf" style="color:green"></i> Fragilidade 1-2 (Baixa)</p>
        <p><i class="fa fa-leaf" style="color:orange"></i> Fragilidade 3 (Média)</p>
        <p><i class="fa fa-leaf" style="color:red"></i> Fragilidade 4 (Alta)</p>
        </div>
        """
        self.map_base.get_root().html.add_child(folium.Element(legend_html))
    
    def generate_csv_report(self, filename: str = None) -> Path:
        """
        Gera relatório CSV com resumo das rotas recomendadas.
        
        Args:
            filename: Nome do arquivo. Se None, usa timestamp.
            
        Returns:
            Caminho do arquivo gerado
        """
        try:
            if not self.recommended_routes:
                raise ValueError("Nenhuma rota recomendada disponível.")
            
            logger.info("Gerando relatório CSV...")
        
        # Preparar dados para CSV
            report_data = []
            for route in self.recommended_routes:
                report_data.append(self.formatter.format_route_for_csv(route))
        
        # Criar DataFrame e salvar
            df_report = pd.DataFrame(report_data)
            
            if filename is None:
                filename = f"relatorio_rotas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
            output_path = self.config.get_output_path(filename)
            df_report.to_csv(output_path, index=False, encoding='utf-8')
        
            logger.info(f"Relatório CSV salvo em: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Erro ao gerar relatório CSV: {e}")
            raise
    
    def generate_json_report(self, filename: str = None) -> Path:
        """
        Gera relatório JSON detalhado com todas as rotas.
        
        Args:
            filename: Nome do arquivo. Se None, usa timestamp.
            
        Returns:
            Caminho do arquivo gerado
        """
        try:
            if not self.recommended_routes:
                raise ValueError("Nenhuma rota recomendada disponível.")
            
            logger.info("Gerando relatório JSON...")
            
            if filename is None:
                filename = f"relatorio_detalhado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            output_path = self.config.get_output_path(filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.recommended_routes, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Relatório JSON salvo em: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório JSON: {e}")
            raise
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do sistema.
        
        Returns:
            Dicionário com estatísticas completas
        """
        try:
            stats = {
                'data_loaded': self.df is not None,
                'ml_enabled': self.use_ml,
                'routes_generated': len(self.recommended_routes),
                'map_created': self.map_base is not None
            }
            
            if self.df is not None:
                data_stats = self.data_processor.get_statistics()
                stats.update(data_stats)
            
            if self.ml_engine and hasattr(self.ml_engine, 'rating_model') and self.ml_engine.rating_model:
                stats['ml_model_trained'] = True
                if hasattr(self.ml_engine, 'feature_importance'):
                    stats['ml_features'] = len(self.ml_engine.feature_importance.get('rating', {}))
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def print_route_summary(self) -> None:
        """
        Imprime resumo das rotas recomendadas no console.
        """
        try:
            if not self.recommended_routes:
            print("❌ Nenhuma rota recomendada disponível.")
            return
        
        print("\n" + "="*80)
        print("🌍 RESUMO DAS ROTAS DE ECOTURISMO RECOMENDADAS - ANGOLA")
        print("="*80)
        
            for i, route in enumerate(self.recommended_routes, 1):
                print(f"\n📍 ROTA {i}: {route['nome']}")
                print(f"   🏃 Distância Total: {route['distancia_total_km']} km")
                print(f"   💰 Custo Total: {route['custo_total_aoa']:,} AOA")
                print(f"   🌱 Fragilidade Média: {route['fragilidade_media']}/5")
                
                if 'score' in route:
                    print(f"   ⭐ Score: {route['score']}")
                elif 'rating_medio_previsto' in route:
                    print(f"   ⭐ Rating ML: {route['rating_medio_previsto']}")
                
                print(f"   🗺️  Províncias: {', '.join(route.get('provincias', []))}")
                print(f"   🌿 Ecossistemas: {', '.join(route.get('tipos_ecosistema', []))}")
                print(f"   📍 Locais ({route['num_locais']}):")
                
                for j, local in enumerate(route['locais'], 1):
                print(f"      {j}. {local['nome']} ({local['provincia']}) - {local['taxa_aoa']:,} AOA")
        
        print("\n" + "="*80)
        print("💡 Dica: Abra o arquivo HTML gerado para visualizar as rotas no mapa interativo!")
        print("="*80)

        except Exception as e:
            logger.error(f"Erro ao imprimir resumo: {e}")


if __name__ == "__main__":
    """Teste do sistema principal."""
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Teste básico
    sistema = EcoTurismoSystem(use_ml=False)
    
    try:
    # Carregar dados
        df = sistema.load_data()
        print(f"✅ Dados carregados: {len(df)} locais")
        
        # Gerar rotas tradicionais
        rotas = sistema.generate_traditional_routes(
            max_budget=20000,
            max_locations=5,
            num_routes=3
        )
        print(f"✅ Rotas geradas: {len(rotas)}")
        
        # Criar mapa
        mapa = sistema.criar_mapa_interativo()
        print("✅ Mapa criado")
    
    # Gerar relatórios
        csv_file = sistema.generate_csv_report()
        json_file = sistema.generate_json_report()
        print(f"✅ Relatórios gerados: {csv_file.name}, {json_file.name}")
    
    # Imprimir resumo
        sistema.print_route_summary()
        
        print("✅ Teste do sistema concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")