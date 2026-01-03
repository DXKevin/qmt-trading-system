import time, datetime, traceback, sys

sys.path.append('./scripts')
sys.path.append('./src')

from trader import Trader
from trader import Account
from logger import SimpleLogger


logger = SimpleLogger(keep_days=5)

if __name__ == "__main__":
    path = r'D:\山西证券QMT交易端-模拟\userdata_mini'
    account_id = "11031122"
    account_type = "STOCK"
    
    trader = Trader(path, logger).connect()
    
    if trader is None:
        raise Exception("交易客户端连接失败，程序退出")
    
    acc = Account(account_id, account_type).get_account()

    # account_info = trader.query_stock_asset(acc)
    # positions = trader.query_stock_positions(acc)
    
    # position_total_dict = {i.stock_code : i.m_nVolume for i in positions}
    # position_available_dict = {i.stock_code : i.m_nCanUseVolume for i in positions}
    # print(acc.account_id, '持仓字典', position_total_dict)  # type: ignore
    # print(acc.account_id, '可用持仓字典', position_available_dict) # type: ignore