#!/usr/bin/env python3
"""
Script de Demonstração do Sistema EcoRota Angola
===============================================

Este script demonstra as principais funcionalidades do sistema de forma
interativa e educativa, ideal para apresentações e demonstrações.

Execute com: python demo.py
"""

import sys
import os
from ecoturismo_system import EcoTurismoSystem
import time


def print_header():
    """Imprime o cabeçalho do sistema."""
    print("\n" + "="*80)
    print("🌍 SISTEMA DE ROTEIRO INTELIGENTE DE ECOTURISMO EM ANGOLA")
    print("="*80)
    print("🎯 Promovendo Turismo Sustentável e Responsável")
    print("🔬 Algoritmos Inteligentes para Preservação Ambiental")
    print("="*80)


def print_section(title, content):
    """Imprime uma seção formatada."""
    print(f"\n📋 {title}")
    print("-" * 60)
    for line in content:
        print(f"   {line}")
    print("-" * 60)


def demo_carregamento_dados():
    """Demonstra o carregamento de dados."""
    print_section("CARREGAMENTO DE DADOS", [
        "🔄 Carregando dataset de locais de ecoturismo...",
        "📊 Processando informações geográficas e ambientais...",
        "✅ Validação de critérios de sustentabilidade..."
    ])
    
    sistema = EcoTurismoSystem()
    df = sistema.carregar_dados()
    
    if df is not None:
        print(f"\n✅ Dados carregados com sucesso!")
        print(f"   📍 Total de locais: {len(df)}")
        print(f"   🗺️  Províncias: {df['provincia'].nunique()}")
        print(f"   🌿 Ecossistemas: {df['tipo_ecosistema'].nunique()}")
        print(f"   🌱 Fragilidade média: {df['fragilidade'].mean():.2f}/5")
        
        # Mostrar alguns exemplos
        print(f"\n📋 Exemplos de locais:")
        for i, row in df.head(3).iterrows():
            print(f"   • {row['nome']} ({row['provincia']}) - Fragilidade: {row['fragilidade']}")
    
    return sistema


def demo_filtros_sustentabilidade(sistema):
    """Demonstra os filtros de sustentabilidade."""
    print_section("FILTROS DE SUSTENTABILIDADE", [
        "🌱 Aplicando critérios de fragilidade ambiental...",
        "💰 Verificando viabilidade orçamental...",
        "📍 Otimizando distribuição geográfica..."
    ])
    
    df_sustentavel = sistema.filtrar_locais_sustentaveis(fragilidade_max=4)
    
    if df_sustentavel is not None:
        print(f"\n✅ Filtros aplicados com sucesso!")
        print(f"   🌱 Locais sustentáveis: {len(df_sustentavel)}")
        print(f"   📊 Taxa de aprovação: {len(df_sustentavel)/len(sistema.df)*100:.1f}%")
        
        # Distribuição por fragilidade
        fragilidade_dist = df_sustentavel['fragilidade'].value_counts().sort_index()
        print(f"\n📈 Distribuição por fragilidade:")
        for frag, count in fragilidade_dist.items():
            status = "🟢 Baixa" if frag <= 2 else "🟡 Média" if frag == 3 else "🔴 Alta"
            print(f"   • Fragilidade {frag}: {count} locais {status}")


def demo_algoritmo_rotas(sistema):
    """Demonstra o algoritmo de geração de rotas."""
    print_section("ALGORITMO DE GERAÇÃO DE ROTAS", [
        "🗺️  Aplicando clustering geográfico...",
        "🔍 Implementando algoritmo do vizinho mais próximo...",
        "⚖️  Calculando scores de sustentabilidade...",
        "🎯 Selecionando melhores rotas..."
    ])
    
    print(f"\n🔄 Gerando rotas recomendadas...")
    time.sleep(1)
    
    rotas = sistema.gerar_rotas_recomendadas(
        orcamento_max=20000,
        max_locais=6,
        fragilidade_max=4,
        num_rotas=5
    )
    
    if rotas:
        print(f"\n✅ {len(rotas)} rotas geradas com sucesso!")
        
        # Mostrar resumo das rotas
        print(f"\n📊 Resumo das rotas:")
        for i, rota in enumerate(rotas[:3], 1):  # Mostrar apenas as 3 melhores
            print(f"   {i}. {rota['nome']}")
            print(f"      🏃 {rota['distancia_total_km']} km | 💰 {rota['custo_total_aoa']:,} AOA | 🌱 {rota['fragilidade_media']}/5 | ⭐ {rota['score']}")
    
    return rotas


def demo_visualizacao(sistema):
    """Demonstra a criação de visualizações."""
    print_section("CRIAÇÃO DE VISUALIZAÇÕES", [
        "🗺️  Gerando mapa interativo com Folium...",
        "📍 Adicionando marcadores por fragilidade...",
        "🛣️  Desenhando rotas otimizadas...",
        "📊 Criando relatórios estruturados..."
    ])
    
    print(f"\n🔄 Criando visualizações...")
    time.sleep(1)
    
    # Criar mapa
    mapa = sistema.criar_mapa_interativo()
    if mapa:
        print(f"✅ Mapa interativo criado!")
    
    # Gerar relatórios
    csv_file = sistema.gerar_relatorio_csv()
    json_file = sistema.gerar_relatorio_json()
    
    if csv_file and json_file:
        print(f"✅ Relatórios gerados:")
        print(f"   📊 CSV: {csv_file}")
        print(f"   📋 JSON: {json_file}")


def demo_analise_resultados(sistema, rotas):
    """Demonstra a análise dos resultados."""
    print_section("ANÁLISE DOS RESULTADOS", [
        "📈 Calculando métricas de performance...",
        "🎯 Avaliando critérios de sustentabilidade...",
        "💡 Identificando insights importantes..."
    ])
    
    if not rotas:
        print("❌ Nenhuma rota disponível para análise.")
        return
    
    # Métricas gerais
    distancia_media = sum([r['distancia_total_km'] for r in rotas]) / len(rotas)
    custo_medio = sum([r['custo_total_aoa'] for r in rotas]) / len(rotas)
    fragilidade_media = sum([r['fragilidade_media'] for r in rotas]) / len(rotas)
    score_medio = sum([r['score'] for r in rotas]) / len(rotas)
    
    print(f"\n📊 Métricas Gerais:")
    print(f"   🏃 Distância média: {distancia_media:.1f} km")
    print(f"   💰 Custo médio: {custo_medio:,.0f} AOA")
    print(f"   🌱 Fragilidade média: {fragilidade_media:.2f}/5")
    print(f"   ⭐ Score médio: {score_medio:.3f}")
    
    # Melhor rota
    melhor_rota = min(rotas, key=lambda x: x['score'])
    print(f"\n🏆 Melhor Rota (menor score):")
    print(f"   📍 {melhor_rota['nome']}")
    print(f"   🏃 {melhor_rota['distancia_total_km']} km")
    print(f"   💰 {melhor_rota['custo_total_aoa']:,} AOA")
    print(f"   🌱 {melhor_rota['fragilidade_media']}/5")
    print(f"   ⭐ Score: {melhor_rota['score']}")
    
    # Diversidade
    todas_provincias = set()
    todos_ecossistemas = set()
    for rota in rotas:
        todas_provincias.update(rota['provincias'])
        todos_ecossistemas.update(rota['tipos_ecosistema'])
    
    print(f"\n🌍 Diversidade:")
    print(f"   🗺️  Províncias cobertas: {len(todas_provincias)}")
    print(f"   🌿 Ecossistemas: {len(todos_ecossistemas)}")


def demo_impacto_sustentabilidade():
    """Demonstra o impacto na sustentabilidade."""
    print_section("IMPACTO NA SUSTENTABILIDADE", [
        "🌱 Preservação ambiental através de critérios rigorosos",
        "💰 Otimização de recursos e custos",
        "🗺️  Distribuição equilibrada do turismo",
        "📚 Educação ambiental integrada"
    ])
    
    print(f"\n✅ Benefícios Alcançados:")
    print(f"   🌱 Fragilidade máxima respeitada (≤ 4)")
    print(f"   💰 Orçamento otimizado (≤ 20.000 AOA)")
    print(f"   🗺️  Rotas geograficamente distribuídas")
    print(f"   📊 Métricas de sustentabilidade quantificadas")
    print(f"   🎯 Algoritmo de otimização implementado")


def main():
    """Função principal da demonstração."""
    print_header()
    
    try:
        # 1. Carregamento de dados
        sistema = demo_carregamento_dados()
        if sistema is None:
            print("❌ Erro no carregamento de dados. Encerrando demonstração.")
            return
        
        time.sleep(2)
        
        # 2. Filtros de sustentabilidade
        demo_filtros_sustentabilidade(sistema)
        time.sleep(2)
        
        # 3. Algoritmo de rotas
        rotas = demo_algoritmo_rotas(sistema)
        if not rotas:
            print("❌ Erro na geração de rotas. Encerrando demonstração.")
            return
        
        time.sleep(2)
        
        # 4. Visualizações
        demo_visualizacao(sistema)
        time.sleep(2)
        
        # 5. Análise de resultados
        demo_analise_resultados(sistema, rotas)
        time.sleep(2)
        
        # 6. Impacto na sustentabilidade
        demo_impacto_sustentabilidade()
        
        # Resumo final
        print(f"\n" + "="*80)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*80)
        print("📁 Arquivos gerados:")
        print("   🗺️  mapa_ecoturismo_angola_*.html")
        print("   📊 relatorio_rotas_ecoturismo_*.csv")
        print("   📋 relatorio_detalhado_ecoturismo_*.json")
        print("\n💡 Próximos passos:")
        print("   • Abra o arquivo HTML para visualizar o mapa interativo")
        print("   • Consulte os relatórios CSV/JSON para análises detalhadas")
        print("   • Execute 'streamlit run app_streamlit.py' para interface web")
        print("="*80)
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Demonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        print("💡 Verifique se todos os arquivos necessários estão presentes.")


if __name__ == "__main__":
    main()
