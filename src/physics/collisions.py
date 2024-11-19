import numpy as np
import pybullet as p
from ..config import SimConfig

class CollisionHandler:
    def __init__(self, env):
        self.env = env
        
    def check_collisions(self, nanobot_id):
        """Check for collisions with obstacles and boundaries"""
        # Get collision points
        points = p.getContactPoints(bodyA=nanobot_id)
        
        if len(points) > 0:
            return True, points[0][5]  # Contact point position
        
        # Check environment boundaries
        pos, _ = p.getBasePositionAndOrientation(nanobot_id)
        if np.any(np.abs(pos) > SimConfig.ENV_SIZE):
            return True, pos
            
        return False, None
        
    def handle_collision(self, nanobot_id, contact_point):
        """Handle collision response"""
        # Get current velocity
        lin_vel, ang_vel = p.getBaseVelocity(nanobot_id)
        
        # Simple elastic collision response
        # Reverse velocity component in direction of collision
        normal = np.array(contact_point) / np.linalg.norm(contact_point)
        reflected_vel = lin_vel - 2 * np.dot(lin_vel, normal) * normal
        
        # Apply new velocity with some energy loss
        p.resetBaseVelocity(
            nanobot_id,
            linearVelocity=0.8 * reflected_vel,  # 20% energy loss
            angularVelocity=[0, 0, 0]  # Reset angular velocity
        )