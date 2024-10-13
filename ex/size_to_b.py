import re


def size_b_to_other(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    # 处理异常
    if size <= 0:
        return False

    # 遍历单位的位置并用取整除赋值
    for unit in units:
        if size >= 1024:
            size //= 1024
        else:
            size_h = '{} {}'.format(size, unit)
            return size_h

    size_h = '{} {}'.format(size, unit)
    return size_h


def size_other_to_b(size, unit):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    # 处理异常
    if size <= 0:
        return False

    # 找出单位的索引位置
    nu = units.index(unit)

    # 根据索引位置次幂在乘以系数
    size_h = int(size) * 1024 ** nu
    return int(size_h)


def convert(data):
    # 忽略大小写敏感
    size = re.sub("\D", "", data)
    size = int(size)
    unit = ''.join(re.findall(r'[A-Za-z]', str.upper(data)))
    if unit == "B":
        result = size_b_to_other(size)
    else:
        # 支持单位简写
        if len(unit) == 1:
            unit = unit + "B"
        result = size_other_to_b(size, unit)
    return result
