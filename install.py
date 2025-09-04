#!/usr/bin/env python3
"""
Script de Instalação do EcoRota Angola
=====================================

Este script instala todas as dependências e configura o sistema.
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências do requirements.txt"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def test_imports():
    """Testa se todas as importações funcionam"""
    print("🔍 Testando importações...")
    try:
        import pandas as pd
        import folium
        import numpy as np
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.cluster import KMeans
        import haversine
        print("✅ Todas as importações funcionando!")
        return True
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        return False

def main():
    print("🌍 INSTALAÇÃO DO ECOROTA ANGOLA")
    print("="*40)
    
    if install_requirements() and test_imports():
        print("\n🎉 Instalação concluída com sucesso!")
        print("💡 Execute 'python demo_ml.py' para testar o sistema")
    else:
        print("\n❌ Instalação falhou. Verifique os erros acima.")

if __name__ == "__main__":
    main()
