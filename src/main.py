import numpy as np
import pybullet as p
from environment.nanobot_env import NanobotEnv
from agents.nanobot import NanobotAgent
from training.ppo_trainer import PPOTrainer
from utils.visualization import Visualizer
from utils.metrics import MetricsLogger

def main():
    env = NanobotEnv()
    agent = NanobotAgent(obs_dim=9, action_dim=3)
    trainer = PPOTrainer(agent, env)
    visualizer = Visualizer()
    metrics = MetricsLogger()
    
    num_episodes = 1000
    
    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        episode_rewards = []
        
        while not done:
            mean, std = agent(torch.FloatTensor(obs))
            dist = torch.distributions.Normal(mean, std)
            action = dist.sample().numpy()
            
            next_obs, reward, done, _, info = env.step(action)
            episode_rewards.append(reward)
            
            visualizer.update(next_obs[:3], env.target_pos)
            obs = next_obs
            
        metrics.log_episode(episode_rewards, len(episode_rewards), 
                          info.get('success', False), info.get('collisions', 0))
                          
        if episode % 10 == 0:
            print(f"Episode {episode}: {metrics.get_metrics()}")
            
    env.close()

if __name__ == "__main__":
    main()