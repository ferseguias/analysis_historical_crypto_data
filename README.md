# project_1_analysis_historical_crypto_data

![portada](https://www.sap.com/dam/application/imagelibrary/photos/287000/287437.jpg/_jcr_content/renditions/287437_homepage_3840_1200.jpg.adapt.1920_522.true.false.false.false.jpg/1629157434919.jpg)

# Objetive 🎯
The main intention of this work is to analize market data, transfor it into conclusions based in market facts and investing logic to increase knowleadge of this new important sector.

# Scope and assets extra information 🔎
From a wide list of cryptocurrencies in the market, I'll select the most relevant by market capitalization for the purpose of this project. 
| Assets | Ticker | Creation year | Timeframe analyzed |
| :---        |    :---:   |          ---: |          ---: |
| Bitcoin | btc | 2009 | 2018-2021 |
| Ethereum | eth | 2015 | 2018-2021 |
| Binance | bnb | 2017 | 2018-2021 |
| Terra | luna | 2018 | 2018-2021 |
| UST Stable | ust | 2018 | 2018-2021 |
| Solana | sol | 2017 | 2018-2021 |
| ADA | ada | 2017 | 2018-2021 |
| Avalanche | avax | 2020 | 2020-2021 |
| Polkadot | dot | 2020 | 2020-2021 |
| Doge Coin | doge | 2013 | 2018-2021 |
| Polygon | matic | 2017 | 2018-2021 |
| Cosmos | atom | 2014 | 2018-2021 |
| Litecoin | ltc | 2011 | 2018-2021 |
| Fantom | ftm | 2018 | 2018-2021 |
| Decentraland | mana | 2017 | 2018-2021 |
| Sandbox | sand | 2021 | 2021 |

***oredered by marketcap*

# Data sources 📊

[Kaggle](https://www.kaggle.com/kaushiksuresh147/top-10-cryptocurrencies-historical-dataset): to get daily cyptocurrencies historical prices dataset since the beginning of each coin (csv format).

[Coingecko API doc](https://www.coingecko.com/en/api/documentation): to get cyptocurrencies daily historical market capitalization dataset since 2018 till 2021.

Relevant column names used in data:
| column | description |
| :---        | :---        |
| open | price at the begining of the day |
| high | higher price reached |
| low | higher price reached |
| close |price at the end of the day |
| volume | total trades in US dollars |
| market_cap | total market capitalization (mkt_cap = circ_supply * price) |
| circulating_supply | total coins in circulation |

# Step by step through data obtention 🏃🏽‍♂️

1. Get prices:
    - Download csv files from web into "data" folder, clean names and rename them (one file per coin)
    - In order to unify data, loop by list names and concatenate all coins data into one dataframe

2. Get marketcap:
    - Connect to API, provide parameters and export json files (one per coin)
    - In order to unify data, loop by list names and concatenate all coins data into one dataframe

3. Merge databases by coin/date (cleaning, filling missings and filtering data)

4. Dictionary creation to perform queries

![image](https://blackwellglobal.com/wp-content/uploads/2019/09/Japanese-Candlesticks-Technical-Analysis-Blackwell-Global-FCA-Forex-Broker-2-1200x420.jpg)

# A picture is worth a thousand words:

1. btc_maxi: overview of most the relevant asset by market cap and history
    - Daily price
    - Weekly price
    - Monthly price candles (max, min, close)
    - Semesterly price candles (max, min, close)
    - Monthly marketcap
    - Circulating supply effect after last btc halving event

2. bullish_or_bearish: given a certain list of coins and date range, plot the accumulated gain/(loss) from each asset (funny fact: in the list of coins i selected during 2021, non of them gained less than 50% in that year - of course none of them reported loss)

3. market_cake: top 10 cryptocurrencies pie chart by their market value

4. metaverse:
    - SAND/MANA marketcap and price comparasion
    - How Facebook's name change announcement affected these coins market value

5. terra_protocol: according to terra's protocol, ust and luna supply is correlated (not in direct way). Minting (creating) ust implies luna burnt (destruction)
    - Daily luna/ust price chart
    - Daily luna/ust circulating supply chart

# Files structure 📦

1. data folder: csv/json files used

2. notebooks folder: 
    - api
    - data_cleaning
    - exploratory
    - visualization

2. scr folder: folder where all the .py files are stored with all the explained functions used during the whole project.The .py files included are: 
    - 
    - 
    - 

3. Output: all output files. 

# Conclusion 📈


Having a customized dashbord
- Volatility: bigger market cap, less volatility

- Market growth

- News impact in the market

- Quick market overview to improve decisions

- Buy crypto - not financial advice, DYOR 😄

This project is a part of the Data Analyst Bootcamp at Ironhack (Madrid)
-- Project Status: 1/3 [Completed]

# Tools 🔧

[sys](https://docs.python.org/3/library/sys.html)

[requests](https://pypi.org/project/requests/2.7.0/)

[pandas](https://pandas.pydata.org/)

[dotenv](https://pypi.org/project/python-dotenv/)

[pymongo](https://www.mongodb.com/2)

[json](https://docs.python.org/3/library/json.html)

[os](https://docs.python.org/3/library/os.html)

[geopandas](https://geopandas.org/)

[shapely](https://pypi.org/project/Shapely/)

[reduce](https://docs.python.org/3/library/functools.html)

[operator](https://docs.python.org/3/library/operator.html)

[import dumps](https://pymongo.readthedocs.io/en/stable/api/bson/json_util.html)

[re](https://docs.python.org/3/library/re.html)