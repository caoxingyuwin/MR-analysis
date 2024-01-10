import os
import subprocess
import time
import pandas as pd

# 定义 Pfilter 函数
def Pfilter(input_file, output_directory):
    # 读取 CSV 文件
    df = pd.read_csv(input_file, delimiter='\t')
    
    # 进行过滤
    filter_data = df[df['P'] < 5e-8]
    
    # 重命名列
    filter_data.rename(columns={'SNP': 'rsid', 'P': 'pval'}, inplace=True)
    
    # 生成输出文件名
    output_file = os.path.join(output_directory, os.path.basename(input_file).replace('.txt', 'japan5e-8.txt'))
    
    # 将过滤后的数据保存到新文件
    filter_data.to_csv(output_file, sep='\t', index=False)

    # 返回输出文件路径
    return output_file

# 定义运行R脚本的函数
def run_r_script(input_file, output_directory):
    r_script = '''
        library(TwoSampleMR)
        ad <- read.table("{input_file}", header=TRUE, sep="\t")
        Tg_out_data <- ld_clump(dat=ad, clump_r2=0.01, pop="EAS")
        write.table(Tg_out_data, "{output_file}", sep="\t", row.names=FALSE)
    '''

    # 生成输出文件名
    output_file = os.path.join(output_directory, os.path.basename(input_file).replace('.txt', '_LD_filtered.txt'))

    # 写入R脚本到临时文件
    with open('temp_script.R', 'w') as script_file:
        script_file.write(r_script.format(input_file=input_file, output_file=output_file))

    # 运行R脚本
    try:
        subprocess.run(['Rscript', 'temp_script.R'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'R-script fail:{e}')
        return None

    return output_file

# 定义 main 函数
def main():
    # 指定输入文件夹和输出文件夹
    input_folder = '/Users/cell_response_lab/Desktop/cxy/Men/MR1'
    output_folder_pfilter = '/Users/cell_response_lab/Desktop/cxy/Men/MRpfilter'
    output_folder_rscript = '/Users/cell_response_lab/Desktop/cxy/Men/MRLD'

    # 列出输入文件夹中的所有 txt 文件
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]

    # 对每个文件执行 Pfilter 函数和运行 R 脚本
    for txt_file in txt_files:
        input_file_path = os.path.join(input_folder, txt_file)

        # 执行 Pfilter 函数
        output_file_pfilter = Pfilter(input_file_path, output_folder_pfilter)

        # 如果 Pfilter 成功生成了输出文件，则运行 R 脚本
        if output_file_pfilter is not None:
            success = False
            attempts = 0
            max_attempts = 10  # 最大尝试次数

            while not success and attempts < max_attempts:
                # 运行 R 脚本并检查返回值
                output_file_rscript = run_r_script(output_file_pfilter, output_folder_rscript)

                if output_file_rscript is not None:
                    success = True
                else:
                    attempts += 1
                    time.sleep(5)  # 等待5秒后重试

# 调用 main 函数
main()






