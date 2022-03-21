from os import walk
import os
import pandas as pd
from pycoingecko import CoinGeckoAPI
import datetime
import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

######################################################################

#01_csv_rename:
def csv_rename():

    """ renames the csv files into non separated lower names
        parameters: -no parameters-  """

    data_path = "/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/data/top_100_crypto_coins"

    original_filename = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        original_filename.extend(filenames)
        break

    filename = []
    for name in original_filename:
        new_name = name.replace(" ", "_").lower()
        filename.append(new_name)
        os.rename(data_path + "/" + name, data_path + "/" + new_name)
    return print("done!")

######################################################################

#01_json_export:

def json_marketcap(coin, pair, from_date, to_date):

    """ export from coingeckoAPI json file with marketcap data for all coins listed
        parameters:
        coin: list of coins selected in scope
        pair: always usd for price comparasion
        from_date: date selected
        to_date: date selected """

    cg = CoinGeckoAPI()

    #translate from coin ticker (unique) to coin id (json)
    coin_list = pd.DataFrame(cg.get_coins_list())
    coin_id = coin_list.loc[lambda coin_list : coin_list['symbol'] == f"{coin}"]["id"].iloc[0]
    time.sleep(4)

    #query marketcap by date range
    marketcap = pd.DataFrame(cg.get_coin_market_chart_range_by_id(id=coin_id, vs_currency=pair, from_timestamp=from_date.strftime('%s'), to_timestamp=to_date.strftime('%s')))
    marketcap["coin"] = coin
    variable_path = f"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/data/coingecko_marketcap/{coin}.json"
    time.sleep(4)
    return marketcap.to_json(variable_path, index = True)

######################################################################

#02_csv_unification:
def csv_unification():

    """ unifies the csv files with prices into one csv file to be transformed
        parameters: -no parameters-  """

    cryptos = {"btc" : "bitcoin", 
            "eth" : "ethereum", 
            "bnb" : "bnb", 
            "luna" : "terra", 
            "sol" : "solana", 
            "ada" : "cardano", 
            "avax" : "avalanche", 
            "dot" : "polkadot", 
            "doge" : "dogecoin", 
            "matic" : "polygon", 
            "atom" : "cosmos", 
            "ltc" : "litecoin", 
            "ftm" : "fantom", 
            "mana" : "decentraland", 
            "sand" : "the_sandbox", 
            "usdt" : "tether", 
            "usdc" : "usd_coin", 
            "busd" : "binance_usd", 
            "ust" : "terrausd", 
            "dai" : "dai"}

    data_path = "/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/data/top_100_crypto_coins/"
    columns_csv = ["Date", "Open", "High", "Low", "Close", "Volume", "Currency", "Coin"]
    df = pd.DataFrame([], columns=columns_csv)

    for key, value in cryptos.items():
        csv_file = pd.read_csv(data_path + value + ".csv")
        csv_file["Coin"] = key
        df = pd.concat([df, csv_file], axis=0, join='outer', ignore_index=False)

    output_path = r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/cryptos_raw.csv"
    return df.to_csv(output_path, index = False)

######################################################################

#02_json_unification:
def json_unification():

    """ unifies the json files with marketcaps into one json file to be transformed
        parameters: -no parameters-  """

    cryptos = ['btc', 'eth', 'bnb', 'luna', 
            'sol', 'ada', 'avax', 'dot', 
            'doge', 'matic', 'atom', 'ltc', 
            'ftm', 'mana', 'sand', 'usdt', 
            'usdc', 'busd', 'ust', 'dai']

    data_path = "/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/data/coingecko_marketcap/"
    columns_json = ["prices", "market_caps", "total_volumes", "coin"]
    df = pd.DataFrame([], columns=columns_json)

    for coin in cryptos:
        json_file = pd.read_json(f"{data_path}{coin}.json")
        df = pd.concat([df, json_file], axis=0, join='outer', ignore_index=True)

    output_path = r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/cryptos_raw.json"
    return df.to_json(output_path, index=True)

######################################################################

#03_price_transformation:
def price_transfor(df):

    """ price dataframe transformation (clean columns, change data types) and csv creation
        parameters:
        df: dataframe with all prices data """

    #rename columns to lower
    clean_columns = []
    for col in df.columns:
        clean_columns.append(col.lower())
    df.columns = clean_columns

    #change types: date to datetime / coin to category / floats to round float
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.strftime('%d/%m/%Y')
    df["coin"] = df["coin"].astype('category')
    round_list = ["open", "high", "low", "close"]
    for col in round_list:
        df[col] = df[col].astype(float)
        df[col] = df[col].round(5)
    output_path = "/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/cryptos_price.csv"
    return df.to_csv(output_path, index=False)

######################################################################

#03_mc_transformation:
def mc_transfor(df):

    """ marketcap dataframe transformation (clean columns, change data types) and csv creation
        parameters:
        df: dataframe with all marketcap data """

    #get values in lists and drop old colums
    df[['date','price']] = pd.DataFrame(df.prices.tolist(), index= df.index)
    df['market_cap'] = df["market_caps"].apply(lambda x : x[1])
    df['total_volume'] = df["total_volumes"].apply(lambda x : x[1])
    df.drop(["prices", "market_caps", "total_volumes"], axis=1, inplace=True)

    #change types: date to datetime / coin to category / floats to round float
    df["date"] = df["date"].apply(lambda x : datetime.datetime.fromtimestamp(x / 1e3))
    df["date"] = df["date"].dt.strftime('%d/%m/%Y')
    df["coin"] = df["coin"].astype('category')
    df["price"] = df["price"].astype(float).round(5)
    df[["market_cap", "total_volume"]] = df[["market_cap", "total_volume"]].astype(int)

    output_path = "/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/cryptos_mc.csv"
    return df.to_csv(output_path, index=False)

######################################################################

#04_price_mc_integration:
def merge_data(price, marketcap):

    """ prices/marketcap dataframe integration (merge) and csv merged creation
        parameters:
        price: dataframe with all prices data
        marketcap: dataframe with all marketcap data """

    outer_merged = pd.merge(price, marketcap, how="outer", on=["date", "coin"])
    output_path = "/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/cryptos_merged.csv"
    return outer_merged.to_csv(output_path, index=False)

######################################################################

#05_data_cleaning:
def data_cleaning():

    """ cleans integrated data, also performs filter with scope 2018-2021 and exports clean data to csv
        parameters: -no parameters-  """

    df = pd.read_csv("/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/cryptos_merged.csv")

    #add year/month column to filter easier
    df['date'] = df['date'].astype("str")
    df['year'] = df['date'].apply(lambda x : x.split("/")[2])
    df['month'] = df['date'].apply(lambda x : x.split("/")[1])
    df['day'] = df['date'].apply(lambda x : x.split("/")[0])

    #substitude zero values in market_cap column for NaN
    df.loc[df["market_cap"] == 0,"market_cap"] = np.nan

    #replace price (ohlc), volume and currency null values
    mask_price = df["open"].isnull(), ["open", "high", "low", "close"]
    df.loc[mask_price] = df["price"]

    mask_vol = df["volume"].isnull(), "volume"
    df.loc[mask_vol] = df["total_volume"]

    mask_cur = df["currency"].isnull(), "currency"
    df.loc[mask_cur] = "USD"

    mask_price1 = df["price"].isnull(), "price"
    df.loc[mask_price1] = df["close"]

    mask_vol1 = df["total_volume"].isnull(), "total_volume"
    df.loc[mask_vol1] = df["volume"]

    #df filter by date (scope)
    df.set_index("year", inplace=True)
    scope = df.loc[["2018", "2019", "2020", "2021"], :]
    scope.reset_index()

    #drop duplicated columns
    scope.drop(["currency", "price", "total_volume"], inplace=True, axis=1)

    #supply column (market_cap = close * circulating_supply / circulating_supply = market_cap / close)
    scope["circulating_supply"] = scope["market_cap"] / scope["close"]

    #order columns
    scope = scope.reset_index()
    scope = scope[['coin', 'date', 'year', 'month', 'day', 'open', 'high', 'low', 'close', 'volume', 'market_cap', 'circulating_supply']]

    #export clean csv
    output_path = r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/scope.csv"
    return scope.to_csv(output_path, index = False)

######################################################################

#visualization btc_maxi:
def btc_maxi():

    """ plots several different analysis of bitcoin (price in different timeframes, marketcap and supply with halving)
        parameters: -no parameters-  """

    sns.set_style("darkgrid")
    warnings.filterwarnings('ignore')

    scope = pd.read_csv(r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/scope.csv")
    scope = scope.loc[scope["coin"] == "btc"]
    scope["period"] = scope["date"].astype("str")

    #weekly candlesticks:
    scope['date'] = pd.to_datetime(scope['date'])
    scope['week_number'] = scope['date'].dt.week #getting week number
    weekly_scope = scope.groupby(['year', 'week_number'], as_index=False).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last', 'volume':'sum', 'market_cap':"mean", "circulating_supply":"mean"}) #grouping based on required values
    weekly_scope["period"] = weekly_scope["year"].astype("str") + "-" + weekly_scope["week_number"].astype("str")

    #monthly candlesticks:
    monthly_scope = scope.groupby(['year','month'], as_index=False).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last', 'volume':'sum', 'market_cap':"mean", "circulating_supply":"mean"}) #grouping based on required values
    monthly_scope["period"] = monthly_scope["year"].astype("str") + "-" + monthly_scope["month"].astype("str")

    #semester candlesticks:
    def semester(month):
        if month > 6:
            return 2
        else:
            return 1
    scope['semester'] = scope["month"].apply(semester) #getting semester number
    semester_scope = scope.groupby(['year','semester'], as_index=False).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last', 'volume':'sum', 'market_cap':"mean", "circulating_supply":"mean"}) #grouping based on required values
    semester_scope["period"] = semester_scope["year"].astype("str") + "-" + semester_scope["semester"].astype("str")

    fig, axes = plt.subplots(6, 1, figsize=(20, 25), sharex=False, sharey=False)

    fig = sns.lineplot(data=scope, x="period", y="close", ax=axes[0], color = "black", marker = "o", markersize = 3)
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 100 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    axes[0].set_title('Bitcoin analysis: price over time - candles timeframe daily')

    fig = sns.lineplot(data=weekly_scope, x="period", y="close", ax=axes[1])
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 20 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    axes[1].set_title('Bitcoin analysis: price over time - candles timeframe weekly')

    fig = sns.lineplot(data=monthly_scope, x="period", y="close", ax=axes[2], label="price")
    fig = sns.lineplot(data=monthly_scope, x="period", y="low", ax=axes[2], label="min price")
    fig = sns.lineplot(data=monthly_scope, x="period", y="high", ax=axes[2], label="max price")
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 5 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    axes[2].set_title('Bitcoin analysis: price over time - candles timeframe monthly')

    fig = sns.lineplot(data=semester_scope, x="period", y="close", ax=axes[3], label="price")
    fig = sns.lineplot(data=semester_scope, x="period", y="low", ax=axes[3], label="min price")
    fig = sns.lineplot(data=semester_scope, x="period", y="high", ax=axes[3], label="max price")
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 1 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    axes[3].set_title('Bitcoin analysis: price over time - candles timeframe semester')

    fig = sns.lineplot(data=monthly_scope, x="period", y="market_cap", ax=axes[4])
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 5 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    axes[4].set_title('Bitcoin analysis: marketcap over time - bitcoin halving event marked')

    #halving analysis 11-may-2020
    fig = sns.lineplot(data=monthly_scope, x="period", y="circulating_supply", color = "black", marker = "o", markersize = 3, ax=axes[5])
    plt.axvline(x="2020-5", color='red')
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 5 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    axes[5].set_title('Bitcoin analysis: circulating supply over time - bitcoin halving event marked')
    plt.text(x="2020-6", y=monthly_scope["circulating_supply"].mean(), s="Halving BTC - 11-may-2020 \nShortage on BTC rewards produced by mining", color='black')
    plt.tight_layout()
    return print("done!")

######################################################################

#visualization bullish_or_bearish:
def bullish_or_bearish():

    """ plots the acumulated % of gain or loss by coins during an specific period of time
        parameters: -no parameters-  """

    sns.set_style("darkgrid")
    sns.color_palette()

    scope = pd.read_csv(r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/scope.csv")

    #dictionary creation
    tickers = scope["coin"].unique()
    dict_tickers = {}

    for key in tickers.tolist():
        dict_tickers[key] = key
        dict_tickers[key] = scope.loc[scope.coin == key]

    stable_coins = ["usdt", "usdc", "dai", "busd", "ust"]
    top_10 = ['btc', 'eth', 'luna', 'sol', 'avax', 'doge', 'matic', 'ftm', 'mana', 'sand'] #scope for this analysis

    #plot by iteration
    fig, axes = plt.subplots(1, 1, figsize=(25, 15), sharex=False, sharey=False)

    for i in top_10:

        df = dict_tickers[i]
        df = df.loc[df["year"] == 2021]
        df = df.sort_values(["month", "date"]).reset_index()

        initial_price = df["close"].loc[df["date"] == "01/01/2021"].item()
        final_price = df["close"].loc[df["date"] == "30/12/2021"].item()
        increase_decrease = int(((final_price - initial_price) / initial_price) * 100)

        df['acum_daily_change'] = ((df["close"] - initial_price) / initial_price * 100) + 100
        df.loc[0, 'acum_daily_change'] = 100

        fig = sns.lineplot(data=df, x="date", y="acum_daily_change", label=f'{i}: {increase_decrease}%')
        axes.get_xaxis().set_visible(False)
    axes.title.set_text('Crypto Race: multiple coin price increase or decrese percentage during the period selected (starting at 100% or 1)')
    axes.get_xaxis().set_visible(True)
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 20 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    return print("done!")

######################################################################

#visualization market_cake:
def market_cake():

    """ plots the % of dominance by market cap for several assets selected in pie chart
        parameters: -no parameters-  """

    sns.set_style("darkgrid")

    scope = pd.read_csv(r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/scope.csv")
    pie = scope.groupby("coin").last() #to obtain unique coins with last value in dataframe
    pie = pie.drop(["date", "year", "month", "day", "open", "high", "low", "close", "volume", "circulating_supply"], axis=1).dropna()
    pie = pie.sort_values(by="market_cap", ascending=False).reset_index().head(10) #filtrado por cantidad de monedas ordenadas por marketcap

    labels = pie["coin"].to_list()
    data = pie["market_cap"].to_list()

    plt.figure(figsize=(10,14))
    ax = plt.pie(data, labels=labels)
    ax = plt.title("Top 10 cryptocurrencies marketcap distribution")
    return plt.show()

######################################################################

#visualization metaverse:
def metaverse():

    """ comparation of price and marketcap for two coins related to metaverse creation, also plots impact of media news in the market
        parameters: -no parameters-  """

    sns.set_style("darkgrid")
    warnings.filterwarnings('ignore')

    scope = pd.read_csv(r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/scope.csv")

    sand_scope = scope.loc[scope["coin"] == "sand"]
    sand_scope["coin"] = "sand"
    sand_scope["circulating_supply"] = 900000000 #circulating supply mana-1.800.000.000 / sand-900.000.000 aprox
    mana_scope = scope.loc[scope["coin"] == "mana"]
    mana_scope["coin"] = "mana"
    mana_scope["circulating_supply"] = 1800000000 #circulating supply mana-1.800.000.000 / sand-900.000.000 aprox

    #concat both tables
    scope = pd.concat([mana_scope.tail(350), sand_scope.tail(350)], join='outer')
    scope["period"] = scope["date"].astype("str")
    scope["market_cap"] = scope["close"] * scope["circulating_supply"]

    #facebook announcement its name change to meta 28-oct-2021
    fig, axes = plt.subplots(2, 1, figsize=(30, 15), sharex=False, sharey=False)

    fig = sns.lineplot(data=scope, x="period", y="close", hue="coin", ax=axes[0])
    axes[0].set_title("price_analysis")
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 30 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)

    fig = sns.lineplot(data=scope, x="period", y="market_cap", hue="coin", ax=axes[1])
    axes[1].set_title("marketcap_analysis")
    plt.axvline(x="28/10/2021", color='red')
    plt.text(x="31/10/2021", y=scope["circulating_supply"].mean(), s="Facebook announced its name company change to Meta", color='black')
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 30 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    return print("done!")

######################################################################

#visualization terra_protocol:
def terra_protocol():

    """ plots price, marketcap and circulating supply for coins involved in terra protocol (luna, ust)
        relationship between supply for both coins is plotted (more supply ust, less supply luna and viceversa)
        parameters: -no parameters-  """

    sns.set_style("darkgrid")
    warnings.filterwarnings('ignore')
    scope = pd.read_csv(r"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/scope.csv")

    luna_scope = scope.loc[scope["coin"] == "luna"]
    luna_scope["coin"] = "luna"
    ust_scope = scope.loc[scope["coin"] == "ust"]
    ust_scope["coin"] = "ust"
    scope = pd.concat([luna_scope.tail(350), ust_scope.tail(350)], join='outer')
    scope["period"] = scope["date"].astype("str")

    #api link to download important missing data about luna supply
    cg = CoinGeckoAPI()

    from_ = datetime.date(2018, 12, 31)
    to_ = datetime.date(2021, 12, 31)

    unix_from = from_.strftime('%s')
    unix_to = to_.strftime('%s')

    df = pd.DataFrame(cg.get_coin_market_chart_range_by_id(id="terra-luna", vs_currency="usd", from_timestamp=unix_from, to_timestamp=unix_to))

    def mc_transfor(df):
        df[['date','price']] = pd.DataFrame(df.prices.tolist(), index= df.index) #get values in lists and drop old colums
        df['market_cap'] = df["market_caps"].apply(lambda x : x[1])
        df['total_volume'] = df["total_volumes"].apply(lambda x : x[1])
        df.drop(["prices", "market_caps", "total_volumes"], axis=1, inplace=True)

        df["date"] = df["date"].apply(lambda x : datetime.datetime.fromtimestamp(x / 1e3)) #change types: date to datetime / coin to category / floats to round float
        df["date"] = df["date"].dt.strftime('%d/%m/%Y')
        df["price"] = df["price"].astype(float).round(5)
        df[["market_cap", "total_volume"]] = df[["market_cap", "total_volume"]].astype(int)
        df["supply"] = df["market_cap"] / df["price"]
        return df

    mc_transfor(df)

    #luna and ust price - note that ust is pegged to us dollar
    fig, axes = plt.subplots(3, 1, figsize=(25, 15), sharex=False, sharey=False)
    fig = sns.lineplot(data=scope, x="period", y="close", hue="coin", ax=axes[0])
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 20 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)

    ust_scope = scope.loc[scope["coin"] == "ust"]
    fig = sns.lineplot(data=ust_scope, x="period", y="circulating_supply", ax=axes[1], label="ust")
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 20 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)

    luna_scope = df.tail(350)
    fig = sns.lineplot(data=luna_scope, x="date", y="supply", ax=axes[2], label="luna")
    for ind, label in enumerate(fig.get_xticklabels()):
        if ind % 20 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    return print("done!")