"""
Main CLI application for autonomous delivery agent.
"""

import click
import time
from typing import Dict
from environment.grid import Grid, TerrainType, DynamicGrid
from environment.obstacles import MovingObstacle
from agent.delivery_agent import DeliveryAgent
from utils.visualizer import GridVisualizer

@click.group()
def cli():
    """Autonomous Delivery Agent CLI"""
    pass

@cli.command()
@click.option('--map-file', required=True, help='Path to map file')
@click.option('--algorithm', default='astar', 
              type=click.Choice(['bfs', 'ucs', 'astar', 'hillclimbing', 'annealing']),
              help='Path planning algorithm')
@click.option('--heuristic', default='manhattan',
              type=click.Choice(['manhattan', 'euclidean', 'chebyshev']),
              help='Heuristic for A*')
@click.option('--fuel', default=100, help='Initial fuel')
@click.option('--time-limit', default=100, help='Time limit')
def plan(map_file, algorithm, heuristic, fuel, time_limit):
    """Plan and execute a delivery mission."""
    # Load map
    grid, start, goal, moving_obstacles = load_map(map_file)
    dynamic_grid = DynamicGrid(grid)
    
    # Add moving obstacles
    for obs_id, schedule in moving_obstacles.items():
        dynamic_grid.add_moving_obstacle(obs_id, schedule)
    
    # Create and run agent
    agent = DeliveryAgent(start, goal, grid, fuel, time_limit)
    
    print(f"Starting delivery with {algorithm} algorithm")
    start_time = time.time()
    
    metrics = agent.run_delivery(algorithm, dynamic_grid, 'astar')
    
    end_time = time.time()
    metrics['execution_time'] = end_time - start_time
    
    # Display results
    print("\n=== Delivery Results ===")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    # Visualize if possible
    try:
        visualizer = GridVisualizer(grid)
        visualizer.visualize_path(agent.path if agent.path else [], start, goal)
    except:
        print("Visualization not available")

def load_map(map_file: str):
    """Load map from file."""
    # Simplified map loading - implement based on your format
    # This is a placeholder implementation
    grid = Grid(10, 10)
    start = (0, 0)
    goal = (9, 9)
    moving_obstacles = {}
    
    return grid, start, goal, moving_obstacles

@cli.command()
@click.option('--map-dir', default='maps', help='Directory containing test maps')
def experiment(map_dir):
    """Run comparative experiments on all algorithms."""
    # Implement experimental comparison
    pass

if __name__ == '__main__':
    cli()
