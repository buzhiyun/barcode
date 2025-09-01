# Dockerfile.multi-stage
# 构建阶段
FROM python:3.12-slim AS builder

# 安装构建依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ && \
    rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:0.8.13 /uv /bin/uv

# 设置工作目录
WORKDIR /app

# 复制项目配置文件
COPY pyproject.toml uv.lock ./

# 安装项目依赖
RUN uv sync --frozen

# 生产阶段
FROM python:3.12-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# 安装运行时依赖
RUN sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    # libgl1-mesa-glx \
    # libglx-mesa0 \
    libgl1 \
    # libglib2.0-0 \
    libsm6 \
    # libxext6 \
    libzbar-dev \
    libxrender-dev \
    # libgomp1 \
    libjpeg62-turbo-dev \
    # zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制 uv
COPY --from=ghcr.io/astral-sh/uv:0.2.25 /uv /bin/uv

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 复制源代码
COPY barcode barcode

# 创建非 root 用户
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uv", "run", "uvicorn", "barcode.main:app","--workers", "8","--host","0.0.0.0"]