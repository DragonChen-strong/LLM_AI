import os
import re
from playwright.sync_api import sync_playwright
from llm import generate_document_from_model
import json
import time

account_cookies_path = os.getenv("ACCOUNT_COOKIES_PATH")
file_to_upload=os.getenv("FILE_TO_UPLOAD")

# 生成10个标题列表
titles = ["如何优化机器学习模型中的过拟合问题",
          "在Flask中如何避免硬编码并进行配置管理",
          "使用孤立森林去除异常值时如何避免AUC下降",
          "如何有效地处理大规模文本数据进行知识库构建",
          "如何提高XGBoost模型的性能，避免早停轮次报错",
          "在Docker中如何部署Flask应用并进行外部访问",
          "稳定性扩散模型的调优：如何更好地实现图像生成",
          "如何通过Python脚本调用Stable Diffusion进行自动化图像生成",
          "在Metabase中如何创建动态报表并进行数据分析",
          "如何通过Transformer和CLIP优化文本到图像的转换流程"]


def sanitize_filename(title):
    # 确保 title 是字符串类型
    if not isinstance(title, str):
        title = str(title)  # 转换为字符串
    # 将标题中的非法字符替换为空，并将空格替换为下划线
    sanitized_title = re.sub(r'[\/:*?"<>|]', '', title)  # 去除非法字符
    sanitized_title = sanitized_title.replace(" ", "_")  # 替换空格为下划线
    return sanitized_title



def generate_docs_for_titles(titles):
    doc_files = []
    for title in titles:
        filename = f"{sanitize_filename(title)}.docx"  # 文件名按顺序生成
        generate_document_from_model(title, filename=filename)  # 调用大模型生成内容并保存为docx
        doc_files.append(os.path.abspath(f"/document/{filename}"))
    return doc_files  # 返回生成的文档文件列表


def batch_upload_files(page, file_paths):
    for file_path in file_paths:
        print(f"正在上传 {file_path}")
        page.locator('.file-selector-input').nth(0).set_input_files(file_path)
        page.get_by_role("radio", name="VIP文档").click()
        time.sleep(1)
        page.get_by_role("button", name="确认提交").click()
        time.sleep(1)
        page.locator(".upload-dialog-close").click()
        print(f"{file_path} 上传成功")
        time.sleep(10)  # 等待几秒，确保每个文件完全上传

def load_cookies(page):
    # 从文件加载 cookies
    with open(account_cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    # 将 cookies 设置到当前页面
    page.context.add_cookies(cookies)




# def upload_file(page):
#     # 等待并定位文件上传的 input 元素（请替换 file_input_selector 为实际的选择器）
#     file_input_selector = 'input[type="file"]'  # 上传文件的 input 选择器
#     page.wait_for_selector(file_input_selector, state="visible", timeout=10000)
#
#     # 设置文件路径并上传
#     page.set_input_files(file_input_selector, file_to_upload)
#     print("文件已成功上传")
#
#     # 等待文件上传完成后的反馈（根据需要调整时间）
#     time.sleep(5)
#
#     # 检查是否有上传成功的提示
#     if page.locator(".doc-upload-list").is_visible():
#         print("上传成功")
#         # 可选择性地关闭上传成功提示
#         page.locator(".doc-upload-btn-bar button[type='button']").click()
#     else:
#         print("上传未成功或未显示上传成功提示")




def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 加载保存的 cookies
    load_cookies(page)

    page.goto("https://cuttlefish.baidu.com/shopmis?_wkts_=1731576183614#/taskCenter/majorTask",timeout=40000)
    page.wait_for_load_state("networkidle")  # 等待所有网络请求完成

    page.locator("#app").get_by_role("button", name="Close").click()
    time.sleep(1)
    page.get_by_role("button", name="Close").click()
    time.sleep(1)

    # 点击“去完成”按钮
    page.get_by_text("去完成 >").first.click()
    time.sleep(1)
    # 点击“上传文档”按钮并调用文件上传函数
    page.get_by_role("button", name="+ 上传文档").click()
    time.sleep(1)

    # 生成文档
    doc_files = generate_docs_for_titles(titles)

    # 上传文档
    batch_upload_files(page, doc_files)

    # 暂停以观察结果
    time.sleep(10)

    # 关闭浏览器
    context.close()
    browser.close()




with sync_playwright() as playwright:
    run(playwright)
