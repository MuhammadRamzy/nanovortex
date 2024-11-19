import numpy as np
import pybullet as p
from ...config import SimConfig

class Vessel:
    def __init__(self, radius, length, position, orientation):
        self.radius = radius
        self.length = length
        self.position = position
        self.orientation = orientation
        self.id = None
        
    def create_in_pybullet(self):
        cylinder_height = self.length
        cylinder_radius = self.radius
        
        collision_shape = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=cylinder_radius,
            height=cylinder_height
        )
        
        visual_shape = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=cylinder_radius,
            length=cylinder_height,
            rgbaColor=[0.8, 0.8, 0.8, 0.5]
        )
        
        self.id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=self.position,
            baseOrientation=self.orientation
        )
        
        return self.id
        
    def get_inner_points(self, num_points):
        points = []
        for _ in range(num_points):
            r = np.random.uniform(0, self.radius)
            theta = np.random.uniform(0, 2 * np.pi)
            z = np.random.uniform(0, self.length)
            
            point = np.array([
                r * np.cos(theta),
                r * np.sin(theta),
                z
            ])
            
            rotated_point = np.dot(p.getMatrixFromQuaternion(self.orientation), point)
            global_point = rotated_point + self.position
            points.append(global_point)
            
        return np.array(points)
