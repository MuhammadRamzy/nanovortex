import numpy as np
from ..config import SimConfig

class MagneticField:
    def __init__(self):
        self.strength = SimConfig.MAGNETIC_FIELD_STRENGTH
        
    def calculate_magnetic_force(self, position, field_source_position, material_susceptibility):
        """Calculate magnetic force on nanobot based on field gradient"""
        # F = V * χ * (B * ∇)B / μ0
        # Simplified model assuming linear field gradient
        
        r = position - field_source_position
        distance = np.linalg.norm(r)
        
        if distance == 0:
            return np.zeros(3)
            
        # Calculate field gradient (simplified model)
        direction = r / distance
        field_gradient = -self.strength * direction / (distance ** 2)
        
        # Calculate force
        force = (material_susceptibility * self.strength * field_gradient) / (4 * np.pi * 1e-7)
        
        # Clip force magnitude
        force_magnitude = np.linalg.norm(force)
        if force_magnitude > SimConfig.MAX_MAGNETIC_FORCE:
            force = force * SimConfig.MAX_MAGNETIC_FORCE / force_magnitude
            
        return force