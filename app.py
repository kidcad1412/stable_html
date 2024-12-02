from flask import Flask, request, jsonify, render_template
import requests
from googletrans import Translator

app = Flask(__name__)

# Stable Diffusion API 配置
# API_URL = "https://stablediffusionapi.com/api/v3/text2img"
API_URL = f"https://api.stability.ai/v2beta/stable-image/generate/ultra"
API_KEY = "sk-bnKrlryvOKqp4OT0JrtYQ8DtuZjYmQQMGXAAB4l4aCvKrmoI"

# 初始化 Google 翻译
translator = Translator()


def google_translate(query, from_lang="zh-cn", to_lang="en"):
    """
    使用 googletrans 翻译文本
    """
    try:
        result = translator.translate(query, src=from_lang, dest=to_lang)
        return result.text
    except Exception as e:
        print(f"翻译失败: {e}")
        return None


def generate_image(prompt):
    """
    使用 Stable Diffusion API 生成图像
    """

    if 1:
        # response = requests.post(API_URL, headers=headers, json=data)

        response = requests.post(
            API_URL,
            headers={
                "authorization": f"Bearer {API_KEY}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": prompt,
                "output_format": "webp",
            },
        )
        result = response.content
        print('------------------------------------------')
        print(f"Parsed JSON!!!!!!!!!!!!!!!: {result}")  # 打印解析后的 JSON 内容

    #     response.raise_for_status()
    #     result = response.json()
    #     return result.get("output", [])[0]  # 返回生成的图像 URL
    # except requests.exceptions.RequestException as e:
    #     print(f"API 调用失败: {e}")
    #     return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    idiom = request.form.get('idiom')
    if not idiom:
        return jsonify({"error": "Missing 'idiom' in request"}), 400

    # 使用 Googletrans 翻译成语为英文
    # english_translation = google_translate(idiom)
    english_translation='tmp test'

    if not english_translation:
        return jsonify({"error": "Translation failed"}), 500

    # 构造生成图像的提示语句
    # prompt = f"An artistic depiction of the Chinese idiom: {idiom} ({english_translation}). Include symbolic elements and traditional art style."
    prompt = f"draw a  {idiom}."

    # 生成图像
    image_url = generate_image(prompt)

    if image_url:
        return jsonify({
            "idiom": idiom,
            "english_translation": english_translation,
            "prompt": prompt,
            "image_url": image_url
        })
    else:
        return jsonify({"error": "Image generation failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)
