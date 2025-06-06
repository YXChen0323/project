# 使用官方 Python 映像檔
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製程式碼進容器
COPY . .

# 安裝相依套件
RUN pip install --no-cache-dir -r requirements.txt

# 開放 FastAPI 使用的埠
EXPOSE 8000

# 啟動 FastAPI 應用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
