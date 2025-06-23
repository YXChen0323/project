import { useState } from "react";
import QuestionInput from "./components/QuestionInput";
import SQLDisplay from "./components/SQLDisplay";
import AnswerDisplay from "./components/AnswerDisplay";
import DataDisplay from "./components/DataDisplay";

function App() {
  const [userQuestion, setUserQuestion] = useState("");
  const [generatedSQL, setGeneratedSQL] = useState("");
  const [answerText, setAnswerText] = useState("");
  const [dataRows, setDataRows] = useState([]);

  const handleQuestionSubmit = (question) => {
    setUserQuestion(question);
    setGeneratedSQL(`SELECT * FROM locations WHERE city = '新北市';`);
    setAnswerText(`共有 50 筆資料來自新北市。`);
    setDataRows([]); // 清除舊資料
  };

  const handleRunSQL = (sql) => {
    console.log("執行 SQL：", sql);

    // 模擬數據
    const mockData = [
      { district: "板橋", count: 12 },
      { district: "新店", count: 8 },
      { district: "中和", count: 7 },
      { district: "永和", count: 6 },
      { district: "土城", count: 4 },
    ];

    setAnswerText("成功查詢，共 5 區域。");
    setDataRows(mockData);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">地理查詢介面</h1>
      <QuestionInput onSubmit={handleQuestionSubmit} />
      <SQLDisplay initialSQL={generatedSQL} onRunSQL={handleRunSQL} />
      <AnswerDisplay answer={answerText} />
      <DataDisplay data={dataRows} />
    </div>
  );
}

export default App;