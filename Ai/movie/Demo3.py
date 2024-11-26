
import os
os.environ["IMAGEMAGICK_BINARY"] = r"D:\\download\\ImageMagick\\ImageMagick-7.1.1-39-portable-Q16-HDRI-x64\\magick.exe"  # 替换为你的实际路径

from moviepy.editor import VideoFileClip, concatenate_videoclips,AudioFileClip,TextClip,CompositeVideoClip

# 加载视频片段
clip1 = VideoFileClip("魔法树屋的秘密.mp4")  # 第一个视频片段
clip2 = VideoFileClip("魔法树屋的秘密 (3).mp4")  # 第二个视频片段

#加载语音
audio=AudioFileClip("output.mp3")


# 设置淡入和淡出的持续时间
fade_duration = 2  # 2秒

# 为第一个视频片段添加淡出效果
clip1 = clip1.fadeout(fade_duration)

# 为第二个视频片段添加淡入效果
clip2 = clip2.fadein(fade_duration)

# 合并两个视频片段
final_clip = concatenate_videoclips([clip1, clip2])

#添加音频
final_clip.set_audio(audio)

#添加文本
txt_clip=TextClip("Hello,World!",fontsize=70,color="white")
txt_clip=txt_clip.set_position('center').set_duration(final_clip.duration)
# 将文本与视频合成
video_with_text = CompositeVideoClip([final_clip, txt_clip])

# 保存最终视频
video_with_text.write_videofile("output1.mp4", codec="libx264")
