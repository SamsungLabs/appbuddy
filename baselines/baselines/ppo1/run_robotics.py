#!/usr/bin/env python3

# Importing required libraries
from mpi4py import MPI
import mujoco_py
from baselines import logger
from baselines.common import set_global_seeds
from baselines.common.cmd_util import make_robotics_env, robotics_arg_parser
from baselines.ppo1 import mlp_policy, pposgd_simple
import baselines.common.tf_util as U


# Function to train the PPO1 algorithm
def train(env_id, num_timesteps, seed):
    
    # Get the rank of the current MPI process
    rank = MPI.COMM_WORLD.Get_rank()
    
    # Create a single-threaded TensorFlow session
    sess = U.single_threaded_session()
    sess.__enter__()
    
    # Ignore warnings related to MuJoCo
    mujoco_py.ignore_mujoco_warnings().__enter__()
    
    # Set the random seed for this worker
    workerseed = seed + 10000 * rank
    set_global_seeds(workerseed)
    
    # Create the OpenAI robotics environment
    env = make_robotics_env(env_id, workerseed, rank=rank)
    
    # Define the neural network policy function
    def policy_fn(name, ob_space, ac_space):
        return mlp_policy.MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space,
            hid_size=256, num_hid_layers=3)
    
    # Train the PPO1 algorithm
    pposgd_simple.learn(env, policy_fn,
            max_timesteps=num_timesteps,
            timesteps_per_actorbatch=2048,
            clip_param=0.2, entcoeff=0.0,
            optim_epochs=5, optim_stepsize=3e-4, optim_batchsize=256,
            gamma=0.99, lam=0.95, schedule='linear',
        )
    
    # Close the environment
    env.close()


# Main function
def main():
    # Parse command line arguments
    args = robotics_arg_parser().parse_args()
    
    # Train the PPO1 algorithm
    train(args.env, num_timesteps=args.num_timesteps, seed=args.seed)


# Run the main function if this script is executed
if __name__ == '__main__':
    main()
