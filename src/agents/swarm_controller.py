import numpy as np
from ..config import SimConfig

class SwarmController:
    def __init__(self, num_nanobots):
        self.num_nanobots = num_nanobots
        self.nanobots = []
        self.target_positions = []
        
    def initialize_swarm(self, env):
        """Initialize multiple nanobots in the environment"""
        for _ in range(self.num_nanobots):
            nanobot = env._create_nanobot()
            self.nanobots.append(nanobot)
            
    def assign_targets(self, global_target):
        """Assign individual targets to nanobots in formation"""
        # Simple circular formation around target
        radius = SimConfig.NANOBOT_RADIUS * 4
        angles = np.linspace(0, 2*np.pi, self.num_nanobots, endpoint=False)
        
        self.target_positions = []
        for angle in angles:
            offset = radius * np.array([np.cos(angle), np.sin(angle), 0])
            target = global_target + offset
            self.target_positions.append(target)
            
    def get_swarm_actions(self, observations, agent):
        """Get actions for entire swarm"""
        actions = []
        for i, obs in enumerate(observations):
            action = agent.get_action(obs, self.target_positions[i])
            actions.append(action)
        return actions