import time
import sys
import queue

sys.path.append('./scripts')
sys.path.append('./src')

from read_config_ini import read_config
from reveiver_server import ReceiverServer
from trader import Trader
from trader import TraderExecutor
from trader import Account
from logger import SimpleLogger


logger = SimpleLogger(keep_days=5)

if __name__ == "__main__":
    # 读取配置文件
    config_path = 'config.ini'
    cfg = read_config(config_path)
    
    # 连接交易客户端
    path = cfg['CLIENT']['path']
    trader = Trader(path, logger).connect()

    if trader is None:
        raise Exception("交易客户端连接失败，程序退出")

    # 启动管道接收服务
    msg_queue = queue.Queue()
    pipe_name = cfg['MESSAGE SERVER']['pipe_name']
    ReceiverServer(pipe_name, logger, msg_queue).run()
    
    # 启动消息处理循环
    executor = TraderExecutor(trader, logger, msg_queue)
    executor.run()
    
    # account_info = trader.query_stock_asset(acc)
    # positions = trader.query_stock_positions(acc)
    
    # position_total_dict = {i.stock_code : i.m_nVolume for i in positions}
    # position_available_dict = {i.stock_code : i.m_nCanUseVolume for i in positions}
    # print(acc.account_id, '持仓字典', position_total_dict)  # type: ignore
    # print(acc.account_id, '可用持仓字典', position_available_dict) # type: ignore
    
    
    
    
    
    
    
    # order_id = 1098922992
    # acc = Account('40079077', 'STOCK').get_account()
    # # trader.cancel_order_stock(acc, order_id)

    # orders = trader.query_stock_orders(acc, False)
    
    # for order in orders:
    #     print(order.stock_code)
    #     print(order.order_id)
        
    #     print(trader.cancel_order_stock(acc, order.order_id))