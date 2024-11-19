import pybullet as p
import numpy as np
import torch
import os

def check_system_compatibility():
    checks = {
        "GPU Available": torch.cuda.is_available(),
        "PyBullet Version": p.getAPIVersion(),
        "CUDA Version": torch.version.cuda if torch.cuda.is_available() else "Not available",
        "Python Version": sys.version,
    }
    return checks

def test_environment(env):
    try:
        # Test reset
        obs = env.reset()
        assert len(obs) == 9, "Observation space mismatch"
        
        # Test step
        action = np.zeros(3)
        next_obs, reward, done, _, info = env.step(action)
        assert len(next_obs) == 9, "Next observation space mismatch"
        assert isinstance(reward, float), "Reward type mismatch"
        assert isinstance(done, bool), "Done flag type mismatch"
        
        return True, "Environment tests passed"
    except Exception as e:
        return False, f"Environment test failed: {str(e)}"

def test_agent(agent):
    try:
        # Test forward pass
        dummy_input = torch.randn(1, 9)
        mean, std = agent(dummy_input)
        assert mean.shape == (1, 3), "Agent output shape mismatch"
        assert std.shape == (3,), "Agent std shape mismatch"
        
        return True, "Agent tests passed"
    except Exception as e:
        return False, f"Agent test failed: {str(e)}"

def run_diagnostics():
    print("Running system diagnostics...")
    
    # Check system compatibility
    compat = check_system_compatibility()
    for key, value in compat.items():
        print(f"{key}: {value}")
    
    # Check directory structure
    required_dirs = ['logs', 'src', 'tests']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"Creating missing directory: {dir_name}")
            os.makedirs(dir_name)
            
    # Test PyBullet
    try:
        client = p.connect(p.DIRECT)
        p.disconnect()
        print("PyBullet test: Passed")
    except Exception as e:
        print(f"PyBullet test failed: {str(e)}")
        
    print("Diagnostics complete")

if __name__ == "__main__":
    run_diagnostics()