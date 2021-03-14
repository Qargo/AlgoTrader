#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 15:53:35 2021

@author: dejan
trains five RL models that are implemented in Stable Baseline 3
"""
import os
import sys
import warnings
import pickle

sys.path.append("FinRL-Library")

from algotrader.config import config
from algotrader.model.agent import Agent
from finrl.env.env_stocktrading import StockTradingEnv


def train_a2c(agent):
    ### Model 1: A2C ###
    print("\n")
    print("==============Model 1: Training Model A2C===========")
    model_a2c = agent.get_model("a2c")
    trained_a2c = agent.train_model(model=model_a2c,
                                    tb_log_name='a2c',
                                    total_timesteps=100000)
    # save trained a2c model
    path_a2c = "./" + config.TRAINED_MODEL_DIR + "/trained_a2c"
    if os.path.exists(path_a2c):
        os.remove(path_a2c)
    agent.save_model(model=trained_a2c, path=path_a2c)
    # delete trained a2c model
    del trained_a2c


def train_ddpg(agent):
    #### Model 2: DDPG ###
    print("\n")
    print("==============Model 2: Training Model DDPG===========")
    model_ddpg = agent.get_model("ddpg")
    trained_ddpg = agent.train_model(model=model_ddpg,
                                     tb_log_name='ddpg',
                                     total_timesteps=50000)
    # save trained ddpg model
    path_ddpg = "./" + config.TRAINED_MODEL_DIR + "/trained_ddpg"
    if os.path.exists(path_ddpg):
        os.remove(path_ddpg)
    agent.save_model(model=trained_ddpg, path=path_ddpg)
    # delete trained ddpg model
    del trained_ddpg


def train_ppo(agent):
    ### Model 3: PPO ###
    print("\n")
    print("==============Model 3: Training Model PPO===========")
    PPO_PARAMS = {
        "n_steps": 2048,
        "ent_coef": 0.01,
        "learning_rate": 0.00025,
        "batch_size": 128,
    }
    model_ppo = agent.get_model("ppo", model_kwargs=PPO_PARAMS)
    trained_ppo = agent.train_model(model=model_ppo,
                                    tb_log_name='ppo',
                                    total_timesteps=100000)
    # save trained ppo model
    path_ppo = "./" + config.TRAINED_MODEL_DIR + "/trained_ppo"
    if os.path.exists(path_ppo):
        os.remove(path_ppo)
    agent.save_model(model=trained_ppo, path=path_ppo)
    # delete trained ppo model
    del trained_ppo


def train_td3(agent):
    ### Model 4: TD3 ###
    print("\n")
    print("==============Model 4: Training Model TD3===========")
    TD3_PARAMS = {"batch_size": 100,
                  "buffer_size": 1000000,
                  "learning_rate": 0.001}
    model_td3 = agent.get_model("td3", model_kwargs=TD3_PARAMS)
    trained_td3 = agent.train_model(model=model_td3,
                                    tb_log_name='td3',
                                    total_timesteps=30000)
    # save trained td3 model
    path_td3 = "./" + config.TRAINED_MODEL_DIR + "/trained_td3"
    if os.path.exists(path_td3):
        os.remove(path_td3)
    agent.save_model(model=trained_td3, path=path_td3)
    # delete trained td3 model
    del trained_td3

def train_sac(agent):
    ### Model 5: SAC ###
    print("\n")
    print("==============Model 5: Training Model TD3===========")
    SAC_PARAMS = {
        "batch_size": 128,
        "buffer_size": 1000000,
        "learning_rate": 0.0001,
        "learning_starts": 100,
        "ent_coef": "auto_0.1",
    }
    model_sac = agent.get_model("sac", model_kwargs=SAC_PARAMS)
    trained_sac = agent.train_model(model=model_sac,
                                    tb_log_name='sac',
                                    total_timesteps=80000)
    # save trained sac model
    path_sac = "./" + config.TRAINED_MODEL_DIR + "/trained_sac"
    if os.path.exists(path_sac):
        os.remove(path_sac)
    agent.save_model(model=trained_sac, path=path_sac)
    # delete trained sac model
    del trained_sac


def main():

    # Basic setup
    # Disable warnings
    warnings.filterwarnings('ignore')

    tech_indicator_list = config.TECHNICAL_INDICATORS_LIST

    # add following folders
    if not os.path.exists("./" + config.TRAINED_MODEL_DIR):
        os.makedirs("./" + config.TRAINED_MODEL_DIR)
    if not os.path.exists("./" + config.TENSORBOARD_LOG_DIR):
        os.makedirs("./" + config.TENSORBOARD_LOG_DIR)

    print()
    print("==============Load Training Data===========")
    path_training = "./" + config.DATA_SAVE_DIR + "/training.txt"

    with open(path_training, "rb") as f:
        dump = pickle.load(f)


    stock_dimension = len(dump.tic.unique())
    state_space = 1 + 2 * stock_dimension + len(tech_indicator_list) * stock_dimension
    print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")

    env_kwargs = {
        "hmax": 100,
        "initial_amount": 1000000,
        "buy_cost_pct": 0.001,
        "sell_cost_pct": 0.001,
        "state_space": state_space,
        "stock_dim": stock_dimension,
        "tech_indicator_list": tech_indicator_list,
        "action_space": stock_dimension,
        "reward_scaling": 1e-4
    }

    e_training_gym = StockTradingEnv(df=dump, **env_kwargs)

    print("Get Environment for Training")
    env_training, _ = e_training_gym.get_sb_env()
    print(type(env_training))

    # Implement DRL Algorithms
    #
    # The implementation of the DRL algorithms are based on OpenAI Baselines and Stable
    # Baselines.Stable Baselines is a fork of OpenAI Baselines,
    # with a major structural refactoring, and code cleanups.
    # FinRL library includes fine - tuned standard DRL algorithms, such as DQN, DDPG, Multi - Agent
    # DDPG, PPO, SAC, A2C and TD3. We also allow users to design their own
    # DRL algorithms by adapting these DRL algorithms.Instead of installing
    # FinRL lib I have included the source code and created my own version.

    agent = Agent(env=env_training)

    print("======================================================")
    print("Please select which training you want me to perform.")
    print("1. A2C - Advalntage Actor-Critic algorithm")
    print("2. DDPG - Deep Deterministic Policy Gradient algorithm")
    print("3. PPO - Proximal Policy Optimization algorithm")
    print("4. TD3 - Twin Delayed Deep Deterministic Policy Gradient algorithm")
    print("5. SAC - Soft Actor-Critic algorithm")
    print("6. All Algorithms")
    print("7. Exit")
    print("-------------------------------------------------------")
    selection = int(input("Select what you want me to do: "))

    if selection == 1:
        train_a2c(agent)

    elif selection == 2:
        train_ddpg(agent)

    elif selection == 3:
        train_ppo(agent)

    elif selection == 4:
        train_td3(agent)

    elif selection == 5:
        train_sac(agent)

    elif selection == 6:
        train_a2c(agent)
        train_ddpg(agent)
        train_ppo(agent)
        train_td3(agent)
        train_sac(agent)

    elif selection == 7:
        print("exit")
    else:
        print("Invalid option selected!")

if __name__ == "__main__":
    main()

