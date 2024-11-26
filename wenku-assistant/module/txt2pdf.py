import os
from fpdf import FPDF
import warnings
warnings.filterwarnings("ignore")

# 创建保存PDF的文件夹
def create_document_directory():
    # 直接指定输出路径为 /app/document
    output_dir = "/app/document"
    os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，则创建
    return output_dir

# 从文本内容生成 PDF，支持标题显示和插入图片
def generate_pdf_from_text(content, image_path=None, filename="document.pdf"):
    output_dir = create_document_directory()
    pdf = FPDF()
    pdf.add_page()

    # 如果 filename 没有后缀，则添加 .pdf 后缀
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    # 确保字体路径正确
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "word", "SimSun.ttf")


    # 使用 SimSun.ttf 字体加载，确保支持 UTF-8 字符
    pdf.add_font("SimSun", "", font_path, uni=True)  # 加载字体
    pdf.set_font("SimSun", size=12)  # 设置默认字体

    # 插入图片（可选）
    if image_path and os.path.exists(image_path):
        pdf.image(image_path, x=10, y=10, w=100)  # 设置图片位置和宽度
        pdf.ln(85)  # 图片下方留出空行

    # 解析文本内容
    lines = content.splitlines()  # 将文本内容按行分割
    for line in lines:
        # 检查是否为标题行
        if line.startswith("#"):
            level = line.count("#")  # 获取标题层级
            title_text = line.replace("#", "").strip()  # 去掉 # 号和多余空白

            # 设置标题样式：层级越低，字号越大
            pdf.set_font("SimSun", size=16 - level)  # 设置标题字体
            pdf.cell(0, 10, title_text,ln=True)     # 写入标题并换行

            pdf.ln(5)  # 在标题下方留出一些空行
        else:
            # 设置较宽的宽度，避免过早换行
            pdf.set_font("SimSun", size=12)  # 恢复为正文字体
            pdf.multi_cell(0, 10, line.strip())  # 使用 `cell` 避免强制换行


    # 保存 PDF 文件
    output_path = os.path.join(output_dir, filename)
    pdf.output(output_path)



