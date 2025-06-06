import { useState, useEffect } from 'react'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'

function App() {
  const [input, setInput] = useState('')
  const [sql, setSql] = useState('')
  const [result, setResult] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [lang, setLang] = useState('zh')
  const [tables, setTables] = useState([])
  const [selectedTable, setSelectedTable] = useState('')

  const t = (zh, en) => (lang === 'zh' ? zh : en)

  useEffect(() => {
    axios.get('/list_tables')
      .then((res) => setTables(res.data.tables))
      .catch((err) => console.error('取得資料表失敗', err))
  }, [])

  const handleSubmit = async (e, queryText = null, isRetry = false) => {
    e.preventDefault()
    const query = queryText ?? input

    if (!query || !selectedTable) {
      alert('⚠️ 請輸入問題並選擇資料表')
      return
    }

    setLoading(true)
    setError(null)
    setSql('')
    setResult([])

    try {
      const res = await axios.post('/query', { query, table: selectedTable })
      setSql(res.data.sql)
      setResult(res.data.result)
      setHistory((prev) =>
        [query, ...prev.filter((item) => item !== query)].slice(0, 10)
      )
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        err.message ||
        '查詢時發生未知錯誤'

      // ✅ 第一次錯誤就自動重試一次
      if (!isRetry) {
        console.warn('首次查詢失敗，自動重試一次...')
        await handleSubmit(e, query, true)
        return
      }

      setError(msg)
      setSql('')
      setResult([])
      alert(`❌ 查詢失敗：\n${msg}`)
  } finally {
    setLoading(false)
  }
}


  const handleClear = () => {
    setInput('')
    setSql('')
    setResult([])
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-gray-800">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-right">
          <button
            onClick={() => setLang(lang === 'zh' ? 'en' : 'zh')}
            className="text-sm text-blue-600 hover:underline"
          >
            🌐 {lang === 'zh' ? 'English' : '中文'}
          </button>
        </div>
        <div className="bg-white shadow rounded-2xl p-6">
          <h2 className="text-xl font-bold mb-4">📁 {t('上傳 CSV/XLSX 匯入資料表', 'Upload CSV/XLSX to Database')}</h2>
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={async (e) => {
              const file = e.target.files[0]
              if (!file) return
              const formData = new FormData()
              formData.append('file', file)
              try {
                const res = await axios.post('/upload_csv', formData, {
                  headers: { 'Content-Type': 'multipart/form-data' },
                })
                alert(res.data.message)
              } catch (err) {
                alert('上傳失敗：' + (err.response?.data?.message || err.message))
              }
            }}
            className="w-full border border-gray-300 rounded px-4 py-2"
          />
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 bg-white shadow rounded-2xl p-6 space-y-4">
            <h2 className="text-xl font-bold text-blue-700">{t('🔍 自然語言查詢', 'Natural Language Query')}</h2>
            <div>
              <label className="block mb-1 text-sm font-medium">
                {t('選擇資料表', 'Select Table')}
              </label>
              <select
                className="w-full border border-gray-300 p-2 rounded"
                value={selectedTable}
                onChange={(e) => setSelectedTable(e.target.value)}
              >
                <option value="">{t('請選擇一個資料表', 'Please select a table')}</option>
                {Array.isArray(tables) &&
                  tables.map((table, idx) => (
                    <option key={idx} value={table}>{table}</option>
                  ))
                }
              </select>
            </div>
            <form onSubmit={handleSubmit} className="space-y-4 pt-2">
              <textarea
                className="w-full border border-gray-300 p-3 rounded-xl resize-none focus:ring-2 focus:ring-blue-400"
                rows="3"
                placeholder={t('請輸入自然語言問題，例如：有哪些蘋果手機？', 'e.g., What Apple phones are there?')}
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={loading}
                  className={`px-6 py-2 rounded-xl text-white font-semibold transition ${loading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'}`}
                >
                  {loading ? t('查詢中…', 'Querying...') : t('查詢', 'Query')}
                </button>
                <button
                  type="button"
                  onClick={handleClear}
                  className="px-4 py-2 border rounded-xl text-gray-700 hover:bg-gray-100"
                >
                  {t('清除', 'Clear')}
                </button>
              </div>
            </form>
            {error && (
              <div className="bg-red-100 text-red-700 p-3 rounded whitespace-pre-wrap">⚠️ {error}</div>
            )}
            {sql && (
              <div>
                <h3 className="font-semibold mb-1">{t('🧠 生成 SQL：', '🧠 SQL generated:')}</h3>
                <pre className="bg-gray-100 p-3 rounded border text-sm overflow-x-auto">{sql}</pre>
              </div>
            )}
          </div>
          <div className="bg-white shadow rounded-2xl p-4 space-y-2 h-fit">
            <h2 className="text-lg font-semibold mb-2">🕘 {t('查詢紀錄', 'Query History')}</h2>
            {history.length === 0 && <p className="text-sm text-gray-500">{t('尚無紀錄', 'No history yet')}</p>}
            {history.map((item, i) => (
              <button
                key={i}
                onClick={(e) => handleSubmit(e, item)}
                className="block w-full text-left p-2 bg-gray-50 hover:bg-blue-50 rounded text-sm border"
              >
                {item}
              </button>
            ))}
          </div>
        </div>
        {Array.isArray(result) && result.length > 0 && (
          <div className="bg-white shadow rounded-2xl p-6">
            <h2 className="text-xl font-semibold mb-2">📋 {t('查詢結果', 'Query Results')}</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full border border-gray-300 text-sm">
                <thead className="bg-gray-100">
                  <tr>
                    {Object.keys(result[0]).map((key, i) => (
                      <th key={i} className="p-2 border text-left">{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.map((row, i) => (
                    <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                      {Object.values(row).map((cell, j) => (
                        <td key={j} className="p-2 border">{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
