import PIL
import PIL.Image as Image
import imagehash
import scipy
import scipy.stats

import dashscope
import base64
import os
from openai import OpenAI

import json
class ImageQueryError(Exception):
    def __init__(self, message = 'image is none'):
        super().__init__(message)
        
class ImageQueryShapeNotMatchError(ImageQueryError):
    def __init__(self, message = 'Image Query Shape Not Match Error'):
        super().__init__(message)
        
class ImageQuery:
    def __init__(self,file_path):
        self.file_path = file_path
        self.image = self._create_and_image()
    def _create_and_image(self):
        file_path = self.file_path
        try:
            image = Image.open(file_path)
            return image
        except FileNotFoundError as e:
            print(f"{file_path} not found: {e}")
        except PIL.UnidentifiedImageError as e:
            print(f"{file_path} cannot be identified: {e}")
            
    def pixel_difference(self, other_image_query):
        image = self.image
        image2 = other_image_query.image
        
        self.im = image
        self.im2 = image2
        
        print("image1 width:",image.size[0], "image1 height:",image.size[1])
        print("image2 width:",image2.size[0], "image2 height:",image2.size[1])
        
        try:
            if image == None or image2 == None:
                raise ImageQueryError
            if image.size != image2.size:
                raise ImageQueryShapeNotMatchError
            # 获取图像的像素值，并进行两个图片的像素相减
            
            value_hash1 = imagehash.average_hash(image)
            value_hash2 = imagehash.average_hash(image2)
            
            return value_hash1 - value_hash2
        
        except ImageQueryShapeNotMatchError as e:
            print(f"please make sure the two images are the same size! {e}")
        except ImageQueryError as e:
            print(f"ImageQueryError: {e}")
            
    def get_histogram(self):
        image = self.im
        image2 = self.im2
        try: 
            if image == None or image2 == None:
                raise ImageQueryError
            
            c_hist = image.histogram()
            c_hist2= image2.histogram()
            
            pearson_correct = scipy.stats.pearsonr(c_hist, c_hist2)
            spearman_correct = scipy.stats.spearmanr(c_hist, c_hist2)
            kendalltau_correct = scipy.stats.kendalltau(c_hist, c_hist2)
            
            print("pearson_correct:",pearson_correct)
            print("spearman_correct:",spearman_correct)
            print("kendalltau_correct:",kendalltau_correct)
            
        except ImageQueryError as e:
            print(f"ImageQueryError: {e}")
            
    def get_cosine_similarity(self, other_image_path):
        image_path = self.file_path
        image_path2 = other_image_path
        with open(image_path, "rb") as imf:
            base64_image = base64.b64encode(imf.read()).decode("utf-8")
        with open(image_path2, "rb") as imf2:
            base64_image2 = base64.b64encode(imf2.read()).decode("utf-8")

        # image_format = sys.argv[2]  # 根据实际情况修改，比如png, jpg、bmp 等
        # image_data = f"data:image/{image_format};base64,{base64_image}"

        # 输入数据
        inputs = [{'image': image_data}]
            
        client = dashscope.MultiModalEmbedding.call(# 将输入的图片或其他多模态数据传递给指定的模型，生成对应的嵌入向量。
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=os.getenv("DASHSCOPE_API_KEY"), 
            model="qwen-vl-max-latest",
            input=input_image
            # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": [{"type":"text","text": "You are a helpful assistant."}]},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                            # PNG图像：  f"data:image/png;base64,{base64_image}"
                            # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                            # WEBP图像： f"data:image/webp;base64,{base64_image}"
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                        },
                        {
                            "type": "image_url",
                            # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                            # PNG图像：  f"data:image/png;base64,{base64_image}"
                            # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                            # WEBP图像： f"data:image/webp;base64,{base64_image}"
                            "image_url": {"url": f"data:image/png;base64,{base64_image2}"}, 
                        },
                        {"type": "text", "text": "图中描绘的是什么?"},
                    ],
                }
            ],
        )
        print(completion.choices[0].message.content)
        print(json.dumps(client.output, ensure_ascii=False, indent=4))
        
if __name__ == "__main__":
    file_path = "test.png"
    file_path2 = "test2.jpg"
    imageQuery = ImageQuery(file_path)
    imageQuery2 = ImageQuery(file_path2)
    
    difference = imageQuery.pixel_difference(imageQuery2)
    print("pixel difference:",difference)
    
    imageQuery.get_histogram()
    
    imageQuery.get_cosine_similarity(file_path2)
    
#看demo 中对顶层异常的阐述，主要编写两个异常类
    