## 将 多个 pdf 合并到 一个 pdf 中

import PyPDF2
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", default="C:\\workspace\\ProductSpace\\", help="设置pdf文件路径",)
args = parser.parse_args()
pdf_path = args.d

# 定义要合并的PDF文件列表
# pdf_path = r"C:\workspace\ProductSpace\27-振华永光-IGBT数字孪生\第三方测试报告\新建文件夹"
pdf_files = os.listdir(pdf_path)
pdf_files = [os.path.join(pdf_path,pdf) for pdf in pdf_files if "pdf" in os.path.splitext(pdf)[1]]

# 创建一个PDF写入器对象
pdf_writer = PyPDF2.PdfWriter()

# 循环遍历所有PDF文件
for filename in pdf_files:
    with open(filename, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in range(len(pdf_reader.pages)): 
            pdf_writer.add_page(pdf_reader.pages[page])

# 写入合并后的PDF文件
merge_pdf = os.path.join(pdf_path,"merged.pdf")
with open(merge_pdf, 'wb') as f:
    pdf_writer.write(f)

print("PDF files have been merged successfully.")

