import uvicorn
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 正在啟動 AI 情感諮商室 (Web UI)...")
    print("請打開瀏覽器前往: http://127.0.0.1:8000")
    
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=True)