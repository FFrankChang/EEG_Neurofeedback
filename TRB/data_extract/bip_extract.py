import pandas as pd

# 加载CSV文件
df = pd.read_csv(r'E:\NFB_data_backup\20240730\S12_D01\EEG_20240730150926.csv')

# 检查列名，确保'BIP 01'列存在
if 'BIP 01' in df.columns:
    # 提取'BIP 01'列
    bip_01_data = df[['BIP 01']]
    final = bip_01_data.head(10000)
    final.to_csv('BIP_01_output.csv', index=False)
    print("文件已成功保存为 'BIP_01_output.csv'")
else:
    print("错误：CSV文件中不存在'BIP 01'列。")
