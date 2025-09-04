#!/usr/bin/env python3
"""
Sistema de Logging para EcoRota Angola
=====================================

Este módulo contém configurações e utilitários para logging:
- Configuração de loggers
- Formatação de mensagens
- Rotação de arquivos de log
- Níveis de logging personalizados

Autor: Sistema EcoRota Angola
Data: 2024
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logger(name: str = "ecorota", 
                level: str = "INFO",
                log_file: Optional[str] = None,
                max_file_size: int = 10 * 1024 * 1024,  # 10MB
                backup_count: int = 5) -> logging.Logger:
    """
    Configura e retorna um logger para o sistema.
    
    Args:
        name: Nome do logger
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho do arquivo de log. Se None, usa configuração padrão.
        max_file_size: Tamanho máximo do arquivo de log em bytes
        backup_count: Número de arquivos de backup a manter
        
    Returns:
        Logger configurado
        
    Example:
        >>> logger = setup_logger("ecorota", "INFO")
        >>> logger.info("Sistema inicializado")
    """
    # Criar logger
    logger = logging.getLogger(name)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Configurar nível
    logger.setLevel(getattr(logging, level.upper()))
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        # Criar diretório de logs se não existir
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Handler com rotação
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "ecorota") -> logging.Logger:
    """
    Retorna um logger existente ou cria um novo.
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger
    """
    return logging.getLogger(name)


class EcoRotaLogger:
    """
    Classe para logging personalizado do sistema EcoRota.
    
    Esta classe fornece métodos específicos para logging
    de diferentes componentes do sistema.
    """
    
    def __init__(self, component_name: str):
        """
        Inicializa o logger personalizado.
        
        Args:
            component_name: Nome do componente
        """
        self.component_name = component_name
        self.logger = get_logger(f"ecorota.{component_name}")
    
    def system_start(self, version: str = "1.0.0"):
        """Log de inicialização do sistema."""
        self.logger.info(f"🚀 Sistema EcoRota Angola v{version} iniciado")
    
    def system_stop(self):
        """Log de finalização do sistema."""
        self.logger.info("🛑 Sistema EcoRota Angola finalizado")
    
    def data_loaded(self, count: int, source: str = "CSV"):
        """Log de carregamento de dados."""
        self.logger.info(f"📊 Dados carregados: {count} registros de {source}")
    
    def routes_generated(self, count: int, method: str = "tradicional"):
        """Log de geração de rotas."""
        self.logger.info(f"🗺️ Rotas geradas: {count} rotas ({method})")
    
    def ml_model_trained(self, performance: dict):
        """Log de treinamento de modelo ML."""
        r2 = performance.get('r2_score', 0)
        rmse = performance.get('rmse', 0)
        self.logger.info(f"🤖 Modelo ML treinado - R²: {r2:.3f}, RMSE: {rmse:.3f}")
    
    def map_created(self, locations: int, routes: int):
        """Log de criação de mapa."""
        self.logger.info(f"🗺️ Mapa criado: {locations} locais, {routes} rotas")
    
    def report_generated(self, report_type: str, filename: str):
        """Log de geração de relatório."""
        self.logger.info(f"📋 Relatório {report_type} gerado: {filename}")
    
    def error_occurred(self, error: Exception, context: str = ""):
        """Log de erro."""
        context_msg = f" em {context}" if context else ""
        self.logger.error(f"❌ Erro{context_msg}: {str(error)}")
    
    def warning_issued(self, message: str, context: str = ""):
        """Log de aviso."""
        context_msg = f" em {context}" if context else ""
        self.logger.warning(f"⚠️ Aviso{context_msg}: {message}")
    
    def performance_metric(self, metric_name: str, value: float, unit: str = ""):
        """Log de métrica de performance."""
        unit_msg = f" {unit}" if unit else ""
        self.logger.info(f"📈 {metric_name}: {value:.3f}{unit_msg}")


def log_function_call(func):
    """
    Decorator para logging de chamadas de função.
    
    Args:
        func: Função a ser decorada
        
    Returns:
        Função decorada
    """
    def wrapper(*args, **kwargs):
        logger = get_logger("ecorota.function")
        logger.debug(f"Chamando {func.__name__} com args={len(args)}, kwargs={len(kwargs)}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Função {func.__name__} executada com sucesso")
            return result
        except Exception as e:
            logger.error(f"Erro em {func.__name__}: {str(e)}")
            raise
    
    return wrapper


def log_execution_time(func):
    """
    Decorator para logging de tempo de execução.
    
    Args:
        func: Função a ser decorada
        
    Returns:
        Função decorada
    """
    def wrapper(*args, **kwargs):
        logger = get_logger("ecorota.performance")
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"⏱️ {func.__name__} executada em {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ {func.__name__} falhou após {execution_time:.3f}s: {str(e)}")
            raise
    
    return wrapper


if __name__ == "__main__":
    """Teste do sistema de logging."""
    
    # Teste básico
    logger = setup_logger("test", "DEBUG", "logs/test.log")
    
    print("🧪 Testando sistema de logging...")
    
    # Teste de diferentes níveis
    logger.debug("Mensagem de debug")
    logger.info("Mensagem de informação")
    logger.warning("Mensagem de aviso")
    logger.error("Mensagem de erro")
    
    # Teste do logger personalizado
    eco_logger = EcoRotaLogger("test")
    eco_logger.system_start("1.0.0")
    eco_logger.data_loaded(100, "CSV")
    eco_logger.routes_generated(5, "ML")
    eco_logger.performance_metric("Accuracy", 0.95, "%")
    eco_logger.system_stop()
    
    # Teste de decorators
    @log_function_call
    @log_execution_time
    def test_function(x, y):
        import time
        time.sleep(0.1)  # Simular processamento
        return x + y
    
    result = test_function(5, 3)
    print(f"Resultado da função: {result}")
    
    print("✅ Testes de logging concluídos!")
