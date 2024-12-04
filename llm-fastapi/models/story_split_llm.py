from langchain_experimental.llms.ollama_functions import OllamaFunctions
import json
from core.config import config
from models.story_picture import save_image
import numpy as np
# 初始化 OllamaFunctions 模型
model = OllamaFunctions(
    model=config.LLM_MODEL,
    base_url=config.LLM_URL,
    format="json"  # 输出格式设置为 JSON
)


def call_ollama_to_segment_story(user_input):
    """
    该函数接受用户输入的故事，并调用 LLM 对故事进行分段
    """
    # 给模型提供的系统消息：故事分段规则
    message = [
        {"role": "system", "content": """
            你是一个优秀的故事分段助手。你将根据输入的故事文本进行合理的分段，并确保每段的内容清晰、自然、逻辑通顺。
            规则：
            1. 你需要对长篇故事进行合理的分段，确保每段的内容不冗长且易于理解。
            2. 每段的长度不应超过 300 字。
            3. 请根据故事的情节变化、时间和空间的转换等进行分段。
            4. 每一段应有明确的主题或情节发展。
            5. 请将每个段落以数字编号的方式呈现，例如：
                1. 第一段的内容。
                2. 第二段的内容。
                3. 第三段的内容。
            6. 输出格式应为 JSON，字段为 `segments`，值为段落数组。
        """}
    ]

    # 给模型传递输入故事内容
    user_message = {"role": "user", "content": user_input}

    # 完整的消息
    message.append(user_message)

    # 调用模型并获取响应，模型将返回分段后的故事内容
    res = model.invoke(message)

    # 检查是否能获取到JSON格式的分段内容
    try:
        response_json = json.loads(res.content)
        # 如果返回的是JSON格式的响应
        segments = response_json.get("segments", [])
        return segments
    except json.JSONDecodeError:
        # 如果返回的是文本格式，进行手动分段处理
        return res.content.split("\n")  # 按照换行分段

#生成正反提示词
def generate_prompts_from_segment(segment):
    """
    根据每段故事生成 ComfyUI 的正面和反面提示词，利用大模型进行内容理解和生成提示词
    """
    # 发送请求到大模型，让其生成正面和反面提示词
    message = [
        {"role": "system", "content": """
            你是一个适用于** ComfyUI **提示词生成助手。你将根据输入的段落内容，生成适合生成图像的正面提示词和反面提示词。
            正面提示词应描述这段内容中的主要场景、人物、情感氛围等，而反面提示词应描述不希望出现在图像中的元素。
            请根据段落生成一组合理的正面提示词和反面提示词，两个提示词的格式应该是：
            正面提示词：描述场景的积极元素，建议使用细节和情感来描绘 （cute kitten, small furry cat, playful kitten）生成的正提示词像括号里面的格式。
            反面提示词：描述反面场景的消极元素，避免不需要的情感或场景（aggressive cat, adult cat, dark colors）生成的正提示词像括号里面的格式。
            
        """},
        {"role": "user", "content": segment}
    ]

    # 调用大模型生成正面和反面提示词
    res = model.invoke(message)

    try:
        # 解析返回的响应，获取正面提示词和反面提示词
        res_content = res.content

        # 正面提示词和反面提示词的分割符号
        pos_prompt_start = '正面提示词：'
        neg_prompt_start = '反面提示词：'

        # 提取正面提示词和反面提示词
        pos_prompt_start_index = res_content.find(pos_prompt_start)
        neg_prompt_start_index = res_content.find(neg_prompt_start)

        if pos_prompt_start_index != -1 and neg_prompt_start_index != -1:
            # 提取正面提示词（从正面提示词开始到反面提示词之前）
            pos_prompt = res_content[pos_prompt_start_index + len(pos_prompt_start):neg_prompt_start_index].strip()

            # 提取反面提示词（从反面提示词开始到结尾）
            neg_prompt = res_content[neg_prompt_start_index + len(neg_prompt_start):].strip()

            # 返回正面提示词和反面提示词
            return pos_prompt, neg_prompt
        else:
            return "positive prompt not found", "negative prompt not found"

    except Exception as e:
        # 若解析失败，则返回默认值
        print(f"Error: {e}")
        return "positive prompt not found", "negative prompt not found"




def call_story_to_picture(user_story):

    # 调用函数分段故事
    story_segments = call_ollama_to_segment_story(user_story)

    # 输出分段后的结果
    for idx, segment in enumerate(story_segments, start=1):
        print(f"第 {idx} 段: {segment}")


    # 为每段生成 ComfyUI 正反提示词
    # 为每段生成 ComfyUI 正反提示词
    for idx, segment in enumerate(story_segments, start=1):
        # 生成正面和反面提示词
        pos_prompt, neg_prompt = generate_prompts_from_segment(segment)
        save_image(pos_prompt,neg_prompt,np.random.randint(100000, 1000000),idx)


    return {"status":200,"message":"图片已全部加载完成"}

