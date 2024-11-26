import io
import random
import time

import cv2
import numpy as np
from PIL import Image
import requests
from playwright.sync_api import Playwright, sync_playwright, expect

from playwright.sync_api import sync_playwright, TimeoutError



def get_captcha_images(page):
    #截图获取滑块和图片背景
    background_url=page.locator(".passMod_puzzle-background").get_attribute("src")
    slider_url=page.locator(".passMod_puzzle-block").get_attribute("src")

    #下载图片并转化为二进制格式
    background_image=requests.get(background_url).content
    slider_image=requests.get(slider_url).content

    return background_image,slider_image


def calculate_slider_offset(background_image,slider_image):
    #使用openCV计算滑块需要移动的距离
    background=Image.open(io.BytesIO(background_image)).convert("L")
    slider=Image.open(io.BytesIO(slider_image)).convert("L")

    background=np.array(background)
    slider=np.array(slider)

    #使用模块匹配算法寻找滑块缺口的位置
    result=cv2.matchTemplate(background,slider,cv2.TM_CCORR_NORMED)
    _,_,_,max_loc=cv2.minMaxLoc(result)

    #滑块缺口的x轴位置
    slider_offset_x=max_loc[0]
    return slider_offset_x


def handle_slider_verification(page,offset_x):
    #等待滑块容器出现
    page.wait_for_selector(".passMod_dialog-container",timeout=10000) #滑块容器的选择器

    #找到滑块按钮并获取其位置
    slider=page.locator(".passMod_slide-btn")
    box=slider.bounding_box()

    if box:
        start_x=box["x"] + box["width"] / 2
        start_y=box["y"]+box["height"]  / 2
        target_x=start_x+offset_x

        #开始拖动
        page.mouse.move(start_x,start_y)
        page.mouse.down()

    #模拟逐步拖动滑块到目标位置
    current_x= start_x
    while current_x <target_x:
        step=random.randint(5,10) #随机步长
        current_x+=step
        page.mouse.move(current_x,start_y)
        time.sleep(random.uniform(0.01,0.03))

    page.mouse.up()
    time.sleep(2) #等待验证结果


def handle_text_click_verification(page):
    # 获取并点击指定的文字验证内容
    targets = page.locator(".target-text-class")
    for target in targets:
        target.click()



def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()


    page.goto("https://wenku.baidu.com")
    page.get_by_text("登录").click()
    page.get_by_placeholder("手机号/用户名/邮箱").fill("13327869267")
    page.get_by_placeholder("密码").fill("chw124862")
    page.get_by_role("checkbox", name="阅读并接受").check()
    page.get_by_role("button", name="登录").click()
    # page.goto("https://seccaptcha.baidu.com/v1/webapi/verint/svcp.html?ak=M7bcdh2k6uqtYV5miaRiI8m8x6LIaONq&backurl=https%3A%2F%2Fwenku.baidu.com%2F%3F_wkts_%3D1731488524942&ext=nSk2Z9RmDg5JK3m%2BWtLgGYs5Ho4d39IeAChp4cFZp%2B%2BdyfgQ3Ic9vtWJHglqKHZZJ2YFEZ2SBodvGtVV1xbpMdzDkbsVmFxkr7myUh5yXVkKb%2FJHoxChzCC5hBG%2FxNjR&subid=pc_home&ts=1731488588&sign=55165f23b8997366b7e0969e8e8b4db8")
    # page.locator("canvas:nth-child(10)").click(position={"x":34,"y":54})
    # page.locator("canvas:nth-child(10)").click(position={"x":214,"y":169})
    # page.locator("canvas:nth-child(10)").click(position={"x":232,"y":61})
    # page.locator("canvas:nth-child(10)").click(position={"x":99,"y":167})
    # page.goto("https://wenku.baidu.com/?_wkts_=1731488589312&svcp_stk=1_cZtZE1vKKRWbvcL3HORD4ckIVdfw0vRAjizWpY6mNCo2OLeiLVMHx12IuLv9q0Q8Bm7BNW5mTc4tFN_eom8R9XYl-9sAp6H1CQsIaFQzHNNQB_0HADkXtSuwHsSRXhjMUYQsIsyo861sxd9b-jJNoa9H4O1MkZqIQpQQgDPPuNiIy6boOvPsl5CtY572847siSsoU1iL-XU8YKjwGou3-jZnp_DR1tWRHN6AfJsm6N4%3D")
    # 检测验证类型



    try:

        page.wait_for_selector(".passMod_slide-btn, .text-click-verification-class", timeout=5000)

        if page.locator(".passMod_slide-btn").is_visible():  # 滑块验证
            print("滑块验证出现，处理滑块验证...")
            # 获取验证码图片
            background_image, slider_image = get_captcha_images(page)
            # 计算滑块需要移动的距离
            offset_x = calculate_slider_offset(background_image, slider_image)
            # 处理滑块验证
            handle_slider_verification(page, offset_x)
        elif page.locator(".text-click-verification-class").is_visible():  # 文字点选验证
            handle_text_click_verification(page)
        else:
            print("登录完成，无需滑块验证。")
    except TimeoutError:
        print("验证类型无法识别或未检测到")



    # # ---------------------
    # context.close()
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)
