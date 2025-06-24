import { useState } from "react";
import QuestionInput from "./components/QuestionInput";
import SQLDisplay from "./components/SQLDisplay";
import AnswerDisplay from "./components/AnswerDisplay";
import DataDisplay from "./components/DataDisplay";

function App() {
  const [, setUserQuestion] = useState("");
  const [generatedSQL, setGeneratedSQL] = useState("");
  const [answerText, setAnswerText] = useState("");
  const [dataRows, setDataRows] = useState([]);
  const [selectedModel, setSelectedModel] = useState("sqlcoder:7b");

  const handleQuestionSubmit = async (question) => {
    setUserQuestion(question);
    setAnswerText("查詢中...");
    setGeneratedSQL("");
    setDataRows([]);

    try {
      const response = await fetch("/api/rpc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          jsonrpc: "2.0",
          method: "generate_sql",
          params: { question, model: selectedModel },
          id: "frontend-query"
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log("收到回應：", result);

      if (result?.result) {
        const { sql, summary, data } = result.result;
        setGeneratedSQL(sql);
        setAnswerText(summary);
        setDataRows(sql === "[No SQL generated]" ? [] : data || []); // 僅在有有效 SQL 時顯示數據
      } else {
        setAnswerText("查詢失敗：" + (result.error?.message || "未知錯誤"));
        setGeneratedSQL("");
        setDataRows([]);
      }
    } catch (error) {
      console.error("發送查詢錯誤：", error);
      setAnswerText(`系統錯誤：${error.message}`);
    }
  };

  const handleRunSQL = (sql) => {
    alert("尚未開放手動 SQL 執行。");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 space-y-4">
      <h1 className="text-2xl font-bold">地理查詢介面</h1>
      <div className="mb-2">
        <label className="mr-2 font-semibold">選擇模型：</label>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="border px-2 py-1 rounded"
        >
          <option value="sqlcoder:7b">sqlcoder:7b</option>
          <option value="qwen2.5-coder:7b">qwen2.5-coder:7b</option>
          <option value="phi3:3.8b">phi3:3.8b</option>
        </select>
      </div>
      <QuestionInput onSubmit={handleQuestionSubmit} />
      <SQLDisplay initialSQL={generatedSQL} onRunSQL={handleRunSQL} />
      <AnswerDisplay answer={answerText} />
      <DataDisplay data={dataRows} />
    </div>
  );
}

export default App;