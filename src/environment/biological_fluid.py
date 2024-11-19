import numpy as np
from ..config import SimConfig

class BiologicalFluid:
    def __init__(self):
        self.density = SimConfig.FLUID_DENSITY
        self.viscosity = SimConfig.FLUID_VISCOSITY
        
    def calculate_drag_force(self, velocity, radius):
        """Calculate drag force using Stokes' law (for low Reynolds numbers)"""
        # F_drag = 6πμrv
        drag_coeff = 6 * np.pi * self.viscosity * radius
        drag_force = -drag_coeff * velocity
        return drag_force
        
    def calculate_buoyancy_force(self, volume):
        """Calculate buoyancy force"""
        # F_buoyancy = ρVg
        return np.array([0, 0, -SimConfig.GRAVITY * self.density * volume])