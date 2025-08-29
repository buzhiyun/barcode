# app/services/barcode_service.py
import base64
import io
from typing import List
from PIL import Image
import cv2
import numpy as np
from pyzbar import pyzbar
from barcode.models.barcode import BarcodeInfo
import requests

class BarcodeService:
    @staticmethod
    def decode_base64_image(base64_string: str) -> Image.Image:
        """
        解码Base64图片字符串为PIL图像
        """
        # 移除可能的数据URI前缀
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        # 解码Base64字符串
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return image
    

    @staticmethod
    def identify_barcodes_from_image(image: Image) -> List[BarcodeInfo]:
        """
        识别图片中的条码
        
        Args:
            image: PIL图像
            
        Returns:
            识别到的条码列表
        """
        try:
            # 转换为OpenCV格式
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # 使用pyzbar识别条码
            decoded_objects = pyzbar.decode(opencv_image)
            
            barcodes = []
            for obj in decoded_objects:
                # print(obj.polygon)
                location = {}
                for i in range(len(obj.polygon)):
                    x ,y  = obj.polygon[i]
                    location[f'x{i+1}'] = x
                    location[f'y{i+1}'] = y
                barcode_info = BarcodeInfo(
                    type=obj.type,
                    barCodeText=obj.data.decode('utf-8'),
                    quality=obj.quality,
                    # bounding_box={
                    #     'x': obj.rect.left,
                    #     'y': obj.rect.top,
                    #     'width': obj.rect.width,
                    #     'height': obj.rect.height
                    # }
                    location= location,
                )
                # print(location)
                barcodes.append(barcode_info)
            
            return barcodes
        except Exception as e:
            raise ValueError(f"条码识别失败: {str(e)}")



    @staticmethod
    def identify_barcodes_from_base64str(image_content: str) -> List[BarcodeInfo]:
        """
        识别图片中的条码
        
        Args:
            image_content: Base64编码的图片内容
            
        Returns:
            识别到的条码列表
        """
        try:
            # 解码Base64图片
            pil_image = BarcodeService.decode_base64_image(image_content)
            return BarcodeService.identify_barcodes_from_image(pil_image)
        except Exception as e:
            raise ValueError(f"条码识别失败: {str(e)}")



    @staticmethod
    def identify_barcodes_from_url(image_url: str) -> List[BarcodeInfo]:
        """
        从URL中获取图片并识别条码
        
        Args:
            image_url: 图片URL
            
        Returns:
            识别到的条码列表
        """
        try:
            # 使用requests获取图片
            response = requests.get(image_url)
            response.raise_for_status()
            
            # 解码Base64图片
            image = Image.open(io.BytesIO(response.content))
            return BarcodeService.identify_barcodes_from_image(image)

        except:
            print(f"无法获取图片: {image_url}", )
            return []


# 创建服务实例
barcode_service = BarcodeService()