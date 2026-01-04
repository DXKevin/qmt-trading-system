import time
import sys
import queue

sys.path.append('./scripts')
sys.path.append('./src')

from reveiver_server import ReceiverServer
from trader import Trader
from trader import Account
from trader import TraderExecutor
from logger import SimpleLogger
from utils import parse_stock_fund_string


logger = SimpleLogger(keep_days=5)

if __name__ == "__main__":
    # 连接交易客户端
    path = r'D:\山西证券QMT交易端-模拟\userdata_mini'
    account_id = "11031122"
    account_type = "STOCK"
    
    trader = Trader(path, logger).connect()
    
    if trader is None:
        raise Exception("交易客户端连接失败，程序退出")
    
    # 启动管道接收服务
    msg_queue = queue.Queue()
    pipe_name = "\\\\.\\pipe\\to_python_pipe"
    ReceiverServer(pipe_name, msg_queue).run()
    
    # 启动消息处理循环
    executor = TraderExecutor(trader, logger, msg_queue)
    executor.run()
    
    
    

    # account_info = trader.query_stock_asset(acc)
    # positions = trader.query_stock_positions(acc)
    
    # position_total_dict = {i.stock_code : i.m_nVolume for i in positions}
    # position_available_dict = {i.stock_code : i.m_nCanUseVolume for i in positions}
    # print(acc.account_id, '持仓字典', position_total_dict)  # type: ignore
    # print(acc.account_id, '可用持仓字典', position_available_dict) # type: ignore