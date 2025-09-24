# Autonomous-Delivery-Agent-AI-ML-
Vityarthi project
Project Overview
An intelligent autonomous delivery agent that navigates a 2D grid city to deliver packages using various search algorithms. The agent models complex environments with static obstacles, varying terrain costs, and dynamic moving obstacles while optimizing for efficiency under constraints.
Quick Start
Prerequisites
Python 3.8+

pip (Python package manager)

Installation
Clone the repository
git clone https://github.com/yourusername/autonomous-delivery-agent.git
cd autonomous-delivery-agent

Install dependencies
pip install -r requirements.txt

Install the package (optional)
pip install -e .
Basic Usage

Run a simple delivery mission:
python src/main.py plan --map-file maps/small.map --algorithm astar

Run with specific parameters:
python src/main.py plan --map-file maps/medium.map --algorithm ucs --fuel 200 --time-limit 150
 Available Maps
maps/small.map (5x5) - Quick testing

maps/medium.map (10x10) - Standard testing

maps/large.map (15x15) - Performance testing

maps/dynamic.map (8x8) - Moving obstacles demo
