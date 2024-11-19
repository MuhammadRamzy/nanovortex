import os
import sys
import traceback
import numpy as np
import torch
import pybullet as p
from datetime import datetime

from src.environment.nanobot_env import NanobotEnv
from src.agents.nanobot import NanobotAgent
from src.training.ppo_trainer import PPOTrainer
from src.utils.visualization import Visualizer
from src.utils.metrics import MetricsLogger
from src.utils.data_logger import DataLogger
from src.environment.geometry.obstacles import ObstacleField
from src.config import SimConfig

def setup_logging():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join("logs", timestamp)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def initialize_simulation():
    try:
        # Initialize environment
        env = NanobotEnv()
        
        # Create obstacle field
        obstacle_field = ObstacleField()
        obstacle_field.add_random_obstacles(5, SimConfig.ENV_SIZE[0])
        obstacle_field.create_all_in_pybullet()
        
        # Initialize agent
        agent = NanobotAgent(obs_dim=9, action_dim=3)
        
        # Initialize trainer and loggers
        trainer = PPOTrainer(agent, env)
        visualizer = Visualizer()
        metrics = MetricsLogger()
        data_logger = DataLogger(setup_logging())
        
        return env, agent, trainer, visualizer, metrics, data_logger
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def train_simulation(env, agent, trainer, visualizer, metrics, data_logger):
    try:
        num_episodes = 1000
        best_reward = float('-inf')
        
        for episode in range(num_episodes):
            obs = env.reset()
            done = False
            episode_rewards = []
            data_logger.start_episode()
            
            while not done:
                try:
                    # Get action from agent
                    with torch.no_grad():
                        mean, std = agent(torch.FloatTensor(obs).unsqueeze(0))
                        dist = torch.distributions.Normal(mean, std)
                        action = dist.sample().squeeze(0).numpy()
                        
                    # Take step in environment
                    next_obs, reward, done, _, info = env.step(action)
                    
                    # Log data
                    episode_rewards.append(reward)
                    data_logger.log_step(
                        obs, 
                        action, 
                        reward, 
                        info.get('collision', False),
                        info.get('magnetic_force', np.zeros(3))
                    )
                    
                    # Update visualization
                    visualizer.update(next_obs[:3], env.target_pos)
                    
                    obs = next_obs
                    
                except Exception as e:
                    print(f"Error during episode step: {str(e)}")
                    traceback.print_exc()
                    break
                    
            # End of episode processing
            episode_reward = sum(episode_rewards)
            metrics.log_episode(
                episode_rewards,
                len(episode_rewards),
                info.get('success', False),
                info.get('collisions', 0)
            )
            
            data_logger.end_episode()
            
            # Save best model
            if episode_reward > best_reward:
                best_reward = episode_reward
                torch.save(agent.state_dict(), 'best_model.pth')
                
            # Print progress
            if episode % 10 == 0:
                metrics_dict = metrics.get_metrics()
                print(f"Episode {episode}")
                print(f"Average Reward: {metrics_dict['avg_reward']:.2f}")
                print(f"Success Rate: {metrics_dict['success_rate']:.2f}")
                print(f"Average Collisions: {metrics_dict['avg_collisions']:.2f}")
                print("-" * 50)
                
    except Exception as e:
        print(f"Error during training: {str(e)}")
        traceback.print_exc()
    finally:
        env.close()
        data_logger.save_logs("training_log")
        visualizer.save("final_trajectory.png")

def main():
    try:
        # Set random seeds for reproducibility
        torch.manual_seed(42)
        np.random.seed(42)
        
        # Initialize all components
        env, agent, trainer, visualizer, metrics, data_logger = initialize_simulation()
        
        # Run training
        train_simulation(env, agent, trainer, visualizer, metrics, data_logger)
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()