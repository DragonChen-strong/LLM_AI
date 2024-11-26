import asyncio  #用于并发编写代码
import nest_asyncio
from playwright.sync_api import sync_playwright

# 允许嵌套事件循环
nest_asyncio.apply()

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('http://wenku.baidu.com')
        # print(page.content())
        browser.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, run)



