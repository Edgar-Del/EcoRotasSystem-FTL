#!/usr/bin/env python3
"""
Otimizador de Rotas para EcoRota Angola
======================================

Este módulo contém a classe RouteOptimizer responsável por:
- Geração de rotas otimizadas
- Algoritmos de clustering geográfico
- Otimização com algoritmo do vizinho mais próximo
- Cálculo de scores de sustentabilidade
- Seleção das melhores rotas

Autor: Sistema EcoRota Angola
Data: 2024
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
from sklearn.cluster import KMeans
import logging

from ..utils.geographic import GeographicCalculator
from ..utils.validators import DataValidator

logger = logging.getLogger(__name__)


class RouteOptimizer:
    """
    Classe para otimização de rotas de ecoturismo.
    
    Esta classe implementa algoritmos de otimização para gerar rotas
    que equilibram sustentabilidade, custo e experiência do usuário.
    
    Algoritmos implementados:
    - Clustering geográfico (K-Means)
    - Algoritmo do vizinho mais próximo
    - Score de sustentabilidade ponderado
    - Seleção de rotas por critérios múltiplos
    """
    
    def __init__(self, config):
        """
        Inicializa o otimizador de rotas.
        
        Args:
            config: Instância de configuração do sistema
        """
        self.config = config
        self.geo_calc = GeographicCalculator(config.data.luanda_coords)
        self.validator = DataValidator(config)
        
        logger.info("RouteOptimizer inicializado")
    
    def generate_routes(self, 
                       df: pd.DataFrame,
                       max_locations: int = None,
                       num_routes: int = None,
                       max_budget: float = None) -> List[Dict[str, Any]]:
        """
        Gera rotas otimizadas baseadas nos critérios especificados.
        
        Este método implementa o pipeline completo de otimização:
        1. Clustering geográfico de locais
        2. Geração de rotas por cluster
        3. Otimização com algoritmo do vizinho mais próximo
        4. Cálculo de scores de sustentabilidade
        5. Seleção das melhores rotas
        
        Args:
            df: DataFrame com locais filtrados
            max_locations: Número máximo de locais por rota
            num_routes: Número de rotas a gerar
            max_budget: Orçamento máximo por rota
            
        Returns:
            Lista de dicionários com rotas otimizadas
            
        Example:
            >>> optimizer = RouteOptimizer(config)
            >>> routes = optimizer.generate_routes(
            ...     df=filtered_df,
            ...     max_locations=5,
            ...     num_routes=3,
            ...     max_budget=20000
            ... )
        """
        try:
            # Usar valores padrão se não especificados
            max_locations = max_locations or self.config.route.default_max_locations
            num_routes = num_routes or self.config.route.default_num_routes
            max_budget = max_budget or self.config.route.default_max_budget
            
            logger.info(f"Gerando rotas: max_locations={max_locations}, "
                       f"num_routes={num_routes}, max_budget={max_budget}")
            
            if df.empty:
                logger.warning("DataFrame vazio - nenhuma rota pode ser gerada")
                return []
            
            # Criar clusters geográficos
            df_clustered = self._create_geographic_clusters(df)
            
            # Gerar rotas por cluster
            all_routes = []
            for cluster_id in df_clustered['cluster'].unique():
                cluster_df = df_clustered[df_clustered['cluster'] == cluster_id]
                cluster_routes = self._generate_cluster_routes(
                    cluster_df, max_locations, max_budget
                )
                all_routes.extend(cluster_routes)
            
            # Calcular scores e ordenar
            scored_routes = self._calculate_route_scores(all_routes)
            
            # Selecionar melhores rotas
            best_routes = self._select_best_routes(scored_routes, num_routes)
            
            logger.info(f"Rotas geradas: {len(best_routes)}")
            return best_routes
            
        except Exception as e:
            logger.error(f"Erro ao gerar rotas: {e}")
            raise
    
    def _create_geographic_clusters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria clusters geográficos usando K-Means.
        
        Args:
            df: DataFrame com locais
            
        Returns:
            DataFrame com coluna de cluster adicionada
        """
        try:
            logger.debug("Criando clusters geográficos...")
            
            # Determinar número de clusters
            n_clusters = min(
                self.config.route.route_clustering and self.config.ml.clustering_params.get('n_clusters', 6) or 1,
                len(df) // 2,  # Pelo menos 2 locais por cluster
                len(df)  # Não mais clusters que locais
            )
            
            if n_clusters < 2:
                # Se poucos locais, não usar clustering
                df['cluster'] = 0
                return df
            
            # Features para clustering
            features = ['latitude', 'longitude', 'fragilidade', 'capacidade_diaria', 'taxa_aoa']
            if 'sustentabilidade_score' in df.columns:
                features.append('sustentabilidade_score')
            if 'atratividade_score' in df.columns:
                features.append('atratividade_score')
            
            # Preparar dados para clustering
            X = df[features].values
            
            # Normalizar features
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Aplicar K-Means
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=self.config.ml.clustering_params.get('random_state', 42),
                n_init=self.config.ml.clustering_params.get('n_init', 10)
            )
            
            clusters = kmeans.fit_predict(X_scaled)
            df['cluster'] = clusters
            
            logger.debug(f"Clusters criados: {n_clusters}, distribuição: {np.bincount(clusters)}")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao criar clusters: {e}")
            # Fallback: sem clustering
            df['cluster'] = 0
            return df
    
    def _generate_cluster_routes(self, 
                                cluster_df: pd.DataFrame,
                                max_locations: int,
                                max_budget: float) -> List[Dict[str, Any]]:
        """
        Gera rotas para um cluster específico.
        
        Args:
            cluster_df: DataFrame com locais do cluster
            max_locations: Número máximo de locais por rota
            max_budget: Orçamento máximo por rota
            
        Returns:
            Lista de rotas do cluster
        """
        try:
            routes = []
            cluster_size = len(cluster_df)
            
            # Se cluster pequeno, gerar uma rota com todos os locais
            if cluster_size <= max_locations:
                route = self._create_route_from_locations(
                    cluster_df, max_budget
                )
                if route:
                    routes.append(route)
            else:
                # Gerar múltiplas rotas com subconjuntos
                for _ in range(min(3, cluster_size // 2)):  # Máximo 3 tentativas
                    # Selecionar locais aleatórios
                    selected_locations = cluster_df.sample(
                        n=min(max_locations, cluster_size),
                        random_state=np.random.randint(1000)
                    )
                    
                    route = self._create_route_from_locations(
                        selected_locations, max_budget
                    )
                    if route:
                        routes.append(route)
            
            return routes
            
        except Exception as e:
            logger.error(f"Erro ao gerar rotas do cluster: {e}")
            return []
    
    def _create_route_from_locations(self, 
                                   locations_df: pd.DataFrame,
                                   max_budget: float) -> Optional[Dict[str, Any]]:
        """
        Cria uma rota a partir de um conjunto de locais.
        
        Args:
            locations_df: DataFrame com locais selecionados
            max_budget: Orçamento máximo
            
        Returns:
            Dicionário com dados da rota ou None se inválida
        """
        try:
            # Verificar orçamento
            total_cost = locations_df['taxa_aoa'].sum()
            if total_cost > max_budget:
                return None
            
            # Converter para lista de dicionários
            locations_list = locations_df.to_dict('records')
            
            # Otimizar ordem da rota
            optimized_indices = self.geo_calc.nearest_neighbor_route(
                [(loc['latitude'], loc['longitude']) for loc in locations_list]
            )
            
            # Reordenar locais
            optimized_locations = [locations_list[i] for i in optimized_indices]
            
            # Calcular métricas da rota
            total_distance = self.geo_calc.calculate_route_distance(
                [(loc['latitude'], loc['longitude']) for loc in optimized_locations],
                list(range(len(optimized_locations)))
            )
            
            avg_fragility = np.mean([loc['fragilidade'] for loc in optimized_locations])
            
            # Criar dados da rota
            route_data = {
                'nome': f"Rota Cluster {locations_df['cluster'].iloc[0] + 1} - {len(optimized_locations)} locais",
                'locais': optimized_locations,
                'num_locais': len(optimized_locations),
                'distancia_total_km': round(total_distance, 2),
                'custo_total_aoa': total_cost,
                'fragilidade_media': round(avg_fragility, 2),
                'provincias': list(set([loc['provincia'] for loc in optimized_locations])),
                'tipos_ecosistema': list(set([loc['tipo_ecosistema'] for loc in optimized_locations]))
            }
            
            return route_data
            
        except Exception as e:
            logger.error(f"Erro ao criar rota: {e}")
            return None
    
    def _calculate_route_scores(self, routes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calcula scores de sustentabilidade para todas as rotas.
        
        Args:
            routes: Lista de rotas
            
        Returns:
            Lista de rotas com scores calculados
        """
        try:
            logger.debug("Calculando scores das rotas...")
            
            scored_routes = []
            weights = self.config.route.score_weights
            
            for route in routes:
                # Calcular score de sustentabilidade
                score = (
                    weights['fragilidade'] * route['fragilidade_media'] +
                    weights['distancia'] * (route['distancia_total_km'] / 1000) +
                    weights['custo'] * (route['custo_total_aoa'] / 100000)
                )
                
                route['score'] = round(score, 3)
                scored_routes.append(route)
            
            logger.debug(f"Scores calculados para {len(scored_routes)} rotas")
            return scored_routes
            
        except Exception as e:
            logger.error(f"Erro ao calcular scores: {e}")
            return routes
    
    def _select_best_routes(self, 
                           scored_routes: List[Dict[str, Any]],
                           num_routes: int) -> List[Dict[str, Any]]:
        """
        Seleciona as melhores rotas baseado nos scores.
        
        Args:
            scored_routes: Lista de rotas com scores
            num_routes: Número de rotas a selecionar
            
        Returns:
            Lista das melhores rotas
        """
        try:
            if not scored_routes:
                return []
            
            # Ordenar por score (menor é melhor)
            sorted_routes = sorted(scored_routes, key=lambda x: x['score'])
            
            # Selecionar top rotas
            best_routes = sorted_routes[:num_routes]
            
            # Validar rotas selecionadas
            validated_routes = []
            for route in best_routes:
                if self.validator.validate_route_data(route['locais']):
                    validated_routes.append(route)
                else:
                    logger.warning(f"Rota inválida removida: {route['nome']}")
            
            logger.info(f"Melhores rotas selecionadas: {len(validated_routes)}")
            return validated_routes
            
        except Exception as e:
            logger.error(f"Erro ao selecionar melhores rotas: {e}")
            return scored_routes[:num_routes] if scored_routes else []
    
    def optimize_existing_route(self, 
                               locations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Otimiza uma rota existente usando algoritmo do vizinho mais próximo.
        
        Args:
            locations: Lista de locais da rota
            
        Returns:
            Lista de locais otimizada
        """
        try:
            if len(locations) <= 1:
                return locations
            
            # Extrair coordenadas
            coordinates = [(loc['latitude'], loc['longitude']) for loc in locations]
            
            # Otimizar ordem
            optimized_indices = self.geo_calc.nearest_neighbor_route(coordinates)
            
            # Reordenar locais
            optimized_locations = [locations[i] for i in optimized_indices]
            
            logger.debug(f"Rota otimizada: {len(locations)} locais")
            return optimized_locations
            
        except Exception as e:
            logger.error(f"Erro ao otimizar rota: {e}")
            return locations
    
    def calculate_route_metrics(self, route: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula métricas detalhadas de uma rota.
        
        Args:
            route: Dicionário com dados da rota
            
        Returns:
            Dicionário com métricas calculadas
        """
        try:
            locations = route.get('locais', [])
            if not locations:
                return {}
            
            # Métricas básicas
            metrics = {
                'total_locations': len(locations),
                'total_distance_km': route.get('distancia_total_km', 0),
                'total_cost_aoa': route.get('custo_total_aoa', 0),
                'avg_fragility': route.get('fragilidade_media', 0),
                'provinces_visited': len(route.get('provincias', [])),
                'ecosystems_visited': len(route.get('tipos_ecosistema', []))
            }
            
            # Métricas derivadas
            if metrics['total_locations'] > 0:
                metrics['avg_cost_per_location'] = metrics['total_cost_aoa'] / metrics['total_locations']
                metrics['avg_distance_per_location'] = metrics['total_distance_km'] / metrics['total_locations']
            
            # Score de diversidade
            diversity_score = (
                metrics['provinces_visited'] * 0.4 +
                metrics['ecosystems_visited'] * 0.6
            )
            metrics['diversity_score'] = round(diversity_score, 2)
            
            # Score de sustentabilidade
            sustainability_score = 5 - metrics['avg_fragility']  # Inversão
            metrics['sustainability_score'] = round(sustainability_score, 2)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas da rota: {e}")
            return {}
    
    def get_route_recommendations(self, 
                                 user_preferences: Dict[str, Any],
                                 available_routes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recomenda rotas baseado nas preferências do usuário.
        
        Args:
            user_preferences: Dicionário com preferências do usuário
            available_routes: Lista de rotas disponíveis
            
        Returns:
            Lista de rotas recomendadas ordenadas por relevância
        """
        try:
            if not available_routes:
                return []
            
            # Calcular scores de relevância
            scored_routes = []
            for route in available_routes:
                relevance_score = self._calculate_relevance_score(
                    route, user_preferences
                )
                route['relevance_score'] = relevance_score
                scored_routes.append(route)
            
            # Ordenar por relevância
            recommended_routes = sorted(
                scored_routes, 
                key=lambda x: x['relevance_score'], 
                reverse=True
            )
            
            logger.info(f"Rotas recomendadas: {len(recommended_routes)}")
            return recommended_routes
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações: {e}")
            return available_routes
    
    def _calculate_relevance_score(self, 
                                  route: Dict[str, Any],
                                  preferences: Dict[str, Any]) -> float:
        """
        Calcula score de relevância de uma rota para o usuário.
        
        Args:
            route: Dados da rota
            preferences: Preferências do usuário
            
        Returns:
            Score de relevância (0-1)
        """
        try:
            score = 0.0
            
            # Preferência por sustentabilidade
            if 'preferencia_sustentabilidade' in preferences:
                sustainability_weight = preferences['preferencia_sustentabilidade']
                sustainability_score = (5 - route['fragilidade_media']) / 5
                score += sustainability_weight * sustainability_score * 0.3
            
            # Preferência por orçamento
            if 'orcamento_max' in preferences:
                budget_ratio = min(1.0, preferences['orcamento_max'] / route['custo_total_aoa'])
                score += budget_ratio * 0.2
            
            # Preferência por diversidade
            diversity_score = (
                len(route.get('provincias', [])) * 0.1 +
                len(route.get('tipos_ecosistema', [])) * 0.1
            )
            score += min(1.0, diversity_score / 5) * 0.2
            
            # Score original da rota
            if 'score' in route:
                original_score = max(0, 1 - route['score'] / 10)  # Normalizar
                score += original_score * 0.3
            
            return min(1.0, score)
            
        except Exception as e:
            logger.error(f"Erro ao calcular score de relevância: {e}")
            return 0.5


if __name__ == "__main__":
    """Teste do otimizador de rotas."""
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Teste básico
    from config.settings import get_config
    config = get_config()
    optimizer = RouteOptimizer(config)
    
    print("🧪 Testando otimizador de rotas...")
    
    # Dados de teste
    test_data = {
        'nome': ['Parque Nacional da Kissama', 'Cascatas de Kalandula', 'Parque Nacional de Iona'],
        'provincia': ['Luanda', 'Malange', 'Namibe'],
        'latitude': [-8.7500, -9.0833, -16.7500],
        'longitude': [13.2500, 16.0167, 12.2500],
        'fragilidade': [3, 2, 4],
        'capacidade_diaria': [150, 200, 100],
        'taxa_aoa': [25000, 15000, 30000],
        'tipo_ecosistema': ['savana', 'floresta', 'deserto'],
        'descricao': ['Reserva natural', 'Cachoeiras', 'Deserto costeiro']
    }
    
    df = pd.DataFrame(test_data)
    
    # Teste de geração de rotas
    routes = optimizer.generate_routes(
        df=df,
        max_locations=3,
        num_routes=2,
        max_budget=50000
    )
    
    print(f"✅ Rotas geradas: {len(routes)}")
    
    for i, route in enumerate(routes, 1):
        print(f"   Rota {i}: {route['nome']}")
        print(f"   Distância: {route['distancia_total_km']} km")
        print(f"   Custo: {route['custo_total_aoa']} AOA")
        print(f"   Score: {route['score']}")
    
    # Teste de otimização
    if routes:
        optimized = optimizer.optimize_existing_route(routes[0]['locais'])
        print(f"✅ Rota otimizada: {len(optimized)} locais")
    
    # Teste de métricas
    if routes:
        metrics = optimizer.calculate_route_metrics(routes[0])
        print(f"✅ Métricas calculadas: {len(metrics)} campos")
    
    print("✅ Testes do otimizador concluídos!")
