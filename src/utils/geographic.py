#!/usr/bin/env python3
"""
Calculadora Geográfica para EcoRota Angola
=========================================

Este módulo contém funções para cálculos geográficos, incluindo:
- Cálculo de distâncias entre coordenadas
- Otimização de rotas geográficas
- Análise de proximidade e clustering
- Conversões de coordenadas

Autor: Sistema EcoRota Angola
Data: 2024
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from haversine import haversine
import logging

logger = logging.getLogger(__name__)


class GeographicCalculator:
    """
    Classe para cálculos geográficos e otimização de rotas.
    
    Esta classe fornece métodos para:
    - Calcular distâncias entre pontos geográficos
    - Otimizar rotas usando algoritmo do vizinho mais próximo
    - Analisar proximidade e densidade de locais
    - Converter coordenadas e formatos
    """
    
    def __init__(self, reference_point: Optional[Tuple[float, float]] = None):
        """
        Inicializa a calculadora geográfica.
        
        Args:
            reference_point: Ponto de referência (lat, lon) para cálculos relativos.
                           Se None, usa Luanda como padrão.
        """
        self.reference_point = reference_point or (-8.8390, 13.2894)  # Luanda
        logger.info(f"Calculadora geográfica inicializada com ponto de referência: {self.reference_point}")
    
    def calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """
        Calcula a distância entre duas coordenadas geográficas usando a fórmula de Haversine.
        
        A fórmula de Haversine é usada para calcular a distância entre dois pontos
        na superfície de uma esfera (Terra) considerando sua curvatura.
        
        Args:
            coord1: Tupla (latitude, longitude) do primeiro ponto
            coord2: Tupla (latitude, longitude) do segundo ponto
            
        Returns:
            Distância em quilômetros
            
        Raises:
            ValueError: Se as coordenadas forem inválidas
            
        Example:
            >>> calc = GeographicCalculator()
            >>> dist = calc.calculate_distance((-8.8390, 13.2894), (-9.0833, 16.0167))
            >>> print(f"Distância: {dist:.2f} km")
        """
        try:
            # Validar coordenadas
            self._validate_coordinates(coord1)
            self._validate_coordinates(coord2)
            
            # Calcular distância usando Haversine
            distance = haversine(coord1, coord2)
            
            logger.debug(f"Distância calculada: {coord1} -> {coord2} = {distance:.2f} km")
            return distance
            
        except Exception as e:
            logger.error(f"Erro ao calcular distância entre {coord1} e {coord2}: {e}")
            raise
    
    def calculate_distance_matrix(self, coordinates: List[Tuple[float, float]]) -> np.ndarray:
        """
        Calcula matriz de distâncias entre todos os pares de coordenadas.
        
        Esta função é otimizada para calcular distâncias entre múltiplos pontos,
        útil para algoritmos de otimização de rotas.
        
        Args:
            coordinates: Lista de tuplas (latitude, longitude)
            
        Returns:
            Matriz numpy de distâncias (n x n)
            
        Example:
            >>> coords = [(-8.8390, 13.2894), (-9.0833, 16.0167), (-16.7500, 12.2500)]
            >>> matrix = calc.calculate_distance_matrix(coords)
            >>> print(f"Matriz de distâncias: {matrix.shape}")
        """
        try:
            n = len(coordinates)
            distance_matrix = np.zeros((n, n))
            
            # Calcular distâncias entre todos os pares
            for i in range(n):
                for j in range(i + 1, n):
                    distance = self.calculate_distance(coordinates[i], coordinates[j])
                    distance_matrix[i, j] = distance
                    distance_matrix[j, i] = distance  # Matriz simétrica
            
            logger.info(f"Matriz de distâncias calculada: {n}x{n}")
            return distance_matrix
            
        except Exception as e:
            logger.error(f"Erro ao calcular matriz de distâncias: {e}")
            raise
    
    def nearest_neighbor_route(self, coordinates: List[Tuple[float, float]], 
                             start_index: int = 0) -> List[int]:
        """
        Otimiza rota usando algoritmo do vizinho mais próximo.
        
        O algoritmo do vizinho mais próximo é uma heurística simples mas eficaz
        para o problema do caixeiro viajante (TSP). Embora não garanta a solução
        ótima, é computacionalmente eficiente e produz resultados razoáveis.
        
        Args:
            coordinates: Lista de coordenadas (latitude, longitude)
            start_index: Índice do ponto de partida
            
        Returns:
            Lista de índices ordenados pela rota otimizada
            
        Example:
            >>> coords = [(-8.8390, 13.2894), (-9.0833, 16.0167), (-16.7500, 12.2500)]
            >>> route = calc.nearest_neighbor_route(coords, start_index=0)
            >>> print(f"Rota otimizada: {route}")
        """
        try:
            if len(coordinates) <= 1:
                return [0]
            
            n = len(coordinates)
            visited = [False] * n
            route = [start_index]
            visited[start_index] = True
            current = start_index
            
            # Algoritmo do vizinho mais próximo
            for _ in range(n - 1):
                min_distance = float('inf')
                next_index = -1
                
                # Encontrar o vizinho mais próximo não visitado
                for i in range(n):
                    if not visited[i]:
                        distance = self.calculate_distance(
                            coordinates[current], 
                            coordinates[i]
                        )
                        
                        if distance < min_distance:
                            min_distance = distance
                            next_index = i
                
                # Adicionar próximo ponto à rota
                if next_index != -1:
                    route.append(next_index)
                    visited[next_index] = True
                    current = next_index
            
            logger.info(f"Rota otimizada calculada: {len(route)} pontos, distância total: {self._calculate_route_distance(coordinates, route):.2f} km")
            return route
            
        except Exception as e:
            logger.error(f"Erro ao otimizar rota: {e}")
            raise
    
    def calculate_route_distance(self, coordinates: List[Tuple[float, float]], 
                               route_indices: List[int]) -> float:
        """
        Calcula a distância total de uma rota.
        
        Args:
            coordinates: Lista de coordenadas
            route_indices: Lista de índices da rota
            
        Returns:
            Distância total em quilômetros
        """
        try:
            total_distance = 0.0
            
            for i in range(len(route_indices) - 1):
                current_idx = route_indices[i]
                next_idx = route_indices[i + 1]
                
                distance = self.calculate_distance(
                    coordinates[current_idx],
                    coordinates[next_idx]
                )
                total_distance += distance
            
            return total_distance
            
        except Exception as e:
            logger.error(f"Erro ao calcular distância da rota: {e}")
            raise
    
    def calculate_distance_from_reference(self, coordinate: Tuple[float, float]) -> float:
        """
        Calcula distância de um ponto até o ponto de referência.
        
        Args:
            coordinate: Coordenada (latitude, longitude)
            
        Returns:
            Distância em quilômetros
        """
        return self.calculate_distance(self.reference_point, coordinate)
    
    def find_nearest_points(self, target_coord: Tuple[float, float], 
                          coordinates: List[Tuple[float, float]], 
                          k: int = 5) -> List[Tuple[int, float]]:
        """
        Encontra os k pontos mais próximos de uma coordenada alvo.
        
        Args:
            target_coord: Coordenada alvo
            coordinates: Lista de coordenadas para buscar
            k: Número de pontos mais próximos a retornar
            
        Returns:
            Lista de tuplas (índice, distância) ordenada por distância
        """
        try:
            distances = []
            
            for i, coord in enumerate(coordinates):
                distance = self.calculate_distance(target_coord, coord)
                distances.append((i, distance))
            
            # Ordenar por distância e retornar os k mais próximos
            distances.sort(key=lambda x: x[1])
            return distances[:k]
            
        except Exception as e:
            logger.error(f"Erro ao encontrar pontos mais próximos: {e}")
            raise
    
    def calculate_centroid(self, coordinates: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        Calcula o centroide (centro de massa) de um conjunto de coordenadas.
        
        Args:
            coordinates: Lista de coordenadas
            
        Returns:
            Tupla (latitude_centro, longitude_centro)
        """
        try:
            if not coordinates:
                raise ValueError("Lista de coordenadas não pode estar vazia")
            
            # Calcular média das coordenadas
            lat_sum = sum(coord[0] for coord in coordinates)
            lon_sum = sum(coord[1] for coord in coordinates)
            n = len(coordinates)
            
            centroid = (lat_sum / n, lon_sum / n)
            
            logger.debug(f"Centroide calculado: {centroid}")
            return centroid
            
        except Exception as e:
            logger.error(f"Erro ao calcular centroide: {e}")
            raise
    
    def _validate_coordinates(self, coord: Tuple[float, float]) -> None:
        """
        Valida se as coordenadas estão dentro dos limites válidos.
        
        Args:
            coord: Tupla (latitude, longitude)
            
        Raises:
            ValueError: Se as coordenadas forem inválidas
        """
        lat, lon = coord
        
        if not (-90 <= lat <= 90):
            raise ValueError(f"Latitude inválida: {lat}. Deve estar entre -90 e 90.")
        
        if not (-180 <= lon <= 180):
            raise ValueError(f"Longitude inválida: {lon}. Deve estar entre -180 e 180.")
    
    def _calculate_route_distance(self, coordinates: List[Tuple[float, float]], 
                                route_indices: List[int]) -> float:
        """
        Método privado para calcular distância de rota (usado internamente).
        
        Args:
            coordinates: Lista de coordenadas
            route_indices: Lista de índices da rota
            
        Returns:
            Distância total em quilômetros
        """
        return self.calculate_route_distance(coordinates, route_indices)


def create_distance_matrix(coordinates: List[Tuple[float, float]]) -> np.ndarray:
    """
    Função utilitária para criar matriz de distâncias.
    
    Args:
        coordinates: Lista de coordenadas
        
    Returns:
        Matriz de distâncias
    """
    calc = GeographicCalculator()
    return calc.calculate_distance_matrix(coordinates)


def optimize_route(coordinates: List[Tuple[float, float]], 
                  start_index: int = 0) -> List[int]:
    """
    Função utilitária para otimizar rota.
    
    Args:
        coordinates: Lista de coordenadas
        start_index: Índice de partida
        
    Returns:
        Lista de índices da rota otimizada
    """
    calc = GeographicCalculator()
    return calc.nearest_neighbor_route(coordinates, start_index)


if __name__ == "__main__":
    """Teste das funções geográficas."""
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Teste básico
    calc = GeographicCalculator()
    
    # Coordenadas de teste (alguns locais em Angola)
    test_coords = [
        (-8.8390, 13.2894),  # Luanda
        (-9.0833, 16.0167),  # Kalandula
        (-16.7500, 12.2500), # Iona
        (-11.5000, 17.0000)  # Luando
    ]
    
    print("🧪 Testando calculadora geográfica...")
    
    # Teste de distância
    dist = calc.calculate_distance(test_coords[0], test_coords[1])
    print(f"Distância Luanda -> Kalandula: {dist:.2f} km")
    
    # Teste de matriz de distâncias
    matrix = calc.calculate_distance_matrix(test_coords)
    print(f"Matriz de distâncias: {matrix.shape}")
    
    # Teste de otimização de rota
    route = calc.nearest_neighbor_route(test_coords)
    print(f"Rota otimizada: {route}")
    
    # Teste de distância total
    total_dist = calc.calculate_route_distance(test_coords, route)
    print(f"Distância total da rota: {total_dist:.2f} km")
    
    print("✅ Testes concluídos com sucesso!")
