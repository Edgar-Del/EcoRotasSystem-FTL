#!/usr/bin/env python3
"""
Sistema Principal EcoRota Angola
===============================

Este é o arquivo principal para executar o sistema de recomendação
de rotas de ecoturismo sustentável em Angola.

Funcionalidades:
- Sistema tradicional de recomendação
- Sistema com Machine Learning
- Interface web interativa
- Demonstrações e testes

Autor: Sistema EcoRota Angola
Data: 2024
"""

import sys
import argparse
import logging
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.ecoturismo_system import EcoTurismoSystem
from src.utils.logger import setup_logger, EcoRotaLogger
from config.settings import get_config, validate_environment


def main():
    """Função principal do sistema."""
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Sistema EcoRota Angola - Recomendação de Rotas de Ecoturismo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --mode traditional                    # Sistema tradicional
  python main.py --mode ml --user-age 30               # Sistema ML com perfil
  python main.py --mode web                            # Interface web
  python main.py --mode demo                           # Demonstração
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['traditional', 'ml', 'web', 'demo'],
        default='demo',
        help='Modo de execução do sistema'
    )
    
    parser.add_argument(
        '--user-age',
        type=int,
        default=30,
        help='Idade do usuário para sistema ML'
    )
    
    parser.add_argument(
        '--budget',
        type=float,
        default=20000,
        help='Orçamento máximo em AOA'
    )
    
    parser.add_argument(
        '--max-locations',
        type=int,
        default=5,
        help='Número máximo de locais por rota'
    )
    
    parser.add_argument(
        '--num-routes',
        type=int,
        default=3,
        help='Número de rotas a gerar'
    )
    
    parser.add_argument(
        '--sustainability',
        type=float,
        default=0.8,
        help='Preferência por sustentabilidade (0-1)'
    )
    
    parser.add_argument(
        '--adventure',
        type=float,
        default=0.6,
        help='Preferência por aventura (0-1)'
    )
    
    parser.add_argument(
        '--culture',
        type=float,
        default=0.7,
        help='Preferência por cultura (0-1)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Nível de logging'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    logger = setup_logger("ecorota", args.log_level, "logs/ecorota.log")
    eco_logger = EcoRotaLogger("main")
    
    try:
        # Validar ambiente
        eco_logger.system_start("1.0.0")
        
        if not validate_environment():
            eco_logger.error_occurred(Exception("Ambiente inválido"), "validação")
            return 1
        
        # Executar modo selecionado
        if args.mode == 'traditional':
            return run_traditional_mode(args, eco_logger)
        elif args.mode == 'ml':
            return run_ml_mode(args, eco_logger)
        elif args.mode == 'web':
            return run_web_mode(args, eco_logger)
        elif args.mode == 'demo':
            return run_demo_mode(args, eco_logger)
        
    except KeyboardInterrupt:
        eco_logger.warning_issued("Execução interrompida pelo usuário")
        return 0
    except Exception as e:
        eco_logger.error_occurred(e, "execução principal")
        return 1
    finally:
        eco_logger.system_stop()


def run_traditional_mode(args, eco_logger):
    """Executa sistema tradicional."""
    try:
        eco_logger.info("Executando sistema tradicional...")
        
        # Inicializar sistema
        sistema = EcoTurismoSystem(use_ml=False)
        
        # Carregar dados
        df = sistema.load_data()
        eco_logger.data_loaded(len(df))
        
        # Gerar rotas
        rotas = sistema.generate_traditional_routes(
            max_budget=args.budget,
            max_locations=args.max_locations,
            num_routes=args.num_routes
        )
        eco_logger.routes_generated(len(rotas), "tradicional")
        
        # Criar visualizações
        mapa = sistema.create_interactive_map()
        eco_logger.map_created(len(df), len(rotas))
        
        # Gerar relatórios
        csv_file = sistema.generate_csv_report()
        json_file = sistema.generate_json_report()
        eco_logger.report_generated("CSV", csv_file.name)
        eco_logger.report_generated("JSON", json_file.name)
        
        # Imprimir resumo
        sistema.print_route_summary()
        
        return 0
        
    except Exception as e:
        eco_logger.error_occurred(e, "sistema tradicional")
        return 1


def run_ml_mode(args, eco_logger):
    """Executa sistema com ML."""
    try:
        eco_logger.info("Executando sistema com ML...")
        
        # Inicializar sistema
        sistema = EcoTurismoSystem(use_ml=True)
        
        # Carregar dados
        df = sistema.load_data()
        eco_logger.data_loaded(len(df))
        
        # Criar perfil do usuário
        user_profile = {
            'idade': args.user_age,
            'orcamento_max': args.budget,
            'preferencia_sustentabilidade': args.sustainability,
            'preferencia_aventura': args.adventure,
            'preferencia_cultura': args.culture
        }
        
        # Gerar rotas personalizadas
        rotas = sistema.generate_ml_routes(
            user_profile=user_profile,
            max_budget=args.budget,
            max_locations=args.max_locations,
            num_routes=args.num_routes
        )
        eco_logger.routes_generated(len(rotas), "ML")
        
        # Criar visualizações
        mapa = sistema.create_interactive_map()
        eco_logger.map_created(len(df), len(rotas))
        
        # Gerar relatórios
        csv_file = sistema.generate_csv_report()
        json_file = sistema.generate_json_report()
        eco_logger.report_generated("CSV", csv_file.name)
        eco_logger.report_generated("JSON", json_file.name)
        
        # Imprimir resumo
        sistema.print_route_summary()
        
        return 0
        
    except Exception as e:
        eco_logger.error_occurred(e, "sistema ML")
        return 1


def run_web_mode(args, eco_logger):
    """Executa interface web."""
    try:
        eco_logger.info("Iniciando interface web...")
        
        import subprocess
        import sys
        
        # Executar Streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "src/web/app_ml_streamlit.py"]
        subprocess.run(cmd)
        
        return 0
        
    except Exception as e:
        eco_logger.error_occurred(e, "interface web")
        return 1


def run_demo_mode(args, eco_logger):
    """Executa demonstração completa."""
    try:
        eco_logger.info("Executando demonstração completa...")
        
        print("\n" + "="*80)
        print("🌍 DEMONSTRAÇÃO DO SISTEMA ECOROTA ANGOLA")
        print("="*80)
        
        # Sistema tradicional
        print("\n📊 1. Sistema Tradicional")
        print("-" * 40)
        
        sistema_trad = EcoTurismoSystem(use_ml=False)
        df = sistema_trad.load_data()
        rotas_trad = sistema_trad.generate_traditional_routes(
            max_budget=args.budget,
            max_locations=args.max_locations,
            num_routes=2
        )
        
        print(f"✅ Rotas tradicionais geradas: {len(rotas_trad)}")
        
        # Sistema ML
        print("\n🤖 2. Sistema com Machine Learning")
        print("-" * 40)
        
        sistema_ml = EcoTurismoSystem(use_ml=True)
        sistema_ml.load_data()
        
        user_profile = {
            'idade': args.user_age,
            'orcamento_max': args.budget,
            'preferencia_sustentabilidade': args.sustainability,
            'preferencia_aventura': args.adventure,
            'preferencia_cultura': args.culture
        }
        
        rotas_ml = sistema_ml.generate_ml_routes(
            user_profile=user_profile,
            max_budget=args.budget,
            max_locations=args.max_locations,
            num_routes=2
        )
        
        print(f"✅ Rotas ML geradas: {len(rotas_ml)}")
        
        # Comparação
        print("\n📊 3. Comparação de Resultados")
        print("-" * 40)
        
        if rotas_trad and rotas_ml:
            print(f"Tradicional: {rotas_trad[0]['nome']} - Score: {rotas_trad[0].get('score', 'N/A')}")
            print(f"ML: {rotas_ml[0]['nome']} - Rating: {rotas_ml[0].get('rating_medio_previsto', 'N/A')}")
        
        # Visualizações
        print("\n🗺️ 4. Criando Visualizações")
        print("-" * 40)
        
        if rotas_ml:
            mapa = sistema_ml.create_interactive_map()
            csv_file = sistema_ml.generate_csv_report()
            json_file = sistema_ml.generate_json_report()
            
            print(f"✅ Mapa interativo criado")
            print(f"✅ Relatórios gerados: {csv_file.name}, {json_file.name}")
        
        # Estatísticas
        print("\n📈 5. Estatísticas do Sistema")
        print("-" * 40)
        
        stats = sistema_ml.get_system_statistics()
        print(f"• Total de locais: {stats.get('total_locations', 0)}")
        print(f"• Províncias: {stats.get('provinces', 0)}")
        print(f"• Ecossistemas: {stats.get('ecosystems', 0)}")
        print(f"• Modelo ML treinado: {'Sim' if stats.get('ml_model_trained') else 'Não'}")
        
        print("\n" + "="*80)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*80)
        print("💡 Próximos passos:")
        print("   • Abra o arquivo HTML para visualizar o mapa interativo")
        print("   • Consulte os relatórios CSV/JSON para análises detalhadas")
        print("   • Execute 'python main.py --mode web' para interface web")
        print("="*80)
        
        return 0
        
    except Exception as e:
        eco_logger.error_occurred(e, "demonstração")
        return 1


if __name__ == "__main__":
    sys.exit(main())
