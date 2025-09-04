#!/bin/bash

# Script para iniciar o Sistema EcoRota Angola
# Inclui API FastAPI e Frontend NextJS

echo "🌍 Iniciando Sistema EcoRota Angola..."
echo "=================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale Node.js 18+"
    exit 1
fi

# Verificar se npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Por favor, instale npm"
    exit 1
fi

echo "✅ Dependências básicas verificadas"

# Função para instalar dependências da API
install_api_deps() {
    echo "📦 Instalando dependências da API..."
    cd api
    if [ ! -d "venv" ]; then
        echo "🔧 Criando ambiente virtual Python..."
        python3 -m venv venv
    fi
    
    echo "🔧 Ativando ambiente virtual..."
    source venv/bin/activate
    
    echo "📦 Instalando dependências Python..."
    pip install -r requirements.txt
    
    cd ..
    echo "✅ Dependências da API instaladas"
}

# Função para instalar dependências do Frontend
install_frontend_deps() {
    echo "📦 Instalando dependências do Frontend..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "📦 Instalando dependências Node.js..."
        npm install
    else
        echo "✅ Dependências do Frontend já instaladas"
    fi
    
    cd ..
    echo "✅ Dependências do Frontend instaladas"
}

# Função para iniciar a API
start_api() {
    echo "🚀 Iniciando API FastAPI..."
    cd api
    source venv/bin/activate
    python run.py --reload &
    API_PID=$!
    cd ..
    echo "✅ API iniciada (PID: $API_PID)"
    echo "📚 Documentação: http://localhost:8000/docs"
}

# Função para iniciar o Frontend
start_frontend() {
    echo "🚀 Iniciando Frontend NextJS..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    echo "✅ Frontend iniciado (PID: $FRONTEND_PID)"
    echo "🌐 Aplicação: http://localhost:3000"
}

# Função para parar os serviços
cleanup() {
    echo ""
    echo "🛑 Parando serviços..."
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        echo "✅ API parada"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend parado"
    fi
    echo "👋 Sistema EcoRota Angola encerrado"
    exit 0
}

# Capturar Ctrl+C para cleanup
trap cleanup SIGINT

# Menu principal
echo ""
echo "Escolha uma opção:"
echo "1) Instalar dependências e iniciar sistema completo"
echo "2) Apenas iniciar sistema (dependências já instaladas)"
echo "3) Instalar apenas dependências"
echo "4) Sair"
echo ""

read -p "Digite sua escolha (1-4): " choice

case $choice in
    1)
        install_api_deps
        install_frontend_deps
        echo ""
        echo "🚀 Iniciando sistema completo..."
        start_api
        sleep 3
        start_frontend
        echo ""
        echo "🎉 Sistema EcoRota Angola iniciado com sucesso!"
        echo "🌐 Frontend: http://localhost:3000"
        echo "📚 API Docs: http://localhost:8000/docs"
        echo ""
        echo "Pressione Ctrl+C para parar o sistema"
        wait
        ;;
    2)
        start_api
        sleep 3
        start_frontend
        echo ""
        echo "🎉 Sistema EcoRota Angola iniciado com sucesso!"
        echo "🌐 Frontend: http://localhost:3000"
        echo "📚 API Docs: http://localhost:8000/docs"
        echo ""
        echo "Pressione Ctrl+C para parar o sistema"
        wait
        ;;
    3)
        install_api_deps
        install_frontend_deps
        echo "✅ Dependências instaladas. Execute novamente com opção 2 para iniciar."
        ;;
    4)
        echo "👋 Até logo!"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac
