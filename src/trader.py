import time,sys

sys.path.append('./scripts')
sys.path.append('./src')

from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from trader_callback import MyXtQuantTraderCallback


class Trader:
    def __init__(self, client_path, logger):
        self.client_path = client_path
        self.logger = logger
    
    def connect(self):
        session_id = int(time.time())
        xt_trader = XtQuantTrader(self.client_path, session_id)
        xt_trader.register_callback(MyXtQuantTraderCallback())
        xt_trader.start()
        
        connect_result = xt_trader.connect()
        
        if connect_result == 0:
            self.logger.info('连接交易客户端成功')
            return xt_trader
        else:
            self.logger.info('连接交易客户端失败')
            return None
        
class Account:
    def __init__(self, account_id, account_type):
        self.account_id = account_id
        self.account_type = account_type
    
    def get_account(self):
        account = StockAccount(self.account_id, self.account_type)
        return account