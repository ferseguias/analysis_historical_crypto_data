# project_1_analysis_historical_crypto_data

![portada](https://www.sap.com/dam/application/imagelibrary/photos/287000/287437.jpg/_jcr_content/renditions/287437_homepage_3840_1200.jpg.adapt.1920_522.true.false.false.false.jpg/1629157434919.jpg)

# Objetive 🎯
The main intention of this work is to analize market data, transfor it into conclusions based in market facts and investing logic to increase knowleadge of this new important sector.

# Scope and extra information 🔎
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

1. btc_maxi🥇 : overview of most the relevant asset by market cap and history
    - Daily price
    - Weekly price
    - Monthly price candles (max, min, close)
    - Semesterly price candles (max, min, close)
    - Monthly marketcap
    - Circulating supply effect after last btc halving event

2. bullish_or_bearish🐂 🐻 : given a certain list of coins and date range, plot the accumulated gain/(loss) from each asset (funny fact: in the list of coins I selected during 2021, none of them gained less than 50% in that year - none of them reported loss 😎)

3. market_cake🍰 : top 10 cryptocurrencies pie chart by their market value

4. metaverse🎧 :
    - SAND/MANA marketcap and price comparasion
    - How Facebook's name change announcement affected these coins market value

5. terra_protocol🌝 : according to terra's protocol, ust and luna supply is correlated (not in direct way). Minting (creating) ust implies luna burnt (destruction)
    - Daily luna/ust price chart
    - Daily luna/ust circulating supply chart

# Files structure 📦

1. data folder: csv/json files used

2. notebooks folder: 
    - api: marketcap extraction
    - data_cleaning: transform and merge data
    - exploratory: visual image of data obtained
    - visualization: all analysis performed

3. scr folder: folder where all functions used along the project are stored

4. Output: all output files. 

![image](https://media-exp1.licdn.com/dms/image/C5616AQFPsX_nM6cvHw/profile-displaybackgroundimage-shrink_350_1400/0/1517365325735?e=1653523200&v=beta&t=0-8GdkJMo_wAa-ctg1OSBDel0MaXOgpQqp9deKCgMJY)

# Learnings 📈

- Analyzing historical data we can obtain insights of the market (in real time if desired) and improve our decisions. It's generaly accepted that patters repeat over time

- There are many opportunities in this industry, but as reflected in all charts, there is still a lot of volatility/risk

- As it is a young industry, the growth is supernatural. The less marketcap, the more volatility. It can be taken as an advantage or you get rekt!

- News clearly impact the market

- Buy crypto - not financial advice, DYOR 😄

# Tools 🔧

[sys](https://docs.python.org/3/library/sys.html)

[os](https://docs.python.org/3/library/os.html)

[pandas](https://pandas.pydata.org/)

[pycoingeckoAPI](https://www.coingecko.com/en/api/documentation)

[datetime](https://docs.python.org/3/library/datetime.html)

[time](https://docs.python.org/3/library/time.html)

[matplotlib](https://matplotlib.org/)

[pycoingecko](https://www.coingecko.com/en/api/documentation)
