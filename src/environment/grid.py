"""
2D Grid environment for autonomous delivery agent.
Handles terrain costs, static obstacles, and dynamic obstacles.
"""

from typing import List, Tuple, Dict, Set, Optional
from enum import Enum
import numpy as np

class TerrainType(Enum):
    FLAT = 1
    HILLS = 2
    MOUNTAINS = 3
    WATER = 4

class Cell:
    """Represents a single cell in the grid."""
    
    def __init__(self, terrain: TerrainType, is_obstacle: bool = False):
        self.terrain = terrain
        self.is_obstacle = is_obstacle
        self.cost = self._get_terrain_cost()
        
    def _get_terrain_cost(self) -> int:
        """Get movement cost based on terrain type."""
        costs = {
            TerrainType.FLAT: 1,
            TerrainType.HILLS: 2,
            TerrainType.MOUNTAINS: 3,
            TerrainType.WATER: 4
        }
        return costs[self.terrain]
    
    def __str__(self):
        return f"Cell(terrain={self.terrain.name}, obstacle={self.is_obstacle}, cost={self.cost})"

class Grid:
    """2D grid environment for path planning."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.empty((height, width), dtype=object)
        self._initialize_grid()
        
    def _initialize_grid(self):
        """Initialize grid with flat terrain and no obstacles."""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y, x] = Cell(TerrainType.FLAT)
    
    def set_terrain(self, x: int, y: int, terrain: TerrainType):
        """Set terrain type for a cell."""
        if self.is_valid_position(x, y):
            self.grid[y, x].terrain = terrain
            self.grid[y, x].cost = self.grid[y, x]._get_terrain_cost()
    
    def set_obstacle(self, x: int, y: int, is_obstacle: bool = True):
        """Set obstacle status for a cell."""
        if self.is_valid_position(x, y):
            self.grid[y, x].is_obstacle = is_obstacle
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_traversable(self, x: int, y: int, time: int = 0) -> bool:
        """Check if cell is traversable at given time."""
        if not self.is_valid_position(x, y):
            return False
        return not self.grid[y, x].is_obstacle
    
    def get_cost(self, x: int, y: int) -> int:
        """Get movement cost for a cell."""
        if self.is_valid_position(x, y):
            return self.grid[y, x].cost
        return float('inf')
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get 4-connected neighbors of a cell."""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny):
                neighbors.append((nx, ny))
                
        return neighbors
    
    def __str__(self):
        """String representation of the grid for debugging."""
        result = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = self.grid[y, x]
                if cell.is_obstacle:
                    row.append('X')
                else:
                    row.append(str(cell.terrain.value))
            result.append(' '.join(row))
        return '\n'.join(result)
