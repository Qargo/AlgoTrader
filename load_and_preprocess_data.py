#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  14 2021

@author: dejan
loads downloaded financial data for all stocks specified in config file and
add technical indicators. Split the dataset on training and testing set.
"""
# import all libraries
import pickle

import os
import sys
import pandas as pd
import warnings
from argparse import ArgumentParser


# add FinRL-Library path
sys.path.append("./FinRL-Library")

from algotrader.config import config
from finrl.preprocessing.preprocessors import FeatureEngineer
from finrl.preprocessing.data import data_split


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--name",
        dest="name",
        help="",
        metavar="NAME",
        default="dow_30_ticker",
    )
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()

    # Basic setup
    #Disable warnings
    warnings.filterwarnings('ignore')

    # Load the saved data in a pandas DataFrame:
    data_frame = pd.read_csv("./" + config.DATA_SAVE_DIR + "/" + options.name + ".csv")

    print("Data Frame shape is: ", data_frame.shape)
    print("Data Frame format is following: \n\n", data_frame.head())

    ## we store the stockstats technical indicator column names in config.py
    tech_indicator_list=config.TECHNICAL_INDICATORS_LIST
    print("Technical Indicators that are going to be calculated: ", tech_indicator_list)

    feature_engineering = FeatureEngineer(
                        use_technical_indicator=True,
                        tech_indicator_list=tech_indicator_list,
                        use_turbulence=True,
                        user_defined_feature=False)

    processed = feature_engineering.preprocess_data(data_frame)

    print(processed.sort_values(['date','tic'], ignore_index=True).head(10))

    training_set = data_split(processed, config.START_DATE, config.START_TRADE_DATE)
    testing_set = data_split(processed, config.START_TRADE_DATE, config.END_DATE)
    print("Size of training set: ", len(training_set))
    print("Size of testing set: ", len(testing_set))

    print("Training set format:\n\n", training_set.head())

    print("Testing set format: \n\n", testing_set.head())

    stock_dimension = len(training_set.tic.unique())
    state_space = 1 + 2*stock_dimension + len(tech_indicator_list)*stock_dimension
    print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")

    ##
    ## Save data to file, both training and trading
    ##
    if os.path.exists("./" + config.DATA_SAVE_DIR + "/training.txt"):
        os.remove("./" + config.DATA_SAVE_DIR + "/training.txt")
        print("The training data file deleted")
    else:
        print("The training data file does not exist")

    if os.path.exists("./" + config.DATA_SAVE_DIR + "/testing.txt"):
        os.remove("./" + config.DATA_SAVE_DIR + "/testing.txt")
        print("The testing data file deleted")
    else:
        print("The testing data file does not exist")

    path_training = "./" + config.DATA_SAVE_DIR + "/training.txt"
    path_testing = "./" + config.DATA_SAVE_DIR + "/testing.txt"

    with open(path_training, "wb") as f:
        pickle.dump(training_set, f, pickle.HIGHEST_PROTOCOL)

    with open(path_testing, "wb") as f:
        pickle.dump(testing_set, f, pickle.HIGHEST_PROTOCOL)

    print("Successfuly completed the task of creation of test and training data files.")


if __name__ == "__main__":
    main()