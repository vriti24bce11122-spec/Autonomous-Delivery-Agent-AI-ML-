"""
Uninformed search algorithms: BFS and Uniform Cost Search.
"""

from typing import List, Tuple, Dict, Set, Optional
import heapq
from collections import deque
from environment.grid import Grid

class Node:
    """Represents a node in the search tree."""
    
    def __init__(self, x: int, y: int, parent: Optional['Node'] = None, 
                 cost: float = 0, time: int = 0):
        self.x = x
        self.y = y
        self.parent = parent
        self.cost = cost
        self.time = time
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class UninformedSearch:
    """Base class for uninformed search algorithms."""
    
    def __init__(self, grid: Grid):
        self.grid = grid
        self.nodes_expanded = 0
    
    def reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """Reconstruct path from goal node to start."""
        path = []
        current = node
        while current is not None:
            path.append((current.x, current.y))
            current = current.parent
        return path[::-1]
    
    def get_successors(self, node: Node) -> List[Node]:
        """Get valid successor nodes."""
        successors = []
        for nx, ny in self.grid.get_neighbors(node.x, node.y):
            if self.grid.is_traversable(nx, ny):
                cost = node.cost + self.grid.get_cost(nx, ny)
                successors.append(Node(nx, ny, node, cost, node.time + 1))
        return successors

class BFS(UninformedSearch):
    """Breadth-First Search implementation."""
    
    def search(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int, int]:
        """Perform BFS search.
        
        Returns:
            Tuple of (path, cost, nodes_expanded)
        """
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])
        
        if start_node == goal_node:
            return [start], 0, 0
        
        frontier = deque([start_node])
        explored = set()
        explored.add((start_node.x, start_node.y))
        self.nodes_expanded = 0
        
        while frontier:
            current = frontier.popleft()
            self.nodes_expanded += 1
            
            if current == goal_node:
                path = self.reconstruct_path(current)
                return path, current.cost, self.nodes_expanded
            
            for successor in self.get_successors(current):
                if (successor.x, successor.y) not in explored:
                    explored.add((successor.x, successor.y))
                    frontier.append(successor)
        
        return [], float('inf'), self.nodes_expanded

class UniformCostSearch(UninformedSearch):
    """Uniform Cost Search implementation."""
    
    def search(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int, int]:
        """Perform UCS search."""
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])
        
        frontier = []
        heapq.heappush(frontier, (0, start_node))
        explored = {}
        explored[(start_node.x, start_node.y)] = 0
        self.nodes_expanded = 0
        
        while frontier:
            current_cost, current = heapq.heappop(frontier)
            self.nodes_expanded += 1
            
            if current == goal_node:
                path = self.reconstruct_path(current)
                return path, current.cost, self.nodes_expanded
            
            if current_cost > explored.get((current.x, current.y), float('inf')):
                continue
            
            for successor in self.get_successors(current):
                new_cost = current_cost + self.grid.get_cost(successor.x, successor.y)
                
                if (successor.x, successor.y) not in explored or new_cost < explored[(successor.x, successor.y)]:
                    explored[(successor.x, successor.y)] = new_cost
                    successor.cost = new_cost
                    heapq.heappush(frontier, (new_cost, successor))
        
        return [], float('inf'), self.nodes_expanded
