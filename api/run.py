#!/usr/bin/env python3
"""
Script para executar a API EcoRota Angola
=========================================

Script simples para iniciar o servidor FastAPI com configurações otimizadas.

Uso:
    python run.py                    # Modo desenvolvimento
    python run.py --prod             # Modo produção
    python run.py --port 8080        # Porta customizada
"""

import argparse
import uvicorn
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Executar API EcoRota Angola")
    parser.add_argument("--host", default="0.0.0.0", help="Host para bind")
    parser.add_argument("--port", type=int, default=8000, help="Porta para bind")
    parser.add_argument("--reload", action="store_true", help="Modo desenvolvimento com reload")
    parser.add_argument("--prod", action="store_true", help="Modo produção")
    parser.add_argument("--workers", type=int, default=1, help="Número de workers (apenas produção)")
    
    args = parser.parse_args()
    
    # Configurações baseadas no modo
    if args.prod:
        # Modo produção
        config = {
            "host": args.host,
            "port": args.port,
            "workers": args.workers,
            "log_level": "info",
            "access_log": True
        }
        print(f"🚀 Iniciando API EcoRota Angola em modo PRODUÇÃO")
        print(f"   Host: {args.host}:{args.port}")
        print(f"   Workers: {args.workers}")
    else:
        # Modo desenvolvimento
        config = {
            "host": args.host,
            "port": args.port,
            "reload": True,
            "log_level": "info",
            "access_log": True
        }
        print(f"🔧 Iniciando API EcoRota Angola em modo DESENVOLVIMENTO")
        print(f"   Host: {args.host}:{args.port}")
        print(f"   Reload: Habilitado")
    
    print(f"📚 Documentação: http://{args.host}:{args.port}/docs")
    print(f"🔍 ReDoc: http://{args.host}:{args.port}/redoc")
    print("=" * 50)
    
    try:
        uvicorn.run("main:app", **config)
    except KeyboardInterrupt:
        print("\n👋 API encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
