from playwright.sync_api import sync_playwright
import json
import time


def load_cookies(page):
    # 从文件加载 cookies
    with open('cookies.json', 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    # 将 cookies 设置到当前页面
    page.context.add_cookies(cookies)


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 加载保存的 cookies
    load_cookies(page)

    page.goto("https://cuttlefish.baidu.com/shopmis?_wkts_=1731576183614#/taskCenter/majorTask",timeout=40000)
    page.wait_for_load_state("networkidle")  # 等待所有网络请求完成



    # page.locator(".user-icon").click()
    # with page.expect_popup() as page1_info:
    #     # page.wait_for_selector("text=文库创作中心", state="visible", timeout=60000)
    #     # page.get_by_text("文库创作中心").click()
    #     page.get_by_text("文库创作中心", exact=True).click()
    # page1 = page1_info.value
    # page1.locator("#app").get_by_role("button", name="Close").click()
    # time.sleep(1)
    # page1.get_by_role("button", name="Close").click()
    time.sleep(50)



with sync_playwright() as playwright:
    run(playwright)
