#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 08:49:06 2021

@author: srdjan
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
    
    if not os.path.exists("./" + config.DATA_SAVE_DIR):
        os.makedirs("./" + config.DATA_SAVE_DIR)

    df = YahooDownloader(start_date=config.START_DATE,
                         end_date=config.END_DATE,
                         ticker_list=config.DOW_30_TICKER).fetch_data()
    df.to_csv("./" + config.DATA_SAVE_DIR + "/" + options.name + ".csv")

        
if __name__ == "__main__":
    main()