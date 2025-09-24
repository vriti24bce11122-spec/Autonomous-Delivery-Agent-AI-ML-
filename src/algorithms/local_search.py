"""
Local search algorithms for dynamic replanning.
"""

import random
import math
from typing import List, Tuple, Optional
from environment.grid import Grid
from algorithms.uninformed_search import Node

class HillClimbing:
    """Hill Climbing with random restarts for path optimization."""
    
    def __init__(self, grid: Grid, max_restarts: int = 10, max_iterations: int = 100):
        self.grid = grid
        self.max_restarts = max_restarts
        self.max_iterations = max_iterations
    
    def get_path_cost(self, path: List[Tuple[int, int]]) -> int:
        """Calculate total cost of a path."""
        cost = 0
        for i in range(len(path) - 1):
            x, y = path[i + 1]
            cost += self.grid.get_cost(x, y)
        return cost
    
    def generate_random_path(self, start: Tuple[int, int], goal: Tuple[int, int], 
                           max_length: int = 50) -> Optional[List[Tuple[int, int]]]:
        """Generate a random valid path using random walks."""
        path = [start]
        current = start
        visited = set([start])
        
        for _ in range(max_length):
            neighbors = [n for n in self.grid.get_neighbors(current[0], current[1]) 
                        if self.grid.is_traversable(n[0], n[1]) and n not in visited]
            
            if not neighbors:
                break
                
            next_pos = random.choice(neighbors)
            path.append(next_pos)
            visited.add(next_pos)
            current = next_pos
            
            if current == goal:
                return path
        
        return None
    
    def mutate_path(self, path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Mutate a path by replacing a segment with a random walk."""
        if len(path) < 3:
            return path
        
        # Choose a random segment to replace
        start_idx = random.randint(0, len(path) - 2)
        end_idx = random.randint(start_idx + 1, len(path) - 1)
        
        new_segment = self._find_alternative_route(path[start_idx], path[end_idx], end_idx - start_idx)
        if new_segment:
            return path[:start_idx] + new_segment + path[end_idx + 1:]
        
        return path
    
    def _find_alternative_route(self, start: Tuple[int, int], end: Tuple[int, int], 
                              max_steps: int) -> Optional[List[Tuple[int, int]]]:
        """Find an alternative route between two points."""
        # Simple BFS for short alternative routes
        from collections import deque
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue and len(visited) < 100:  # Limit search
            current, path = queue.popleft()
            
            if len(path) > max_steps + 2:  # Allow slight detour
                continue
                
            if current == end:
                return path[1:]  # Exclude start
            
            for neighbor in self.grid.get_neighbors(current[0], current[1]):
                if (self.grid.is_traversable(neighbor[0], neighbor[1]) and 
                    neighbor not in visited):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def search(self, start: Tuple[int, int], goal: Tuple[int, int], 
               initial_path: List[Tuple[int, int]] = None) -> Tuple[List[Tuple[int, int]], int, int]:
        """Perform hill climbing search with random restarts."""
        best_path = initial_path
        best_cost = float('inf') if not initial_path else self.get_path_cost(initial_path)
        nodes_evaluated = 0
        
        for restart in range(self.max_restarts):
            if best_path is None:
                current_path = self.generate_random_path(start, goal)
            else:
                current_path = best_path.copy()
            
            if not current_path:
                continue
                
            current_cost = self.get_path_cost(current_path)
            nodes_evaluated += 1
            
            for iteration in range(self.max_iterations):
                # Generate neighbor by mutation
                new_path = self.mutate_path(current_path)
                if not new_path or new_path[-1] != goal:
                    continue
                
                new_cost = self.get_path_cost(new_path)
                nodes_evaluated += 1
                
                if new_cost < current_cost:
                    current_path = new_path
                    current_cost = new_cost
                
                if current_cost < best_cost:
                    best_path = current_path
                    best_cost = current_cost
        
        return best_path, best_cost, nodes_evaluated

class SimulatedAnnealing:
    """Simulated Annealing for path optimization."""
    
    def __init__(self, grid: Grid, initial_temp: float = 1000, cooling_rate: float = 0.95):
        self.grid = grid
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
    
    def get_path_cost(self, path: List[Tuple[int, int]]) -> int:
        """Calculate total cost of a path."""
        cost = 0
        for i in range(len(path) - 1):
            x, y = path[i + 1]
            cost += self.grid.get_cost(x, y)
        return cost
    
    def search(self, start: Tuple[int, int], goal: Tuple[int, int], 
               initial_path: List[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], int, int]:
        """Perform simulated annealing search."""
        current_path = initial_path.copy()
        current_cost = self.get_path_cost(current_path)
        best_path = current_path.copy()
        best_cost = current_cost
        
        temperature = self.initial_temp
        nodes_evaluated = 1
        
        hill_climbing = HillClimbing(self.grid)
        
        while temperature > 1:
            # Generate neighbor using hill climbing's mutation
            new_path = hill_climbing.mutate_path(current_path)
            nodes_evaluated += 1
            
            if not new_path or new_path[-1] != goal:
                continue
            
            new_cost = self.get_path_cost(new_path)
            
            # Accept worse solution with probability based on temperature
            if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
                current_path = new_path
                current_cost = new_cost
                
                if current_cost < best_cost:
                    best_path = current_path.copy()
                    best_cost = current_cost
            
            temperature *= self.cooling_rate
        
        return best_path, best_cost, nodes_evaluated
