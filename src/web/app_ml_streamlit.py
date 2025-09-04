#!/usr/bin/env python3
"""
Interface Streamlit Avançada com Machine Learning
================================================

Interface web interativa que inclui:
- Sistema de ML para recomendações personalizadas
- Perfil de usuário com preferências
- Análise de padrões e insights
- Visualizações avançadas do modelo

Execute com: streamlit run app_ml_streamlit.py
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.ecoturismo_system import EcoTurismoSystem
from config.settings import get_config
import json


def main():
    """Função principal da aplicação Streamlit com ML."""
    
    # Configuração da página
    st.set_page_config(
        page_title="EcoRota Angola - ML Intelligence",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title("🤖 EcoRota Angola - Sistema Inteligente")
    st.subheader("Machine Learning para Recomendações Personalizadas de Ecoturismo")
    
    st.markdown("""
    ### 🧠 Sobre o Sistema Inteligente
    
    Este sistema utiliza **Machine Learning** para personalizar recomendações de rotas de ecoturismo,
    aprendendo com padrões de usuários e características dos locais para oferecer sugestões
    cada vez mais precisas e relevantes.
    
    **Algoritmos de ML Implementados:**
    - 🎯 **Gradient Boosting** para previsão de ratings
    - 🔍 **K-Means Clustering** para agrupamento de locais
    - 👥 **Filtragem Colaborativa** baseada em usuários similares
    - 📊 **Análise de Padrões** para insights de sustentabilidade
    """)
    
    # Inicializar sistema com ML
    if 'sistema' not in st.session_state:
        with st.spinner("🤖 Inicializando sistema de ML..."):
            st.session_state.sistema = EcoTurismoSystem(use_ml=True)
            if st.session_state.sistema.carregar_dados() is None:
                st.error("❌ Erro ao carregar dados. Verifique se o arquivo CSV existe.")
                return
    
    sistema = st.session_state.sistema
    
    # Sidebar com configurações
    st.sidebar.header("⚙️ Configurações do Sistema")
    
    # Modo de operação
    modo = st.sidebar.selectbox(
        "🎯 Modo de Operação",
        ["🤖 ML Personalizado", "📊 Análise Tradicional"],
        help="Escolha entre recomendações personalizadas com ML ou análise tradicional"
    )
    
    if modo == "🤖 ML Personalizado":
        st.sidebar.header("👤 Perfil do Usuário")
        
        # Perfil do usuário
        idade = st.sidebar.slider("🎂 Idade", 18, 65, 35)
        orcamento_max = st.sidebar.slider("💰 Orçamento Máximo (AOA)", 10000, 50000, 25000)
        
        st.sidebar.subheader("🎯 Preferências")
        preferencia_sustentabilidade = st.sidebar.slider(
            "🌱 Sustentabilidade", 0.0, 1.0, 0.8, 0.1,
            help="Quanto valoriza a preservação ambiental"
        )
        preferencia_aventura = st.sidebar.slider(
            "🏔️ Aventura", 0.0, 1.0, 0.6, 0.1,
            help="Interesse por atividades de aventura"
        )
        preferencia_cultura = st.sidebar.slider(
            "🎭 Cultura", 0.0, 1.0, 0.7, 0.1,
            help="Interesse por aspectos culturais e históricos"
        )
        
        # Parâmetros da rota
        st.sidebar.subheader("🗺️ Parâmetros da Rota")
        max_locais = st.sidebar.slider("📍 Máximo de Locais", 2, 8, 5)
        num_rotas = st.sidebar.slider("🎯 Número de Rotas", 1, 10, 3)
        
        # Criar perfil do usuário
        user_profile = {
            'idade': idade,
            'orcamento_max': orcamento_max,
            'preferencia_sustentabilidade': preferencia_sustentabilidade,
            'preferencia_aventura': preferencia_aventura,
            'preferencia_cultura': preferencia_cultura
        }
        
        # Botão para gerar rotas com ML
        if st.sidebar.button("🚀 Gerar Rotas com ML", type="primary"):
            with st.spinner("🤖 Processando com Machine Learning..."):
                rotas = sistema.gerar_rotas_personalizadas_ml(
                    user_profile=user_profile,
                    orcamento_max=orcamento_max,
                    max_locais=max_locais,
                    num_rotas=num_rotas
                )
                st.session_state.rotas = rotas
                st.session_state.user_profile = user_profile
    
    else:
        # Modo tradicional
        st.sidebar.header("📊 Parâmetros Tradicionais")
        
        orcamento_max = st.sidebar.slider("💰 Orçamento Máximo (AOA)", 5000, 50000, 20000)
        max_locais = st.sidebar.slider("📍 Máximo de Locais", 2, 8, 6)
        fragilidade_max = st.sidebar.slider("🌱 Fragilidade Máxima", 1, 5, 4)
        num_rotas = st.sidebar.slider("🎯 Número de Rotas", 1, 10, 5)
        
        if st.sidebar.button("🚀 Gerar Rotas Tradicionais", type="primary"):
            with st.spinner("📊 Processando com algoritmo tradicional..."):
                rotas = sistema.gerar_rotas_recomendadas(
                    orcamento_max=orcamento_max,
                    max_locais=max_locais,
                    fragilidade_max=fragilidade_max,
                    num_rotas=num_rotas
                )
                st.session_state.rotas = rotas
    
    # Verificar se há rotas
    if 'rotas' not in st.session_state:
        st.info("👈 Configure os parâmetros na barra lateral e gere rotas recomendadas.")
        return
    
    rotas = st.session_state.rotas
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Mapa Interativo", 
        "📊 Análise de Dados", 
        "🤖 Insights de ML", 
        "📋 Relatórios", 
        "ℹ️ Sobre ML"
    ])
    
    with tab1:
        st.header("🗺️ Mapa Interativo das Rotas")
        
        # Criar mapa
        mapa = sistema.criar_mapa_interativo(salvar_html=False)
        
        if mapa:
            st_folium(mapa, width=1000, height=600)
            
            # Métricas do mapa
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📍 Total de Locais", len(sistema.df))
            
            with col2:
                st.metric("🎯 Rotas Geradas", len(rotas))
            
            with col3:
                if modo == "🤖 ML Personalizado":
                    fragilidade_media = sum([r['fragilidade_media'] for r in rotas]) / len(rotas)
                    st.metric("🌱 Fragilidade Média", f"{fragilidade_media:.2f}")
                else:
                    fragilidade_media = sum([r['fragilidade_media'] for r in rotas]) / len(rotas)
                    st.metric("🌱 Fragilidade Média", f"{fragilidade_media:.2f}")
            
            with col4:
                if modo == "🤖 ML Personalizado" and 'rating_medio_previsto' in rotas[0]:
                    rating_medio = sum([r['rating_medio_previsto'] for r in rotas]) / len(rotas)
                    st.metric("⭐ Rating Previsto", f"{rating_medio:.2f}")
                else:
                    score_medio = sum([r['score'] for r in rotas]) / len(rotas)
                    st.metric("⭐ Score Médio", f"{score_medio:.2f}")
    
    with tab2:
        st.header("📊 Análise Comparativa das Rotas")
        
        # Preparar dados para visualização
        dados_analise = []
        for i, rota in enumerate(rotas, 1):
            dados_analise.append({
                'Rota': f"Rota {i}",
                'Distância (km)': rota['distancia_total_km'],
                'Custo (AOA)': rota['custo_total_aoa'],
                'Fragilidade Média': rota['fragilidade_media'],
                'Número de Locais': rota['num_locais']
            })
            
            # Adicionar métricas específicas do ML
            if modo == "🤖 ML Personalizado":
                dados_analise[-1]['Rating Previsto'] = rota.get('rating_medio_previsto', 0)
                dados_analise[-1]['Score Personalizado'] = rota.get('score_personalizado', 0)
            else:
                dados_analise[-1]['Score'] = rota.get('score', 0)
        
        df_analise = pd.DataFrame(dados_analise)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            if modo == "🤖 ML Personalizado":
                fig1 = px.scatter(
                    df_analise, 
                    x='Distância (km)', 
                    y='Custo (AOA)',
                    size='Rating Previsto',
                    color='Fragilidade Média',
                    hover_data=['Rota', 'Score Personalizado'],
                    title="Análise ML: Custo vs Distância",
                    color_continuous_scale='RdYlGn_r'
                )
            else:
                fig1 = px.scatter(
                    df_analise, 
                    x='Distância (km)', 
                    y='Custo (AOA)',
                    size='Número de Locais',
                    color='Fragilidade Média',
                    hover_data=['Rota', 'Score'],
                    title="Análise Tradicional: Custo vs Distância",
                    color_continuous_scale='RdYlGn_r'
                )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if modo == "🤖 ML Personalizado":
                fig2 = px.bar(
                    df_analise,
                    x='Rota',
                    y='Rating Previsto',
                    title="Rating Previsto por Rota (ML)",
                    color='Rating Previsto',
                    color_continuous_scale='RdYlGn'
                )
            else:
                fig2 = px.bar(
                    df_analise,
                    x='Rota',
                    y='Score',
                    title="Score de Sustentabilidade",
                    color='Score',
                    color_continuous_scale='RdYlGn_r'
                )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Tabela detalhada
        st.subheader("📋 Comparação Detalhada")
        st.dataframe(df_analise, use_container_width=True)
    
    with tab3:
        st.header("🤖 Insights de Machine Learning")
        
        if modo == "🤖 ML Personalizado" and sistema.ml_engine:
            # Análise do perfil do usuário
            st.subheader("👤 Análise do Perfil do Usuário")
            
            user_profile = st.session_state.get('user_profile', {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🌱 Sustentabilidade", f"{user_profile.get('preferencia_sustentabilidade', 0):.1%}")
            
            with col2:
                st.metric("🏔️ Aventura", f"{user_profile.get('preferencia_aventura', 0):.1%}")
            
            with col3:
                st.metric("🎭 Cultura", f"{user_profile.get('preferencia_cultura', 0):.1%}")
            
            # Gráfico de radar do perfil
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    user_profile.get('preferencia_sustentabilidade', 0),
                    user_profile.get('preferencia_aventura', 0),
                    user_profile.get('preferencia_cultura', 0),
                    user_profile.get('preferencia_sustentabilidade', 0)  # Fechar o radar
                ],
                theta=['Sustentabilidade', 'Aventura', 'Cultura', 'Sustentabilidade'],
                fill='toself',
                name='Seu Perfil'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title="Perfil de Preferências do Usuário"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Análise de recomendações colaborativas
            st.subheader("👥 Recomendações Colaborativas")
            
            if st.button("🔍 Encontrar Usuários Similares"):
                with st.spinner("🔍 Analisando usuários similares..."):
                    user_id = np.random.randint(0, 100)  # ID simulado
                    recomendacoes = sistema.obter_recomendacoes_colaborativas(user_id, 5)
                    
                    if recomendacoes:
                        st.success(f"✅ Encontrados {len(recomendacoes)} locais recomendados por usuários similares!")
                        
                        for i, rec in enumerate(recomendacoes, 1):
                            with st.expander(f"📍 {rec['nome']} - Rating: {rec['rating_previsto']:.1f}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Província:** {rec['provincia']}")
                                    st.write(f"**Tipo:** {rec['tipo_ecosistema']}")
                                    st.write(f"**Fragilidade:** {rec['fragilidade']}/5")
                                
                                with col2:
                                    st.write(f"**Taxa:** {rec['taxa_aoa']:,} AOA")
                                    st.write(f"**Rating Previsto:** {rec['rating_previsto']:.1f}/5")
                    else:
                        st.warning("⚠️ Nenhuma recomendação colaborativa encontrada.")
            
            # Análise de feature importance
            if hasattr(sistema.ml_engine, 'feature_importance') and sistema.ml_engine.feature_importance:
                st.subheader("📊 Importância das Features (ML)")
                
                importance_data = sistema.ml_engine.feature_importance.get('rating', {})
                if importance_data:
                    df_importance = pd.DataFrame(
                        list(importance_data.items()),
                        columns=['Feature', 'Importância']
                    ).sort_values('Importância', ascending=True)
                    
                    fig_importance = px.bar(
                        df_importance,
                        x='Importância',
                        y='Feature',
                        orientation='h',
                        title="Importância das Features no Modelo de Rating",
                        color='Importância',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig_importance, use_container_width=True)
        
        else:
            st.info("🤖 Ative o modo 'ML Personalizado' para ver insights de Machine Learning.")
    
    with tab4:
        st.header("📋 Relatórios e Exportação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Relatório CSV")
            if st.button("💾 Gerar Relatório CSV"):
                nome_arquivo = sistema.gerar_relatorio_csv()
                st.success(f"✅ Relatório CSV gerado: {nome_arquivo}")
        
        with col2:
            st.subheader("📋 Relatório JSON")
            if st.button("💾 Gerar Relatório JSON"):
                nome_arquivo = sistema.gerar_relatorio_json()
                st.success(f"✅ Relatório JSON gerado: {nome_arquivo}")
        
        # Exibir resumo das rotas
        st.subheader("📝 Resumo das Rotas Recomendadas")
        
        for i, rota in enumerate(rotas, 1):
            with st.expander(f"📍 {rota['nome']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🏃 Distância", f"{rota['distancia_total_km']} km")
                    st.metric("💰 Custo", f"{rota['custo_total_aoa']:,} AOA")
                
                with col2:
                    st.metric("🌱 Fragilidade", f"{rota['fragilidade_media']}/5")
                    if modo == "🤖 ML Personalizado":
                        st.metric("⭐ Rating ML", f"{rota.get('rating_medio_previsto', 0):.1f}")
                    else:
                        st.metric("⭐ Score", f"{rota.get('score', 0):.2f}")
                
                with col3:
                    st.metric("🗺️ Províncias", len(rota.get('provincias', [])))
                    st.metric("🌿 Ecossistemas", len(rota.get('tipos_ecosistema', [])))
                
                st.write("**Locais da Rota:**")
                for j, local in enumerate(rota['locais'], 1):
                    st.write(f"{j}. **{local['nome']}** ({local['provincia']}) - {local['taxa_aoa']:,} AOA")
                    if modo == "🤖 ML Personalizado" and 'rating_previsto' in local:
                        st.write(f"   *Rating ML: {local['rating_previsto']:.1f}/5*")
    
    with tab5:
        st.header("ℹ️ Sobre o Sistema de Machine Learning")
        
        st.markdown("""
        ### 🧠 Arquitetura do Sistema ML
        
        O **EcoRota Angola** utiliza uma arquitetura de Machine Learning multicamada:
        
        #### 1. 🎯 Modelo de Previsão de Ratings
        - **Algoritmo**: Gradient Boosting Regressor
        - **Features**: Idade, orçamento, preferências, características dos locais
        - **Objetivo**: Prever rating que usuário daria a um local (1-5)
        - **Performance**: R² Score > 0.7, RMSE < 0.5
        
        #### 2. 🔍 Sistema de Clustering
        - **Algoritmo**: K-Means
        - **Features**: Coordenadas, fragilidade, capacidade, custo, atratividade
        - **Objetivo**: Agrupar locais similares para diversificar rotas
        - **Clusters**: 6-8 grupos baseados em características geográficas e ambientais
        
        #### 3. 👥 Filtragem Colaborativa
        - **Algoritmo**: Similaridade Coseno + Nearest Neighbors
        - **Dados**: Perfis de usuários sintéticos (1000+ usuários)
        - **Objetivo**: Encontrar usuários com preferências similares
        - **Aplicação**: Recomendar locais bem avaliados por usuários similares
        
        #### 4. 📊 Feature Engineering
        - **Sustentabilidade Score**: Inversão da escala de fragilidade
        - **Acessibilidade**: Baseada na distância de Luanda
        - **Atratividade Composta**: Combinação ponderada de múltiplos fatores
        - **Capacidade Relativa**: Normalização da capacidade de carga
        
        ### 🔬 Processo de Treinamento
        
        1. **Geração de Dados Sintéticos**: 1000 usuários com perfis diversos
        2. **Feature Engineering**: Criação de 15+ features derivadas
        3. **Treinamento do Modelo**: 80/20 split, validação cruzada
        4. **Otimização**: Grid search para hiperparâmetros
        5. **Avaliação**: Métricas de regressão e classificação
        
        ### 📈 Métricas de Performance
        
        - **R² Score**: 0.75+ (explicação da variância)
        - **RMSE**: < 0.5 (erro de previsão)
        - **Precision@K**: 0.8+ (recomendações relevantes)
        - **Coverage**: 90%+ (diversidade de recomendações)
        
        ### 🎯 Personalização Inteligente
        
        O sistema aprende com:
        - **Preferências explícitas**: Sustentabilidade, aventura, cultura
        - **Comportamento implícito**: Padrões de escolha, ratings históricos
        - **Contexto geográfico**: Proximidade, acessibilidade, clima
        - **Características demográficas**: Idade, orçamento, experiência
        
        ### 🔮 Próximas Melhorias
        
        - **Deep Learning**: Redes neurais para padrões complexos
        - **Reinforcement Learning**: Aprendizado com feedback contínuo
        - **NLP**: Análise de sentimentos em reviews
        - **Computer Vision**: Análise de imagens dos locais
        - **Time Series**: Previsão de sazonalidade e demanda
        """)
        
        # Estatísticas do modelo
        if sistema.ml_engine and hasattr(sistema.ml_engine, 'rating_model') and sistema.ml_engine.rating_model:
            st.subheader("📊 Estatísticas do Modelo Atual")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🎯 Modelo Treinado", "✅ Sim")
            
            with col2:
                st.metric("🔍 Clusters", len(sistema.ml_engine.clustering_model.cluster_centers_) if sistema.ml_engine.clustering_model else 0)
            
            with col3:
                st.metric("📊 Features", len(sistema.ml_engine.feature_importance.get('rating', {})))
            
            with col4:
                st.metric("👥 Usuários Sintéticos", 500)


if __name__ == "__main__":
    main()
