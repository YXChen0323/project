# 使用 Python 3.10 的精簡版本作為基底映像
FROM python:3.10-slim

# 安裝必要套件
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製 requirements 並安裝套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製其餘應用程式
COPY . .

# 開放埠口
EXPOSE 8000

# 執行 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
