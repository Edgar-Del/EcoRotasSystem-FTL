#!/usr/bin/env python3
"""
Sistema de Machine Learning para Recomendação de Rotas de Ecoturismo
===================================================================

Este módulo implementa algoritmos de ML para personalizar recomendações
de rotas de ecoturismo baseado em:
- Preferências do usuário
- Padrões históricos
- Características dos locais
- Feedback de usuários similares

Autor: Equipa 01 - UNDP FTL
Data: 2025
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import joblib
import json
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class MLRecommendationEngine:
    """Motor de recomendação baseado em Machine Learning."""
    
    def __init__(self, csv_file: str = "locais_ecoturismo_angola.csv"):
        """
        Inicializa o motor de ML.
        
        Args:
            csv_file: Caminho para o arquivo CSV com dados dos locais
        """
        # Permitir passar Config ou caminho string
        try:
            from config.settings import Config
        except Exception:
            Config = None  # type: ignore

        if Config is not None and isinstance(csv_file, Config):
            # Recebemos a Config do sistema
            self.config = csv_file
            self.csv_file = str(self.config.get_data_path())
        else:
            self.config = None
            self.csv_file = csv_file
        self.df = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.models = {}
        self.user_profiles = {}
        self.feature_importance = {}
        
        # Modelos de ML
        self.rating_model = None
        self.clustering_model = None
        self.recommendation_model = None
        
    def carregar_dados(self) -> pd.DataFrame:
        """Carrega e prepara os dados para ML."""
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"Dados carregados para ML: {len(self.df)} locais")
            return self.df
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None
    
    def criar_features_engenharia(self) -> pd.DataFrame:
        """
        Cria features para o modelo de ML.
        
        Returns:
            DataFrame com features
        """
        if self.df is None:
            print("Dados não carregados.")
            return None
        
        df_features = self.df.copy()
        
        # 1. Features geográficas
        df_features['distancia_luanda'] = df_features.apply(
            lambda row: self._calcular_distancia_luanda(row['latitude'], row['longitude']), axis=1
        )
        
        # 2. Features de sustentabilidade
        df_features['sustentabilidade_score'] = 5 - df_features['fragilidade']  # Inverter escala
        df_features['capacidade_relativa'] = df_features['capacidade_diaria'] / df_features['capacidade_diaria'].max()
        df_features['custo_relativo'] = df_features['taxa_aoa'] / df_features['taxa_aoa'].max()
        
        # 3. Features categóricas codificadas
        le_provincia = LabelEncoder()
        le_ecosistema = LabelEncoder()
        
        df_features['provincia_encoded'] = le_provincia.fit_transform(df_features['provincia'])
        df_features['ecosistema_encoded'] = le_ecosistema.fit_transform(df_features['tipo_ecosistema'])
        
        # Salvar encoders
        self.label_encoders['provincia'] = le_provincia
        self.label_encoders['ecosistema'] = le_ecosistema
        
        # 4. Features de popularidade (simuladas)
        np.random.seed(42)
        df_features['popularidade'] = np.random.normal(0.5, 0.2, len(df_features))
        df_features['popularidade'] = np.clip(df_features['popularidade'], 0, 1)
        
        # 5. Features de acessibilidade
        df_features['acessibilidade'] = 1 - (df_features['distancia_luanda'] / df_features['distancia_luanda'].max())
        
        # 6. Score composto de atratividade
        df_features['atratividade_score'] = (
            0.3 * df_features['sustentabilidade_score'] +
            0.2 * df_features['capacidade_relativa'] +
            0.2 * df_features['popularidade'] +
            0.2 * df_features['acessibilidade'] +
            0.1 * (1 - df_features['custo_relativo'])
        )
        
        print(f"Features criadas: {df_features.shape[1]} colunas")
        return df_features
    
    # ---- Aliases para compatibilidade com o orquestrador ----
    def load_data(self) -> pd.DataFrame:
        """Alias de carregar_dados para compatibilidade."""
        return self.carregar_dados()

    def generate_personalized_routes(self, user_profile: Dict,
                                     max_budget: float = 20000,
                                     max_locations: int = 6,
                                     num_routes: int = 5) -> List[Dict]:
        """Alias de gerar_rotas_personalizadas para compatibilidade."""
        return self.gerar_rotas_personalizadas(
            user_profile=user_profile,
            orcamento_max=max_budget,
            max_locais=max_locations,
            n_rotas=num_routes
        )

    def create_features_engineering(self) -> pd.DataFrame:
        """Alias de criar_features_engenharia para compatibilidade."""
        return self.criar_features_engenharia()

    def create_synthetic_users(self, n_users: int = 1000) -> pd.DataFrame:
        """Alias de criar_dados_sinteticos_usuarios para compatibilidade."""
        return self.criar_dados_sinteticos_usuarios(n_users)

    def train_rating_model(self, df_users: pd.DataFrame) -> Dict:
        """Alias de treinar_modelo_rating para compatibilidade."""
        return self.treinar_modelo_rating(df_users)

    def create_location_clusters(self, df_features: pd.DataFrame) -> Dict:
        """Alias de criar_clusters_locais para compatibilidade."""
        return self.criar_clusters_locais(df_features)

    def save_models(self) -> None:
        """Salva modelos treinados em disco se possível."""
        try:
            base_path = None
            if self.config is not None:
                # Usar caminho padrão de modelos da Config
                base_path = self.config.get_model_path("base").parent
            else:
                from pathlib import Path
                base_path = Path("models")
            base_path.mkdir(parents=True, exist_ok=True)

            if self.rating_model is not None:
                joblib.dump(self.rating_model, base_path / "rating_model.pkl")
            if self.clustering_model is not None:
                joblib.dump(self.clustering_model, base_path / "location_clusters.pkl")
            if self.scaler is not None:
                joblib.dump(self.scaler, base_path / "scaler.pkl")
            if self.label_encoders:
                joblib.dump(self.label_encoders, base_path / "label_encoders.pkl")
            print(f"Modelos salvos em: {base_path}")
        except Exception as e:
            print(f"Erro ao salvar modelos: {e}")

    def load_models(self) -> None:
        """Carrega modelos treinados do disco, se existirem."""
        try:
            from pathlib import Path
            base_path = None
            if self.config is not None:
                base_path = self.config.get_model_path("base").parent
            else:
                base_path = Path("models")

            rating_path = base_path / "rating_model.pkl"
            cluster_path = base_path / "location_clusters.pkl"
            scaler_path = base_path / "scaler.pkl"
            enc_path = base_path / "label_encoders.pkl"

            if rating_path.exists():
                self.rating_model = joblib.load(rating_path)
            if cluster_path.exists():
                self.clustering_model = joblib.load(cluster_path)
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
            if enc_path.exists():
                self.label_encoders = joblib.load(enc_path)
        except Exception as e:
            print(f"Erro ao carregar modelos: {e}")

    def _calcular_distancia_luanda(self, lat: float, lon: float) -> float:
        """Calcula distância de Luanda (capital)."""
        from haversine import haversine
        luanda_coords = (-8.8390, 13.2894)  # Luanda
        return haversine(luanda_coords, (lat, lon))
    
    def criar_dados_sinteticos_usuarios(self, n_usuarios: int = 1000) -> pd.DataFrame:
        """
        Cria dados sintéticos de usuários para treinar o modelo.
        
        Args:
            n_usuarios: Número de usuários sintéticos a criar
            
        Returns:
            DataFrame com dados de usuários
        """
        np.random.seed(42)
        
        dados_usuarios = []
        
        for user_id in range(n_usuarios):
            # Perfil do usuário
            idade = np.random.randint(18, 65)
            orcamento_max = np.random.randint(10000, 50000)
            preferencia_sustentabilidade = np.random.beta(2, 2)  # Preferência por sustentabilidade
            preferencia_aventura = np.random.beta(2, 2)  # Preferência por aventura
            preferencia_cultura = np.random.beta(2, 2)  # Preferência por cultura
            
            # Simular visitas a locais (com ratings)
            n_visitas = np.random.randint(3, 15)
            locais_visitados = np.random.choice(self.df.index, n_visitas, replace=False)
            
            for local_id in locais_visitados:
                local = self.df.iloc[local_id]
                
                # Calcular rating baseado em preferências
                rating_base = 3.0
                
                # Ajustar por fragilidade (usuários sustentáveis preferem baixa fragilidade)
                if preferencia_sustentabilidade > 0.7:
                    rating_base += (5 - local['fragilidade']) * 0.3
                else:
                    rating_base += np.random.normal(0, 0.2)
                
                # Ajustar por tipo de ecossistema
                if local['tipo_ecosistema'] == 'floresta' and preferencia_aventura > 0.6:
                    rating_base += 0.5
                elif local['tipo_ecosistema'] == 'savana' and preferencia_cultura > 0.6:
                    rating_base += 0.3
                
                # Ajustar por custo
                if local['taxa_aoa'] > orcamento_max * 0.3:
                    rating_base -= 0.5
                
                # Adicionar ruído
                rating = rating_base + np.random.normal(0, 0.3)
                rating = np.clip(rating, 1, 5)
                
                dados_usuarios.append({
                    'user_id': user_id,
                    'local_id': local_id,
                    'rating': rating,
                    'idade': idade,
                    'orcamento_max': orcamento_max,
                    'preferencia_sustentabilidade': preferencia_sustentabilidade,
                    'preferencia_aventura': preferencia_aventura,
                    'preferencia_cultura': preferencia_cultura,
                    'fragilidade_local': local['fragilidade'],
                    'tipo_ecosistema': local['tipo_ecosistema'],
                    'provincia': local['provincia'],
                    'taxa_aoa': local['taxa_aoa']
                })
        
        df_usuarios = pd.DataFrame(dados_usuarios)
        print(f"👥 Dados sintéticos criados: {len(df_usuarios)} interações de {n_usuarios} usuários")
        return df_usuarios
    
    def treinar_modelo_rating(self, df_usuarios: pd.DataFrame) -> Dict:
        """
        Treina modelo para prever ratings de usuários.
        
        Args:
            df_usuarios: DataFrame com dados de usuários
            
        Returns:
            Dicionário com métricas do modelo
        """
        # Preparar features
        features = [
            'idade', 'orcamento_max', 'preferencia_sustentabilidade',
            'preferencia_aventura', 'preferencia_cultura', 'fragilidade_local',
            'taxa_aoa'
        ]
        
        # Codificar variáveis categóricas
        df_model = df_usuarios.copy()
        le_ecosistema = LabelEncoder()
        le_provincia = LabelEncoder()
        
        df_model['ecosistema_encoded'] = le_ecosistema.fit_transform(df_model['tipo_ecosistema'])
        df_model['provincia_encoded'] = le_provincia.fit_transform(df_model['provincia'])
        
        features.extend(['ecosistema_encoded', 'provincia_encoded'])
        
        X = df_model[features]
        y = df_model['rating']
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar modelo
        self.rating_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.rating_model.fit(X_train_scaled, y_train)
        
        # Avaliar modelo
        y_pred = self.rating_model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        self.feature_importance['rating'] = dict(zip(features, self.rating_model.feature_importances_))
        
        print(f"Modelo de rating treinado:")
        print(f" R² Score: {r2:.3f}")
        print(f" RMSE: {np.sqrt(mse):.3f}")
        
        return {
            'r2_score': r2,
            'rmse': np.sqrt(mse),
            'feature_importance': self.feature_importance['rating']
        }
    
    def criar_clusters_locais(self, df_features: pd.DataFrame) -> Dict:
        """
        Cria clusters de locais similares usando ML.
        
        Args:
            df_features: DataFrame com features dos locais
            
        Returns:
            Dicionário com informações dos clusters
        """
        # Features para clustering (usar as mesmas 5 usadas na previsão)
        features_cluster = [
            'latitude', 'longitude', 'fragilidade', 'capacidade_diaria',
            'taxa_aoa'
        ]
        
        X_cluster = df_features[features_cluster].values
        X_cluster_scaled = StandardScaler().fit_transform(X_cluster)
        
        # Clustering com K-Means
        n_clusters = min(8, len(df_features) // 3)
        self.clustering_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = self.clustering_model.fit_predict(X_cluster_scaled)
        
        df_features['cluster_ml'] = clusters
        
        # Análise dos clusters
        cluster_info = {}
        for cluster_id in range(n_clusters):
            cluster_data = df_features[df_features['cluster_ml'] == cluster_id]
            
            cluster_info[cluster_id] = {
                'size': len(cluster_data),
                'avg_fragilidade': cluster_data['fragilidade'].mean(),
                'avg_custo': cluster_data['taxa_aoa'].mean(),
                'provincias': cluster_data['provincia'].unique().tolist(),
                'ecosistemas': cluster_data['tipo_ecosistema'].unique().tolist(),
                'locais': cluster_data['nome'].tolist()
            }
        
        print(f"{n_clusters} clusters de locais criados")
        return cluster_info
    
    def sistema_recomendacao_colaborativo(self, df_usuarios: pd.DataFrame, 
                                        user_id: int, n_recommendations: int = 10) -> List[Dict]:
        """
        Sistema de recomendação colaborativo baseado em usuários similares.
        
        Args:
            df_usuarios: DataFrame com dados de usuários
            user_id: ID do usuário para recomendar
            n_recommendations: Número de recomendações
            
        Returns:
            Lista de recomendações
        """
        # Encontrar usuários similares
        user_features = df_usuarios[df_usuarios['user_id'] == user_id][
            ['preferencia_sustentabilidade', 'preferencia_aventura', 'preferencia_cultura', 'idade']
        ].mean()
        
        # Calcular similaridade com outros usuários
        similarities = []
        for other_user in df_usuarios['user_id'].unique():
            if other_user == user_id:
                continue
                
            other_features = df_usuarios[df_usuarios['user_id'] == other_user][
                ['preferencia_sustentabilidade', 'preferencia_aventura', 'preferencia_cultura', 'idade']
            ].mean()
            
            # Similaridade coseno
            similarity = np.dot(user_features, other_features) / (
                np.linalg.norm(user_features) * np.linalg.norm(other_features)
            )
            similarities.append((other_user, similarity))
        
        # Ordenar por similaridade
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Pegar usuários mais similares
        similar_users = [user_id for user_id, _ in similarities[:20]]
        
        # Encontrar locais bem avaliados por usuários similares
        locais_avaliados = df_usuarios[df_usuarios['user_id'] == user_id]['local_id'].tolist()
        
        recomendacoes = []
        for similar_user in similar_users:
            user_ratings = df_usuarios[
                (df_usuarios['user_id'] == similar_user) & 
                (df_usuarios['rating'] >= 4.0) &
                (~df_usuarios['local_id'].isin(locais_avaliados))
            ]
            
            for _, rating in user_ratings.iterrows():
                local_info = self.df.iloc[rating['local_id']]
                recomendacoes.append({
                    'local_id': rating['local_id'],
                    'nome': local_info['nome'],
                    'provincia': local_info['provincia'],
                    'rating_previsto': rating['rating'],
                    'tipo_ecosistema': local_info['tipo_ecosistema'],
                    'fragilidade': local_info['fragilidade'],
                    'taxa_aoa': local_info['taxa_aoa']
                })
        
        # Remover duplicatas e ordenar
        recomendacoes_unicas = {}
        for rec in recomendacoes:
            local_id = rec['local_id']
            if local_id not in recomendacoes_unicas or rec['rating_previsto'] > recomendacoes_unicas[local_id]['rating_previsto']:
                recomendacoes_unicas[local_id] = rec
        
        # Retornar top recomendações
        top_recomendacoes = sorted(
            recomendacoes_unicas.values(), 
            key=lambda x: x['rating_previsto'], 
            reverse=True
        )[:n_recommendations]
        
        return top_recomendacoes
    
    def prever_rating_usuario(self, user_profile: Dict, local_id: int) -> float:
        """
        Prevê o rating que um usuário daria a um local.
        
        Args:
            user_profile: Perfil do usuário
            local_id: ID do local
            
        Returns:
            Rating previsto (1-5)
        """
        if self.rating_model is None:
            print("Modelo de rating não treinado.")
            return 3.0
        
        local = self.df.iloc[local_id]
        
        # Preparar features
        features = np.array([[
            user_profile['idade'],
            user_profile['orcamento_max'],
            user_profile['preferencia_sustentabilidade'],
            user_profile['preferencia_aventura'],
            user_profile['preferencia_cultura'],
            local['fragilidade'],
            local['taxa_aoa'],
            self.label_encoders['ecosistema'].transform([local['tipo_ecosistema']])[0],
            self.label_encoders['provincia'].transform([local['provincia']])[0]
        ]])
        
        # Normalizar e prever
        features_scaled = self.scaler.transform(features)
        rating_previsto = self.rating_model.predict(features_scaled)[0]
        
        return np.clip(rating_previsto, 1, 5)
    
    def gerar_rotas_personalizadas(self, user_profile: Dict, 
                                 orcamento_max: float = 20000,
                                 max_locais: int = 6,
                                 n_rotas: int = 5) -> List[Dict]:
        """
        Gera rotas personalizadas baseadas no perfil do usuário.
        
        Args:
            user_profile: Perfil do usuário
            orcamento_max: Orçamento máximo
            max_locais: Máximo de locais por rota
            n_rotas: Número de rotas a gerar
            
        Returns:
            Lista de rotas personalizadas
        """
        # Filtrar locais por orçamento
        locais_viáveis = self.df[self.df['taxa_aoa'] <= orcamento_max * 0.4]  # Máximo 40% do orçamento por local
        
        # Prever ratings para todos os locais viáveis
        ratings_previstos = []
        for idx, local in locais_viáveis.iterrows():
            rating = self.prever_rating_usuario(user_profile, idx)
            ratings_previstos.append({
                'local_id': idx,
                'rating_previsto': rating,
                'local': local
            })
        
        # Ordenar por rating previsto
        ratings_previstos.sort(key=lambda x: x['rating_previsto'], reverse=True)
        
        # Gerar rotas usando clustering
        if self.clustering_model is not None:
            # Usar clusters para diversificar rotas
            rotas = []
            clusters_usados = set()
            
            for _ in range(n_rotas):
                rota = []
                orcamento_usado = 0
                
                # Selecionar locais de clusters diferentes
                for item in ratings_previstos:
                    if len(rota) >= max_locais:
                        break
                    
                    local_id = item['local_id']
                    local = item['local']
                    
                    # Verificar cluster
                    cluster_id = self.clustering_model.predict([[
                        local['latitude'], local['longitude'], local['fragilidade'],
                        local['capacidade_diaria'], local['taxa_aoa']
                    ]])[0]
                    
                    # Evitar clusters já usados (exceto se necessário)
                    if cluster_id in clusters_usados and len(rota) < max_locais // 2:
                        continue
                    
                    # Verificar orçamento
                    if orcamento_usado + local['taxa_aoa'] <= orcamento_max:
                        rota.append({
                            'local_id': local_id,
                            'nome': local['nome'],
                            'provincia': local['provincia'],
                            'latitude': local['latitude'],
                            'longitude': local['longitude'],
                            'fragilidade': local['fragilidade'],
                            'taxa_aoa': local['taxa_aoa'],
                            'rating_previsto': item['rating_previsto'],
                            'tipo_ecosistema': local['tipo_ecosistema']
                        })
                        orcamento_usado += local['taxa_aoa']
                        clusters_usados.add(cluster_id)
                
                if rota:
                    # Calcular métricas da rota
                    distancia_total = self._calcular_distancia_rota(rota)
                    rating_medio = np.mean([l['rating_previsto'] for l in rota])
                    fragilidade_media = np.mean([l['fragilidade'] for l in rota])
                    
                    rota_info = {
                        'nome': f"Rota Personalizada {len(rotas) + 1}",
                        'locais': rota,
                        'num_locais': len(rota),
                        'distancia_total_km': round(distancia_total, 2),
                        'custo_total_aoa': orcamento_usado,
                        'rating_medio_previsto': round(rating_medio, 2),
                        'fragilidade_media': round(fragilidade_media, 2),
                        'score_personalizado': round(rating_medio - (fragilidade_media * 0.2), 2)
                    }
                    
                    rotas.append(rota_info)
            
            return rotas
        
        return []
    
    def _calcular_distancia_rota(self, rota: List[Dict]) -> float:
        """Calcula distância total de uma rota."""
        from haversine import haversine
        
        distancia_total = 0
        for i in range(len(rota) - 1):
            coord1 = (rota[i]['latitude'], rota[i]['longitude'])
            coord2 = (rota[i+1]['latitude'], rota[i+1]['longitude'])
            distancia_total += haversine(coord1, coord2)
        
        return distancia_total
    
    def salvar_modelos(self, prefixo: str = "ml_models"):
        """Salva os modelos treinados."""
        if self.rating_model is not None:
            joblib.dump(self.rating_model, f"{prefixo}_rating.pkl")
        
        if self.clustering_model is not None:
            joblib.dump(self.clustering_model, f"{prefixo}_clustering.pkl")
        
        # Salvar scaler e encoders
        joblib.dump(self.scaler, f"{prefixo}_scaler.pkl")
        joblib.dump(self.label_encoders, f"{prefixo}_encoders.pkl")
        
        print(f"Modelos salvos com prefixo: {prefixo}")
    
    def carregar_modelos(self, prefixo: str = "ml_models"):
        """Carrega modelos previamente treinados."""
        try:
            self.rating_model = joblib.load(f"{prefixo}_rating.pkl")
            self.clustering_model = joblib.load(f"{prefixo}_clustering.pkl")
            self.scaler = joblib.load(f"{prefixo}_scaler.pkl")
            self.label_encoders = joblib.load(f"{prefixo}_encoders.pkl")
            
            print(f"Modelos carregados com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao carregar modelos: {e}")
            return False


def main():
    """Função principal só para demonstrar o sistema de ML basicamente.."""
    print("SISTEMA DE MACHINE LEARNING PARA ECOTURISMO")
    print("="*60)
    
    # Inicializar motor de ML
    ml_engine = MLRecommendationEngine()
    
    # Carregar dados
    if ml_engine.carregar_dados() is None:
        return
    
    # Criar features
    print("\n Criando features para ML...")
    df_features = ml_engine.criar_features_engenharia()
    
    # Criar dados sintéticos de usuários
    print("\nCriando dados sintéticos de usuários...")
    df_usuarios = ml_engine.criar_dados_sinteticos_usuarios(n_usuarios=500)
    
    # Treinar modelo de rating
    print("\nTreinando modelo de rating...")
    metrics = ml_engine.treinar_modelo_rating(df_usuarios)
    
    # Criar clusters
    print("\nCriando clusters de locais...")
    cluster_info = ml_engine.criar_clusters_locais(df_features)
    
    # Exemplo de recomendação personalizada
    print("\nExemplo de recomendação personalizada...")
    user_profile = {
        'idade': 35,
        'orcamento_max': 25000,
        'preferencia_sustentabilidade': 0.8,
        'preferencia_aventura': 0.6,
        'preferencia_cultura': 0.7
    }
    
    rotas_personalizadas = ml_engine.gerar_rotas_personalizadas(
        user_profile=user_profile,
        orcamento_max=20000,
        max_locais=5,
        n_rotas=3
    )
    
    # Mostrar resultados
    print(f"\nResultados do ML:")
    print(f"  R² Score do modelo: {metrics['r2_score']:.3f}")
    print(f"   RMSE: {metrics['rmse']:.3f}")
    print(f"   Clusters criados: {len(cluster_info)}")
    print(f"   Rotas personalizadas: {len(rotas_personalizadas)}")
    
    # Salvar modelos
    ml_engine.salvar_modelos()
    
    print("\nSistema de ML executado com sucesso!")


if __name__ == "__main__":
    main()

