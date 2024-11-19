import numpy as np
from src.config import SimulationConfig as cfg

class BiologicalFluid:
    """
    Simulates biological fluid properties and forces.
    Implements Navier-Stokes equations for microscale fluid dynamics.
    """
    
    def __init__(self):
        self.viscosity = cfg.BLOOD_VISCOSITY
        self.density = cfg.BLOOD_DENSITY
        self.flow_velocity = cfg.BLOOD_FLOW_VELOCITY
        
    def calculate_reynolds_number(self, velocity: np.ndarray, characteristic_length: float) -> float:
        """
        Calculate Reynolds number to determine flow regime.
        Re = (ρvL)/μ where:
        ρ = fluid density
        v = fluid velocity
        L = characteristic length
        μ = dynamic viscosity
        """
        velocity_magnitude = np.linalg.norm(velocity)
        return (self.density * velocity_magnitude * characteristic_length) / self.viscosity
    
    def calculate_drag_force(self, velocity: np.ndarray, radius: float) -> np.ndarray:
        """
        Calculate drag force using Stokes' law for low Reynolds number flow.
        F = 6πμrv where:
        μ = dynamic viscosity
        r = particle radius
        v = relative velocity
        """
        relative_velocity = velocity - np.array([self.flow_velocity, 0, 0])
        reynolds_number = self.calculate_reynolds_number(relative_velocity, 2 * radius)
        
        if reynolds_number < 1:  # Stokes flow regime
            drag_coefficient = 6 * np.pi * self.viscosity * radius
        else:  # Transition regime
            # Use more complex drag coefficient for higher Reynolds numbers
            cd = 24 / reynolds_number * (1 + 0.15 * reynolds_number**0.687)
            area = np.pi * radius**2
            drag_coefficient = 0.5 * self.density * cd * area
            
        return -drag_coefficient * relative_velocity
    
    def calculate_lift_force(self, velocity: np.ndarray, radius: float) -> np.ndarray:
        """
        Calculate Saffman lift force for particles in shear flow.
        """
        shear_rate = self.flow_velocity / cfg.VESSEL_RADIUS
        relative_velocity = velocity - np.array([self.flow_velocity, 0, 0])
        
        # Saffman lift force coefficient
        k = 6.46  # Saffman constant
        lift_coefficient = k * radius**2 * np.sqrt(self.density * self.viscosity * shear_rate)
        
        # Calculate lift force perpendicular to flow
        force_magnitude = lift_coefficient * np.linalg.norm(relative_velocity)
        direction = np.array([0, 0, 1])  # Lift direction (perpendicular to flow)
        
        return force_magnitude * direction
    
    def calculate_brownian_motion(self, radius: float, dt: float) -> np.ndarray:
        """
        Calculate Brownian motion displacement using Einstein-Smoluchowski relation.
        """
        # Boltzmann constant
        kb = 1.380649e-23  # J/K
        
        # Calculate diffusion coefficient
        D = kb * cfg.TEMPERATURE / (6 * np.pi * self.viscosity * radius)
        
        # Calculate standard deviation of displacement
        sigma = np.sqrt(2 * D * dt)
        
        # Generate random displacement
        displacement = np.random.normal(0, sigma, 3)
        
        return displacement