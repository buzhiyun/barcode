# Barcode 解析

一个基于Python的条形码生成器，支持多种条形码格式。

## 功能特点

- 支持多种条形码标准（如EAN-13, UPC-A, Code 128等）
- 没有了

## 安装要求

- Python 3.10+
- pip包管理器

## 安装方法

```bash
# 克隆项目
cd barcode

# 安装依赖
pip install uv
uv sync --frozen

# 开始调试
uv run uvicorn barcode.main:app --reload
```
