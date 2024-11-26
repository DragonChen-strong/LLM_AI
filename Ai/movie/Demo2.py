from PIL import Image, ImageDraw, ImageFont

# 打开图像
image_path = 'fish.jpeg'  # 这里替换为你的图像文件路径
image = Image.open(image_path)

# 旋转图像
rotated_image = image.rotate(0)  # 旋转45度

# 创建一个可用于绘制的对象
draw = ImageDraw.Draw(rotated_image)

# 设置字体（注意：需要系统中有此字体文件）
# 你可以选择其他字体路径，或者使用默认字体
try:
    font = ImageFont.truetype("arial.ttf", 36)
except IOError:
    font = ImageFont.load_default()


# 在图像上添加文字
text = "Hello, Pillow!"
bbox = draw.textbbox((0,0),text, font=font)
text_width = bbox[2] -bbox[0]
text_height = bbox[3] - bbox[1]
draw.text(text_position, text, fill="white", font=font)

# 保存结果图像
output_path = 'output.jpg'
rotated_image.save(output_path)

# 显示图像（可选）
rotated_image.show()
