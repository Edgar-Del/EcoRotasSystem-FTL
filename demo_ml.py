#!/usr/bin/env python3
"""
Demonstração do Sistema de Machine Learning para Ecoturismo
==========================================================

Este script demonstra as capacidades avançadas do sistema de ML,
incluindo personalização, clustering e recomendações colaborativas.

Execute com: python demo_ml.py
"""

import sys
import os
from ecoturismo_system import EcoTurismoSystem
import time
import numpy as np


def print_header():
    """Imprime o cabeçalho do sistema ML."""
    print("\n" + "="*80)
    print("🤖 SISTEMA DE MACHINE LEARNING PARA ECOTURISMO EM ANGOLA")
    print("="*80)
    print("🧠 Inteligência Artificial para Recomendações Personalizadas")
    print("🎯 Aprendizado de Máquina para Turismo Sustentável")
    print("="*80)


def print_section(title, content):
    """Imprime uma seção formatada."""
    print(f"\n📋 {title}")
    print("-" * 60)
    for line in content:
        print(f"   {line}")
    print("-" * 60)


def demo_inicializacao_ml():
    """Demonstra a inicialização do sistema ML."""
    print_section("INICIALIZAÇÃO DO SISTEMA ML", [
        "🤖 Carregando motor de Machine Learning...",
        "📊 Preparando dados para treinamento...",
        "🔧 Configurando algoritmos de ML...",
        "✅ Sistema ML inicializado com sucesso!"
    ])
    
    sistema = EcoTurismoSystem(use_ml=True)
    
    if sistema.carregar_dados() is None:
        print("❌ Erro no carregamento de dados. Encerrando demonstração.")
        return None
    
    print(f"✅ Sistema ML inicializado!")
    print(f"   📍 Locais disponíveis: {len(sistema.df)}")
    print(f"   🤖 Motor ML: {'Ativo' if sistema.ml_engine else 'Inativo'}")
    
    return sistema


def demo_treinamento_modelo(sistema):
    """Demonstra o treinamento do modelo ML."""
    print_section("TREINAMENTO DO MODELO ML", [
        "🔧 Criando features avançadas...",
        "👥 Gerando dados sintéticos de usuários...",
        "🎯 Treinando modelo de previsão de ratings...",
        "🔍 Criando clusters de locais similares...",
        "📊 Avaliando performance do modelo..."
    ])
    
    print(f"\n🔄 Iniciando treinamento do modelo...")
    time.sleep(1)
    
    # Criar features
    df_features = sistema.ml_engine.criar_features_engenharia()
    print(f"✅ Features criadas: {df_features.shape[1]} colunas")
    
    # Criar dados sintéticos
    df_usuarios = sistema.ml_engine.criar_dados_sinteticos_usuarios(n_usuarios=500)
    print(f"✅ Dados sintéticos: {len(df_usuarios)} interações")
    
    # Treinar modelo
    metrics = sistema.ml_engine.treinar_modelo_rating(df_usuarios)
    print(f"✅ Modelo treinado - R²: {metrics['r2_score']:.3f}")
    
    # Criar clusters
    cluster_info = sistema.ml_engine.criar_clusters_locais(df_features)
    print(f"✅ Clusters criados: {len(cluster_info)} grupos")
    
    return metrics, cluster_info


def demo_perfis_usuarios():
    """Demonstra diferentes perfis de usuários."""
    print_section("PERFIS DE USUÁRIOS DIVERSOS", [
        "👤 Criando perfis de usuários variados...",
        "🎯 Simulando preferências diferentes...",
        "📊 Analisando padrões de comportamento..."
    ])
    
    perfis = [
        {
            'nome': 'Eco-Turista Consciente',
            'idade': 28,
            'orcamento_max': 15000,
            'preferencia_sustentabilidade': 0.9,
            'preferencia_aventura': 0.7,
            'preferencia_cultura': 0.6
        },
        {
            'nome': 'Aventureiro Experiente',
            'idade': 35,
            'orcamento_max': 30000,
            'preferencia_sustentabilidade': 0.6,
            'preferencia_aventura': 0.9,
            'preferencia_cultura': 0.4
        },
        {
            'nome': 'Cultural Explorer',
            'idade': 45,
            'orcamento_max': 25000,
            'preferencia_sustentabilidade': 0.7,
            'preferencia_aventura': 0.3,
            'preferencia_cultura': 0.9
        },
        {
            'nome': 'Família com Crianças',
            'idade': 38,
            'orcamento_max': 20000,
            'preferencia_sustentabilidade': 0.8,
            'preferencia_aventura': 0.4,
            'preferencia_cultura': 0.7
        }
    ]
    
    print(f"\n👥 Perfis de usuários criados:")
    for perfil in perfis:
        print(f"   • {perfil['nome']}: Sustentabilidade {perfil['preferencia_sustentabilidade']:.1%}, "
              f"Aventura {perfil['preferencia_aventura']:.1%}, Cultura {perfil['preferencia_cultura']:.1%}")
    
    return perfis


def demo_recomendacoes_personalizadas(sistema, perfis):
    """Demonstra recomendações personalizadas para diferentes perfis."""
    print_section("RECOMENDAÇÕES PERSONALIZADAS", [
        "🎯 Gerando rotas para cada perfil de usuário...",
        "🤖 Aplicando algoritmo de ML personalizado...",
        "📊 Comparando resultados entre perfis...",
        "💡 Analisando insights de personalização..."
    ])
    
    resultados_perfis = {}
    
    for perfil in perfis:
        print(f"\n🔄 Processando perfil: {perfil['nome']}")
        time.sleep(0.5)
        
        # Gerar rotas personalizadas
        rotas = sistema.gerar_rotas_personalizadas_ml(
            user_profile=perfil,
            orcamento_max=perfil['orcamento_max'],
            max_locais=5,
            num_rotas=2
        )
        
        if rotas:
            # Analisar resultados
            rating_medio = np.mean([r.get('rating_medio_previsto', 0) for r in rotas])
            fragilidade_media = np.mean([r['fragilidade_media'] for r in rotas])
            custo_medio = np.mean([r['custo_total_aoa'] for r in rotas])
            
            resultados_perfis[perfil['nome']] = {
                'rotas': rotas,
                'rating_medio': rating_medio,
                'fragilidade_media': fragilidade_media,
                'custo_medio': custo_medio,
                'num_rotas': len(rotas)
            }
            
            print(f"   ✅ {len(rotas)} rotas geradas")
            print(f"   ⭐ Rating médio: {rating_medio:.2f}")
            print(f"   🌱 Fragilidade média: {fragilidade_media:.2f}")
            print(f"   💰 Custo médio: {custo_medio:,.0f} AOA")
    
    return resultados_perfis


def demo_analise_comparativa(resultados_perfis):
    """Demonstra análise comparativa entre perfis."""
    print_section("ANÁLISE COMPARATIVA ENTRE PERFIS", [
        "📊 Comparando métricas entre diferentes perfis...",
        "🔍 Identificando padrões de personalização...",
        "💡 Extraindo insights de comportamento..."
    ])
    
    print(f"\n📊 Comparação de Resultados:")
    print(f"{'Perfil':<25} {'Rating':<8} {'Fragilidade':<12} {'Custo':<12} {'Rotas':<6}")
    print("-" * 70)
    
    for nome, dados in resultados_perfis.items():
        print(f"{nome:<25} {dados['rating_medio']:<8.2f} {dados['fragilidade_media']:<12.2f} "
              f"{dados['custo_medio']:<12,.0f} {dados['num_rotas']:<6}")
    
    # Análise de insights
    print(f"\n💡 Insights de Personalização:")
    
    # Encontrar perfil com maior rating
    melhor_rating = max(resultados_perfis.items(), key=lambda x: x[1]['rating_medio'])
    print(f"   🏆 Melhor rating: {melhor_rating[0]} ({melhor_rating[1]['rating_medio']:.2f})")
    
    # Encontrar perfil mais sustentável
    mais_sustentavel = min(resultados_perfis.items(), key=lambda x: x[1]['fragilidade_media'])
    print(f"   🌱 Mais sustentável: {mais_sustentavel[0]} (fragilidade: {mais_sustentavel[1]['fragilidade_media']:.2f})")
    
    # Encontrar perfil mais econômico
    mais_economico = min(resultados_perfis.items(), key=lambda x: x[1]['custo_medio'])
    print(f"   💰 Mais econômico: {mais_economico[0]} ({mais_economico[1]['custo_medio']:,.0f} AOA)")


def demo_recomendacoes_colaborativas(sistema):
    """Demonstra sistema de recomendações colaborativas."""
    print_section("RECOMENDAÇÕES COLABORATIVAS", [
        "👥 Encontrando usuários com preferências similares...",
        "🔍 Aplicando filtragem colaborativa...",
        "📊 Analisando padrões de usuários similares...",
        "🎯 Gerando recomendações baseadas em comportamento..."
    ])
    
    # Simular diferentes usuários
    usuarios_teste = [42, 156, 289, 445, 678]
    
    print(f"\n👥 Testando recomendações colaborativas para {len(usuarios_teste)} usuários:")
    
    for user_id in usuarios_teste:
        print(f"\n🔄 Usuário {user_id}:")
        
        recomendacoes = sistema.obter_recomendacoes_colaborativas(user_id, 3)
        
        if recomendacoes:
            print(f"   ✅ {len(recomendacoes)} recomendações encontradas:")
            for i, rec in enumerate(recomendacoes, 1):
                print(f"      {i}. {rec['nome']} - Rating: {rec['rating_previsto']:.1f}")
        else:
            print(f"   ⚠️ Nenhuma recomendação encontrada")


def demo_visualizacoes_ml(sistema, resultados_perfis):
    """Demonstra visualizações específicas do ML."""
    print_section("VISUALIZAÇÕES DE MACHINE LEARNING", [
        "📊 Criando mapas com rotas personalizadas...",
        "📈 Gerando relatórios com insights de ML...",
        "🎯 Salvando análises de personalização..."
    ])
    
    print(f"\n🗺️ Criando visualizações ML...")
    
    # Criar mapa com rotas personalizadas
    if sistema.rotas_recomendadas:
        mapa = sistema.criar_mapa_interativo()
        if mapa:
            print(f"✅ Mapa interativo criado com rotas personalizadas")
    
    # Gerar relatórios
    csv_file = sistema.gerar_relatorio_csv()
    json_file = sistema.gerar_relatorio_json()
    
    if csv_file and json_file:
        print(f"✅ Relatórios gerados:")
        print(f"   📊 CSV: {csv_file}")
        print(f"   📋 JSON: {json_file}")
    
    # Salvar modelos ML
    sistema.ml_engine.salvar_modelos("demo_ml_models")
    print(f"💾 Modelos ML salvos para reutilização")


def demo_insights_avancados(sistema, resultados_perfis):
    """Demonstra insights avançados do sistema ML."""
    print_section("INSIGHTS AVANÇADOS DE ML", [
        "🧠 Analisando importância das features...",
        "🔍 Identificando padrões de comportamento...",
        "📊 Calculando métricas de personalização...",
        "💡 Extraindo insights de sustentabilidade..."
    ])
    
    # Feature importance
    if hasattr(sistema.ml_engine, 'feature_importance') and sistema.ml_engine.feature_importance:
        print(f"\n📊 Importância das Features no Modelo:")
        importance = sistema.ml_engine.feature_importance.get('rating', {})
        
        for feature, importance_score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {feature}: {importance_score:.3f}")
    
    # Análise de diversidade
    print(f"\n🌍 Análise de Diversidade:")
    todas_provincias = set()
    todos_ecossistemas = set()
    
    for dados in resultados_perfis.values():
        for rota in dados['rotas']:
            for local in rota['locais']:
                todas_provincias.add(local['provincia'])
                todos_ecossistemas.add(local['tipo_ecosistema'])
    
    print(f"   🗺️ Províncias cobertas: {len(todas_provincias)}")
    print(f"   🌿 Ecossistemas: {len(todos_ecossistemas)}")
    print(f"   📍 Locais únicos: {len(set([local['nome'] for dados in resultados_perfis.values() for rota in dados['rotas'] for local in rota['locais']]))}")
    
    # Métricas de personalização
    print(f"\n🎯 Métricas de Personalização:")
    ratings = [dados['rating_medio'] for dados in resultados_perfis.values()]
    print(f"   📊 Variação de ratings: {np.std(ratings):.3f}")
    print(f"   🎯 Rating médio geral: {np.mean(ratings):.3f}")
    print(f"   📈 Melhor rating: {np.max(ratings):.3f}")
    print(f"   📉 Pior rating: {np.min(ratings):.3f}")


def main():
    """Função principal da demonstração ML."""
    print_header()
    
    try:
        # 1. Inicialização
        sistema = demo_inicializacao_ml()
        if sistema is None:
            return
        
        time.sleep(2)
        
        # 2. Treinamento do modelo
        metrics, cluster_info = demo_treinamento_modelo(sistema)
        time.sleep(2)
        
        # 3. Perfis de usuários
        perfis = demo_perfis_usuarios()
        time.sleep(2)
        
        # 4. Recomendações personalizadas
        resultados_perfis = demo_recomendacoes_personalizadas(sistema, perfis)
        time.sleep(2)
        
        # 5. Análise comparativa
        demo_analise_comparativa(resultados_perfis)
        time.sleep(2)
        
        # 6. Recomendações colaborativas
        demo_recomendacoes_colaborativas(sistema)
        time.sleep(2)
        
        # 7. Visualizações ML
        demo_visualizacoes_ml(sistema, resultados_perfis)
        time.sleep(2)
        
        # 8. Insights avançados
        demo_insights_avancados(sistema, resultados_perfis)
        
        # Resumo final
        print(f"\n" + "="*80)
        print("🎉 DEMONSTRAÇÃO DE MACHINE LEARNING CONCLUÍDA!")
        print("="*80)
        print("🤖 Recursos ML Demonstrados:")
        print("   • Modelo de previsão de ratings (R²: {:.3f})".format(metrics['r2_score']))
        print("   • Sistema de clustering ({:d} clusters)".format(len(cluster_info)))
        print("   • Recomendações personalizadas para {:d} perfis".format(len(perfis)))
        print("   • Filtragem colaborativa")
        print("   • Análise de feature importance")
        print("\n📁 Arquivos gerados:")
        print("   🗺️ mapa_ecoturismo_angola_*.html")
        print("   📊 relatorio_rotas_ecoturismo_*.csv")
        print("   📋 relatorio_detalhado_ecoturismo_*.json")
        print("   💾 demo_ml_models_*.pkl")
        print("\n💡 Próximos passos:")
        print("   • Execute 'streamlit run app_ml_streamlit.py' para interface web")
        print("   • Use os modelos salvos para recomendações rápidas")
        print("   • Analise os insights de personalização")
        print("="*80)
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Demonstração ML interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração ML: {e}")
        print("💡 Verifique se todos os arquivos necessários estão presentes.")


if __name__ == "__main__":
    main()
