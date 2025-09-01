# api/routes/imgproc.py
from fastapi import APIRouter, HTTPException, Request
from barcode.models.barcode import BarcodeIdentifyRequest, BarcodeIdentifyResponse,BarcodeInfo
from barcode.services.barcode_service import barcode_service
from fastapi.responses import Response
from pydantic import BaseModel
import json
router = APIRouter()


# @router.post("/barcodeidentify", response_model=BarcodeIdentifyResponse)
@router.post("/barcodeidentify")
async def identify_barcode(
    # septnet_document: Optional[BarcodeIdentifyRequest] = Form(None),
    # septnet_document: Optional[dict] = None,
    # image_content: Annotated[str, Form(), Body()] = None,
    # request: BarcodeIdentifyRequest = None
    # image_content: Annotated[str, Form()] = None,
    # request: BarcodeIdentifyRequest = None,
    request: Request
    # response: Union[Response, None] = None
    ):
    """
    识别图片中的条码
    
    Args:
        image_content: 包含Base64编码图片内容的请求
        image_url: 图片的URL
        
    Returns:
        识别结果，包含所有找到的条码信息
    """
    # 获取请求内容类型
    content_type = request.headers.get("Content-Type", "")
    
    image_content = None
    image_url = None
    septnet_document = None
    # 处理表单数据
    if "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        septnet_document = form_data.get("_septnet_document",None)
        image_content = form_data.get("image_content",None)
        image_url = form_data.get("image_url",None)

    # 处理JSON数据
    elif "application/json" in content_type:
        json_data = await request.json()
        image_content = json_data.get("image_content",None)
        image_url = json_data.get("image_url",None)

    # print("request:", request , "  image_content:", image_content)
    try:
        # if septnet_document:
            # print("_septnet_document:", septnet_document)
        if septnet_document:
            image_url = json.loads(septnet_document).get("image_url",None)
        
        # barcodes = []
               
        if image_url:
            barcodes = barcode_service.identify_barcodes_from_url(image_url)
            if len(barcodes)>0:
                # 获取第一个条码的数据作为文本
                text_content = barcodes[0].barCodeText
                return Response(content=text_content, media_type="text/plain")
            
        if image_content:
            barcodes = barcode_service.identify_barcodes_from_base64str(image_content)
            if len(barcodes)>0:
                # 返回第一个条码的数据作为文本
                text_content = barcodes[0].barCodeText
                print("barcodes[0]:", barcodes[0])
                return Response(content=text_content, media_type="text/plain")


        # 没有找到条码时返回空文本
        return Response(content="", media_type="text/plain")


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.post("/location")
async def location_barcode(request: Request):
    """
    识别图片中的条码位置
    
    Args:
        image_content: 包含Base64编码图片内容的请求
        image_url: 图片的URL
        
    Returns:
        识别结果，包含所有找到的条码信息
    """

    # 获取请求内容类型
    content_type = request.headers.get("Content-Type", "")
    
    image_content = None
    image_url = None
    septnet_document = None
    # 处理表单数据
    if "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        septnet_document = form_data.get("_septnet_document",None)
        image_content = form_data.get("image_content",None)
        image_url = form_data.get("image_url",None)

    # 处理JSON数据
    elif "application/json" in content_type:
        json_data = await request.json()
        image_content = json_data.get("image_content",None)
        image_url = json_data.get("image_url",None)

    # print("request:", request , "  image_content:", image_content)
    try:
        # if septnet_document:
            # print("_septnet_document:", septnet_document)
        if septnet_document:
            image_url = json.loads(septnet_document).get("image_url",None)
        if image_url:
            barcodes = barcode_service.identify_barcodes_from_url(image_url)
            if len(barcodes)>0:
                # 获取第一个条码的数据作为文本
                return barcodes[0].model_dump(exclude_none=True)

        if image_content:
            barcodes = barcode_service.identify_barcodes_from_base64str(image_content)
            if len(barcodes)>0:
                # 返回第一个条码的数据作为文本
                return barcodes[0].model_dump(exclude_none=True)

        # 没有找到条码时返回空文本
        return Response(content='{"barCodeText":"","location":None}', media_type="application/json")        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")
    



@router.post("/locations")
async def location_barcodes(request: Request):
    """
    识别图片中的条码位置
    
    Args:
        image_content: 包含Base64编码图片内容的请求
        image_url: 图片的URL
        
    Returns:
        识别结果，包含所有找到的条码信息
    """

    # 获取请求内容类型
    content_type = request.headers.get("Content-Type", "")
    
    image_content = None
    image_url = None
    septnet_document = None
    # 处理表单数据
    if "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        septnet_document = form_data.get("_septnet_document",None)
        image_content = form_data.get("image_content",None)
        image_url = form_data.get("image_url",None)

    # 处理JSON数据
    elif "application/json" in content_type:
        json_data = await request.json()
        image_content = json_data.get("image_content",None)
        image_url = json_data.get("image_url",None)

    # print("request:", request , "  image_content:", image_content)
    try:
        # if septnet_document:
            # print("_septnet_document:", septnet_document)
        if septnet_document:
            image_url = json.loads(septnet_document).get("image_url",None)
        if image_url:
            barcodes = barcode_service.identify_barcodes_from_url(image_url)
            if barcodes:
                # 获取第一个条码的数据作为文本
                return barcodes

        if image_content:
            barcodes = barcode_service.identify_barcodes_from_base64str(image_content)
            if barcodes:
                # 返回第一个条码的数据作为文本
                return barcodes

        else:
            # 没有找到条码时返回空文本
            return Response(content='[]', media_type="application/json")         
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")