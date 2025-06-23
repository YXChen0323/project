export default function AnswerDisplay({ answer }) {
  return (
    <div className="w-full p-4 bg-white rounded shadow mt-4">
      <h2 className="text-lg font-bold mb-2 text-gray-800">查詢結果摘要</h2>
      <div className="text-gray-700 whitespace-pre-line">{answer || "尚無資料"}</div>
    </div>
  );
}
