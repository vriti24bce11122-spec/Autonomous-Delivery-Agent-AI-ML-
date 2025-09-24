"""
Visualization utilities for grid and paths.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple
from environment.grid import Grid, TerrainType

class GridVisualizer:
    """Visualize grid environment and paths."""
    
    def __init__(self, grid: Grid):
        self.grid = grid
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
    
    def visualize_path(self, path: List[Tuple[int, int]], 
                      start: Tuple[int, int], goal: Tuple[int, int]):
        """Visualize grid with path."""
        # Create grid visualization
        terrain_colors = {
            TerrainType.FLAT: 'lightgreen',
            TerrainType.HILLS: 'orange',
            TerrainType.MOUNTAINS: 'brown',
            TerrainType.WATER: 'lightblue'
        }
        
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.grid[y, x]
                color = terrain_colors[cell.terrain]
                
                # Darker color for obstacles
                if cell.is_obstacle:
                    color = 'black'
                
                rect = patches.Rectangle((x, self.grid.height - y - 1), 1, 1, 
                                       linewidth=1, edgecolor='black', 
                                       facecolor=color, alpha=0.7)
                self.ax.add_patch(rect)
                
                # Add cost text
                self.ax.text(x + 0.5, self.grid.height - y - 0.5, str(cell.cost),
                           ha='center', va='center', fontsize=8)
        
        # Plot path
        if path:
            path_x = [p[0] + 0.5 for p in path]
            path_y = [self.grid.height - p[1] - 0.5 for p in path]
            self.ax.plot(path_x, path_y, 'r-', linewidth=2, label='Path')
            self.ax.plot(path_x, path_y, 'ro', markersize=4)
        
        # Mark start and goal
        start_x, start_y = start[0] + 0.5, self.grid.height - start[1] - 0.5
        goal_x, goal_y = goal[0] + 0.5, self.grid.height - goal[1] - 0.5
        
        self.ax.plot(start_x, start_y, 'gs', markersize=10, label='Start')
        self.ax.plot(goal_x, goal_y, 'bs', markersize=10, label='Goal')
        
        self.ax.set_xlim(0, self.grid.width)
        self.ax.set_ylim(0, self.grid.height)
        self.ax.set_aspect('equal')
        self.ax.legend()
        self.ax.set_title('Delivery Agent Path Planning')
        
        plt.show()

# Additional utility files would include logger.py, map_loader.py, etc.
