# Logger.py
import os
import logging
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler

class SimpleLogger:
    # 类变量：确保全局只有一个 logger 实例（避免重复 handler）
    _logger = None
    _log_dir = "logs"
    _initialized = False

    def __init__(self, name="AppLogger", keep_days=5):
        """
        初始化日志类
        :param name: logger 名称
        :param keep_days: 保留最近多少天的日志
        """
        if not SimpleLogger._initialized:
            self._setup_logger(name, keep_days)
            SimpleLogger._initialized = True

        self._logger = SimpleLogger._logger

    def _setup_logger(self, name, keep_days):
        # 创建日志目录
        os.makedirs(self._log_dir, exist_ok=True)

        # 创建 logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # 避免重复添加 handler
        if logger.handlers:
            return

        # 格式化器
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 文件处理器：每天一个文件，保留 keep_days 天
        log_file = os.path.join(self._log_dir, "app.log")
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=keep_days,
            encoding="utf-8"
        )
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 控制台处理器（可选）
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 清理旧日志（基于文件修改时间，双重保险）
        self._cleanup_old_logs(keep_days)

        SimpleLogger._logger = logger

    def _cleanup_old_logs(self, keep_days):
        """清理 logs 目录中超过 keep_days 天的日志文件"""
        now = datetime.now()
        for filename in os.listdir(self._log_dir):
            if filename.endswith(".log"):
                filepath = os.path.join(self._log_dir, filename)
                try:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if (now - file_mtime).days > keep_days:
                        os.remove(filepath)
                except (OSError, ValueError):
                    continue  # 忽略无法处理的文件

    def info(self, message):
        """记录 info 级别日志"""
        self._logger.info(message)

    def error(self, message):
        """记录 error 级别日志"""
        self._logger.error(message)