import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import re
import warnings
warnings.filterwarnings("ignore")



# 创建保存Excel文件的文件夹
def create_document_directory():
    # 直接指定输出路径为 /app/document
    output_dir = "/app/document"
    os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，则创建
    return output_dir

# 生成 Excel 文件并解析文本文件
def generate_excel(content, filename="document.xlsx", image_path=None):
    output_dir = create_document_directory()

    # 如果 filename 没有后缀，则添加 .xlsx 后缀
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    output_path = os.path.join(output_dir, filename)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Report"
    row_num = 1

    # 插入图片（如果提供图片路径）
    if image_path and os.path.exists(image_path):
        img = Image(image_path)
        img.width, img.height = 100, 100
        sheet.add_image(img, f"A{row_num}")
        row_num += 8  # 为图片预留一些行数

    # 解析文本文件内容


    sections = []
    section_pattern = re.compile(r"(#+)\s*(.+)")  # 匹配 # 和标题内容
    lines = content.splitlines()
    current_section = {"heading": "", "content": "", "level": 0}

    for line in lines:
        match = section_pattern.match(line)
        if match:
            # 如果当前节有内容，添加到 sections
            if current_section["heading"] or current_section["content"]:
                sections.append(current_section)
                current_section = {"heading": "", "content": "", "level": 0}

            # 设置新的标题和层级
            level = len(match.group(1))
            heading = match.group(2).strip()
            current_section = {"heading": heading, "content": "", "level": level}
        else:
            current_section["content"] += line + "\n"

    # 添加最后一个节
    if current_section["heading"] or current_section["content"]:
        sections.append(current_section)

    # 将解析的内容写入 Excel
    for section in sections:
        if section["heading"]:
            sheet[f"A{row_num}"] = section["heading"]
            sheet[f"A{row_num}"].font = sheet[f"A{row_num}"].font.copy(bold=True, size=14 - section["level"])
            row_num += 1

        if section["content"].strip():
            sheet[f"A{row_num}"] = section["content"].strip()
            row_num += 2  # 空一行再写下一个内容

    workbook.save(output_path)



