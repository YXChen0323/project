export async function sendQuery(naturalQuestion) {
  const response = await fetch("/api/rpc", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "generate_sql",
      params: {
        question: naturalQuestion,
        model: "sqlcoder"
      },
      id: "abc123"
    })
  });

  const result = await response.json();
  return result.result;
}