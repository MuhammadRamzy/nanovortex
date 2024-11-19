import numpy as np
from typing import Tuple
from src.config import SimulationConfig as cfg

class MagneticField:
    """
    Simulates external magnetic field for nanobot control.
    Implements magnetic field calculations and resulting forces.
    """
    
    def __init__(self):
        self.max_field_strength = cfg.MAX_FIELD_STRENGTH
        self.field_direction = np.zeros(3)
        self.gradient = np.zeros((3, 3))
        
    def set_field_direction(self, direction: np.ndarray):
        """Update magnetic field direction"""
        self.field_direction = direction / (np.linalg.norm(direction) + 1e-10)
        
    def set_field_gradient(self, gradient: np.ndarray):
        """Set magnetic field gradient for force calculation"""
        self.gradient = gradient
        
    def calculate_field_at_position(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field vector at given position.
        Includes spatial variation of field.
        """
        # Basic field calculation
        base_field = self.max_field_strength * self.field_direction
        
        # Add spatial variation (simplified model)
        field_variation = np.dot(self.gradient, position)
        
        return base_field + field_variation
    
    def calculate_magnetic_force(self, position: np.ndarray, magnetic_moment: float) -> np.ndarray:
        """
        Calculate magnetic force on nanobot using F = (m·∇)B where:
        m = magnetic moment
        B = magnetic field
        """
        # Get field and gradient at position
        field = self.calculate_field_at_position(position)
        
        # Calculate force using magnetic moment and field gradient
        force = magnetic_moment * np.dot(self.gradient, self.field_direction)
        
        # Add position-dependent modulation
        distance_from_center = np.linalg.norm(position)
        position_factor = np.exp(-distance_from_center / cfg.BOUNDARY_SIZE)
        
        return force * position_factor
    
    def calculate_magnetic_torque(self, magnetic_moment_vector: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic torque τ = m × B where:
        m = magnetic moment vector
        B = magnetic field
        """
        field = self.max_field_strength * self.field_direction
        return np.cross(magnetic_moment_vector, field)

    def calculate_field_energy(self, position: np.ndarray, magnetic_moment: float) -> float:
        """
        Calculate magnetic potential energy E = -m·B
        """
        field = self.calculate_field_at_position(position)
        return -magnetic_moment * np.dot(self.field_direction, field)