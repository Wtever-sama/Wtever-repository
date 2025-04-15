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
###第一题：异常捕获。
# 实现ImageQuery类的_create_and_image方法，其利用PIL.Image类的open方法打开并返回一个Image实例，
# 但考虑到open方法可能产生FileNotFoundError或PIL.UnidentifiedImageError，请在该方法中对这两个异常进行捕获和处理
# （打印或记入日志，相关信息包括打开的文件路径和详细的异常描述）。

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
            
            
###第二题：图片的相似性计算。
# 在ImageQuery类中实现一种简单图片相似性的计算方法pixel_difference，即直接对两个图片逐相素相减，
# 并累积求和差异的绝对值，继而除以相素总数。注意该方法可能会抛出一个叫ImageQueryShapeNotMatchError的自定义异常，
# 其继承了ImageQueryError（本次作业自定义的顶层异常类），即当比较相似性的两张图片形状（长宽）不一致性时。
# 请在该方法中抛出该异常，包含两个图片的形状信息。            

    def pixel_difference(self, other_image_query):
        image = self.image
        image2 = other_image_query.image
        
        self.im = image
        self.im2 = image2
        
        print("image1 width:",image.size[0], "image1 height:",image.size[1])
        print("image2 width:",image2.size[0], "image2 height:",image2.size[1])
        
###附加题五：安装imagehash库，利用其提供的一些hash算法（如average_hash)等，来计算两张图片间的相似性，
# 即其hash值的差异。
        value_hash1 = imagehash.average_hash(image)
        value_hash2 = imagehash.average_hash(image2)
        
        print("image1 and image2 hash value difference:",
                value_hash1 - value_hash2)
            
        #return value_hash1 - value_hash2
        try:
            if image == None or image2 == None:
                raise ImageQueryError
            if image.size != image2.size:
                raise ImageQueryShapeNotMatchError
            
            # 获取图像的像素值，并进行两个图片的像素相减
            # 直接对两个图片逐相素相减，并累积求和差异的绝对值，继而除以相素总数。
            image_array = np.array(image)
            image_array2 = np.array(image2)
            image_diff = np.abs(image_array - image_array2).sum()/(image.size[0]*image.size[1])
            
            return image_diff
        
        except ImageQueryShapeNotMatchError as e:
            print(f"please make sure the two images are the same size! {e}")
        except ImageQueryError as e:
            print(f"ImageQueryError: {e}")


###第三题：图片的直方图相似性计算。
# 在ImageQuery类中实现更多的相似性计算方法。
# 具体地，利用PIL.Image类的histogram方法，获取图片相素的直方图，进而用scipy.states中的相关性计算方法来得到不同的相似性，
# 如pearson，spearman，kendall等。这些方法并不要求图片形状一致。注意，这些相似性方法还能够返回显著性。     
       
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


###第四题：图片的大模型嵌入。
# 在ImageQuery类中实现基于大模型的相似性计算方法，
# 即利用相关API(具体见Demo ali_image_embed.py或者ark_image_embed.py)首先将图片嵌入为向量，
# 继而通过向量的余弦相似度等给出相似性大小(cos_simi.py)。注意，选一个大模型实现即可，ali和字节均提供一定的免费token额度。

    def file_process(
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
                
            
            
            save_path = "/Users/wtsama/Documents/code/Wtever-repository/week7/matrix.py"
        
            # 如果文件路径不存在则执行下列操作
            if not os.path.exists(save_path):
                
                client = dashscope.MultiModalEmbedding.call(# 将输入的图片或其他多模态数据传递给指定的模型，生成对应的嵌入向量。
                # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"), 
                model="multimodal-embedding-v1",
                input=inputs,
                # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                )
                
                if client.status_code == HTTPStatus.OK:
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
                    return save_path
                else:
                    print(f"Error: {client.message}")
                    return None
            else:
                print("file already exists")
            
            
        except FileNotFoundError as e:
            print(e)
        except FileExistsError as e:
            print(e)
        except Exception as e:
            print(f"exception error: {e}")
            
    def get_cosine_similarity(self):
        try:
            vec1 = np.array(v1).reshape(1, -1)
            vec2 = np.array(v2).reshape(1, -1)
            vec3 = np.array(v3).reshape(1, -1)
                
            cos1_2 = cosine_similarity(vec1, vec2)
            cos1_3 = cosine_similarity(vec1, vec3)
            cos2_3 = cosine_similarity(vec2, vec3)
            print("余弦相似度(test, test2):", cos1_2[0][0])
            print("余弦相似度(test, test3):", cos1_3[0][0])
            print("余弦相似度(test2, test3):", cos2_3[0][0])
        except Exception as e:
            print(f"Model Problem:{e}")
            
if __name__ == "__main__":
    file_path = "test.png"
    file_path2 = "test2.jpg"
    file_path3 = "test3.jpeg"
###1
    imageQuery = ImageQuery(file_path)
    imageQuery2 = ImageQuery(file_path2)
    imageQuery3 = ImageQuery(file_path3)
###2    
    difference = imageQuery.pixel_difference(imageQuery2)
    print("pixel difference:",difference)
###3
    print(f"get histogram {file_path}, {file_path2}:")
    imageQuery.get_histogram()
###2,3    
    difference2 = imageQuery.pixel_difference(imageQuery3)
    print("pixel difference2:", difference2)
    print(f"get histogram {file_path}, {file_path3}:")
    imageQuery.get_histogram()
###4    
    imageQuery.file_process(
        file_path2, imageQuery2, 
        file_path3, imageQuery3
    )
    
    imageQuery.get_cosine_similarity()
        
    
    

