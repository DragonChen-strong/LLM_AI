from google.cloud import texttospeech

# 设置 Google Cloud TTS 客户端
client = texttospeech.TextToSpeechClient()

# 配置 TTS 请求
synthesis_input = texttospeech.SynthesisInput(text="你好，这是为你的广告漫画推文生成的配音。")

# 设置语音参数（WaveNet）
voice = texttospeech.VoiceSelectionParams(
    language_code="zh-CN",  # 设置语言
    name="zh-CN-Wavenet-A"  # 设置 WaveNet 语音
)

# 设置音频格式
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3  # 设置音频格式为 MP3
)

# 进行语音合成
response = client.synthesize_speech(
    request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
)

# 保存生成的语音文件
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Audio content written to file 'output.mp3'")
