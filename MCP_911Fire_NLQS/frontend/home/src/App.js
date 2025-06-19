import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const userId = 'frontend_user';
  const [query, setQuery] = useState('');
  const [model, setModel] = useState('sqlcoder');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  // 初始與查詢後都更新歷史
  const loadHistory = async () => {
    const res = await fetch(`http://localhost:8000/history/${userId}`);
    const data = await res.json();
    setHistory(data);
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        query,
        model
      })
    });
    const data = await res.json();
    setResult(data);
    loadHistory(); // 更新歷史
  };

  return (
    <div className="flex flex-col md:flex-row p-6 space-x-4 max-w-6xl mx-auto">
      {/* 左邊主查詢區 */}
      <div className="flex-1">
        <h1 className="text-2xl font-bold mb-4 text-blue-600">🔥 LLM SQL 查詢系統</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            className="w-full border border-gray-300 p-2 rounded"
            rows="4"
            placeholder="請輸入自然語言查詢..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <select
            className="border border-gray-300 p-2 rounded w-full"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="sqlcoder">🧠 sqlcoder-7b</option>
            <option value="phi3">🧠 phi3-3.8b</option>
            <option value="qwen">🧠 Qwen2.5-coder-7b</option>
          </select>
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            查詢
          </button>
        </form>

        {result && (
          <div className="mt-6 space-y-4 text-left">
            <div>
              <h2 className="font-bold">🔧 生成 SQL：</h2>
              <pre className="bg-gray-100 p-2">{result.sql}</pre>
            </div>
            <div>
              <h2 className="font-bold">📋 查詢結果：</h2>
              <pre className="bg-gray-100 p-2 overflow-auto">
                {JSON.stringify(result.result, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>

      {/* 右邊歷史區 */}
      <div className="w-full md:w-1/3 mt-6 md:mt-0 border-l pl-4">
        <h2 className="text-xl font-semibold mb-2 text-gray-700">🕘 查詢歷史</h2>
        <ul className="space-y-2">
          {history.map((item, idx) => (
            <li key={idx} className="border-b pb-2">
              <div className="text-sm font-medium text-gray-800">Q: {item.question}</div>
              <div className="text-xs text-gray-500 whitespace-pre-wrap">SQL: {item.sql}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
