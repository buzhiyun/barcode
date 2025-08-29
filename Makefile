# Makefile
.PHONY: help dev build-docker clean install test

# 默认目标
help:
	@echo "可用命令:"
	@echo "  make dev          - 启动开发环境"
	@echo "  make build-docker - 构建Docker镜像"
	@echo "  make install      - 安装项目依赖"
	@echo "  make test         - 运行测试"
	@echo "  make clean        - 清理临时文件"

# 变量定义
TAG ?= latest

ifeq ($(TAG),master)
	TAG := latest
endif

PROJECT_NAME = barcode
DOCKER_IMAGE = $(PROJECT_NAME):$(TAG)
DOCKER_FILE = Dockerfile

# 安装项目依赖
install:
	uv sync

# 启动开发环境
dev: install
	uv run uvicorn barcode.main:app --reload

# 运行Docker容器
run-docker:
	docker run --rm --name=barcode -p 8000:8000 $(DOCKER_IMAGE)

# 运行测试
test:
	uv run pytest

# 清理临时文件和缓存
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .venv/
	rm -rf dist/
	rm -rf *.egg-info/

# 格式化代码
format:
	uv run black src/
	uv run isort src/

# 开发环境（带热重载）
dev-reload:
	uv run uvicorn barcode.main:app --host 0.0.0.0 --port 8000 --reload

# 构建多阶段Docker镜像（如果存在）
build-docker:
	@if [ -f Dockerfile.multi-stage ]; then \
		docker build -f Dockerfile.multi-stage -t $(DOCKER_IMAGE) . ; \
	else \
		echo "Dockerfile.multi-stage 不存在，使用默认Dockerfile"; \
		docker build -t $(DOCKER_IMAGE) . ; \
	fi

# 推送Docker镜像到仓库（需要先设置DOCKER_REGISTRY）
push-docker:
	@if [ -n "$(DOCKER_REGISTRY)" ]; then \
		docker tag $(DOCKER_IMAGE) $(DOCKER_REGISTRY)/$(DOCKER_IMAGE) ; \
		docker push $(DOCKER_REGISTRY)/$(DOCKER_IMAGE) ; \
	else \
		echo "请设置DOCKER_REGISTRY环境变量"; \
	fi

# 显示项目信息
info:
	@echo "项目名称: $(PROJECT_NAME)"
	@echo "Docker镜像: $(DOCKER_IMAGE)"
	@echo "Python版本: $(shell python --version 2>/dev/null || echo '未安装')"
	@echo "uv版本: $(shell uv --version 2>/dev/null || echo '未安装')"

# 检查依赖安全性
check-deps:
	uv pip audit

# 更新依赖
update-deps:
	uv lock --upgrade

# 显示所有目标
list:
	@$(MAKE) -pRrq -f $(lastword $(