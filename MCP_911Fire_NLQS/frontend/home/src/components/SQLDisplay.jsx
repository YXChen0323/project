import { useState, useEffect } from "react";

export default function SQLDisplay({ initialSQL, onRunSQL }) {
  const [sql, setSQL] = useState(initialSQL || "");

  // 如果外部初始 SQL 更新，內部跟著改
  useEffect(() => {
    setSQL(initialSQL);
  }, [initialSQL]);

  const handleSubmit = () => {
    if (sql.trim() !== "") {
      onRunSQL(sql);
    }
  };

  return (
    <div className="w-full p-4 bg-white rounded shadow mt-4">
      <label className="block text-gray-700 font-bold mb-2">產生的 SQL 查詢</label>
      <textarea
        value={sql}
        onChange={(e) => setSQL(e.target.value)}
        className="w-full h-40 p-2 border rounded resize-none focus:outline-none focus:ring-2 focus:ring-blue-400 font-mono"
        spellCheck={false}
      />
      <div className="text-right mt-2">
        <button
          onClick={handleSubmit}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          執行查詢
        </button>
      </div>
    </div>
  );
}
