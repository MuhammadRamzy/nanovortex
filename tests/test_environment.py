import unittest
import numpy as np
from src.environment.nanobot_env import NanobotEnv

class TestNanobotEnv(unittest.TestCase):
    def setUp(self):
        self.env = NanobotEnv()
        
    def test_reset(self):
        obs = self.env.reset()
        self.assertEqual(len(obs), 9)
        
    def test_step(self):
        self.env.reset()
        obs, reward, done, _, info = self.env.step(np.zeros(3))
        self.assertEqual(len(obs), 9)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)
        
    def tearDown(self):
        self.env.close()