# main.py
from fastapi import FastAPI
from barcode.api.routes import imgproc
from barcode.core.config import settings
# import signal,os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="条码识别API服务"
)

# 注册路由
app.include_router(imgproc.router, prefix="")
# app.include_router(imgproc.router, prefix="/api/imgproc")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# def signal_handler(signum, frame):
#    # 关闭操作
#    # stop_my_server()
#    os._exit(0)

# signal.signal(signal.SIGINT, signal_handler)