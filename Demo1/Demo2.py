import uiautomation as auto
import subprocess
import time


#
# #启动应用程序 (如果它没有运行的话)
# subprocess.Popen("D:\QQ\QQ.exe")
#
# # #等待应用加载
# time.sleep(2)
#
# login_window=auto.WindowControl(searchDepth=1,Name='微信')
#
# # 输入用户名
# username_box = login_window.EditControl(searchDepth=1, Name='username')  # 替换为用户名输入框的名称
# username_box.SetValue('2095769286')  # 替换为你的用户名
#
# # 输入密码
# password_box = login_window.EditControl(searchDepth=1, Name='Password')  # 替换为密码输入框的名称
# password_box.SetValue('chw124862')  # 替换为你的密码
#
# # 点击登录按钮（假设存在一个登录按钮）
# login_button = login_window.ButtonControl(searchDepth=1, Name='登录')  # 替换为实际的登录按钮名称
# login_button.Click()

# import uiautomation as auto
# import subprocess
# import time
#
# # 启动应用程序
# subprocess.Popen(r"D:\QQ\QQ.exe")  # 使用原始字符串，避免转义问题
#
# # 等待应用加载
# time.sleep(5)  # 根据实际情况调整等待时间
#
# # 找到 QQ 窗口
# login_window = auto.WindowControl(searchDepth=1, Name='QQ')  # 确保窗口名称正确
#
# # 输入用户名
# username_box = login_window.EditControl(searchDepth=1, Name='账号')  # 替换为实际的用户名输入框名称
# username_box.SetFocus()  # 设置焦点到用户名输入框
# auto.SendKeys('2095769286')  # 输入用户名
#
# # 输入密码
# password_box = login_window.EditControl(searchDepth=1, Name='密码')  # 替换为实际的密码输入框名称
# password_box.SetFocus()  # 设置焦点到密码输入框
# auto.SendKeys('chw124862')  # 输入密码
#
# # 点击登录按钮（假设存在一个登录按钮）
# login_button = login_window.ButtonControl(searchDepth=1, Name='登录')  # 替换为实际的登录按钮名称
# login_button.Click()

import uiautomation as auto
import time

# 启动 QQ 应用程序
auto.Subprocess.Popen(r"D:\QQ\QQ.exe")

# 等待 QQ 窗口加载
login_window = auto.WindowControl(searchDepth=1, Name='QQ')

# 等待窗口出现
max_wait_time = 10
wait_time = 0
while not login_window.Exists() and wait_time < max_wait_time:
    time.sleep(1)  # 每秒检查一次
    wait_time += 1

# 检查窗口是否找到
if not login_window.Exists():
    raise Exception("登录窗口未找到，可能应用程序未正确启动。")

# 列出所有子控件
for control in login_window.GetChildren():
    print(f'Name: {control.Name}, ControlType: {control.ControlTypeName}')


