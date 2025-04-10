from dotenv import load_dotenv  # 新增此行
load_dotenv()  # 新增此行
import os
from volcenginesdkarkruntime import Ark
# 从环境变量中读取您的方舟API Key
client = Ark(api_key=os.environ.get("ARK_API_KEY"))
completion = client.chat.completions.create(
    # 替换 <Model>为 Model ID
    model="doubao-1.5-vision-pro-32k-250115",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)
print(completion.choices[0].message)

#print("当前工作目录:", os.getcwd())  # 应该显示项目根目录路径
#print("环境文件存在:", os.path.exists('.env'))  # 应该输出 True