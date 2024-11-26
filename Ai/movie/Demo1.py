from gtts import gTTS
import os

# 创建一个gTTS对象
text = "你好，袁灵玉！"
tts = gTTS(text=text, lang='zh', slow=False)

# 保存语音文件
tts.save("output.mp3")

# 播放语音（需要系统支持）
os.system("start output.mp3")  # Windows
