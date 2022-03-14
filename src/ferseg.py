def klines_csv(asset_pair, candle_interval, beg_date, end_date):

    """ creates a csv file with candlestick data in output file, given the following parameters:
        asset_pair: ETHUSDT
        candle_interval:  Client.KLINE_INTERVAL_1DAY
        beg_date: 1 Oct, 2019
        end_date: 23 Feb, 2022 
        
        librerias necesarias:
        import pandas as pd
        from binance import Client
        import os
        from dotenv import load_dotenv
        load_dotenv() """

    from binance import Client
    import os
    import pandas as pd

    api_key = os.getenv("BNB_API_KEY")
    api_secret = os.getenv("BNB_SECRET_KEY")
    client = Client(api_key, api_secret)
    klines = pd.DataFrame(client.get_historical_klines(asset_pair, candle_interval, beg_date, end_date))
    variable_link = f"/Users/fernandoseguias/Desktop/ferseg/Proyectos/Programacion/iron_hack/project_1/output/{asset_pair}_{candle_interval}_{(beg_date.lower().replace(' ', '').replace(',', ''))}_{(end_date.lower().replace(' ', '').replace(',', ''))}.csv"
    klines.to_csv(variable_link, index = False)

    return f'you have downloaded data set of {asset_pair} with {klines.shape[0]} rows and {klines.shape[1]} columns - from {beg_date} to {end_date}'

'----------------------------------------------------------'