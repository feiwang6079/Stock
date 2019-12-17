from datetime import datetime
from yahoofinancials import YahooFinancials
import requests
import time


def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']

    return "Ticker Not Exist"

def get_live_stock_price(ticker_names):
    prices = []
    yahoo_financials = YahooFinancials(ticker_names)
    curr_prices = yahoo_financials.get_current_price()
    for ticker_name in ticker_names:
        prices.append(curr_prices[ticker_name])
    return prices

    # for ticker_name in ticker_names:
    #     # price = si.get_live_price(ticker_name)
    #     print(price)
    #
    #     # prices.append(price)
    #     # print(round(si.get_live_price(ticker_name),2))
    # return prices


def get_cur_portfolio_value(price_dict, allocation):
    portfolio_dict = {}
    stock_buy_amount = {}
    for key, value in price_dict.items():
        amt0 = allocation[0] // value[0];
        amt1 = allocation[1] // value[1];
        amt2 = allocation[2] // value[2];
        cur_portfolio_value = amt0*value[0] +  amt1*value[1] +  amt2*value[2]
        portfolio_dict[key] = round(cur_portfolio_value, 2)
        stock_buy_amount[key] = [amt0, amt1, amt2]
    return portfolio_dict,stock_buy_amount

def get_history_portfolio_value(strategy,stock_buy_amount, start, end):
    history_portfolio_dict = {}
    for key, value in strategy.items():
        yahoo_financials = YahooFinancials(value)
        res = yahoo_financials.get_historical_price_data(str(start), str(end), 'daily')
        # stock1_prices = si.get_data(value[0], start, end)["close"].tolist()
        # stock2_prices = si.get_data(value[1], start, end)["close"].tolist()
        # stock3_prices = si.get_data(value[2], start, end)["close"].tolist()
        stock1_prices = [history['close'] for history in res[value[0]]["prices"]]
        stock2_prices = [history['close'] for history in res[value[1]]["prices"]]
        stock3_prices = [history['close'] for history in res[value[2]]["prices"]]

        print(stock1_prices)
        print(stock2_prices)
        print(stock3_prices)

        history_portfolio = [round(stock1_prices[i]*stock_buy_amount[key][0] + stock2_prices[i]*stock_buy_amount[key][1]+stock3_prices[i]*stock_buy_amount[key][2],2) for i in range(5)];
        history_portfolio_dict[key] = history_portfolio
        # print(stock_buy_amount)
    return history_portfolio_dict

if __name__ == "__main__":
    # print(type(si.get_data("AAPL", "2019-12-03", "2019-12-07")))
    # df = si.get_data("AAPL", "2019-12-03", "2019-12-07")["close"].tolist()
    # # print(df["close"].tolist())
    # print (df)
    # print(si.get_data("AAPL", "2019-12-03", "2019-12-07"))
    # strategy = {"ethical investing": ["AAPL", "TSLA", "ADBE"], "growth investing": ["OXLC", "ECC", "AMD"]}
    # stock_buy_amount = [50, 30, 20]
    # start = "2019-12-02"
    # end =  "2019-12-07"
    # print(get_history_portfolio_value(strategy,stock_buy_amount,start, end))

    print(get_live_stock_price(["AAPL", "TSLA", "ADBE"]))
    # print(round(si.get_live_price("ADBE"),2))
    # time.sleep(5)
    # print(si.get_live_price('ADBE'))
    # time.sleep(5)
    # print(si.get_live_price('AAPL'))
    # time.sleep(5)