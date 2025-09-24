"""
Dynamic obstacle management for the grid environment.
"""

from typing import List, Tuple, Dict, Set
import numpy as np

class MovingObstacle:
    """Represents a moving obstacle with a deterministic schedule."""
    
    def __init__(self, obstacle_id: str, schedule: List[Tuple[int, int, int]]):
        """
        Args:
            obstacle_id: Unique identifier for the obstacle
            schedule: List of (time, x, y) positions
        """
        self.obstacle_id = obstacle_id
        self.schedule = sorted(schedule, key=lambda x: x[0])  # Sort by time
        self.max_time = max(t for t, x, y in self.schedule)
    
    def get_position_at_time(self, time: int) -> Tuple[int, int]:
        """Get obstacle position at given time using linear interpolation."""
        if time <= self.schedule[0][0]:
            return self.schedule[0][1], self.schedule[0][2]
        if time >= self.schedule[-1][0]:
            return self.schedule[-1][1], self.schedule[-1][2]
        
        # Find the segment containing the time
        for i in range(len(self.schedule) - 1):
            t1, x1, y1 = self.schedule[i]
            t2, x2, y2 = self.schedule[i + 1]
            
            if t1 <= time <= t2:
                # Linear interpolation
                if t2 == t1:
                    return x1, y1
                ratio = (time - t1) / (t2 - t1)
                x = int(round(x1 + ratio * (x2 - x1)))
                y = int(round(y1 + ratio * (y2 - y1)))
                return x, y
        
        return self.schedule[-1][1], self.schedule[-1][2]

class DynamicGrid:
    """Extends Grid with dynamic obstacle support."""
    
    def __init__(self, base_grid):
        self.base_grid = base_grid
        self.moving_obstacles: Dict[str, MovingObstacle] = {}
        self.dynamic_obstacles: Set[Tuple[int, int]] = set()
    
    def add_moving_obstacle(self, obstacle_id: str, schedule: List[Tuple[int, int, int]]):
        """Add a moving obstacle with a schedule."""
        self.moving_obstacles[obstacle_id] = MovingObstacle(obstacle_id, schedule)
    
    def update_dynamic_obstacles(self, time: int):
        """Update dynamic obstacle positions for the given time."""
        self.dynamic_obstacles.clear()
        for obstacle in self.moving_obstacles.values():
            x, y = obstacle.get_position_at_time(time)
            self.dynamic_obstacles.add((x, y))
    
    def is_traversable(self, x: int, y: int, time: int = 0) -> bool:
        """Check if cell is traversable at given time considering dynamic obstacles."""
        if not self.base_grid.is_traversable(x, y):
            return False
        
        self.update_dynamic_obstacles(time)
        return (x, y) not in self.dynamic_obstacles
    
    def __getattr__(self, name):
        """Delegate other attributes to base grid."""
        return getattr(self.base_grid, name)
