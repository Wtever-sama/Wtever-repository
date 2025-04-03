from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt
class ImageProcessor:
    def __init__(self, imageData = None):
        self.imageData = imageData # 一个dic，存储修改的参数
        self.image_path = imageData['image_path']
        self.window = imageData['window']
        self.rotation = imageData['rotation']
        
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
       # self.resolution = self.image.info.get['dpi',(1,1)]        
    def process(self):
        self.image.show()

class imp1(ImageProcessor):
    def __init__(self, imageData):
        super().__init__(imageData)# 调用基类的构造函数
    def process(self):
        
        # 对图片进行灰度化处理
        no_color = self.image.convert('L')
        no_color.show()
        # 裁剪图片大小
        # window = (15,15,200,200)
        region = self.image.crop(self.window)
        region.show()
        # 模糊处理
        blr = self.image.filter(ImageFilter.BLUR)
        blr.show()
        # 边缘提取
        edge = self.image.filter(ImageFilter.FIND_EDGES)
        edge.show()

if __name__ == '__main__':
    image_path = '/Users/wtsama/Documents/code/Wtever-repository/week6/lx.jpg'
    imageData = {
                'image_path': image_path,
                 'window':(15,15,200,200),
                 'rotation': 45
                 }
    processor = imp1(imageData)
    processor.process()
        
