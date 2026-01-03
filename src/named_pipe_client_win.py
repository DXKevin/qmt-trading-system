import win32file
import win32pipe
import time
import sys


def connect_to_pipe(pipe_name):
    """尝试连接到命名管道"""
    while True:
        try:
            # 尝试连接到已存在的管道
            handle = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ,
                0,  # 不允许共享
                None,  # 默认安全属性
                win32file.OPEN_EXISTING,  # 必须已存在
                0,  # 默认属性
                None  # 模板文件句柄
            )
            
            print(f"成功连接到管道 {pipe_name}")
            return handle
        except Exception as e:
            # ERROR_PIPE_BUSY 通常意味着服务器端存在，但正忙
            if e.args[0] == 2: # ERROR_FILE_NOT_FOUND, 表示管道不存在
                print(f"等待服务器启动... 管道 {pipe_name} 不存在。")
            elif e.args[0] == 231: # ERROR_PIPE_BUSY, 表示管道存在但忙
                print("管道正忙，等待客户端...")
                win32pipe.WaitNamedPipe(pipe_name, 5000) # 等待最多5秒
                continue # 再次尝试连接
            else:
                print(f"连接失败: {e}")
                sys.exit(1)
            time.sleep(1) # 等待一秒后重试


def read_from_pipe(handle):
    """从管道读取消息"""
    while True:
        try:
            # 读取数据
            # (返回码, 数据)
            result, data = win32file.ReadFile(handle, 1024) 
            if result == 0: # 读取成功
                message = data.decode('utf-8')
                print(f"收到消息: {message}\n")
                # 可以在这里处理消息
                # 如果服务器发送完消息后关闭，客户端会收到空数据
                if not message:
                    print("服务器已关闭连接。")
                    break
            else:
                # 如果 ReadFile 返回非零值，表示有错误
                print(f"读取错误: {result}")
                break
        except Exception as e:
            # 通常当服务器关闭管道时，这里会抛出异常
            print(f"连接中断或发生错误: {e}")
            break


def main():
    # Windows 命名管道的格式是 \\.\pipe\管道名
    pipe_name = "\\\\.\\pipe\\to_python_pipe"
    
    print("客户端启动，尝试连接到管道...")
    handle = connect_to_pipe(pipe_name)
    
    print("开始读取消息...")
    read_from_pipe(handle)
    
    print("关闭管道连接...")
    win32file.CloseHandle(handle)
    print("客户端退出。")


if __name__ == "__main__":
    main()