from transformers import CLIPProcessor, CLIPModel
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# 加载模型
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
stable_diffusion_model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")

# 文本提示
text_prompt = "a sunset over the beach"

# 生成图像
generated_image = stable_diffusion_model(text_prompt).images[0]

# 使用 CLIP 评估图像和文本的相似度
inputs = clip_processor(text=text_prompt, images=generated_image, return_tensors="pt", padding=True)
outputs = clip_model(**inputs)
logits_per_image = outputs.logits_per_image # 图像与文本之间的相似度
probs = logits_per_image.softmax(dim=1)     # 计算相似度

print("文本与图像的相似度：", probs)
