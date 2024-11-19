import matplotlib.pyplot as plt
import numpy as np
import pybullet as p

class Visualizer:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.trajectory = []
        
    def update(self, nanobot_pos, target_pos):
        self.trajectory.append(nanobot_pos)
        
        self.ax.clear()
        trajectory = np.array(self.trajectory)
        
        self.ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 'b-')
        self.ax.scatter(*nanobot_pos, color='red', s=100)
        self.ax.scatter(*target_pos, color='green', s=100)
        
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])
        plt.pause(0.01)
        
    def save(self, filename):
        plt.savefig(filename)