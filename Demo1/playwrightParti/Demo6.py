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

    page.goto("https://wenku.baidu.com/view/e437ef44bceb19e8b9f6baa1.html?fr=hp_RecentDoc&_wkts_=1731547306337",timeout=40000)
    # page.goto("https://wenku.baidu.com/ndcore/browse/aiunion?svcp_stk=1_pHNtyT-QRFbyTaxwI_N0iusXH66qXafYa8YEFfSuSwYhAhBguoE8_m6TEepwsNnXnkPecOHgKsSkHDLJbulVHPfVkCY2YwOfoeeReqI1gq_2Eg6VxsjI0hIwJO2QHsMTxtF5sEiSQGiu4kQmfxBhsn5xs5SmREuVxHqj_HXz9ZU_vBCVGdJanDa4wWiI1UhG6XF0zHnFNWAXYdzkE0iCFjRqCu1HjyEns1YnoaeQnzE%3D&_wkts_=1731564847801&actTab=chat&aiCreat=aiChat&t=1731564810854",timeout=40000)
    page.wait_for_load_state("networkidle")  # 等待所有网络请求完成

    cont = ''
    i = 1  # 从第一个段落开始
    while True:
        try:
            # 构造当前段落的 XPath
            paragraph = page.locator(f'//*[@id="editor-view"]/div/p[{i}]')
            text_content = paragraph.text_content(timeout=2000)  # 设置超时时间以防止无限等待
            if text_content:
                cont += text_content + "\n"
            i += 1  # 下一个段落
        except Exception:
            break  # 跳出循环，表示没有更多段落
    print(cont)

    #
    # # 遍历所有<p> 标签
    # for p in paragraphs.element_handles():
    #     te = p.text_content()
    #     if te:
    #         cont += te
    # print(cont)
    # p1_text=page.locator('// *[ @ id = "editor-view"] / div / p[1]')
    # print(p1_text.text_content())

    # page.locator(".user-icon").click()
    # with page.expect_popup() as page1_info:
    #     # page.wait_for_selector("text=文库创作中心", state="visible", timeout=60000)
    #     # page.get_by_text("文库创作中心").click()
    #     page.get_by_text("文库创作中心", exact=True).click()
    # page1 = page1_info.value
    # page1.locator("#app").get_by_role("button", name="Close").click()
    # time.sleep(1)
    # page1.get_by_role("button", name="Close").click()
    # time.sleep(1)


with sync_playwright() as playwright:
    run(playwright)
