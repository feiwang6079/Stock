from flask import Flask, render_template, request
import os
from financeInfo import get_live_stock_price, get_cur_portfolio_value,get_history_portfolio_value
from datetime import date, timedelta
import json

app = Flask(__name__)

ethical_investing = ["AAPL", "TSLA", "ADBE"]
growth_investing = ["OXLC", "ECC", "AMD"]
index_investing = ["VOO", "VTI", "ILTB"]
quality_investing = ["NVDA", "MU", "CSCO"]
value_investing = ["INTC", "BABA", "GE"]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def post():

    # Get amount of money

    amount = float(request.form["amount"])
    print(amount)

    # # Get selected strategy
    strategy = {}
    if request.form.get("ethical"):
        strategy["Ethical Investing"] = ethical_investing
    if request.form.get("growth"):
        strategy["Growth Investing"] = growth_investing
    if request.form.get("index"):
        strategy["Index Investing"] = index_investing
    if request.form.get("quality"):
        strategy["Quality Investing"] = quality_investing
    if request.form.get("value"):
        strategy["Value Investing"] = value_investing
    print("User selects the following options: ")
    print(strategy)

    # # get current price
    live_price_dict = {}
    for key, value in strategy.items():
        stock_live_prices = get_live_stock_price(value)
        live_price_dict[key] = stock_live_prices
    print(live_price_dict)

    # # money allocation
    allocation = [amount*0.5, amount*0.3, amount*0.2]
    print(allocation)

    # # get current portfolio value
    cur_portfolio_dict, stock_buy_amount = get_cur_portfolio_value(live_price_dict, allocation);
    print(cur_portfolio_dict)

    # # get 5 day's portfolio value
    cur_date = date.today()
    seven_days_ago = date.today() - timedelta(7)
    five_days_ago = date.today() - timedelta(5)
    one_day_ago = date.today() - timedelta(1)

    dt = daterange(five_days_ago, one_day_ago)

    dt_list = get_date_list(dt)

    print(cur_date)
    print(five_days_ago)

    history_portfolio_dict = get_history_portfolio_value(strategy,stock_buy_amount, seven_days_ago, cur_date)

    result_arr = [strategy, allocation, cur_portfolio_dict,dt_list, history_portfolio_dict]
    print(result_arr)
    # return result_dict_arr
    return render_template('dashboard.html', value=result_arr)

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def get_date_list(dt):
    date_list = []
    for item in dt:
        date_list.append(item.strftime("%Y-%m-%d"))
    return date_list



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

    # five_days_ago = date.today() - timedelta(5)
    # one_day_ago = date.today() - timedelta(1)
    # 
    # dt = daterange(five_days_ago, one_day_ago)
    # dt_list = get_date_list(dt)
    # print(dt_list)