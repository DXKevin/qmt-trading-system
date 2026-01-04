
def parse_stock_fund_string(s: str) -> dict:
    """
    解析格式如 "<000001.SZ#23123213,23123123>" 的字符串，
    返回字典：{ 股票代码: [资金账号1, 资金账号2, ...] }
    """
    # 去除首尾的 < 和 >
    s = s.strip()
    if s.startswith('<') and s.endswith('>'):
        s = s[1:-1]
    else:
        raise ValueError("输入字符串格式错误：应以 < 开头、> 结尾")

    part1 = s.split("#")
    part2 = part1[1].split(",")

    return {part1[0]: part2}


if __name__ == "__main__":
    input_str = "<000001.SZ#23123213>"
    #input_str = "<000001.SZ#23123213,23123123>"
    result = parse_stock_fund_string(input_str)
    print(result)
    # 输出: {'000001.SZ': ['23123213', '23123123']}