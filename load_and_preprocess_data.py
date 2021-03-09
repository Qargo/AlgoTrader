#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  14 2021

@author: dejan
loads financial data for all stocks specified in config file and
add technical indicators. Split the dataset on training and testing set.
"""
# import all libraries
import pickle

import os
import sys
import warnings

# add FinRL-Library path
sys.path.append("./FinRL-Library")

from config import config
from finrl.marketdata.yahoodownloader import YahooDownloader
from finrl.preprocessing.preprocessors import FeatureEngineer
from finrl.preprocessing.data import data_split


# Basic setup
#Disable warnings
warnings.filterwarnings('ignore')

# add following folders
if not os.path.exists("./" + config.DATA_SAVE_DIR):
    os.makedirs("./" + config.DATA_SAVE_DIR)

# From config.py file get following:
# start_date
START_DATE = config.START_DATE

# end_date
END_DATE = config.END_DATE

# list of stocks#
STOCK_LIST = config.DOW_30_TICKER

print("All stocks used for training:",STOCK_LIST)
print("Historical data are used from: ", START_DATE)
print("Till end date: ", END_DATE)

# Download and save the data in a pandas DataFrame:
data_frame = YahooDownloader(start_date = START_DATE,
                             end_date = END_DATE,
                             ticker_list = STOCK_LIST).fetch_data()

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
