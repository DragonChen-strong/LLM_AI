from playwright.sync_api import sync_playwright
import time
import json


def save_cookies(page):
    # 获取 cookies 并保存到文件中
    cookies = page.context.cookies()
    with open('cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)

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

    #登录成功后保存cookie
    save_cookies(page)
    print("Cookies 已保存")

    page.goto("https://wenku.baidu.com/view/e437ef44bceb19e8b9f6baa1.html?fr=hp_RecentDoc&_wkts_=1731547306337")


    with page.expect_popup() as page1_info:
        page.get_by_text("文库创作中心").click()
    page1 = page1_info.value
    page1.locator("#app").get_by_role("button", name="Close").click()
    page1.get_by_role("button", name="Close").click()

    # cont = ''
    # paragraphs = page.locator('//*[@id="editor-view"]/div/p')
    #
    # # 遍历所有<p> 标签
    # for p in paragraphs.element_handles():
    #     te = p.text_content()
    #     if te:
    #         cont += te
    # print(cont)
    # p1_text = page.locator('// *[ @ id = "editor-view"] / div / p[1]')
    # print(p1_text.text_content())





with sync_playwright() as playwright:
    run(playwright)
