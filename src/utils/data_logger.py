import numpy as np
import json
from datetime import datetime

class DataLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.episode_data = []
        self.current_episode = {}
        
    def start_episode(self):
        self.current_episode = {
            "timestamp": datetime.now().isoformat(),
            "states": [],
            "actions": [],
            "rewards": [],
            "collisions": [],
            "magnetic_forces": []
        }
        
    def log_step(self, state, action, reward, collision, magnetic_force):
        self.current_episode["states"].append(state.tolist())
        self.current_episode["actions"].append(action.tolist())
        self.current_episode["rewards"].append(float(reward))
        self.current_episode["collisions"].append(bool(collision))
        self.current_episode["magnetic_forces"].append(magnetic_force.tolist())
        
    def end_episode(self):
        self.episode_data.append(self.current_episode)
        self.current_episode = {}
        
    def save_logs(self, filename):
        with open(f"{self.log_dir}/{filename}.json", "w") as f:
            json.dump(self.episode_data, f)