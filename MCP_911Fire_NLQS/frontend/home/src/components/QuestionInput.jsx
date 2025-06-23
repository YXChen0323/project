import { useState } from "react";

export default function QuestionInput({ onSubmit }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() !== "") {
      onSubmit(question);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full p-4 bg-white rounded shadow">
      <label className="block text-gray-700 font-bold mb-2">輸入問題</label>
      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="例如：有哪些地點在新北市？"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          送出
        </button>
      </div>
    </form>
  );
}
