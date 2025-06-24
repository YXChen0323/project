# 簡易記憶體版本的上下文管理模組

# 記憶資料結構：{ user_id: [ {"role": ..., "content": ...}, ... ] }
_memory = {}

def get(user_id: str) -> list:
    """
    取得指定使用者的對話歷史
    """
    return _memory.get(user_id, [])

def add(user_id: str, role: str, content: str):
    """
    新增一則訊息進入指定使用者的對話歷史
    role: "user" 或 "model"
    """
    if user_id not in _memory:
        _memory[user_id] = []
    _memory[user_id].append({"role": role, "content": content})

def clear(user_id: str):
    """
    清除指定使用者的記憶
    """
    _memory[user_id] = []

def limit(user_id: str, max_entries: int = 10):
    """
    限制記憶條數，保留最新的 N 筆
    """
    if user_id in _memory and len(_memory[user_id]) > max_entries:
        _memory[user_id] = _memory[user_id][-max_entries:]
