```md
# 🧠 自然語言資料查詢系統（NLDQS-MCP）

本系統提供使用者透過中文自然語言查詢本地資料庫，並自動轉換為 SQL 查詢語句。  
結合 React 前端、FastAPI 後端、本地部署 LLM（如 LLaMA）、PostgreSQL 資料庫與 Nginx 代理服務。

---

## 📦 系統架構

```
使用者 ⇄ React 前端 (Vite + Tailwind)
         ⇅ HTTP
      Nginx 反向代理
         ⇅ HTTP
     FastAPI 後端 (LLM 推理 + SQL 執行)
         ⇅ psycopg2
     PostgreSQL 資料庫
         ↑
    匯入 CSV / Excel
```

---

## 🚀 快速啟動

1️⃣ 下載本專案後，於根目錄執行：

```bash
docker-compose up -d --build
```

2️⃣ 打開瀏覽器：

```
http://localhost:3000
```

---

## 🗂 功能說明

### 📁 匯入資料表
- 支援 `.csv` 與 `.xlsx`
- 自動寫入 PostgreSQL 中 `query_anything` schema
- 欄位會自動清理特殊字元（如 BOM）

### 🔍 自然語言查詢
- 選擇已上傳的資料表
- 輸入中文查詢問題（例如：「有哪些蘋果手機？」）
- 系統會自動：
  - 擷取欄位名
  - 抽樣範例資料
  - 傳送給本地大型語言模型
  - 回傳 SQL 語句與查詢結果

---

## 🧪 測試範例

1. 上傳 `mobiles_dataset_2025.csv`
2. 查詢：「有哪些 Apple 手機？」
3. 預期產出 SQL：
   ```sql
   SELECT * FROM query_anything.mobiles_dataset_2025
   WHERE "Company Name" = 'Apple';
   ```

---

## ⚙️ 服務說明

| 服務名稱         | 用途                | 預設 Port  |
|------------------|---------------------|------------|
| `nginx_service`  | 前端代理 + 靜態服務 | `3000`     |
| `web`            | FastAPI 查詢 API    | `8000`     |
| `postgres_service` | PostgreSQL 資料庫 | `5432`     |
| `ollama_service` | LLM 模型服務         | `11434`    |

---

## 🛠 技術棧

- React 18 + Vite
- Tailwind CSS
- FastAPI
- PostgreSQL + psycopg2
- LLaMA 3 (via Ollama)
- Docker + Docker Compose
- Nginx 反向代理

---

## 🧯 錯誤防呆與 UX 提升

- 查詢失敗自動重試一次 ✅
- 查詢錯誤會以 alert 提示 ✅
- 系統不會因 SQL 錯誤崩潰（React 白畫面） ✅
- 欄位名自動清洗（避免 invisible character 對不上）✅
- 自動加入 prompt 指令讓模型對應正確欄位 ✅

---

## 📌 TODO（未來可擴充）

- [ ] 中英文雙語切換
- [ ] 多資料表 join 支援
- [ ] 欄位過濾與排序功能
- [ ] 查詢記錄儲存於 localStorage
- [ ] 使用 shadcn/ui 美化元件

---