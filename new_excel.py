import os
import pandas as pd
import numpy as np

# 设置随机种子以确保可重复性
np.random.seed(42)

# 初始化空列表来存储数据
data = {
    'Column1': [],
    'Column2': [],
    'Column3': [],
    'Status': []
}

# 定义状态列表
statuses = ['活跃', '不活跃']

# 生成数据
while len(data['Column1']) < 100:
    col1, col2, col3 = np.random.randint(1, 5, 3)
    
    # 确保前三列不相同
    if col1 == col2 == col3:
        continue
    
    status = np.random.choice(statuses)
    
    data['Column1'].append(col1)
    data['Column2'].append(col2)
    data['Column3'].append(col3)
    data['Status'].append(status)

# 创建 DataFrame
df = pd.DataFrame(data)

# 数据目录
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 保存为 Excel 文件
output_file = os.path.join(DATA_DIR, 'random_data.xlsx')
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Excel 文件已成功创建并保存到 {output_file}！")
