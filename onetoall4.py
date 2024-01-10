import os
import pandas as pd

# 设置输入文件夹和输出文件名
input_folder = "path/to/your/input/folder"  # 替换为包含xlsx文件的文件夹路径
output_file = "path/to/your/output/file.xlsx"  # 替换为输出文件的路径和名称

# 获取文件夹中所有xlsx文件的列表
xlsx_files = [file for file in os.listdir(input_folder) if file.endswith('.xlsx')]

# 创建一个空的DataFrame来存储所有数据
all_data = pd.DataFrame()

# 循环处理每个xlsx文件
for file in xlsx_files:
    # 读取xlsx文件的数据，跳过第一行作为列名
    data = pd.read_excel(os.path.join(input_folder, file), header=0)
    
    # 将数据添加到all_data中
    all_data = all_data.append(data, ignore_index=True)

# 将all_data保存到输出文件中，只保留第一列作为列名
all_data.to_excel(output_file, index=False, columns=[all_data.columns[0]])

print(f"数据已提取并保存到 {output_file}")
