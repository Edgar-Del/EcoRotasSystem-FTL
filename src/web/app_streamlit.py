#!/usr/bin/env python3
"""
Interface Streamlit para o Sistema de Roteiro Inteligente de Ecoturismo em Angola
================================================================================

Interface web interativa que permite aos usuários:
- Ajustar parâmetros de busca (orçamento, fragilidade, número de locais)
- Visualizar rotas recomendadas em tempo real
- Exportar relatórios personalizados

Execute com: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.ecoturismo_system import EcoTurismoSystem
from config.settings import get_config
import plotly.express as px
import plotly.graph_objects as go


def main():
    """Função principal da aplicação Streamlit."""
    
    # Configuração da página
    st.set_page_config(
        page_title="EcoRota Angola - Sistema de Ecoturismo Sustentável",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Título principal
    st.title("🌍 EcoRota Angola")
    st.subheader("Sistema de Roteiro Inteligente de Ecoturismo Sustentável")
    
    st.markdown("""
    ### 🎯 Sobre o Sistema
    
    Este sistema utiliza algoritmos inteligentes para sugerir rotas de ecoturismo em Angola,
    equilibrando **sustentabilidade ambiental**, **custo-benefício** e **experiência cultural**.
    
    **Critérios de Sustentabilidade:**
    - ✅ Fragilidade ambiental ≤ 4 (escala 1-5)
    - ✅ Orçamento otimizado
    - ✅ Máximo de 6 locais por rota
    - ✅ Algoritmo de vizinho mais próximo para distância mínima
    """)
    
    # Sidebar com parâmetros
    st.sidebar.header("⚙️ Parâmetros de Busca")
    
    orcamento_max = st.sidebar.slider(
        "💰 Orçamento Máximo (AOA)",
        min_value=5000,
        max_value=50000,
        value=20000,
        step=1000,
        help="Orçamento máximo para a rota completa"
    )
    
    max_locais = st.sidebar.slider(
        "📍 Número Máximo de Locais",
        min_value=2,
        max_value=8,
        value=6,
        help="Número máximo de locais por rota"
    )
    
    fragilidade_max = st.sidebar.slider(
        "🌱 Fragilidade Máxima",
        min_value=1,
        max_value=5,
        value=4,
        help="Fragilidade ambiental máxima (1=baixa, 5=alta)"
    )
    
    num_rotas = st.sidebar.slider(
        "🎯 Número de Rotas",
        min_value=1,
        max_value=10,
        value=5,
        help="Número de rotas recomendadas a gerar"
    )
    
    # Botão para gerar rotas
    if st.sidebar.button("🚀 Gerar Rotas Recomendadas", type="primary"):
        with st.spinner("🔄 Processando dados e gerando rotas..."):
            # Inicializar sistema
            sistema = EcoTurismoSystem()
            
            # Carregar dados
            if sistema.carregar_dados() is None:
                st.error("❌ Erro ao carregar dados. Verifique se o arquivo CSV existe.")
                return
            
            # Gerar rotas
            rotas = sistema.gerar_rotas_recomendadas(
                orcamento_max=orcamento_max,
                max_locais=max_locais,
                fragilidade_max=fragilidade_max,
                num_rotas=num_rotas
            )
            
            if not rotas:
                st.warning("⚠️ Nenhuma rota encontrada com os critérios especificados.")
                return
            
            # Armazenar no session state
            st.session_state.rotas = rotas
            st.session_state.sistema = sistema
    
    # Verificar se há rotas no session state
    if 'rotas' not in st.session_state:
        st.info("👈 Use a barra lateral para configurar os parâmetros e gerar rotas recomendadas.")
        return
    
    rotas = st.session_state.rotas
    sistema = st.session_state.sistema
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Mapa Interativo", "📊 Análise de Dados", "📋 Relatórios", "ℹ️ Sobre"])
    
    with tab1:
        st.header("🗺️ Mapa Interativo das Rotas")
        
        # Criar mapa
        mapa = sistema.criar_mapa_interativo(salvar_html=False)
        
        if mapa:
            # Exibir mapa
            st_folium(mapa, width=1000, height=600)
            
            # Informações adicionais
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📍 Total de Locais", len(sistema.df))
            
            with col2:
                st.metric("🎯 Rotas Geradas", len(rotas))
            
            with col3:
                fragilidade_media = sum([r['fragilidade_media'] for r in rotas]) / len(rotas)
                st.metric("🌱 Fragilidade Média", f"{fragilidade_media:.2f}")
    
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
                'Score': rota['score'],
                'Número de Locais': rota['num_locais']
            })
        
        df_analise = pd.DataFrame(dados_analise)
        
        # Gráficos comparativos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de custo vs distância
            fig1 = px.scatter(
                df_analise, 
                x='Distância (km)', 
                y='Custo (AOA)',
                size='Número de Locais',
                color='Fragilidade Média',
                hover_data=['Rota', 'Score'],
                title="Custo vs Distância das Rotas",
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Gráfico de score
            fig2 = px.bar(
                df_analise,
                x='Rota',
                y='Score',
                title="Score de Sustentabilidade (menor é melhor)",
                color='Score',
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Tabela detalhada
        st.subheader("📋 Comparação Detalhada")
        st.dataframe(df_analise, use_container_width=True)
    
    with tab3:
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
                    st.metric("⭐ Score", f"{rota['score']}")
                
                with col3:
                    st.metric("🗺️ Províncias", len(rota['provincias']))
                    st.metric("🌿 Ecossistemas", len(rota['tipos_ecosistema']))
                
                st.write("**Locais da Rota:**")
                for j, local in enumerate(rota['locais'], 1):
                    st.write(f"{j}. **{local['nome']}** ({local['provincia']}) - {local['taxa_aoa']:,} AOA")
                    st.write(f"   *{local['descricao']}*")
    
    with tab4:
        st.header("ℹ️ Sobre o Sistema EcoRota Angola")
        
        st.markdown("""
        ### 🎯 Objetivo
        
        O **EcoRota Angola** é um sistema inteligente de recomendação de rotas de ecoturismo 
        que equilibra sustentabilidade ambiental, custo-benefício e experiência cultural 
        para promover o turismo responsável em Angola.
        
        ### 🔬 Metodologia
        
        **Algoritmo de Recomendação:**
        - **Clustering Geográfico**: Agrupa locais por proximidade
        - **Algoritmo do Vizinho Mais Próximo**: Otimiza distâncias
        - **Score de Sustentabilidade**: Combina fragilidade, distância e custo
        
        **Fórmula do Score:**
        ```
        Score = 0.45 × fragilidade_média + 0.35 × distância_total(km/1000) + 0.20 × custo_total(AOA/100.000)
        ```
        
        ### 🌱 Critérios de Sustentabilidade
        
        1. **Fragilidade Ambiental**: Prioriza locais com fragilidade ≤ 4
        2. **Capacidade de Carga**: Considera limite diário de visitantes
        3. **Diversidade Ecológica**: Inclui diferentes tipos de ecossistemas
        4. **Distribuição Geográfica**: Evita concentração em uma única região
        
        ### 🛠️ Tecnologias Utilizadas
        
        - **Python 3.10+**: Linguagem principal
        - **Pandas**: Manipulação de dados
        - **Folium**: Mapas interativos
        - **Scikit-learn**: Algoritmos de clustering
        - **Streamlit**: Interface web
        - **Haversine**: Cálculo de distâncias geográficas
        
        ### 📊 Dados Utilizados
        
        O sistema utiliza um dataset com 25 locais de ecoturismo em Angola, incluindo:
        - Parques Nacionais
        - Reservas Naturais
        - Cachoeiras e formações naturais
        - Áreas de conservação
        
        Cada local possui informações sobre:
        - Coordenadas geográficas
        - Índice de fragilidade ambiental (1-5)
        - Capacidade diária de visitantes
        - Taxa de entrada em AOA
        - Tipo de ecossistema
        - Descrição detalhada
        
        ### 🎯 Impacto Esperado
        
        - **Para Turistas**: Rotas otimizadas e sustentáveis
        - **Para Operadores**: Planejamento eficiente e responsável
        - **Para Comunidades**: Turismo que preserva o meio ambiente
        - **Para Angola**: Promoção do ecoturismo como motor de desenvolvimento
        
        ### 📞 Contato
        
        Desenvolvido para o Hackathon FTL 2024
        **Sistema EcoRota Angola** - Promovendo Ecoturismo Sustentável
        """)
        
        # Estatísticas do dataset
        st.subheader("📈 Estatísticas do Dataset")
        
        if 'sistema' in st.session_state:
            df = sistema.df
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📍 Total de Locais", len(df))
            
            with col2:
                st.metric("🗺️ Províncias", df['provincia'].nunique())
            
            with col3:
                st.metric("🌿 Ecossistemas", df['tipo_ecosistema'].nunique())
            
            with col4:
                fragilidade_media = df['fragilidade'].mean()
                st.metric("🌱 Fragilidade Média", f"{fragilidade_media:.2f}")
            
            # Gráfico de distribuição por província
            st.subheader("🗺️ Distribuição por Província")
            provincias_count = df['provincia'].value_counts()
            fig_prov = px.bar(
                x=provincias_count.index,
                y=provincias_count.values,
                title="Número de Locais por Província",
                labels={'x': 'Província', 'y': 'Número de Locais'}
            )
            st.plotly_chart(fig_prov, use_container_width=True)


if __name__ == "__main__":
    main()
