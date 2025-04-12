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
import sys
from http import HTTPStatus

from matrix import v1, v2, v3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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
            print(f"{file_path} format: ",image.format)
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
            
    def get_cosine_similarity(
        self, 
        other_image_path, other_image_query, 
        other_image_path2, other_image_query2
        ):
        try:
            with open(self.file_path, "rb") as imf:
                base64_image = base64.b64encode(imf.read()).decode("utf-8")
            with open(other_image_path, "rb") as imf2:
                base64_image2 = base64.b64encode(imf2.read()).decode("utf-8")
            with open(other_image_path2, "rb") as imf3:
                base64_image3 = base64.b64encode(imf3.read()).decode("utf-8")

            # 获取文件实际格式
            image = self.image
            image2 = other_image_query.image
            image3 = other_image_query2.image
            
            image_format = image.format.lower()
            image_format2 = image2.format.lower()
            image_format3 = image3.format.lower()
            
            image_data = f"data:image/{image_format};base64,{base64_image}"
            image_data2 = f"data:image/{image_format2};base64,{base64_image2}"
            image_data3 = f"data:image/{image_format3};base64,{base64_image3}"
            
            #print("Generated image_url:", image_data)
            # 输入数据
            inputs = [image_data, image_data2, image_data3]
            # inputs2 = [{'image2': image_data2}]
                
            client = dashscope.MultiModalEmbedding.call(# 将输入的图片或其他多模态数据传递给指定的模型，生成对应的嵌入向量。
                # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"), 
                model="multimodal-embedding-v1",
                input=inputs,
                # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            
            save_path = "matrix.py"
            flag = 0
            # 如果文件路径不存在则执行下列操作
            if not os.path.exists(save_path):
                flag = 1
            if client.status_code == HTTPStatus.OK and flag == 1:
                embeddings = client.output["embeddings"]
                #save file
                with open("matrix.py", "a") as f:#以追加模式（append mode）打开一个文件
                    f.write(f"#ali embedding for the {os.path.basename(file_path)}\n")
                    f.write(f"v1 = {embeddings[0]}\n")
                    f.write(f"#ali embedding for the {os.path.basename(file_path2)}\n")
                    f.write(f"v2 = {embeddings[1]}\n")
                    f.write(f"#ali embedding for the {os.path.basename(file_path3)}\n")
                    f.write(f"v3 = {embeddings[2]}\n")
                    
                print('file has been processed')
            #else:
                #print(f"Error: {client.message}")
                
        except FileNotFoundError as e:
            print(e)
        except FileExistsError as e:
            print(e)
        except Exception as e:
            print(f"exception error: {e}")
        
        vec1 = np.array(v1).reshape(1, -1)
        vec2 = np.array(v2).reshape(1, -1)
        vec3 = np.array(v3).reshape(1, -1)
            
        cos1_2 = cosine_similarity(vec1, vec2)
        cos1_3 = cosine_similarity(vec1, vec3)
        cos2_3 = cosine_similarity(vec2, vec3)
        print("余弦相似度(test, test2):", cos1_2[0][0])
        print("余弦相似度(test, test3):", cos1_3[0][0])
        print("余弦相似度(test2, test3):", cos2_3[0][0])
        
if __name__ == "__main__":
    file_path = "test.png"
    file_path2 = "test2.jpg"
    file_path3 = "test3.jpeg"
    imageQuery = ImageQuery(file_path)
    imageQuery2 = ImageQuery(file_path2)
    imageQuery3 = ImageQuery(file_path3)
    
    difference = imageQuery.pixel_difference(imageQuery2)
    print("pixel difference:",difference)
    print(f"get histogram {file_path}, {file_path2}:")
    imageQuery.get_histogram()
    
    difference2 = imageQuery.pixel_difference(imageQuery3)
    print("pixel difference2:", difference2)
    print(f"get histogram {file_path}, {file_path3}:")
    imageQuery.get_histogram()
    
    
    imageQuery.get_cosine_similarity(
        file_path2, imageQuery2, 
        file_path3, imageQuery3
        )
    
    

