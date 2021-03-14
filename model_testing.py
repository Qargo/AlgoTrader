#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:26:16 2021

@author: srdjan
tests five RL models that are implemented in Stable Baseline 3
"""
import sys
import warnings
import pickle
import pandas as pd

sys.path.append("FinRL-Library")

from algotrader.config import config
from algotrader.model.agent import Agent
from finrl.env.env_stocktrading import StockTradingEnv
from finrl.trade.backtest import backtest_stats


def test_model(model, environment, name):
    df_account_value, df_actions = Agent.DRL_prediction(
        model=model, environment=environment
    )
    df_account_value.to_csv(
        "./" + config.RESULTS_DIR + "/df_account_value_" + name + ".csv"
    )
    df_actions.to_csv("./" + config.RESULTS_DIR + "/df_actions_" + name + ".csv")
    print("==============Get Backtest Results===========")
    perf_stats_all = backtest_stats(account_value=df_account_value)
    perf_stats_all = pd.DataFrame(perf_stats_all)
    perf_stats_all.to_csv("./" + config.RESULTS_DIR + "/perf_stats_all_" + name + '.csv')


def test_a2c(env):
    ### Model 1: A2C ###
    print("\n")
    print("==============Model 1: Testing Model A2C===========")
    # load trained a2c model
    path_a2c = "./" + config.TRAINED_MODEL_DIR + "/trained_a2c"
    model_a2c = Agent.load_model(model_name="a2c", path=path_a2c)
    # test a2c model
    test_model(model=model_a2c, environment=env, name="a2c")


def test_ddpg(env):
    #### Model 2: DDPG ###
    print("\n")
    print("==============Model 2: Testing Model DDPG===========")
    # load trained ddpg model
    path_ddpg = "./" + config.TRAINED_MODEL_DIR + "/trained_ddpg"
    model_ddpg = Agent.load_model(model_name="ddpg", path=path_ddpg)
    # test ddpg model
    test_model(model=model_ddpg, environment=env, name="ddpg")


def test_ppo(env):
    ### Model 3: PPO ###
    print("\n")
    print("==============Model 3: Testing Model PPO===========")
    # load trained ppo model
    path_ppo = "./" + config.TRAINED_MODEL_DIR + "/trained_ppo"
    model_ppo = Agent.load_model(model_name="ppo", path=path_ppo)
    # test ppo model
    test_model(model=model_ppo, environment=env, name="ppo")


def test_td3(env):
    ### Model 4: TD3 ###
    print("\n")
    print("==============Model 4: Testing Model TD3===========")
    # load trained td3 model
    path_td3 = "./" + config.TRAINED_MODEL_DIR + "/trained_td3"
    model_td3 = Agent.load_model(model_name="td3", path=path_td3)
    # test td3 model
    test_model(model=model_td3, environment=env, name="td3")


def test_sac(env):
    ### Model 5: SAC ###
    print("\n")
    print("==============Model 5: Testing Model SAC===========")
    # load trained sac model
    path_sac = "./" + config.TRAINED_MODEL_DIR + "/trained_sac"
    model_sac = Agent.load_model(model_name="sac", path=path_sac)
    # test sac model
    test_model(model=model_sac, environment=env, name="sac")


def main():

    # Basic setup
    # Disable warnings
    warnings.filterwarnings('ignore')

    tech_indicator_list = config.TECHNICAL_INDICATORS_LIST

    print()
    print("==============Load Testing Data===========")
    path_testing = "./" + config.DATA_SAVE_DIR + "/testing.txt"

    with open(path_testing, "rb") as f:
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

    e_testing_gym = StockTradingEnv(df=dump, turbulence_threshold=250, **env_kwargs)

    print("Get Environment for Testing")
    env_testing, _ = e_testing_gym.get_sb_env()
    print(type(env_testing))

    # Implement DRL Algorithms
    #
    # The implementation of the DRL algorithms are based on OpenAI Baselines and Stable
    # Baselines.Stable Baselines is a fork of OpenAI Baselines,
    # with a major structural refactoring, and code cleanups.
    # FinRL library includes fine - tuned standard DRL algorithms, such as DQN, DDPG, Multi - Agent
    # DDPG, PPO, SAC, A2C and TD3. We also allow users to design their own
    # DRL algorithms by adapting these DRL algorithms.Instead of installing
    # FinRL lib I have included the source code and created my own version.

    print("======================================================")
    print("Please select which testing you want me to perform.")
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
        test_a2c(e_testing_gym)

    elif selection == 2:
        test_ddpg(e_testing_gym)

    elif selection == 3:
        test_ppo(e_testing_gym)

    elif selection == 4:
        test_td3(e_testing_gym)

    elif selection == 5:
        test_sac(e_testing_gym)

    elif selection == 6:
        test_a2c(e_testing_gym)
        test_ddpg(e_testing_gym)
        test_ppo(e_testing_gym)
        test_td3(e_testing_gym)
        test_sac(e_testing_gym)

    elif selection == 7:
        print("exit")
    else:
        print("Invalid option selected!")

if __name__ == "__main__":
    main()

