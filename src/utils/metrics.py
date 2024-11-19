class MetricsLogger:
    def __init__(self):
        self.episode_rewards = []
        self.episode_lengths = []
        self.success_rate = []
        self.collision_count = []
        
    def log_episode(self, rewards, length, success, collisions):
        self.episode_rewards.append(sum(rewards))
        self.episode_lengths.append(length)
        self.success_rate.append(float(success))
        self.collision_count.append(collisions)
        
    def get_metrics(self):
        return {
            'avg_reward': np.mean(self.episode_rewards[-100:]),
            'avg_length': np.mean(self.episode_lengths[-100:]),
            'success_rate': np.mean(self.success_rate[-100:]),
            'avg_collisions': np.mean(self.collision_count[-100:])
        }