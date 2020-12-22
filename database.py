#########################################################################################
#  Name: database.py
#  Description: Object relational mapping layer for Postgres db.
#  Author: Dejan Jovanovic
#  Created on:
#  License: MIT
#  Copyright 2021, Dejan Jovanovic
#########################################################################################

from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, BigInteger, Integer, String, DateTime, Boolean, Numeric,
                        ForeignKey, create_engine)

metadata = MetaData()

exchange = Table('algo_trader_dl.exchange', metadata,
                 Column('id', Integer(), autoincrement=True, primary_key=True),
                 Column('abbrev', String(32), nullable=False),
                 Column('name', String(255),nullable=False),
                 Column('city', String(255), nullable=False),
                 Column('country', String(255), nullable=False),
                 Column('currency', String(64), nullable=False),
                 Column('timezone_offset', DateTime(), default=datetime.timezone),
                 Column('created_date', DateTime(), default=datetime.now),
                 Column('last_updated_date', DateTime(), default=datetime.now, onupdate=datetime.now)
                 )

symbol = Table('algo_trader_dl.symbol', metadata,
                Column('id', Integer(), autoincrement=True, primary_key=True),
                Column('is_stock', Boolean(True), nullable=False),
                Column('ticker', String(32),nullable=False),
                Column('name', String(255), nullable=False),
                Column('sector', String(255), nullable=False),
                Column('currency', String(32), nullable=False),
                Column('exchange_id', ForeignKey('algo_trader_dl.exchange.id')),
                Column('created_date', DateTime(), default=datetime.now),
                Column('last_updated_date', DateTime(), default=datetime.now, onupdate=datetime.now)
               )

data_provider = Table('algo_trader_dl.daily_price', metadata,
                      Column('id', BigInteger(), autoincrement=True, primary_key=True),
                      Column('data_vendor_id', ForeignKey('algo_trader_dl.data_provider.id')),
                      Column('price_date', DateTime(), nullable=False),
                      Column('created_date', DateTime(), default=datetime.now),
                      Column('last_updated_date', DateTime(), default=datetime.now),
                      Column('open_price', Numeric(19,4)),
                      Column('high_price', Numeric(19,4)),
                      Column('low_price', Numeric(19,4)),
                      Column('close_price', Numeric(19,4)),
                      Column('adj_close_price', Numeric(19,4)),
                      Column('volume', BigIntiger()),
                      Column('symbol_id', ForeignKey('algo_trader_dl.symbol.id')),
                      Column('data_provider_id', ForeignKey('algo_trader_dl.data_provider.id'))
                      )

daily_price = Table('algo_trader_dl.data_provider', metadata,
                    Column('id', Integer(), autoincrement=True, primary_key=True),
                    Column('name', String(64), nullable=False),
                    Column('website_url', String(255), nullable=False),
                    Column('support_email', String(255), nullable=False),
                    Column('created_date', DateTime(), nullable=False),
                    Column('last_updated_date', DateTime(), nullable=False)
                    )

engine = create_engine('postgresql://algo_trader:algo_trader@192.168.0.28:5432/algo_trader_db')
metadata.create_all(engine)