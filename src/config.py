import numpy as np

class SimConfig:
    # Environment settings
    ENV_SIZE = np.array([1.0, 1.0, 1.0])  # 1 meter cube environment
    TIMESTEP = 1/240.0  # Standard PyBullet timestep
    
    # Nanobot parameters
    NANOBOT_RADIUS = 0.0001  # 100 micrometers
    NANOBOT_MASS = 1e-9  # 1 nanogram
    
    # Magnetic field parameters
    MAX_MAGNETIC_FORCE = 1e-6  # Maximum force in Newtons
    MAGNETIC_FIELD_STRENGTH = 1.0  # Tesla
    
    # Fluid parameters
    FLUID_DENSITY = 1000.0  # kg/m³ (water)
    FLUID_VISCOSITY = 0.001  # Pa·s (water at 20°C)
    
    # Training parameters
    EPISODE_LENGTH = 1000
    MAX_STEPS = 500
    REWARD_SCALE = 1.0
    
    # Physics parameters
    GRAVITY = -9.81
    DRAG_COEFFICIENT = 0.47  # Sphere