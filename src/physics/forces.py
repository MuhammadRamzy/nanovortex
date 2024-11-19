import numpy as np
from ..config import SimConfig

class ForceCalculator:
    def __init__(self, fluid, magnetic_field):
        self.fluid = fluid
        self.magnetic_field = magnetic_field
        
    def calculate_total_force(self, nanobot_state, magnetic_source_pos):
        """Calculate total force acting on nanobot"""
        position = nanobot_state[:3]
        velocity = nanobot_state[3:6]
        
        # Calculate individual forces
        drag_force = self.fluid.calculate_drag_force(
            velocity,
            SimConfig.NANOBOT_RADIUS
        )
        
        buoyancy_force = self.fluid.calculate_buoyancy_force(
            4/3 * np.pi * SimConfig.NANOBOT_RADIUS**3
        )
        
        magnetic_force = self.magnetic_field.calculate_magnetic_force(
            position,
            magnetic_source_pos,
            1.0  # Material susceptibility (simplified)
        )
        
        # Sum all forces
        gravity_force = np.array([0, 0, SimConfig.GRAVITY * SimConfig.NANOBOT_MASS])
        total_force = drag_force + buoyancy_force + magnetic_force + gravity_force
        
        return total_force