import pybullet as p
import numpy as np
from src.environment.nanobot_env import EnhancedNanobotEnv
from src.training.ppo_trainer import train_nanobot
from src.utils.visualization import Visualizer
from src.utils.metrics import MetricsTracker

def main():
    # Initialize environment
    env = EnhancedNanobotEnv()
    
    # Initialize visualization and metrics
    visualizer = Visualizer()
    metrics = MetricsTracker()
    
    # Train the model
    model = train_nanobot(env)
    
    # Run evaluation episodes
    n_evaluation_episodes = 10
    for episode in range(n_evaluation_episodes):
        obs = env.reset()
        done = False
        episode_reward = 0
        
        while not done:
            # Get action from trained model
            action, _ = model.predict(obs, deterministic=True)
            
            # Step environment
            obs, reward, done, info = env.step(action)
            
            # Update metrics
            metrics.update(reward, info)
            
            # Visualize if needed
            visualizer.update(env)
            
            episode_reward += reward
        
        # Log episode results
        metrics.log_episode(episode, episode_reward)
    
    # Save results
    metrics.save_results("evaluation_results.json")
    visualizer.save_animation("nanobot_trajectory.gif")
    
    # Cleanup
    env.close()

if __name__ == "__main__":
    main()