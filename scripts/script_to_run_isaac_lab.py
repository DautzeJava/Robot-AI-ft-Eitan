import argparse
from omni.isaac.lab.app import AppLauncher

# 1. Launch the Simulator (This MUST happen first)
parser = argparse.ArgumentParser(description="Train PPO from scratch.")
# add_app_launcher_args helps handle the GUI/Headless flags
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# 2. Imports that require the app to be running
import torch
import gymnasium as gym
import omni.isaac.lab_tasks  # This registers the default tasks

# 3. Create the Environment
# We will use a default "AnyDrive" or "Cartpole" just to test your PPO first
env_cfg = gym.make("Isaac-Cartpole-v0") # Swap this with your car later

# 5. The Training Loop
obs, _ = env_cfg.reset()

while simulation_app.is_running():
    with torch.inference_mode():
        # This is where your PPO decides what to do
        # actions = agent.act(obs) 
        
        # For now, let's just use random actions to see it move
        actions = torch.rand(env_cfg.action_space.shape, device=env_cfg.device) * 2 - 1
        
        # Step the simulation
        obs, rewards, terminated, truncated, info = env_cfg.step(actions)
        
        # If the car crashes/pole falls, Isaac Lab handles the reset automatically
        if terminated.any():
            print("Resetting environments...")

simulation_app.close()