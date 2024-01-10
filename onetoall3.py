import os
import subprocess
import pandas as pd

# MR分析
# 需改进的地方 ad的文件中a1 a2需要改成alr ref  p 变成 pvalue
def run_r_script(exposure_file, outcome_file,output_file):
    r_script = '''
        options(repos = c(CRAN = "https://cloud.r-project.org"))

        # 安装并加载 TwoSampleMR 包
        if (!requireNamespace("TwoSampleMR", quietly = TRUE)) {
        install.packages("TwoSampleMR")
        }
        library(TwoSampleMR)
        
        if (!requireNamespace("openxlsx", quietly = TRUE)) {
            install.packages("openxlsx")
            }
        library(openxlsx)
        file_exppath <- Sys.getenv("EXPOSURE_FILE")
        print(paste("Exposure file path:", file_exppath))
        sCr_exp_data <- read_exposure_data(
        filename =file_exppath,  # 使用文件路径
        sep = "\t",
        snp_col = "rsid",
        chr_col = "CHR",
        beta_col = "BETA",
        se_col = "SE",
        effect_allele_col = "ALT",
        other_allele_col = "REF",
        eaf_col = "Frq",
        pval_col = "pval",
        samplesize_col = "N",
        phenotype_col ="Phenotype" 
        )
        file_outpath<- Sys.getenv("outcome_FILE")
        ADout_data <- read_outcome_data(
        filename = file_outpath,  # 使用文件路径
        sep = "\t",
        snp_col = "rsid",
        chr_col = "CHR",
        beta_col = "BETA",
        se_col = "SE",
        effect_allele_col = "ALT",
        other_allele_col = "REF",
        pval_col = "pval",
        eaf_col = "Frq",
        phenotype_col = "Phenotype")
        dat <- harmonise_data(sCr_exp_data,ADout_data)
        res <-mr(dat)
        res
        print('ok')
        output<- Sys.getenv("output_FILE")
        write.xlsx(res, output)
    '''
    os.environ["EXPOSURE_FILE"] = exposure_file
    os.environ["outcome_FILE"] = outcome_file
    os.environ["output_FILE"] = output_file

    script_filename = 'temp_script.R'
    with open(script_filename, 'w') as script_file:
        script_file.write(r_script)
    # 运行R脚本
    try:
        subprocess.run(['Rscript', script_filename], check=True)
        print("R-script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f'R-script fail:{e}')
        return None
    finally:
        # 删除临时文件
        os.remove(script_filename)

    return output_file


def main():
    # 指定文件夹路径
    folder_path = '/Volumes/a/Men/MRcombine'

    # 获取所有以_common.txt结尾的文件
    common_files = [f for f in os.listdir(folder_path) if f.endswith('_common.txt')]

    # 遍历文件对，执行MR分析并保存结果
    for common_file in common_files:
        exposure_file = os.path.join(folder_path, common_file)
        print(exposure_file)
        outcome_file = os.path.join(folder_path, common_file.replace('_common.txt', '_common_ad.txt'))
        output_file = os.path.join(folder_path, common_file.replace('_common.txt', '_mr_result.xlsx'))
        # exposure_file, outcome_file, output_file = run_r_script(exposure_file, outcome_file, output_file)
        result = run_r_script(exposure_file, outcome_file, output_file)
        if result is not None:
            output_file = result
        else:
            # 处理异常情况，可能需要打印错误消息或采取其他措施
            print("run_r_script failed.")

main()