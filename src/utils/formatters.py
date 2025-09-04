#!/usr/bin/env python3
"""
Formatadores de Dados para EcoRota Angola
========================================

Este módulo contém classes e funções para formatação de dados:
- Formatação de popups para mapas
- Formatação de relatórios
- Formatação de dados para visualização
- Formatação de saídas do sistema

Autor: Sistema EcoRota Angola
Data: 2024
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataFormatter:
    """
    Classe para formatação de dados do sistema EcoRota Angola.
    
    Esta classe fornece métodos para formatar dados de forma consistente
    em diferentes contextos: mapas, relatórios, visualizações, etc.
    """
    
    def __init__(self, config):
        """
        Inicializa o formatador de dados.
        
        Args:
            config: Instância de configuração do sistema
        """
        self.config = config
        logger.info("DataFormatter inicializado")
    
    def format_location_popup(self, location: Dict[str, Any]) -> str:
        """
        Formata popup para marcador de local no mapa.
        
        Args:
            location: Dicionário com dados do local
            
        Returns:
            String HTML formatada para popup
        """
        try:
            # Determinar status de fragilidade
            fragility = location.get('fragilidade', 0)
            if fragility <= 2:
                fragility_status = "🟢 Baixa"
            elif fragility == 3:
                fragility_status = "🟡 Média"
            else:
                fragility_status = "🔴 Alta"
            
            # Formatar popup
            popup_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 300px;">
                <h3 style="color: #2E8B57; margin: 0 0 10px 0;">{location.get('nome', 'N/A')}</h3>
                
                <div style="margin-bottom: 8px;">
                    <strong>📍 Província:</strong> {location.get('provincia', 'N/A')}
                </div>
                
                <div style="margin-bottom: 8px;">
                    <strong>🌿 Tipo:</strong> {location.get('tipo_ecosistema', 'N/A')}
                </div>
                
                <div style="margin-bottom: 8px;">
                    <strong>🌱 Fragilidade:</strong> {fragility}/5 {fragility_status}
                </div>
                
                <div style="margin-bottom: 8px;">
                    <strong>👥 Capacidade:</strong> {location.get('capacidade_diaria', 'N/A')} pessoas/dia
                </div>
                
                <div style="margin-bottom: 8px;">
                    <strong>💰 Taxa:</strong> {self._format_currency(location.get('taxa_aoa', 0))} AOA
                </div>
                
                <div style="margin-top: 10px; font-style: italic; color: #666;">
                    {location.get('descricao', 'Sem descrição disponível')}
                </div>
            </div>
            """
            
            return popup_html
            
        except Exception as e:
            logger.error(f"Erro ao formatar popup do local: {e}")
            return f"<div>Erro ao carregar informações do local</div>"
    
    def format_route_popup(self, route: Dict[str, Any]) -> str:
        """
        Formata popup para linha de rota no mapa.
        
        Args:
            route: Dicionário com dados da rota
            
        Returns:
            String HTML formatada para popup
        """
        try:
            popup_html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 300px;">
                <h3 style="color: #2E8B57; margin: 0 0 10px 0;">{route.get('nome', 'Rota')}</h3>
                
                <div style="margin-bottom: 8px;">
                    <strong>🏃 Distância:</strong> {route.get('distancia_total_km', 0):.1f} km
                </div>
                
                <div style="margin-bottom: 8px;">
                    <strong>💰 Custo Total:</strong> {self._format_currency(route.get('custo_total_aoa', 0))} AOA
                </div>
                
                <div style="margin-bottom: 8px;">
                    <strong>🌱 Fragilidade Média:</strong> {route.get('fragilidade_media', 0):.1f}/5
                </div>
                
                <div style="margin-bottom: 8px;">
                    <strong>📍 Locais:</strong> {route.get('num_locais', 0)}
                </div>
                
                {self._format_route_score(route)}
                
                <div style="margin-top: 10px; font-size: 12px; color: #666;">
                    Clique nos marcadores para ver detalhes dos locais
                </div>
            </div>
            """
            
            return popup_html
            
        except Exception as e:
            logger.error(f"Erro ao formatar popup da rota: {e}")
            return f"<div>Erro ao carregar informações da rota</div>"
    
    def _format_route_score(self, route: Dict[str, Any]) -> str:
        """
        Formata seção de score da rota.
        
        Args:
            route: Dicionário com dados da rota
            
        Returns:
            String HTML formatada para score
        """
        if 'score' in route:
            return f'<div style="margin-bottom: 8px;"><strong>⭐ Score:</strong> {route["score"]:.3f}</div>'
        elif 'rating_medio_previsto' in route:
            return f'<div style="margin-bottom: 8px;"><strong>🤖 Rating ML:</strong> {route["rating_medio_previsto"]:.1f}/5</div>'
        elif 'score_personalizado' in route:
            return f'<div style="margin-bottom: 8px;"><strong>🎯 Score Personalizado:</strong> {route["score_personalizado"]:.2f}</div>'
        else:
            return ""
    
    def format_route_for_csv(self, route: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formata dados da rota para exportação CSV.
        
        Args:
            route: Dicionário com dados da rota
            
        Returns:
            Dicionário formatado para CSV
        """
        try:
            # Extrair informações básicas
            csv_data = {
                'nome_rota': route.get('nome', 'N/A'),
                'num_locais': route.get('num_locais', 0),
                'distancia_total_km': round(route.get('distancia_total_km', 0), 2),
                'custo_total_aoa': route.get('custo_total_aoa', 0),
                'fragilidade_media': round(route.get('fragilidade_media', 0), 2),
                'provincias': '; '.join(route.get('provincias', [])),
                'tipos_ecosistema': '; '.join(route.get('tipos_ecosistema', [])),
                'locais_visitados': '; '.join([loc['nome'] for loc in route.get('locais', [])])
            }
            
            # Adicionar scores específicos
            if 'score' in route:
                csv_data['score'] = round(route['score'], 3)
            elif 'rating_medio_previsto' in route:
                csv_data['rating_medio_previsto'] = round(route['rating_medio_previsto'], 2)
            elif 'score_personalizado' in route:
                csv_data['score_personalizado'] = round(route['score_personalizado'], 2)
            
            return csv_data
            
        except Exception as e:
            logger.error(f"Erro ao formatar rota para CSV: {e}")
            return {}
    
    def format_user_profile_summary(self, profile: Dict[str, Any]) -> str:
        """
        Formata resumo do perfil do usuário.
        
        Args:
            profile: Dicionário com perfil do usuário
            
        Returns:
            String formatada com resumo do perfil
        """
        try:
            summary = f"""
            👤 Perfil do Usuário:
            • Idade: {profile.get('idade', 'N/A')} anos
            • Orçamento: {self._format_currency(profile.get('orcamento_max', 0))} AOA
            • Sustentabilidade: {profile.get('preferencia_sustentabilidade', 0):.1%}
            • Aventura: {profile.get('preferencia_aventura', 0):.1%}
            • Cultura: {profile.get('preferencia_cultura', 0):.1%}
            """
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Erro ao formatar resumo do perfil: {e}")
            return "Erro ao formatar perfil do usuário"
    
    def format_statistics_summary(self, stats: Dict[str, Any]) -> str:
        """
        Formata resumo de estatísticas do sistema.
        
        Args:
            stats: Dicionário com estatísticas
            
        Returns:
            String formatada com resumo das estatísticas
        """
        try:
            summary = f"""
            📊 Estatísticas do Sistema:
            • Total de Locais: {stats.get('total_locations', 0)}
            • Províncias: {stats.get('provinces', 0)}
            • Ecossistemas: {stats.get('ecosystems', 0)}
            • Fragilidade Média: {stats.get('avg_fragility', 0):.2f}/5
            • Custo Médio: {self._format_currency(stats.get('avg_cost', 0))} AOA
            • Capacidade Média: {stats.get('avg_capacity', 0):.0f} pessoas/dia
            """
            
            if stats.get('ml_model_trained'):
                summary += f"\n• Modelo ML: ✅ Treinado"
                if 'ml_features' in stats:
                    summary += f" ({stats['ml_features']} features)"
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Erro ao formatar resumo de estatísticas: {e}")
            return "Erro ao formatar estatísticas"
    
    def format_route_comparison(self, routes: List[Dict[str, Any]]) -> str:
        """
        Formata comparação entre rotas.
        
        Args:
            routes: Lista de dicionários com dados das rotas
            
        Returns:
            String formatada com comparação
        """
        try:
            if not routes:
                return "Nenhuma rota para comparar"
            
            comparison = "📊 Comparação de Rotas:\n\n"
            
            for i, route in enumerate(routes, 1):
                comparison += f"📍 Rota {i}: {route.get('nome', 'N/A')}\n"
                comparison += f"   🏃 {route.get('distancia_total_km', 0):.1f} km | "
                comparison += f"💰 {self._format_currency(route.get('custo_total_aoa', 0))} AOA | "
                comparison += f"🌱 {route.get('fragilidade_media', 0):.1f}/5 | "
                comparison += f"📍 {route.get('num_locais', 0)} locais\n"
                
                if 'score' in route:
                    comparison += f"   ⭐ Score: {route['score']:.3f}\n"
                elif 'rating_medio_previsto' in route:
                    comparison += f"   🤖 Rating ML: {route['rating_medio_previsto']:.1f}/5\n"
                
                comparison += "\n"
            
            return comparison.strip()
            
        except Exception as e:
            logger.error(f"Erro ao formatar comparação de rotas: {e}")
            return "Erro ao formatar comparação"
    
    def _format_currency(self, amount: float) -> str:
        """
        Formata valor monetário em AOA.
        
        Args:
            amount: Valor em AOA
            
        Returns:
            String formatada com valor monetário
        """
        try:
            if amount >= 1000000:
                return f"{amount/1000000:.1f}M"
            elif amount >= 1000:
                return f"{amount/1000:.0f}K"
            else:
                return f"{amount:,.0f}"
        except:
            return "N/A"
    
    def format_ml_insights(self, insights: Dict[str, Any]) -> str:
        """
        Formata insights do sistema de ML.
        
        Args:
            insights: Dicionário com insights de ML
            
        Returns:
            String formatada com insights
        """
        try:
            formatted_insights = "🤖 Insights de Machine Learning:\n\n"
            
            if 'model_performance' in insights:
                perf = insights['model_performance']
                formatted_insights += f"📊 Performance do Modelo:\n"
                formatted_insights += f"• R² Score: {perf.get('r2_score', 0):.3f}\n"
                formatted_insights += f"• RMSE: {perf.get('rmse', 0):.3f}\n\n"
            
            if 'feature_importance' in insights:
                formatted_insights += f"🔍 Features Mais Importantes:\n"
                importance = insights['feature_importance']
                for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True)[:5]:
                    formatted_insights += f"• {feature}: {score:.3f}\n"
                formatted_insights += "\n"
            
            if 'clusters' in insights:
                formatted_insights += f"🗺️ Clusters de Locais: {insights['clusters']}\n\n"
            
            if 'personalization_metrics' in insights:
                metrics = insights['personalization_metrics']
                formatted_insights += f"🎯 Métricas de Personalização:\n"
                formatted_insights += f"• Variação de Ratings: {metrics.get('rating_variation', 0):.3f}\n"
                formatted_insights += f"• Rating Médio: {metrics.get('avg_rating', 0):.3f}\n"
            
            return formatted_insights.strip()
            
        except Exception as e:
            logger.error(f"Erro ao formatar insights de ML: {e}")
            return "Erro ao formatar insights de ML"


def format_duration(seconds: float) -> str:
    """
    Formata duração em segundos para formato legível.
    
    Args:
        seconds: Duração em segundos
        
    Returns:
        String formatada com duração
    """
    try:
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}min"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    except:
        return "N/A"


def format_file_size(bytes_size: int) -> str:
    """
    Formata tamanho de arquivo em bytes para formato legível.
    
    Args:
        bytes_size: Tamanho em bytes
        
    Returns:
        String formatada com tamanho
    """
    try:
        if bytes_size < 1024:
            return f"{bytes_size}B"
        elif bytes_size < 1024**2:
            return f"{bytes_size/1024:.1f}KB"
        elif bytes_size < 1024**3:
            return f"{bytes_size/(1024**2):.1f}MB"
        else:
            return f"{bytes_size/(1024**3):.1f}GB"
    except:
        return "N/A"


if __name__ == "__main__":
    """Teste dos formatadores."""
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Teste básico
    from config.settings import get_config
    config = get_config()
    formatter = DataFormatter(config)
    
    print("🧪 Testando formatadores...")
    
    # Dados de teste
    test_location = {
        'nome': 'Parque Nacional da Kissama',
        'provincia': 'Luanda',
        'tipo_ecosistema': 'savana',
        'fragilidade': 3,
        'capacidade_diaria': 150,
        'taxa_aoa': 25000,
        'descricao': 'Reserva natural com elefantes e búfalos'
    }
    
    test_route = {
        'nome': 'Rota Teste',
        'distancia_total_km': 1250.5,
        'custo_total_aoa': 75000,
        'fragilidade_media': 2.5,
        'num_locais': 4,
        'score': 2.847
    }
    
    test_profile = {
        'idade': 30,
        'orcamento_max': 20000,
        'preferencia_sustentabilidade': 0.8,
        'preferencia_aventura': 0.6,
        'preferencia_cultura': 0.7
    }
    
    # Teste de formatação
    popup = formatter.format_location_popup(test_location)
    print(f"✅ Popup formatado: {len(popup)} caracteres")
    
    route_popup = formatter.format_route_popup(test_route)
    print(f"✅ Popup de rota formatado: {len(route_popup)} caracteres")
    
    csv_data = formatter.format_route_for_csv(test_route)
    print(f"✅ Dados CSV formatados: {len(csv_data)} campos")
    
    profile_summary = formatter.format_user_profile_summary(test_profile)
    print(f"✅ Resumo do perfil formatado")
    
    print("✅ Testes dos formatadores concluídos!")
