#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 08:49:06 2021

@author: srdjan
downloads financial data for all stocks specified in config file given start
and end date. Save the downloaded data to csv file.
"""
import os
import sys
from argparse import ArgumentParser

# add FinRL-Library path
sys.path.append("./FinRL-Library")

from algotrader.config import config
from finrl.marketdata.yahoodownloader import YahooDownloader


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

    print("All stocks used for training:", STOCK_LIST)
    print("Historical data are used from: ", START_DATE)
    print("Till end date: ", END_DATE)

    # Download and save the data in a pandas DataFrame:
    data_frame = YahooDownloader(start_date = START_DATE,
                                 end_date = END_DATE,
                                 ticker_list = STOCK_LIST).fetch_data()

    print("Data Frame shape is: ", data_frame.shape)
    print("Data Frame format is following: \n\n", data_frame.head())
    
    ##
    ## Save downloaded data to file
    ##
    if os.path.exists("./" + config.DATA_SAVE_DIR + "/" + options.name + ".csv"):
        os.remove("./" + config.DATA_SAVE_DIR + "/" + options.name + ".csv")
        print("The download data file deleted")
    else:
        print("The download data file does not exist")

    data_frame.to_csv("./" + config.DATA_SAVE_DIR + "/" + options.name + ".csv")

    print("Successfuly completed the task of downloading and saving financial data.")


if __name__ == "__main__":
    main()