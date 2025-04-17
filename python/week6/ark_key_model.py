import base64
import os
# 通过 pip install volcengine-python-sdk[ark] 安装方舟SDK
from volcenginesdkarkruntime import Ark

from dotenv import load_dotenv
load_dotenv()  # 加载.env文件

# 从环境变量中读取您的方舟API Key
client = Ark(api_key=os.environ.get("ARK_API_KEY"))
# 定义方法将指定路径图片转为Base64编码
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# 需要传给大模型的图片
image_path = "lx.jpg"

# 检查
if not os.path.exists(image_path):
    raise FileNotFoundError(f"图片文件 {image_path} 不存在")

with open(image_path, "rb") as f:
    print("文件头字节:", f.read(4))  


# 将图片转为Base64编码
base64_image = encode_image(image_path)
print("Base64前10字符:", base64_image[:10])  

response = client.chat.completions.create(
  # 替换 <Model> 为模型的Model ID
  model="doubao-1.5-vision-pro-32k-250115",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "图片里讲了什么?",
        },
        {
          "type": "image_url",
          "image_url": {
          # 需要注意：传入Base64编码前需要增加前缀 data:image/{图片格式};base64,{Base64编码}：
          # PNG图片："url":  f"data:image/png;base64,{base64_image}"
          # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
          # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
            "url":  f"data:image/png;base64,{base64_image}"
            
          },
        },
      ],
    }
  ],
)

print(response.choices[0])