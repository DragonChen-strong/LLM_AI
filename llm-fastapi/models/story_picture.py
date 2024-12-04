import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid  #用于生成唯一的客户端ID
import json  #用于处理json数据格式
import urllib.request  #用于进行HTTP请求
import urllib.parse    #用于url编码
import os
from core.config import config
server_address = config.SERVER_ADDRESS
client_id = str(uuid.uuid4()) #使用uuid生成唯一的客户端ID

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id} #将 prompt 和 client_id 打包
    data = json.dumps(p).encode('utf-8')  #转换成JSON格式并编码为utf-8字节流
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data) #构造post请求
    return json.loads(urllib.request.urlopen(req).read()) #发送请求并返回json响应

'''
filename:用来指定图像的文件名
subfolder:子文件夹
folder_type:文件类型的参数

目的：获取图像文件
return: 返回的是图像的二进制数据，后续可以保存或展示
'''
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data) #将字典data编码为URL查询字符串
    #发送get请求到/view端点，请求图像。URL中包含了上一步编码后的参数
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

'''
prompt_id: 每次生成图像都会生成唯一的prompt_id

根据完成任务的prompt_id查询历史生成记录
return:包括该任务的生成结果、图像信息等
'''
#获取该prompt_id的历史数据
def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        #读取响应数据并将其解析为python对象。这个响应通常包含了生成的图像信息和其他相关的元数据
        return json.loads(response.read())

#
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id'] #首先调用queue_prompt函数向API发送请求，得到生成任务的prompt_id
    output_images = {} #用于存储生成图像，按节点ID分类
    while True:
        out = ws.recv()  #通过WebSocket接收消息，消息通常是一个JSON字符串，表示生成进度
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing': #检查消息类型是否为executing，表示生成过程仍在进行中
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id] #获取完成任务的历史数据，通过prompt_id来查询
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images




def save_image(pos_prompt,Neg_prompt,seednum,idx):

    #load the workflow JSON from file
    with open(config.WORK_STREAM, "r", encoding="utf-8") as f:
        workflow_jsondata=f.read()

    prompt = json.loads(workflow_jsondata)

    # prompt = json.loads()
    #Pos prompt
    prompt["15"]["inputs"]["text"] = pos_prompt
    #Neg Prompt
    prompt["16"]["inputs"]["text"] = Neg_prompt
    #set the seed for our KSampler node
    prompt["3"]["inputs"]["seed"]  = seednum

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, prompt)

    #Commented out code to display the output images:

    # 获取父目录路径
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取与父目录同级的picture文件夹路径
    picture_dir = os.path.join(os.path.dirname(parent_dir), 'picture')

    # 如果picture文件夹不存在，则创建它
    if not os.path.exists(picture_dir):
        os.makedirs(picture_dir)

    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            image_name = f"Output-{idx}.png"
            image_path = os.path.join(picture_dir, image_name)
            image.save(image_path)
            print(f"段落{idx} 图片保存成功")

# pos_prompt = "cute kitten, small furry cat, playful kitten, soft fur, adorable, whiskers, bright eyes, fluffy tail, curious, happy kitten, sitting kitten, playful pose, warm lighting, pastel colors, close-up, photorealistic, soft texture, cat in natural setting, cozy environment, gentle expression, kitten with toy, calm atmosphere"
# neg_prompt = "aggressive cat, adult cat, dark colors, harsh lighting, unrealistic, angry expression, blurry, messy fur, distorted, unnatural pose, overly abstract, no fur, no whiskers, sad kitten, rough textures, cat in a cage, cluttered background, chaotic scene"
# save_image(pos_prompt, neg_prompt)