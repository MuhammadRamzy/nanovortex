import numpy as np

class RewardCalculator:
    def __init__(self):
        self.prev_distance = None
        
    def calculate_reward(self, state, target, collision):
        position = state[:3]
        velocity = state[3:6]
        current_distance = np.linalg.norm(position - target)
        
        reward = 0
        if self.prev_distance is not None:
            reward += (self.prev_distance - current_distance)
            
        reward -= 0.01 * np.linalg.norm(velocity)
        
        if collision:
            reward -= 10
            
        if current_distance < 0.05:
            reward += 100
            
        self.prev_distance = current_distance
        return reward