class SimulationConfig:
    """Global configuration parameters for the simulation"""
    
    # Physical constants
    GRAVITY = -9.81  # m/s²
    TEMPERATURE = 310.15  # K (37°C - body temperature)
    TIMESTEP = 1/240.0  # seconds
    
    # Environment parameters
    BOUNDARY_SIZE = 0.1  # meters
    VESSEL_RADIUS = 0.02  # meters
    VESSEL_LENGTH = 0.2  # meters
    
    # Nanobot parameters
    NANOBOT_RADIUS = 1e-3  # meters (1mm)
    NANOBOT_MASS = 1e-6  # kg (1mg)
    MAGNETIC_MOMENT = 1e-3  # A⋅m²
    
    # Biological fluid parameters
    BLOOD_VISCOSITY = 0.004  # Pa⋅s
    BLOOD_DENSITY = 1060  # kg/m³
    BLOOD_FLOW_VELOCITY = 0.3  # m/s
    
    # Magnetic field parameters
    MAX_FIELD_STRENGTH = 0.1  # Tesla
    
    # Training parameters
    EPISODE_LENGTH = 1000
    REWARD_DISTANCE_FACTOR = -10.0
    REWARD_VELOCITY_FACTOR = -0.1
    REWARD_COLLISION_PENALTY = -10.0
    REWARD_SUCCESS = 100.0
    SUCCESS_DISTANCE = 0.005  # meters