import numpy as np
from scipy.spatial.distance import cdist

class PathPlanner:
    def __init__(self, env_size, obstacle_positions, min_clearance):
        self.env_size = env_size
        self.obstacle_positions = np.array(obstacle_positions)
        self.min_clearance = min_clearance
        
    def generate_waypoints(self, start, goal, num_points=10):
        waypoints = [start]
        current = np.array(start)
        
        for i in range(num_points):
            t = (i + 1) / (num_points + 1)
            ideal_point = start + t * (goal - start)
            
            if self.obstacle_positions.size > 0:
                distances = cdist([ideal_point], self.obstacle_positions)
                if np.min(distances) < self.min_clearance:
                    offset = np.random.normal(0, 0.1, 3)
                    ideal_point += offset
                    
            waypoints.append(ideal_point)
            
        waypoints.append(goal)
        return np.array(waypoints)
        
    def check_path_clearance(self, path):
        path = np.array(path)
        if self.obstacle_positions.size == 0:
            return True
            
        for point in path:
            distances = cdist([point], self.obstacle_positions)
            if np.min(distances) < self.min_clearance:
                return False
        return True