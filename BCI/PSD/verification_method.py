import numpy as np
import ast
import re

def parse_data(s):
    # 使用正则表达式替换array表达式
    s = re.sub(r"array\((.*?)\)", r"\1", s)
    # 解析修改后的字符串为字典
    data_dict = ast.literal_eval(s)
    # 将列表转换为NumPy数组
    for key in data_dict:
        data_dict[key] = np.array(data_dict[key])
    return data_dict

data_str = "{'alpha': array([192089.00698384,   1913.17427472,   7979.753455  , 134617.46447297]), 'beta': array([18385.33134215,   183.13753304,   763.89195531, 12884.78511285]), 'theta': array([1101.88453757,   11.38804991,   47.65221687,  778.72171221]), 'delta': array([267981.75056357,   2631.00823421,  11100.71346499, 187413.75310783])}"
parsed_data = parse_data(data_str)
print(parsed_data)