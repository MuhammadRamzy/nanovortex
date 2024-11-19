import unittest
import torch
from src.agents.nanobot import NanobotAgent

class TestAgents(unittest.TestCase):
    def setUp(self):
        self.agent = NanobotAgent(obs_dim=9, action_dim=3)
        
    def test_forward_pass(self):
        obs = torch.randn(1, 9)
        mean, std = self.agent(obs)
        self.assertEqual(mean.shape, (1, 3))
        self.assertEqual(std.shape, (3,))