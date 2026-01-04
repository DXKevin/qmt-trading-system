import time,sys
import threading

sys.path.append('./scripts')
sys.path.append('./src')

from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from trader_callback import MyXtQuantTraderCallback
from utils import parse_stock_fund_string


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

class TraderExecutor:
    def __init__(self, trader, logger, msg_queue):
        self.trader = trader
        self.logger = logger
        self.msg_queue = msg_queue
        self.accounts = {}
    
    def get_account(self, account_id, account_type):
        if account_id not in self.accounts:
            account = Account(account_id, account_type).get_account()
            self.accounts[account_id] = account
        return self.accounts[account_id]
    
    def run(self):
        thread = threading.Thread(target=self.worker)
        thread.start()
        thread.join()
    
    def worker(self):
        while True:
            message = self.msg_queue.get()
            parsed_message = parse_stock_fund_string(message)
            
            for stock_code, fund_accounts in parsed_message.items():
                for fund_account in fund_accounts:
                    account = self.get_account(fund_account, "STOCK")
                    
                    positions = self.trader.query_stock_positions(account)
                    position_dict = {i.stock_code: i.m_nCanUseVolume for i in positions}
                    self.logger.info(f"处理股票代码 {stock_code}，资金账号 {fund_account}, 可用持仓: {position_dict.get(stock_code, 0)}")
                    

