import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# 设置数据目录和文件路径
DATA_DIR = 'data'
input_file = os.path.join(DATA_DIR, 'random_data.xlsx')
output_file = os.path.join(DATA_DIR, 'merged_data.xlsx')

# 读取 Excel 文件
df = pd.read_excel(input_file)

# 将 DataFrame 写入新的 Excel 文件
df.to_excel(output_file, index=False, engine='openpyxl')

# 加载保存的 Excel 文件以设置单元格对齐和合并
wb = load_workbook(output_file)
ws = wb.active

# 合并相邻且值相同的单元格
def merge_cells(ws, col, start_row, end_row):
    ws.merge_cells(start_row=start_row, start_column=col, end_row=end_row, end_column=col)
    cell = ws.cell(row=start_row, column=col)
    cell.alignment = Alignment(horizontal='center', vertical='center')

# 初始化合并起始行和当前值
for col in range(1, 4):  # 前三列
    merge_start = 2  # 从第二行开始，因为第一行是标题
    current_value = ws.cell(row=merge_start, column=col).value
    
    for row in range(3, ws.max_row + 1):  # 从第三行开始遍历
        cell_value = ws.cell(row=row, column=col).value
        status = ws.cell(row=row, column=4).value  # 第四列为状态列
        
        if cell_value == current_value and status != '不活跃':
            # 如果当前值和前一行的值相同且状态不为“不活跃”，继续
            continue
        else:
            # 如果当前值和前一行的值不同，进行合并操作
            if row - 1 > merge_start:  # 至少有两行需要合并
                merge_cells(ws, col, merge_start, row - 1)
            merge_start = row
            current_value = cell_value

    # 合并最后一组单元格
    if ws.max_row >= merge_start and ws.cell(row=merge_start, column=col).value == current_value:
        merge_cells(ws, col, merge_start, ws.max_row)

# 保存文件
wb.save(output_file)

print(f"处理完成并保存到 '{output_file}' 文件。")
