import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from ..config import SimConfig

class PPOTrainer:
    def __init__(self, agent, env):
        self.agent = agent
        self.env = env
        self.optimizer = optim.Adam(agent.parameters(), lr=3e-4)
        
        self.clip_param = 0.2
        self.ppo_epochs = 10
        self.batch_size = 64
        self.gamma = 0.99
        self.gae_lambda = 0.95
        
    def compute_gae(self, values, rewards, masks):
        """Compute Generalized Advantage Estimation"""
        advantages = torch.zeros_like(rewards)
        gae = 0
        
        for t in reversed(range(len(rewards))):
            if t < len(rewards) - 1:
                delta = rewards[t] + self.gamma * values[t + 1] * masks[t] - values[t]
            else:
                delta = rewards
                gae = delta + self.gamma * self.gae_lambda * masks[t] * gae
                advantages[t] = gae
            
        returns = advantages + values
        return advantages, returns
        
    def update(self, observations, actions, old_log_probs, rewards, masks):
        observations = torch.FloatTensor(observations)
        actions = torch.FloatTensor(actions)
        old_log_probs = torch.FloatTensor(old_log_probs)
        rewards = torch.FloatTensor(rewards)
        masks = torch.FloatTensor(masks)
        
        old_mean, old_std = self.agent(observations)
        old_dist = torch.distributions.Normal(old_mean, old_std)
        
        with torch.no_grad():
            old_values = self.agent.value(observations)
            advantages, returns = self.compute_gae(old_values, rewards, masks)
            
        for _ in range(self.ppo_epochs):
            for batch_idx in range(0, len(observations), self.batch_size):
                batch_obs = observations[batch_idx:batch_idx + self.batch_size]
                batch_actions = actions[batch_idx:batch_idx + self.batch_size]
                batch_old_log_probs = old_log_probs[batch_idx:batch_idx + self.batch_size]
                batch_advantages = advantages[batch_idx:batch_idx + self.batch_size]
                batch_returns = returns[batch_idx:batch_idx + self.batch_size]
                
                mean, std = self.agent(batch_obs)
                dist = torch.distributions.Normal(mean, std)
                
                new_log_probs = dist.log_prob(batch_actions).sum(-1)
                values = self.agent.value(batch_obs)
                
                ratio = torch.exp(new_log_probs - batch_old_log_probs)
                surr1 = ratio * batch_advantages
                surr2 = torch.clamp(ratio, 1.0 - self.clip_param, 1.0 + self.clip_param) * batch_advantages
                
                actor_loss = -torch.min(surr1, surr2).mean()
                critic_loss = nn.MSELoss()(values, batch_returns)
                
                loss = actor_loss + 0.5 * critic_loss
                
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                
        return actor_loss.item(), critic_loss.item()
