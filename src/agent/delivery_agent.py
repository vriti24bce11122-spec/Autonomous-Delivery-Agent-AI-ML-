"""
Autonomous delivery agent with rationality constraints.
"""

from typing import List, Tuple, Dict, Optional
from enum import Enum
from environment.grid import Grid, DynamicGrid
from algorithms.uninformed_search import BFS, UniformCostSearch
from algorithms.informed_search import AStarSearch
from algorithms.local_search import HillClimbing, SimulatedAnnealing

class AgentState(Enum):
    PLANNING = 1
    MOVING = 2
    REPLANNING = 3
    COMPLETED = 4

class DeliveryAgent:
    """Autonomous delivery agent that navigates grid environment."""
    
    def __init__(self, start: Tuple[int, int], goal: Tuple[int, int], 
                 grid: Grid, fuel: int = 100, time_limit: int = 100):
        self.start = start
        self.goal = goal
        self.grid = grid
        self.fuel = fuel
        self.time_limit = time_limit
        
        self.position = start
        self.path = []
        self.cost = 0
        self.time_elapsed = 0
        self.fuel_remaining = fuel
        self.state = AgentState.PLANNING
        
        # Performance metrics
        self.replan_count = 0
        self.total_nodes_expanded = 0
    
    def plan_path(self, algorithm: str, **kwargs) -> bool:
        """Plan initial path using specified algorithm."""
        planner = self._get_planner(algorithm, **kwargs)
        
        if planner:
            self.path, path_cost, nodes_expanded = planner.search(self.position, self.goal)
            self.total_nodes_expanded += nodes_expanded
            
            if self.path:
                print(f"Path found with {algorithm}: cost={path_cost}, nodes={nodes_expanded}")
                return True
            else:
                print(f"No path found with {algorithm}")
                return False
        return False
    
    def _get_planner(self, algorithm: str, **kwargs):
        """Get appropriate path planner."""
        planners = {
            'bfs': BFS(self.grid),
            'ucs': UniformCostSearch(self.grid),
            'astar': AStarSearch(self.grid, kwargs.get('heuristic', 'manhattan')),
            'hillclimbing': HillClimbing(self.grid),
            'annealing': SimulatedAnnealing(self.grid)
        }
        return planners.get(algorithm)
    
    def move(self) -> bool:
        """Move one step along the planned path."""
        if not self.path or self.position == self.goal:
            self.state = AgentState.COMPLETED
            return False
        
        if len(self.path) <= 1:
            return False
        
        next_pos = self.path[1]  # Next position in path
        move_cost = self.grid.get_cost(next_pos[0], next_pos[1])
        
        # Check constraints
        if (self.fuel_remaining < move_cost or 
            self.time_elapsed >= self.time_limit):
            print("Constraints violated - cannot move")
            return False
        
        # Execute move
        self.position = next_pos
        self.cost += move_cost
        self.fuel_remaining -= move_cost
        self.time_elapsed += 1
        self.path = self.path[1:]  # Remove current position from path
        
        print(f"Move to {self.position}, Cost: {move_cost}, Total: {self.cost}")
        return True
    
    def check_for_replan(self, dynamic_grid: Optional[DynamicGrid] = None) -> bool:
        """Check if replanning is necessary."""
        if not self.path:
            return True
        
        # Check if path is blocked by dynamic obstacles
        if dynamic_grid:
            for i, (x, y) in enumerate(self.path):
                future_time = self.time_elapsed + i
                if not dynamic_grid.is_traversable(x, y, future_time):
                    print(f"Dynamic obstacle detected at {(x, y)} at time {future_time}")
                    return True
        
        # Check if we're stuck
        if len(self.path) > 1 and self.path[1] == self.position:
            return True
        
        return False
    
    def replan(self, algorithm: str = 'astar', **kwargs) -> bool:
        """Replan path from current position."""
        self.replan_count += 1
        print(f"Replanning attempt {self.replan_count} with {algorithm}")
        
        # Use local search if we have a current path
        if self.path and algorithm in ['hillclimbing', 'annealing']:
            planner = self._get_planner(algorithm, **kwargs)
            if isinstance(planner, (HillClimbing, SimulatedAnnealing)):
                new_path, new_cost, nodes_expanded = planner.search(
                    self.position, self.goal, self.path)
                self.total_nodes_expanded += nodes_expanded
                
                if new_path:
                    self.path = new_path
                    print(f"Replanning successful: new cost={new_cost}")
                    return True
        else:
            # Use complete search algorithm
            return self.plan_path(algorithm, **kwargs)
        
        return False
    
    def run_delivery(self, algorithm: str, dynamic_grid: Optional[DynamicGrid] = None, 
                    replan_algorithm: str = 'astar') -> Dict:
        """Execute complete delivery mission."""
        print(f"Starting delivery from {self.start} to {self.goal}")
        
        # Initial planning
        if not self.plan_path(algorithm):
            return self._get_metrics(success=False)
        
        self.state = AgentState.MOVING
        
        # Execution loop
        while self.position != self.goal and self.time_elapsed < self.time_limit:
            # Check if replanning is needed
            if self.check_for_replan(dynamic_grid):
                self.state = AgentState.REPLANNING
                if not self.replan(replan_algorithm):
                    print("Replanning failed - mission aborted")
                    return self._get_metrics(success=False)
                self.state = AgentState.MOVING
            
            # Move one step
            if not self.move():
                break
        
        success = self.position == self.goal
        return self._get_metrics(success)
    
    def _get_metrics(self, success: bool) -> Dict:
        """Collect performance metrics."""
        return {
            'success': success,
            'final_position': self.position,
            'total_cost': self.cost,
            'time_elapsed': self.time_elapsed,
            'fuel_remaining': self.fuel_remaining,
            'replan_count': self.replan_count,
            'total_nodes_expanded': self.total_nodes_expanded,
            'path_length': len(self.path) if self.path else 0
        }
