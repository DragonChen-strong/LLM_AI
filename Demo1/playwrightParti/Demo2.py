from playwright.sync_api import sync_playwright

'''
fill和keyboard的区别就是fill适合快速，而keyboard适合模拟用户的真实输入
'''

def run(playwright):
    browser=playwright.chromium.launch(headless=False) #表示以可视化的方式打开浏览器，而不0是再无头模式下运行
    page=browser.new_page() #新建一个页面

    # 等待页面加载完成
    page.wait_for_load_state('networkidle')


    page.goto('https://www.baidu.com/')#访问网址

    #用fill去进行填充
    # page.fill('input[name="wd"]','中华名族')

    #用keyboard适合模拟用户输入 过程
    page.click('input[name="wd"]') #确保输入框已聚焦
    page.keyboard.type("hello",delay=100)

    page.wait_for_timeout(1000)
    page.wait_for_selector('input[id="su"]')
    page.click('input[id="su"]')


    page.wait_for_timeout(10000)





#同步锁创建对象
with sync_playwright() as playwright:
        run(playwright)




