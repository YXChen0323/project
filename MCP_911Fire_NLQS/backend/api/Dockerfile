# 基礎映像：使用 python:3.10-slim
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製必要檔案
COPY . ./api
COPY requirements.txt .

# 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 開放 API 連接埠（如 8000）
EXPOSE 8000

# 啟動 FastAPI 應用
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
