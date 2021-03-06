
#更新rqalpha 股票池里数据: 进入cmd命令行输入:rqalpha update-bundle
import os
from rqalpha.api import *
import talib
import pandas as pd


def init(context):
    context.s1 = "600118.XSHG"
    context.SHORTPERIOD = 10
    context.LONGPERIOD = 30

def handle_bar(context, bar_dict):
    prices = history_bars(context.s1, context.LONGPERIOD+1, '1d', 'close')
    short_avg = talib.SMA(prices, context.SHORTPERIOD)
    long_avg = talib.SMA(prices, context.LONGPERIOD)

    # 计算现在portfolio中股票的仓位
    cur_position = context.portfolio.positions[context.s1].quantity
    avg_price = context.portfolio.positions[context.s1].avg_price
    capital = cur_position*avg_price
    # 计算现在portfolio中的现金可以购买多少股票
    shares = context.portfolio.cash/bar_dict[context.s1].close
    #图形显示当前占用资金
    plot('capital', capital)

    # 如果短均线从上往下跌破长均线，而上一个bar的短线平均值高于长线平均值
    if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0 and cur_position > 0:
        # 进行清仓
        order_target_value(context.s1, 0)

    # 如果短均线从下往上突破长均线，为入场信号
    if short_avg[-1] - long_avg[-1] > 0 and short_avg[-2] - long_avg[-2] < 0:
        # 满仓入股
        order_shares(context.s1, shares)

config = {
  "base": {
    "start_date": "2017-10-09",
    "end_date": "2017-10-11",
    "accounts": {'stock':1000000},
    "benchmark": "000001.XSHG",
#     "strategy_file_path": os.path.abspath(__file__)
  },
  "extra": {
    "log_level": "error",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

# 您可以指定您要传递的参数
rqalpha.run_func(init=init, handle_bar=handle_bar, config=config)