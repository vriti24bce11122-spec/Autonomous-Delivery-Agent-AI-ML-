"""
Informed search algorithms: A* with various heuristics.
"""

import heapq
from typing import List, Tuple, Callable
from algorithms.uninformed_search import UninformedSearch, Node

class AStarSearch(UninformedSearch):
    """A* Search implementation with configurable heuristics."""
    
    def __init__(self, grid, heuristic: str = 'manhattan'):
        super().__init__(grid)
        self.heuristic = self._get_heuristic_function(heuristic)
    
    def _get_heuristic_function(self, heuristic: str) -> Callable:
        """Get heuristic function by name."""
        heuristics = {
            'manhattan': self.manhattan_distance,
            'euclidean': self.euclidean_distance,
            'chebyshev': self.chebyshev_distance
        }
        return heuristics.get(heuristic, self.manhattan_distance)
    
    def manhattan_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """Manhattan distance heuristic."""
        return abs(x1 - x2) + abs(y1 - y2)
    
    def euclidean_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """Euclidean distance heuristic."""
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    def chebyshev_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """Chebyshev distance heuristic."""
        return max(abs(x1 - x2), abs(y1 - y2))
    
    def search(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int, int]:
        """Perform A* search."""
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])
        
        open_set = []
        heapq.heappush(open_set, (0, start_node))
        
        g_score = {}
        g_score[(start_node.x, start_node.y)] = 0
        
        f_score = {}
        h_start = self.heuristic(start[0], start[1], goal[0], goal[1])
        f_score[(start_node.x, start_node.y)] = h_start
        
        self.nodes_expanded = 0
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            self.nodes_expanded += 1
            
            if current == goal_node:
                path = self.reconstruct_path(current)
                return path, current.cost, self.nodes_expanded
            
            for successor in self.get_successors(current):
                tentative_g = g_score[(current.x, current.y)] + self.grid.get_cost(successor.x, successor.y)
                
                if (successor.x, successor.y) not in g_score or tentative_g < g_score[(successor.x, successor.y)]:
                    successor.parent = current
                    successor.cost = tentative_g
                    g_score[(successor.x, successor.y)] = tentative_g
                    
                    h_value = self.heuristic(successor.x, successor.y, goal[0], goal[1])
                    f_value = tentative_g + h_value
                    f_score[(successor.x, successor.y)] = f_value
                    
                    heapq.heappush(open_set, (f_value, successor))
        
        return [], float('inf'), self.nodes_expanded
