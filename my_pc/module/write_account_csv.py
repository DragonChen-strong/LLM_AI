from playwright.sync_api import sync_playwright
import time
import json
import tkinter as tk
from tkinter import messagebox

account_cookies_path = r"D:\work\python3.9\my_pc\conf\cookies.json"
def save_cookies(page):
    # 获取 cookies 并保存到文件中
    cookies = page.context.cookies()
    with open(account_cookies_path, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)


# 注入页面内提示
def inject_js_prompt(page):
    # 注入 JavaScript，在页面上显示一个全屏覆盖的提示
    page.evaluate("""
        const overlay = document.createElement('div');
        overlay.id = 'verification-overlay';
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        overlay.style.color = 'white';
        overlay.style.display = 'flex';
        overlay.style.alignItems = 'center';
        overlay.style.justifyContent = 'center';
        overlay.style.fontSize = '24px';
        overlay.style.zIndex = '10000';
        overlay.innerHTML = '<div>请完成安全验证后返回。完成后此提示将消失。</div>';
        document.body.appendChild(overlay);
    """)

def remove_js_prompt(page):
    # 移除提示覆盖层
    page.evaluate("""
        const overlay = document.getElementById('verification-overlay');
        if (overlay) {
            overlay.remove();
        }
    """)




# 检测验证状态
def wait_for_verification_complete(page):
    while True:
        # 检查页面上是否存在安全验证元素
        if not page.locator("css=selector-for-authentication-element").is_visible():
            print("验证已完成")
            remove_js_prompt(page)
            break
        time.sleep(2)  # 每隔2秒检查一次


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://wenku.baidu.com")
    page.get_by_text("登录").click()
    page.get_by_placeholder("手机号/用户名/邮箱").click()
    time.sleep(1)
    page.get_by_placeholder("手机号/用户名/邮箱").fill("13327869267")
    time.sleep(1)
    page.get_by_placeholder("密码").click()
    time.sleep(1)
    page.get_by_placeholder("密码").fill("chw124862")
    time.sleep(1)
    page.get_by_role("checkbox", name="阅读并接受").check()
    time.sleep(1)
    page.get_by_role("button", name="登录").click()
    time.sleep(10)


    # 等待安全验证窗口加载并显示
    try:
        page.wait_for_selector(".passMod_dialog-container", state="visible", timeout=10000)  # 等待最多10秒
        print("安全验证窗口已显示，等待用户完成验证...")
    except:
        print("安全验证窗口未显示或加载超时，无需验证")

    # 检查安全验证元素的可见性
    if page.locator(".passMod_dialog-container").is_visible():
        # 显示页面内提示
        inject_js_prompt(page)

        # 等待安全验证元素消失（用户完成验证）
        page.wait_for_selector(".passMod_dialog-container", state="hidden", timeout=10000)  # 设置超时时间为60秒

        # 移除提示
        remove_js_prompt(page)
        print("验证已完成")
    else:
        print("无需安全验证")

    #登录成功后保存cookie
    save_cookies(page)
    print("Cookies 已保存")


with sync_playwright() as playwright:
    run(playwright)
