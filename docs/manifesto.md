A **manifesto** is a published declaration of the intentions,  motives, or views of the issuer, be it an individual,  group, political  party or government.

### Goals

- Create a trading strategy
- Build a trading system
- Cashing out strategies (in-house development, banks, funds, ... )



### Trading Strategy (Dejan and Dragan)

Create a trading strategy by analyzing historical data:

- Explore the basic FinRL library
- Test the ensemble strategies using the FinRL library
- If FinRL library modifications are required, then identify, document and implement them 
- If we are happy with the FinRL library, then make it a git submodule of the AlgoTrader project 



### Trading System (Srdjan)

Converting data analysis into real-time software that will connect to a real exchange. In other words, the functional components supporting the trading strategy.

The purpose of a trading system is to automate the trading strategy. Building this kind of software requires taking the following into consideration:

- **Asset class**: knowing which asset class will be used will modify the data structure of the software. If US stocks are being targeted, then it should be clearly stated. [srdjan: I assume US equities]
- **Trading strategy type**: high frequency, long-term position or something else. The design of the software architecture is impacted by trading strategy type. For instance, high-frequency trading strategies require sending orders very rapidly (should decide to send orders within nanoseconds). A regular trading system for US equities should decide to send an order within microseconds.  [srdjan: I assume long-term position; in this case, the speed allowing a trader to get a liquidity faster than others is not important]
- **Number of users** (i.e. the number of trading strategies): when the number of trading strategies increases, the number of orders is higher. In other words, having more users requires a faster trading system [srdjan: I assume a single trading strategy]

The trading system collects the information needed by the trading strategy, and is in charge of sending
orders and receiving responses from the market regarding sent orders. The main functionalities are collecting the data (most of the time this will be price updates). If the trading strategy needs to get some quantitative data involving earnings, fed announcements (more generally news), these news will also trigger orders. When the trading strategy decides the direction of the position, the trading system will send orders accordingly . The trading system will also decide which specific exchange will be the best to
get the order filled for the requested price and for the requested volume.

#### Phase One (estimate: end of March 2021)

The main functionalities of the trading system will be encapsulated into Python objects. These components will communicating through unidirectional communication channels (a deque from the collections package). The first implementation will be limited to the following five main functional components:

- the liquidity provider
- the order book
- the above-mentioned trading strategy integration
- the order manager
- the market simulator



#### Phase Two (estimate: end of June 2021)

TBD 

#### Phase Three (estimate: end of September 2021)

TBD



### Deployment (Dragan, Dejan and Srdjan)

















