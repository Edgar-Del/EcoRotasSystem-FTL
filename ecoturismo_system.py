#!/usr/bin/env python3
"""
Sistema de Roteiro Inteligente de Ecoturismo em Angola
=====================================================

Este sistema sugere rotas de ecoturismo sustentável baseadas em critérios de:
- Fragilidade ambiental (≤ 4)
- Orçamento (≤ 20.000 AOA por padrão)
- Máximo de 6 locais por roteiro
- Algoritmo de vizinho mais próximo para otimização de distância

Autor: Sistema EcoRota Angola
Data: 2025
"""

import pandas as pd
import folium
import numpy as np
from haversine import haversine
from sklearn.cluster import KMeans
import json
from typing import List, Dict, Tuple, Optional
import os
from datetime import datetime
from ml_recommendation_engine import MLRecommendationEngine


class EcoTurismoSystem:
    """Sistema principal para recomendação de rotas de ecoturismo sustentável."""
    
    def __init__(self, csv_file: str = "locais_ecoturismo_angola.csv", use_ml: bool = True):
        """
        Inicializa o sistema de ecoturismo.
        
        Args:
            csv_file: Caminho para o arquivo CSV com dados dos locais
            use_ml: Se deve usar sistema de ML para recomendações
        """
        self.csv_file = csv_file
        self.df = None
        self.rotas_recomendadas = []
        self.mapa_base = None
        self.use_ml = use_ml
        self.ml_engine = None
        
        if self.use_ml:
            self.ml_engine = MLRecommendationEngine(csv_file)
        
    def carregar_dados(self) -> pd.DataFrame:
        """
        Carrega e processa os dados dos locais de ecoturismo.
        
        Returns:
            DataFrame com os dados processados
        """
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"✅ Dados carregados: {len(self.df)} locais de ecoturismo")
            print(f"📊 Províncias: {self.df['provincia'].nunique()}")
            print(f"🌍 Tipos de ecossistema: {self.df['tipo_ecosistema'].nunique()}")
            
            # Carregar dados para ML se habilitado
            if self.use_ml and self.ml_engine:
                self.ml_engine.carregar_dados()
                print(f"🤖 Sistema de ML inicializado")
            
            return self.df
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo {self.csv_file} não encontrado!")
            return None
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return None
    
    def calcular_distancia(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """
        Calcula a distância entre duas coordenadas geográficas.
        
        Args:
            coord1: Tupla (latitude, longitude) do primeiro ponto
            coord2: Tupla (latitude, longitude) do segundo ponto
            
        Returns:
            Distância em quilômetros
        """
        return haversine(coord1, coord2)
    
    def filtrar_locais_sustentaveis(self, fragilidade_max: int = 4) -> pd.DataFrame:
        """
        Filtra locais com fragilidade ambiental adequada para turismo sustentável.
        
        Args:
            fragilidade_max: Fragilidade máxima permitida (1-5, onde 5 é mais frágil)
            
        Returns:
            DataFrame filtrado
        """
        if self.df is None:
            print("❌ Dados não carregados. Execute carregar_dados() primeiro.")
            return None
            
        df_filtrado = self.df[self.df['fragilidade'] <= fragilidade_max].copy()
        print(f"🌱 Locais sustentáveis (fragilidade ≤ {fragilidade_max}): {len(df_filtrado)}")
        return df_filtrado
    
    def criar_clusters_provincias(self, df: pd.DataFrame, n_clusters: int = 5) -> pd.DataFrame:
        """
        Agrupa locais por proximidade geográfica usando clustering.
        
        Args:
            df: DataFrame com os locais
            n_clusters: Número de clusters desejados
            
        Returns:
            DataFrame com coluna de cluster adicionada
        """
        if len(df) < n_clusters:
            n_clusters = len(df)
            
        coords = df[['latitude', 'longitude']].values
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(coords)
        
        print(f"🗺️  Criados {n_clusters} clusters geográficos")
        return df
    
    def algoritmo_vizinho_mais_proximo(self, locais: List[Dict], ponto_inicial: int = 0) -> List[int]:
        """
        Implementa algoritmo do vizinho mais próximo para otimizar rota.
        
        Args:
            locais: Lista de dicionários com informações dos locais
            ponto_inicial: Índice do ponto de partida
            
        Returns:
            Lista de índices ordenados pela rota otimizada
        """
        if len(locais) <= 1:
            return [0]
            
        n = len(locais)
        visitados = [False] * n
        rota = [ponto_inicial]
        visitados[ponto_inicial] = True
        atual = ponto_inicial
        
        for _ in range(n - 1):
            menor_distancia = float('inf')
            proximo = -1
            
            for i in range(n):
                if not visitados[i]:
                    coord_atual = (locais[atual]['latitude'], locais[atual]['longitude'])
                    coord_proximo = (locais[i]['latitude'], locais[i]['longitude'])
                    distancia = self.calcular_distancia(coord_atual, coord_proximo)
                    
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        proximo = i
            
            if proximo != -1:
                rota.append(proximo)
                visitados[proximo] = True
                atual = proximo
        
        return rota
    
    def calcular_score_rota(self, rota_locais: List[Dict]) -> float:
        """
        Calcula o score de uma rota baseado nos critérios de sustentabilidade.
        
        Score = 0.45 × fragilidade_média + 0.35 × distância_total(km/1000) + 0.20 × custo_total(AOA/100.000)
        
        Args:
            rota_locais: Lista de locais na rota
            
        Returns:
            Score da rota (menor é melhor)
        """
        if not rota_locais:
            return float('inf')
            
        # Fragilidade média
        fragilidade_media = np.mean([local['fragilidade'] for local in rota_locais])
        
        # Distância total
        distancia_total = 0
        for i in range(len(rota_locais) - 1):
            coord1 = (rota_locais[i]['latitude'], rota_locais[i]['longitude'])
            coord2 = (rota_locais[i+1]['latitude'], rota_locais[i+1]['longitude'])
            distancia_total += self.calcular_distancia(coord1, coord2)
        
        # Custo total
        custo_total = sum([local['taxa_aoa'] for local in rota_locais])
        
        # Score ponderado
        score = (0.45 * fragilidade_media + 
                0.35 * (distancia_total / 1000) + 
                0.20 * (custo_total / 100000))
        
        return score
    
    def gerar_rotas_recomendadas(self, orcamento_max: float = 20000, 
                                max_locais: int = 6, 
                                fragilidade_max: int = 4,
                                num_rotas: int = 5) -> List[Dict]:
        """
        Gera rotas recomendadas baseadas nos critérios de sustentabilidade.
        
        Args:
            orcamento_max: Orçamento máximo em AOA
            max_locais: Número máximo de locais por rota
            fragilidade_max: Fragilidade máxima permitida
            num_rotas: Número de rotas a gerar
            
        Returns:
            Lista de rotas recomendadas
        """
        if self.df is None:
            print("❌ Dados não carregados. Execute carregar_dados() primeiro.")
            return []
        
        # Filtrar locais sustentáveis
        df_sustentavel = self.filtrar_locais_sustentaveis(fragilidade_max)
        if df_sustentavel.empty:
            print("❌ Nenhum local sustentável encontrado!")
            return []
        
        # Criar clusters por província
        df_clusters = self.criar_clusters_provincias(df_sustentavel, n_clusters=min(6, len(df_sustentavel)))
        
        rotas = []
        
        for cluster_id in df_clusters['cluster'].unique():
            df_cluster = df_clusters[df_clusters['cluster'] == cluster_id]
            
            # Tentar diferentes combinações de locais no cluster
            for tamanho_rota in range(2, min(max_locais + 1, len(df_cluster) + 1)):
                for _ in range(3):  # Tentar 3 combinações diferentes
                    # Selecionar locais aleatórios do cluster
                    locais_selecionados = df_cluster.sample(n=min(tamanho_rota, len(df_cluster)), 
                                                          random_state=np.random.randint(1000))
                    
                    # Verificar orçamento
                    custo_total = locais_selecionados['taxa_aoa'].sum()
                    if custo_total > orcamento_max:
                        continue
                    
                    # Converter para lista de dicionários
                    locais_lista = locais_selecionados.to_dict('records')
                    
                    # Otimizar rota com algoritmo do vizinho mais próximo
                    indices_otimizados = self.algoritmo_vizinho_mais_proximo(locais_lista)
                    rota_otimizada = [locais_lista[i] for i in indices_otimizados]
                    
                    # Calcular métricas da rota
                    distancia_total = 0
                    for i in range(len(rota_otimizada) - 1):
                        coord1 = (rota_otimizada[i]['latitude'], rota_otimizada[i]['longitude'])
                        coord2 = (rota_otimizada[i+1]['latitude'], rota_otimizada[i+1]['longitude'])
                        distancia_total += self.calcular_distancia(coord1, coord2)
                    
                    score = self.calcular_score_rota(rota_otimizada)
                    
                    rota_info = {
                        'nome': f"Rota Cluster {cluster_id + 1} - {len(rota_otimizada)} locais",
                        'locais': rota_otimizada,
                        'num_locais': len(rota_otimizada),
                        'distancia_total_km': round(distancia_total, 2),
                        'custo_total_aoa': custo_total,
                        'fragilidade_media': round(np.mean([l['fragilidade'] for l in rota_otimizada]), 2),
                        'score': round(score, 3),
                        'provincias': list(set([l['provincia'] for l in rota_otimizada])),
                        'tipos_ecosistema': list(set([l['tipo_ecosistema'] for l in rota_otimizada]))
                    }
                    
                    rotas.append(rota_info)
        
        # Ordenar por score (menor é melhor) e pegar as melhores
        rotas_ordenadas = sorted(rotas, key=lambda x: x['score'])[:num_rotas]
        
        self.rotas_recomendadas = rotas_ordenadas
        print(f"🎯 Geradas {len(rotas_ordenadas)} rotas recomendadas")
        
        return rotas_ordenadas
    
    def gerar_rotas_personalizadas_ml(self, user_profile: Dict, 
                                    orcamento_max: float = 20000,
                                    max_locais: int = 6,
                                    num_rotas: int = 5) -> List[Dict]:
        """
        Gera rotas personalizadas usando Machine Learning.
        
        Args:
            user_profile: Perfil do usuário com preferências
            orcamento_max: Orçamento máximo em AOA
            max_locais: Número máximo de locais por rota
            num_rotas: Número de rotas a gerar
            
        Returns:
            Lista de rotas personalizadas
        """
        if not self.use_ml or not self.ml_engine:
            print("❌ Sistema de ML não disponível. Use gerar_rotas_recomendadas()")
            return []
        
        if self.df is None:
            print("❌ Dados não carregados. Execute carregar_dados() primeiro.")
            return []
        
        print(f"🤖 Gerando rotas personalizadas com ML...")
        
        # Treinar modelo se necessário
        if self.ml_engine.rating_model is None:
            print("🔄 Treinando modelo de ML...")
            df_features = self.ml_engine.criar_features_engenharia()
            df_usuarios = self.ml_engine.criar_dados_sinteticos_usuarios(n_usuarios=500)
            self.ml_engine.treinar_modelo_rating(df_usuarios)
            self.ml_engine.criar_clusters_locais(df_features)
        
        # Gerar rotas personalizadas
        rotas_personalizadas = self.ml_engine.gerar_rotas_personalizadas(
            user_profile=user_profile,
            orcamento_max=orcamento_max,
            max_locais=max_locais,
            n_rotas=num_rotas
        )
        
        self.rotas_recomendadas = rotas_personalizadas
        print(f"🎯 {len(rotas_personalizadas)} rotas personalizadas geradas com ML")
        
        return rotas_personalizadas
    
    def obter_recomendacoes_colaborativas(self, user_id: int, n_recommendations: int = 10) -> List[Dict]:
        """
        Obtém recomendações colaborativas baseadas em usuários similares.
        
        Args:
            user_id: ID do usuário
            n_recommendations: Número de recomendações
            
        Returns:
            Lista de recomendações
        """
        if not self.use_ml or not self.ml_engine:
            print("❌ Sistema de ML não disponível.")
            return []
        
        # Criar dados sintéticos se necessário
        if not hasattr(self.ml_engine, 'df_usuarios'):
            df_features = self.ml_engine.criar_features_engenharia()
            self.ml_engine.df_usuarios = self.ml_engine.criar_dados_sinteticos_usuarios(n_usuarios=500)
        
        return self.ml_engine.sistema_recomendacao_colaborativo(
            self.ml_engine.df_usuarios, user_id, n_recommendations
        )
    
    def prever_rating_local(self, user_profile: Dict, local_id: int) -> float:
        """
        Prevê o rating que um usuário daria a um local específico.
        
        Args:
            user_profile: Perfil do usuário
            local_id: ID do local
            
        Returns:
            Rating previsto (1-5)
        """
        if not self.use_ml or not self.ml_engine:
            print("❌ Sistema de ML não disponível.")
            return 3.0
        
        return self.ml_engine.prever_rating_usuario(user_profile, local_id)
    
    def criar_mapa_interativo(self, salvar_html: bool = True) -> folium.Map:
        """
        Cria mapa interativo com todas as rotas recomendadas.
        
        Args:
            salvar_html: Se deve salvar o mapa como arquivo HTML
            
        Returns:
            Mapa Folium interativo
        """
        if not self.rotas_recomendadas:
            print("❌ Nenhuma rota recomendada. Execute gerar_rotas_recomendadas() primeiro.")
            return None
        
        # Centro do mapa (Angola)
        centro_lat = -12.5
        centro_lon = 17.5
        
        # Criar mapa base
        self.mapa_base = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Cores para diferentes rotas
        cores_rotas = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']
        
        # Adicionar cada rota ao mapa
        for idx, rota in enumerate(self.rotas_recomendadas):
            cor = cores_rotas[idx % len(cores_rotas)]
            
            # Adicionar marcadores para cada local
            for i, local in enumerate(rota['locais']):
                # Ícone baseado na fragilidade
                if local['fragilidade'] <= 2:
                    icone = 'green'
                elif local['fragilidade'] == 3:
                    icone = 'orange'
                else:
                    icone = 'red'
                
                # Popup com informações
                popup_text = f"""
                <b>{local['nome']}</b><br>
                <b>Província:</b> {local['provincia']}<br>
                <b>Tipo:</b> {local['tipo_ecosistema']}<br>
                <b>Fragilidade:</b> {local['fragilidade']}/5<br>
                <b>Capacidade:</b> {local['capacidade_diaria']} pessoas/dia<br>
                <b>Taxa:</b> {local['taxa_aoa']:,} AOA<br>
                <b>Descrição:</b> {local['descricao']}
                """
                
                folium.Marker(
                    [local['latitude'], local['longitude']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=f"{local['nome']} (Fragilidade: {local['fragilidade']})",
                    icon=folium.Icon(color=icone, icon='leaf', prefix='fa')
                ).add_to(self.mapa_base)
            
            # Adicionar linha da rota
            coordenadas_rota = [[local['latitude'], local['longitude']] for local in rota['locais']]
            folium.PolyLine(
                coordenadas_rota,
                color=cor,
                weight=3,
                opacity=0.8,
                popup=f"<b>{rota['nome']}</b><br>Distância: {rota['distancia_total_km']} km<br>Custo: {rota['custo_total_aoa']:,} AOA"
            ).add_to(self.mapa_base)
        
        # Adicionar legenda
        legenda_html = """
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
        self.mapa_base.get_root().html.add_child(folium.Element(legenda_html))
        
        if salvar_html:
            nome_arquivo = f"mapa_ecoturismo_angola_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            self.mapa_base.save(nome_arquivo)
            print(f"🗺️  Mapa salvo como: {nome_arquivo}")
        
        return self.mapa_base
    
    def gerar_relatorio_csv(self, nome_arquivo: str = None) -> str:
        """
        Gera relatório CSV com resumo das rotas recomendadas.
        
        Args:
            nome_arquivo: Nome do arquivo CSV (opcional)
            
        Returns:
            Nome do arquivo gerado
        """
        if not self.rotas_recomendadas:
            print("❌ Nenhuma rota recomendada. Execute gerar_rotas_recomendadas() primeiro.")
            return None
        
        # Preparar dados para CSV
        dados_relatorio = []
        for rota in self.rotas_recomendadas:
            dados_relatorio.append({
                'nome_rota': rota['nome'],
                'num_locais': rota['num_locais'],
                'distancia_total_km': rota['distancia_total_km'],
                'custo_total_aoa': rota['custo_total_aoa'],
                'fragilidade_media': rota['fragilidade_media'],
                'score': rota['score'],
                'provincias': '; '.join(rota['provincias']),
                'tipos_ecosistema': '; '.join(rota['tipos_ecosistema']),
                'locais_visitados': '; '.join([l['nome'] for l in rota['locais']])
            })
        
        # Criar DataFrame e salvar
        df_relatorio = pd.DataFrame(dados_relatorio)
        
        if nome_arquivo is None:
            nome_arquivo = f"relatorio_rotas_ecoturismo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df_relatorio.to_csv(nome_arquivo, index=False, encoding='utf-8')
        print(f"📊 Relatório CSV salvo como: {nome_arquivo}")
        
        return nome_arquivo
    
    def gerar_relatorio_json(self, nome_arquivo: str = None) -> str:
        """
        Gera relatório JSON detalhado com todas as rotas recomendadas.
        
        Args:
            nome_arquivo: Nome do arquivo JSON (opcional)
            
        Returns:
            Nome do arquivo gerado
        """
        if not self.rotas_recomendadas:
            print("❌ Nenhuma rota recomendada. Execute gerar_rotas_recomendadas() primeiro.")
            return None
        
        if nome_arquivo is None:
            nome_arquivo = f"relatorio_detalhado_ecoturismo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.rotas_recomendadas, f, ensure_ascii=False, indent=2)
        
        print(f"📋 Relatório JSON salvo como: {nome_arquivo}")
        return nome_arquivo
    
    def imprimir_resumo_rotas(self):
        """Imprime um resumo das rotas recomendadas no console."""
        if not self.rotas_recomendadas:
            print("❌ Nenhuma rota recomendada disponível.")
            return
        
        print("\n" + "="*80)
        print("🌍 RESUMO DAS ROTAS DE ECOTURISMO RECOMENDADAS - ANGOLA")
        print("="*80)
        
        for i, rota in enumerate(self.rotas_recomendadas, 1):
            print(f"\n📍 ROTA {i}: {rota['nome']}")
            print(f"   🏃 Distância Total: {rota['distancia_total_km']} km")
            print(f"   💰 Custo Total: {rota['custo_total_aoa']:,} AOA")
            print(f"   🌱 Fragilidade Média: {rota['fragilidade_media']}/5")
            print(f"   ⭐ Score: {rota['score']}")
            print(f"   🗺️  Províncias: {', '.join(rota['provincias'])}")
            print(f"   🌿 Ecossistemas: {', '.join(rota['tipos_ecosistema'])}")
            print(f"   📍 Locais ({rota['num_locais']}):")
            
            for j, local in enumerate(rota['locais'], 1):
                print(f"      {j}. {local['nome']} ({local['provincia']}) - {local['taxa_aoa']:,} AOA")
        
        print("\n" + "="*80)
        print("💡 Dica: Abra o arquivo HTML gerado para visualizar as rotas no mapa interativo!")
        print("="*80)


def main():
    """Função principal para demonstrar o sistema."""
    print("🌍 SISTEMA DE ROTEIRO INTELIGENTE DE ECOTURISMO EM ANGOLA")
    print("="*60)
    
    # Inicializar sistema
    sistema = EcoTurismoSystem()
    
    # Carregar dados
    if sistema.carregar_dados() is None:
        return
    
    # Gerar rotas recomendadas
    print("\n🎯 Gerando rotas recomendadas...")
    rotas = sistema.gerar_rotas_recomendadas(
        orcamento_max=20000,
        max_locais=6,
        fragilidade_max=4,
        num_rotas=5
    )
    
    if not rotas:
        print("❌ Não foi possível gerar rotas recomendadas.")
        return
    
    # Criar visualizações
    print("\n🗺️  Criando mapa interativo...")
    sistema.criar_mapa_interativo()
    
    # Gerar relatórios
    print("\n📊 Gerando relatórios...")
    sistema.gerar_relatorio_csv()
    sistema.gerar_relatorio_json()
    
    # Imprimir resumo
    sistema.imprimir_resumo_rotas()
    
    print("\n✅ Sistema executado com sucesso!")
    print("📁 Verifique os arquivos gerados no diretório atual.")


if __name__ == "__main__":
    main()
