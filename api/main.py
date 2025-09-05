#!/usr/bin/env python3
"""
API FastAPI para o Sistema EcoRota Angola
=========================================

API REST moderna para o sistema de recomendação de rotas de ecoturismo sustentável.
Substitui a interface Streamlit por uma API que pode ser consumida por qualquer frontend.

Funcionalidades:
- Endpoints para geração de rotas (tradicional e ML)
- Sistema de autenticação JWT
- Documentação automática com Swagger
- CORS habilitado para frontend React
- Validação de dados com Pydantic
- Logging estruturado

Autor: Grupo 01 UNDP FTL
Data: 2025
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

# Adicionar diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn

# Imports do sistema EcoRota
try:
    from src.core.ecoturismo_system import EcoTurismoSystem
    from config.settings import get_config
    SYSTEM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Sistema EcoTurismo não disponível: {e}")
    SYSTEM_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="EcoRota Angola API",
    description="API para sistema de recomendação de rotas de ecoturismo sustentável em Angola",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # NextJS default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sistema de autenticação simples (JWT)
security = HTTPBearer()

# Instância global do sistema (singleton)
ecoturismo_system: Optional[EcoTurismoSystem] = None

# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class UserProfile(BaseModel):
    """Perfil do usuário para sistema ML."""
    idade: int = Field(..., ge=18, le=100, description="Idade do usuário")
    orcamento_max: float = Field(..., gt=0, description="Orçamento máximo em AOA")
    preferencia_sustentabilidade: float = Field(..., ge=0, le=1, description="Preferência por sustentabilidade (0-1)")
    preferencia_aventura: float = Field(..., ge=0, le=1, description="Preferência por aventura (0-1)")
    preferencia_cultura: float = Field(..., ge=0, le=1, description="Preferência por cultura (0-1)")

class RouteRequest(BaseModel):
    """Parâmetros para geração de rotas tradicionais."""
    max_budget: float = Field(20000, gt=0, description="Orçamento máximo em AOA")
    max_locations: int = Field(5, ge=2, le=10, description="Número máximo de locais por rota")
    max_fragility: int = Field(4, ge=1, le=5, description="Fragilidade máxima permitida")
    num_routes: int = Field(3, ge=1, le=10, description="Número de rotas a gerar")

class MLRouteRequest(BaseModel):
    """Parâmetros para geração de rotas com ML."""
    user_profile: UserProfile
    max_locations: int = Field(5, ge=2, le=10, description="Número máximo de locais por rota")
    num_routes: int = Field(3, ge=1, le=10, description="Número de rotas a gerar")

class RouteResponse(BaseModel):
    """Resposta com rotas geradas."""
    success: bool
    message: str
    routes: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class SystemStatsResponse(BaseModel):
    """Estatísticas do sistema."""
    success: bool
    stats: Dict[str, Any]

class HealthResponse(BaseModel):
    """Resposta de health check."""
    status: str
    timestamp: datetime
    version: str

# ============================================================================
# DEPENDÊNCIAS
# ============================================================================

def get_ecoturismo_system() -> EcoTurismoSystem:
    """Dependency para obter instância do sistema."""
    if not SYSTEM_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sistema EcoTurismo não disponível"
        )
    
    global ecoturismo_system
    if ecoturismo_system is None:
        try:
            ecoturismo_system = EcoTurismoSystem(use_ml=True)
            ecoturismo_system.load_data()
            logger.info("Sistema EcoTurismo inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao inicializar sistema de ecoturismo"
            )
    return ecoturismo_system

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificação simples de token (implementação básica)."""
    # Em produção, implementar verificação JWT real
    if credentials.credentials != "demo-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    return credentials.credentials

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Endpoint raiz com informações básicas."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(system: EcoTurismoSystem = Depends(get_ecoturismo_system)):
    """Obter estatísticas do sistema."""
    try:
        stats = system.get_system_statistics()
        return SystemStatsResponse(
            success=True,
            stats=stats
        )
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter estatísticas do sistema"
        )

@app.post("/routes/traditional", response_model=RouteResponse)
async def generate_traditional_routes(
    request: RouteRequest,
    system: EcoTurismoSystem = Depends(get_ecoturismo_system)
):
    """Gerar rotas usando algoritmo tradicional."""
    try:
        logger.info(f"Gerando rotas tradicionais: {request.dict()}")
        
        routes = system.generate_traditional_routes(
            max_budget=request.max_budget,
            max_locations=request.max_locations,
            max_fragility=request.max_fragility,
            num_routes=request.num_routes
        )
        
        if not routes:
            return RouteResponse(
                success=False,
                message="Nenhuma rota encontrada com os critérios especificados",
                routes=[],
                metadata={"request": request.dict()}
            )
        
        # Criar mapa interativo
        map_data = system.create_interactive_map(save_html=False)
        
        return RouteResponse(
            success=True,
            message=f"Geradas {len(routes)} rotas tradicionais com sucesso",
            routes=routes,
            metadata={
                "request": request.dict(),
                "total_routes": len(routes),
                "map_created": map_data is not None,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao gerar rotas tradicionais: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar rotas: {str(e)}"
        )

@app.post("/routes/ml", response_model=RouteResponse)
async def generate_ml_routes(
    request: MLRouteRequest,
    system: EcoTurismoSystem = Depends(get_ecoturismo_system)
):
    """Gerar rotas usando Machine Learning."""
    try:
        logger.info(f"Gerando rotas ML: {request.user_profile.dict()}")
        
        routes = system.generate_ml_routes(
            user_profile=request.user_profile.dict(),
            max_locations=request.max_locations,
            num_routes=request.num_routes
        )
        
        if not routes:
            return RouteResponse(
                success=False,
                message="Nenhuma rota encontrada com os critérios especificados",
                routes=[],
                metadata={"request": request.dict()}
            )
        
        # Criar mapa interativo
        map_data = system.create_interactive_map(save_html=False)
        
        return RouteResponse(
            success=True,
            message=f"Geradas {len(routes)} rotas personalizadas com ML",
            routes=routes,
            metadata={
                "request": request.dict(),
                "total_routes": len(routes),
                "map_created": map_data is not None,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao gerar rotas ML: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar rotas ML: {str(e)}"
        )

@app.get("/routes/export/csv")
async def export_csv_report(
    system: EcoTurismoSystem = Depends(get_ecoturismo_system)
):
    """Exportar relatório CSV das rotas."""
    try:
        if not system.recommended_routes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhuma rota disponível para exportação"
            )
        
        csv_file = system.generate_csv_report()
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Relatório CSV gerado com sucesso",
                "file_path": str(csv_file),
                "filename": csv_file.name
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao exportar CSV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao exportar CSV: {str(e)}"
        )

@app.get("/routes/export/json")
async def export_json_report(
    system: EcoTurismoSystem = Depends(get_ecoturismo_system)
):
    """Exportar relatório JSON das rotas."""
    try:
        if not system.recommended_routes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhuma rota disponível para exportação"
            )
        
        json_file = system.generate_json_report()
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Relatório JSON gerado com sucesso",
                "file_path": str(json_file),
                "filename": json_file.name
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao exportar JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao exportar JSON: {str(e)}"
        )

@app.get("/locations")
async def get_locations(
    system: EcoTurismoSystem = Depends(get_ecoturismo_system)
):
    """Obter lista de todos os locais de ecoturismo."""
    try:
        if system.df is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados não carregados"
            )
        
        # Converter DataFrame para lista de dicionários
        locations = system.df.to_dict('records')
        
        return JSONResponse(
            content={
                "success": True,
                "message": f"Encontrados {len(locations)} locais",
                "locations": locations,
                "total": len(locations)
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter locais: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter locais: {str(e)}"
        )

@app.get("/locations/{location_id}")
async def get_location(
    location_id: int,
    system: EcoTurismoSystem = Depends(get_ecoturismo_system)
):
    """Obter detalhes de um local específico."""
    try:
        if system.df is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados não carregados"
            )
        
        if location_id < 0 or location_id >= len(system.df):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Local não encontrado"
            )
        
        location = system.df.iloc[location_id].to_dict()
        
        return JSONResponse(
            content={
                "success": True,
                "message": "Local encontrado",
                "location": location
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter local {location_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter local: {str(e)}"
        )

# ============================================================================
# MIDDLEWARE DE TRATAMENTO DE ERROS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global para exceções não tratadas."""
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "detail": str(exc) if app.debug else "Erro interno"
        }
    )

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação."""
    logger.info("Iniciando API EcoRota Angola...")
    
    if SYSTEM_AVAILABLE:
        # Inicializar sistema
        global ecoturismo_system
        try:
            ecoturismo_system = EcoTurismoSystem(use_ml=True)
            ecoturismo_system.load_data()
            logger.info("Sistema EcoTurismo inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema: {e}")
    else:
        logger.warning("Sistema EcoTurismo não disponível - API funcionará em modo limitado")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de encerramento da aplicação."""
    logger.info("Encerrando API EcoRota Angola...")

# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
