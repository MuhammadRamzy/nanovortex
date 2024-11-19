import numpy as np
import torch
import torch.nn as nn
from ..config import SimConfig

class NanobotAgent(nn.Module):
    def __init__(self, obs_dim, action_dim):
        super().__init__()
        
        self.network = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )
        
        self.log_std = nn.Parameter(torch.zeros(action_dim))
        
    def forward(self, x):
        mean = self.network(x)
        std = torch.exp(self.log_std)
        return mean, std
