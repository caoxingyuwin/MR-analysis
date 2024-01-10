#注意看一下ldfilter文件里的rsid是不是对应的列 列名有没有错
import os
import csv
import pandas as pd

def modify(file_path):
   with open(file_path, 'r') as file:
    content = file.read().replace('"', '')
   with open(file_path, 'w') as file:
    file.write(content)

def combine(filea, fileb, output_folder):
    # 读取两个文件
    df_a = pd.read_csv(filea, delimiter='\t',escapechar='"', doublequote=False)
    print("Columns in df_a:", df_a.columns)
    df_b = pd.read_csv(fileb, delimiter='\t')
    df_b.rename(columns={'A1': 'ALT','A2':'REF','P': 'pval'}, inplace=True)
    df_a['rsid'] = df_a['rsid'].astype('object')
    df_b['rsid'] = df_b['rsid'].astype('object')
    

    # 取两个文件rsid列的交集
    common_rsid = pd.merge(df_a[['rsid']], df_b[['rsid']], on='rsid')['rsid']

    # 筛选出两个文件中交集的部分，并添加Phenotype列
    result_a = df_a[df_a['rsid'].isin(common_rsid)].copy()
    result_a['Phenotype'] = os.path.basename(filea).replace('japan5e-8_LD_filtered.txt', '')  # 使用文件名作为Phenotype列内容
    result_a['Phenotype'] = result_a['Phenotype'].where(result_a['rsid'].notna(), '')  # 只填充非空的rsid对应的行

    result_b = df_b[df_b['rsid'].isin(common_rsid)].copy()
    result_b['Phenotype'] = 'Alzheimer\'s disease'
    result_b['Phenotype'] = result_b['Phenotype'].where(result_b['rsid'].notna(), '')  # 只填充非空的rsid对应的行


    # 合并两个文件中rsid对应的Frq列
    result_b = pd.merge(result_b, result_a[['rsid', 'Frq']], on='rsid', how='left')

    # 输出到新的文件夹
    output_file_a = os.path.join(output_folder, os.path.basename(filea).replace('.txt', '_common.txt'))
    output_file_b = os.path.join(output_folder, os.path.basename(filea).replace('.txt', '_common_ad.txt'))

    # 保存结果到文件
    result_a.to_csv(output_file_a, sep='\t', index=False)
    result_b.to_csv(output_file_b, sep='\t', index=False)



def main(input_folder_filea, fileb, output_folder):
    # 列出输入文件夹中的所有 filea 文件
    filea_files = [f for f in os.listdir(input_folder_filea) if f.endswith('.txt')]

    # 对每个 filea 文件执行 combine 函数
    for filea in filea_files:
        filea_path = os.path.join(input_folder_filea, filea)
        modify(filea_path)
        combine(filea_path, fileb, output_folder)


main('/Volumes/a/Men/MRld', '/Volumes/a/00.NCGG_GWAS_data/NCGG_AD_GWAS2.txt', '/Volumes/a/Men/MRcombine')
