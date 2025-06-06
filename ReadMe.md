# Natural Language Database Query System (DQS)

本專案提供一個以自然語言查詢資料庫的系統，支援 `.csv`、`.xlsx`、`.db` 等格式，並結合大型語言模型自動生成 SQL 查詢與摘要。

## 目錄結構

```
DQS/
├── docker-compose.yaml
├── getModel.py
├── app/
│   ├── app.py                # Streamlit 主應用程式
│   ├── Dockerfile.dqs
│   ├── requirements.txt      # 依賴套件
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── db_utils.py       # 資料庫/檔案 schema 工具
│   │   ├── llm_interface.py  # LLM 介接與 SQL/摘要生成
│   │   ├── sql_executor.py   # SQL 執行工具
│   │   └── uploaded_files/
│   └── uploaded_files/       # 使用者上傳檔案存放處
```

## 快速開始

### 1. 安裝依賴

進入 [`DQS/app`](DQS/app/) 目錄，安裝 Python 依賴：

```sh
pip install -r requirements.txt
```

### 2. 下載模型

使用 `getModel.py` 拉取模型：

```sh
python getModel.py
```

這會將 HuggingFace 上的 Qwen2.5-Coder-3B 模型與 tokenizer 下載至 `transformer_model/Qwen2_5-Coder-3B/`。

### 3. 啟動服務

使用 Docker Compose 啟動服務：

```sh
docker-compose up --build
```

### 4. 使用方式

1. 於側邊欄上傳或選擇資料檔案（支援 `.csv`、`.xlsx`、`.db`）。
2. 輸入自然語言查詢問題。
3. 系統會自動生成 SQL、執行查詢並以表格顯示結果，同時給出摘要說明。

## 主要功能

- 自然語言轉 SQL 查詢
- 支援多種資料格式（CSV、Excel、SQLite）
- 查詢結果摘要
- 查詢歷史紀錄
- LLM 本地推論（Qwen2.5-Coder-3B）

## Docker 支援

可參考 [`DQS/docker-compose.yaml`](DQS/docker-compose.yaml) 及 [`DQS/app/Dockerfile.dqs`](DQS/app/Dockerfile.dqs) 進行容器化部署。

## 聯絡方式

如有問題請開 issue 或聯絡專案維護者。
