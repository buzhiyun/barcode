# barcode/models/barcode.py
from pydantic import BaseModel,Field
from typing import List, Optional

class BarcodeIdentifyRequest(BaseModel):
    image_content: Optional[str]  = None # Base64编码的图片内容
    image_url: Optional[str] = None 
    # septnet_document: Optional[str] = Field(..., alias='_septnet_document')  

class BarcodeInfo(BaseModel):
    type: str
    barCodeText: str
    quality: Optional[int] = None
    # bounding_box: Optional[dict] = None
    location: Optional[dict] = None

# class BarcodeIdentifyResponse(BaseModel):
#     success: bool
#     barcodes: List[BarcodeInfo]
#     message: Optional[str] = None


class BarcodeIdentifyResponse(BaseModel):
    success: bool
    barcodes: List[BarcodeInfo]
    message: Optional[str] = None

