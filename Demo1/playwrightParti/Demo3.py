import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://wenku.baidu.com/view/e437ef44bceb19e8b9f6baa1.html?fr=hp_RecentDoc&_wkts_=1731547306337")

    page.wait_for_timeout(15000)

    # page.wait_for_selector('//*[@id="editor-view"]/div/p[1]')
    # p1_text=page.locator('// *[ @ id = "editor-view"] / div / p[1]')
    # print(p1_text.text_content())

    cont=''
    paragraphs=page.locator('//*[@id="editor-view"]/div/p')


    #遍历所有<p> 标签
    for p in paragraphs.element_handles():
        te=p.text_content()
        if te:
            cont+=te
    print(cont)




    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
