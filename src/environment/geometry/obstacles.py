import numpy as np
import pybullet as p
from ...config import SimConfig

class Obstacle:
    def __init__(self, shape_type, dimensions, position, orientation):
        self.shape_type = shape_type
        self.dimensions = dimensions
        self.position = position
        self.orientation = orientation
        self.id = None
        
    def create_in_pybullet(self):
        if self.shape_type == "sphere":
            collision_shape = p.createCollisionShape(
                p.GEOM_SPHERE,
                radius=self.dimensions[0]
            )
            visual_shape = p.createVisualShape(
                p.GEOM_SPHERE,
                radius=self.dimensions[0],
                rgbaColor=[0.7, 0.7, 0.7, 0.8]
            )
        elif self.shape_type == "box":
            collision_shape = p.createCollisionShape(
                p.GEOM_BOX,
                halfExtents=self.dimensions
            )
            visual_shape = p.createVisualShape(
                p.GEOM_BOX,
                halfExtents=self.dimensions,
                rgbaColor=[0.7, 0.7, 0.7, 0.8]
            )
        else:
            raise ValueError(f"Unknown shape type: {self.shape_type}")
            
        self.id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=self.position,
            baseOrientation=self.orientation
        )
        
        return self.id

class ObstacleField:
    def __init__(self):
        self.obstacles = []
        
    def add_random_obstacles(self, num_obstacles, env_size):
        for _ in range(num_obstacles):
            shape_type = np.random.choice(["sphere", "box"])
            
            if shape_type == "sphere":
                dimensions = [np.random.uniform(0.05, 0.15)]
            else:
                dimensions = np.random.uniform(0.05, 0.15, 3)
                
            position = np.random.uniform(-env_size, env_size, 3)
            orientation = p.getQuaternionFromEuler(
                np.random.uniform(0, 2*np.pi, 3)
            )
            
            obstacle = Obstacle(shape_type, dimensions, position, orientation)
            self.obstacles.append(obstacle)
            
    def create_all_in_pybullet(self):
        for obstacle in self.obstacles:
            obstacle.create_in_pybullet()
            
    def get_obstacle_positions(self):
        return [obstacle.position for obstacle in self.obstacles]