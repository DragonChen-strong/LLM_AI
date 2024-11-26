import requests
from core.config import config
import json
import spacy
from dotenv import load_dotenv
from datetime import datetime, timedelta
import re
import os
# 加载 .env 文件
load_dotenv()

# 从环境变量中获取 JSON 文件路径
# DATA_JSON_PATH = os.getenv("DATA_JSON_PATH", "./document/data.json")

# 加载 JSON 文件
def load_location_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

location_data = load_location_data(r"D:\work\python3.9\weather-assistant\document\data.json")
# location_data = load_location_data(DATA_JSON_PATH)



# 提取城市名称
def extract_city_with_spacy(input_text):
    """
        使用 spaCy 和规则提取地名，包括省、市、区。
        """
    nlp = spacy.load("zh_core_web_sm")
    doc = nlp(input_text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]

    # 如果只识别出一个地名，尝试通过规则提取更细粒度的地名
    if len(locations) == 1:
        # 常见地名后缀
        location_suffixes = ["省", "市", "区", "县", "州"]
        tokens = [token.text for token in doc]
        additional_locations = [
            token for token in tokens if any(token.endswith(suffix) for suffix in location_suffixes)
        ]
        # 合并去重
        locations = list(set(locations + additional_locations))

    return locations



# 根据输入名称补全省市区信息
def find_location(input_names,data):

    '''
    根据输入的地名（省、市、区县）补全完整的省、市、区信息。
    :param input_name: 用户输入的地名
    :param data: 从data.json加载的行政区划分数据
    '''
    matched_locations = []

    # 遍历省级数据
    for province in data:
        province_name = province["fullname"]

        # 遍历市级数据
        for city in province.get("children", []):
            city_name = city["fullname"]

            # 遍历区县数据
            for district in city.get("children", []):
                district_name = district["fullname"]

                # 如果区县匹配上
                if any(name in district_name for name in input_names):
                    matched_locations.append({
                        "province": province_name,
                        "city": city_name,
                        "district": district_name
                    })
            # 如果市级匹配上（允许模糊匹配）
            if any(name in city_name for name in input_names):
                matched_locations.append({
                    "province": province_name,
                    "city": city_name,
                    "district": None  # 没有区县时，设置为空
                })


    # 如果只有一个匹配结果，无需进一步处理
    if len(matched_locations) == 1:
        return matched_locations[0]

    # 如果有多个结果，根据上级信息逐级筛选
    for location in matched_locations:
        # 检查上级城市是否匹配
        if any(name in location["city"] for name in input_names):
            return location

        # 检查上级省份是否匹配
        if any(name in location["province"] for name in input_names):
            return location

    # 如果无法确定唯一结果，返回提示
    return None


#调用天气的api
def fetch_weather_data(city, province, county=None):
    """
    调用腾讯天气 API 获取实时天气数据。
    :param city: 城市名称（必需）。
    :param province: 省份名称（必需）。
    :param county: 区县名称（可选）。
    :return: JSON 格式天气数据或错误信息。
    """

    if not city or not province:
        return {"error": "省份和城市是必需的参数"}

    # 请求参数
    params = config.WEATHER_API_PARAMS.copy()
    params.update({
        "city": city,
        "province": province,
    })

    if county:
        params["county"] = county

    try:
        response = requests.get(config.WEATHER_API_URL, params=params)
        response.raise_for_status()
        # 确保返回的是 JSON 格式
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()  #返回查询到的天气结果
        else:
            raise ValueError("API 返回的不是 JSON 格式")

    except requests.RequestException as e:
        return {"error": f"HTTP 请求失败：{str(e)}"}
    except ValueError as e:
        return {"error": f"数据解析错误：{str(e)}"}



# 解析日期
def parse_date_from_input(user_input):
    """
    从用户输入中解析目标日期（支持今天、明天、后天、大后天、几天后，以及具体日期）。
    """
    today = datetime.now()

    # 匹配"几天后"的模式
    days_later_match = re.search(r'(\d+)天后', user_input)
    if days_later_match:
        days_later = int(days_later_match.group(1))
        return (today + timedelta(days=days_later)).strftime('%Y-%m-%d')

    # 明天、后天、大后天
    if "明天" in user_input:
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    elif "后天" in user_input and "大后天" not in user_input:
        return (today + timedelta(days=2)).strftime('%Y-%m-%d')
    elif "大后天" in user_input:
        return (today + timedelta(days=3)).strftime('%Y-%m-%d')

    # 具体日期（例如"11月30日"）
    date_match = re.search(r'(\d{1,2})月(\d{1,2})日', user_input)
    if date_match:
        month, day = map(int, date_match.groups())
        year = today.year
        try:
            target_date = datetime(year, month, day)
            return target_date.strftime('%Y-%m-%d')
        except ValueError:
            return None  # 如果日期无效，返回 None

    # 默认返回今天
    return today.strftime('%Y-%m-%d')


# 整合提取、补全和 API 调用
def get_weather_info(user_input):

    ''' 整合地名解析和天气查询'''
    places=extract_city_with_spacy(user_input)

    # 补全地名后缀（如“市”、“区”）
    common_suffixes = ["市", "区", "县"]

    if not places:
        return {"error": "未能从输入中提取到有效的地名"}

    places = [
        place if any(place.endswith(suffix) for suffix in common_suffixes) else place + "市"
        for place in places
    ]

    #在地名库中查找匹配的地点
    location = find_location(places, location_data)
    if not location:
        return {"error": f"未找到输入 '{places}' 中的有效省市区信息"}


    province = location["province"]
    city = location["city"]
    district = location["district"]

    #获取目标日期
    target_date = parse_date_from_input(user_input)
    if not target_date:
        return {"error": f"未能解析输入中的日期信息: {user_input}"}


    #调用天气API
    weather_data = fetch_weather_data(city, province, district)
    if "error" in weather_data:
        return weather_data

    # 筛选目标日期的天气信息
    forecast_24h = weather_data.get('data', {}).get('forecast_24h', {})
    target_weather = next(
        (details for day, details in forecast_24h.items() if details["time"] == target_date),
        None
    )

    if not target_weather:
        return {"error": f"未找到 {target_date} 的天气信息"}

    # 返回天气数据和完整地点信息
    return {
        "weather_data": target_weather,
        "location": {
            "province": province,
            "city": city,
            "district": district,
        },
        "user_question": user_input
    }












