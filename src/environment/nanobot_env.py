import pybullet as p
import pybullet_data
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from ..config import SimConfig

class NanobotEnv(gym.Env):
    def __init__(self):
        super().__init__()
        
        # Initialize PyBullet
        self.physics_client = p.connect(p.DIRECT)  # Headless mode
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, SimConfig.GRAVITY)
        p.setTimeStep(SimConfig.TIMESTEP)
        
        # Action and observation spaces
        self.action_space = spaces.Box(
            low=-SimConfig.MAX_MAGNETIC_FORCE,
            high=SimConfig.MAX_MAGNETIC_FORCE,
            shape=(3,),
            dtype=np.float32
        )
        
        # Observation space: position, velocity, orientation
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(9,),
            dtype=np.float32
        )
        
        self.nanobot = None
        self.target_pos = None
        self.steps = 0
        
    def reset(self, seed=None):
        super().reset(seed=seed)
        p.resetSimulation()
        p.setGravity(0, 0, SimConfig.GRAVITY)
        
        # Create nanobot
        self.nanobot = self._create_nanobot()
        
        # Set random target position
        self.target_pos = self._generate_target()
        self.steps = 0
        
        return self._get_observation(), {}
    
    def step(self, action):
        self.steps += 1
        
        # Apply magnetic force
        p.applyExternalForce(
            self.nanobot,
            -1,
            forceObj=action,
            posObj=[0, 0, 0],
            flags=p.WORLD_FRAME
        )
        
        # Step simulation
        p.stepSimulation()
        
        # Get new state
        obs = self._get_observation()
        reward = self._calculate_reward(obs)
        done = self._check_termination(obs)
        
        return obs, reward, done, False, {}
    
    def _create_nanobot(self):
        collision_shape = p.createCollisionShape(
            p.GEOM_SPHERE,
            radius=SimConfig.NANOBOT_RADIUS
        )
        
        visual_shape = p.createVisualShape(
            p.GEOM_SPHERE,
            radius=SimConfig.NANOBOT_RADIUS,
            rgbaColor=[1, 0, 0, 1]
        )
        
        nanobot = p.createMultiBody(
            baseMass=SimConfig.NANOBOT_MASS,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=[0, 0, 0]
        )
        
        return nanobot
    
    def _get_observation(self):
        pos, quat = p.getBasePositionAndOrientation(self.nanobot)
        vel, ang_vel = p.getBaseVelocity(self.nanobot)
        return np.concatenate([pos, vel, ang_vel])
    
    def _calculate_reward(self, obs):
        # Distance-based reward
        pos = obs[:3]
        dist = np.linalg.norm(pos - self.target_pos)
        reward = -dist
        
        # Add bonus for reaching target
        if dist < SimConfig.NANOBOT_RADIUS * 2:
            reward += 100
            
        return reward * SimConfig.REWARD_SCALE
    
    def _check_termination(self, obs):
        pos = obs[:3]
        
        # Check if out of bounds
        if np.any(np.abs(pos) > SimConfig.ENV_SIZE):
            return True
            
        # Check if reached target
        if np.linalg.norm(pos - self.target_pos) < SimConfig.NANOBOT_RADIUS * 2:
            return True
            
        # Check if exceeded max steps
        if self.steps >= SimConfig.MAX_STEPS:
            return True
            
        return False
    
    def _generate_target(self):
        return np.random.uniform(-0.8, 0.8, 3) * SimConfig.ENV_SIZE
        
    def close(self):
        p.disconnect()