import os
import json
import time
import logging
import random
from datetime import datetime
from flask import Flask, request
import requests
import yfinance as yf
import google.generativeai as genai
from dotenv import load_dotenv

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# --- 設定區 ---
# 注意：真實金鑰不應出現在此處，請使用 .env 檔案
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# --- 工具函式 ---

def send_telegram(message):
    """發送 Telegram 訊息"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logger.warning("Telegram Token 或 Chat ID 未設定，跳過發送")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        logger.error(f"Telegram 發送失敗: {e}")

def get_stock_price_safe(ticker):
    """
    [教學用] 獲取股價
    注意：使用 yfinance 免費數據會有 15-20 分鐘延遲。
    商業用途請務必串接付費 API (如 Fugle, Alpaca)。
    """
    try:
        # 增加隨機延遲，模擬人類行為，避免觸發 API 限制
        time.sleep(random.uniform(0.5, 1.5))
        
        stock = yf.Ticker(ticker)
        # 嘗試獲取最新價格 (延遲)
        price = stock.fast_info.last_price
        
        if not price:
            # 如果抓不到，嘗試抓取歷史數據
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                
        return float(price) if price else 0.0
    except Exception as e:
        logger.warning(f"獲取股價失敗 {ticker}: {e}")
        return 0.0

def get_ai_analysis_safe(data_summary):
    """
    [教學用] AI 數據解讀
    注意：此 Prompt 僅用於教學演示，不構成投資建議。
    """
    if not GEMINI_KEY:
        return "⚠️ AI Key 未設定，無法進行分析。"

    # 安全的 Prompt 設計：強調客觀性
    instruction = (
        "你是一位金融數據教學助理。請根據提供的股市數據，"
        "用繁體中文撰寫一份客觀的數據摘要。\n"
        "⚠️ 規範：\n"
        "1. 僅描述數據事實 (如漲跌幅、RSI數值意義)。\n"
        "2. 嚴禁提供任何買賣建議或預測未來股價。\n"
        "3. 語氣保持中立、學術。\n"
        "數據如下：\n"
    )
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(instruction + data_summary)
        return response.text
    except Exception as e:
        return f"AI 分析暫時不可用 ({str(e)})"

# --- 主程式路由 ---

@app.route("/", methods=["GET", "POST"])
def demo_handler():
    # 為了演示方便，這裡使用模擬的 Demo 數據
    # 實際專案中，這裡會連接 Google Sheets
    
    logger.info("收到請求，開始執行教學演示...")
    
    # 1. 定義演示用的觀察清單
    demo_portfolio = [
        {"symbol": "2330.TW", "cost": 600, "shares": 100},
        {"symbol": "AAPL", "cost": 150, "shares": 10}
    ]
    
    report = "🎓 **FinBot 教學版演示報告**\n\n"
    ai_data_context = ""
    
    for item in demo_portfolio:
        symbol = item['symbol']
        price = get_stock_price_safe(symbol)
        
        if price > 0:
            profit = (price - item['cost']) / item['cost'] * 100
            icon = "🟢" if profit >= 0 else "🔴"
            line = f"{icon} {symbol}: 現價 {price:.2f} (損益 {profit:.1f}%)\n"
            report += line
            ai_data_context += f"{symbol}: 現價{price}, 成本{item['cost']}\n"
        else:
            report += f"⚪ {symbol}: 無法獲取報價\n"

    # 2. 呼叫 AI 進行總結
    report += "\n🤖 **AI 數據摘要**：\n"
    ai_comment = get_ai_analysis_safe(ai_data_context)
    report += ai_comment
    
    report += "\n\n_此為教學專案，數據僅供參考_"
    
    # 3. 發送測試訊息
    if request.args.get('send') == 'true':
        send_telegram(report)
        return "已發送 Telegram 通知", 200
        
    return f"<pre>{report}</pre>", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))