from diffusers import StableDiffusionPipeline
import torch

#加载Stable Diffusion 模型
model_path=r"C:\Users\jdkj\Desktop\sd\stableDiffusion3SD3_sd3Medium.safetensors"
pipe=StableDiffusionPipeline.from_pretrained(model_path,torch_dtype=torch.float16)
pipe=pipe.to("cuda")

#定义图像生成函数
def generate_image(prompt):
    image=pipe(prompt).images[0]
    return image

#生成一张图像
prompt=("iGirl, look, solo, braids, frilly, brown hair, hat, twin braids, smiles, long hair, white background, "
        "open mouth, collared shirt, teeth, bangs, twintails, puffy sleeves, polka dot dress, upper teeth only, dress")
image=generate_image(prompt)
image.save("test.png")
