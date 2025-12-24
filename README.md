# 📈 FinTech-Lab-101：金融科技實驗室-打造你的第一個Python理財助理
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Gemini](https://img.shields.io/badge/AI-Gemini%202.0-orange.svg)](https://deepmind.google/technologies/gemini/)

>教你如何串接 Google Sheets、Gemini AI 與 Python，打造屬於自己的 24 小時金融數據守護者。

⚠️ **重要聲明**：
- 本專案僅供**個人學習與研究**使用
- 使用官方授權的免費 API（yfinance）
- 不提供即時交易建議或商業化服務
- 投資有風險，請謹慎評估

---

## ✨ 學習目標

通過這個專案，你將學會：

- ✅ 如何使用 Python 處理金融數據
- ✅ 如何整合 Google Sheets 作為資料庫
- ✅ 如何使用 Gemini AI 進行文本分析
- ✅ 如何在 Google Cloud Run 部署 Serverless 應用
- ✅ 如何使用 Telegram Bot 發送通知

**這是一個教學專案，不是生產級金融系統**

---

## 🎯 功能說明

### 核心功能

1. **資產追蹤模式**
   - 從 Google Sheets 讀取投資組合
   - 使用 yfinance 獲取**延遲報價**（非即時）
   - 計算損益百分比
   - AI 生成投資組合評論

2. **學習掃描模式**
   - 計算基礎技術指標（RSI、MA）
   - 練習基本面分析概念
   - AI 輔助產業趨勢分析

### 明確的限制

- ⚠️ 數據延遲：15-20 分鐘（yfinance 限制）
- ⚠️ 請求限制：避免過度頻繁查詢
- ⚠️ 不適用於：即時交易、商業用途

---

## 🚀 快速開始

### 前置需求

- Python 3.9+
- Google Cloud Platform 帳號（免費額度）
- Google Sheets
- Telegram 帳號

### 安裝步驟

#### 1. Clone 專案

```bash
git clone https://github.com/你的帳號/finbot-pro-tutorial.git
cd finbot-pro-tutorial
```

#### 2. 安裝套件

```bash
pip install -r requirements.txt
```

**requirements.txt 內容**：
```txt
flask==3.0.0
gunicorn==21.2.0
python-dotenv==1.0.0
gspread==5.12.0
oauth2client==4.1.3
google-generativeai>=0.8.3
requests==2.31.0
yfinance==0.2.32
pandas==2.1.3
pandas-ta==0.3.14b0
```

#### 3. 設定環境變數

建立 `.env` 檔案（不要上傳到 GitHub）：

```bash
SHEET_ID=你的試算表ID
TELEGRAM_TOKEN=你的BotToken
TELEGRAM_CHAT_ID=你的ChatID
GEMINI_API_KEY=你的GeminiKey
SECRET_KEY=自訂安全金鑰
```

#### 4. 準備 Google Sheets

建立試算表並包含兩個分頁：

**Portfolio（資產配置範例）**：
```
| Symbol | Cost | Shares |
|--------|------|--------|
| 2330   | 680  | 100    |
| AAPL   | 180  | 10     |
```

**Watchlist（觀察清單範例）**：
```
| Symbol | Market | Sector | Name | Priority |
|--------|--------|--------|------|----------|
| 2454   | TW     | 面板   | 聯詠 | High     |
```
註：以上股票僅供測試程式格式使用，非投資建議。

#### 5. 本地測試

```bash
python main.py
```

開啟瀏覽器訪問：`http://localhost:8080/?run=now&key=your-secret-key`

---

## 📖 程式碼架構說明

### main.py 核心邏輯

```python
# 1. 從 Google Sheets 讀取資料
def get_portfolio():
    # 使用 gspread 連接試算表
    pass

# 2. 使用 yfinance 獲取股價（延遲數據）
def get_stock_price(symbol):
    # 遵守 API 使用規範
    # 避免過度頻繁請求
    pass

# 3. 使用 Gemini AI 分析
def ai_analysis(data):
    # 使用官方 SDK
    # 遵守免費額度限制
    pass

# 4. 發送 Telegram 通知
def send_telegram(message):
    # 使用官方 Bot API
    pass
```

### 資料流程圖

```
使用者手動觸發
    ↓
讀取 Google Sheets
    ↓
yfinance 獲取價格（延遲 15-20 分鐘）
    ↓
計算損益
    ↓
Gemini AI 分析
    ↓
Telegram 推送結果
```

---

## 🎓 學習重點

### 學習路徑 1：Python 金融數據處理

```python
import yfinance as yf

# 下載歷史數據
stock = yf.Ticker("2330.TW")
hist = stock.history(period="1mo")

# 計算簡單移動平均
hist['MA20'] = hist['Close'].rolling(window=20).mean()
```

### 學習路徑 2：Google Cloud 部署

```bash
# Dockerfile 範例
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT main:app
```

### 學習路徑 3：AI Prompt Engineering

```python
prompt = f"""
你是一位金融數據教學助理。
請客觀解讀以下投資組合的數據結構：
{portfolio_data}

請用教學的口吻，為初學者說明這個組合的「產業分佈」與「集中度風險」，
不需要提供任何買賣建議。
"""
```

---

## ⚠️ 重要限制說明

### API 使用規範

1. **yfinance**
   - 數據延遲 15-20 分鐘
   - 不可用於商業用途
   - 避免每秒超過 1 次請求
   - 參考：[yfinance GitHub](https://github.com/ranaroussi/yfinance)

2. **Gemini AI**
   - 免費額度：每日 1,500 次
   - 需遵守使用政策
   - 不得用於金融詐欺

3. **Google Sheets API**
   - 每 100 秒最多 100 次請求
   - 參考：[官方文件](https://developers.google.com/sheets/api/limits)

### 不適用場景

❌ **請勿用於以下用途**：
- 即時交易決策
- 商業化數據服務
- 大量自動化交易
- 繞過官方 API 限制

---

## 🤝 貢獻指南

歡迎提交改進建議！但請確保：

- ✅ 遵守所有 API 使用條款
- ✅ 不包含任何破解或繞過機制
- ✅ 標註清楚「教學用途」
- ✅ 提供充分的錯誤處理

---

## 📜 授權與免責

### MIT License

本專案採用 MIT License 開源，但附加以下條件：

```
使用者需自行承擔：
1. 確保符合所有第三方 API 的使用條款
2. 不將本專案用於違法或不當用途
3. 投資決策的盈虧風險
```

### 免責聲明

- 本專案**不提供投資建議**
- 數據可能不準確或延遲
- 作者不對任何損失負責
- 僅供學習與研究用途

---

## 📚 延伸學習資源

### 推薦閱讀

- [Python for Finance](https://www.oreilly.com/library/view/python-for-finance/9781492024323/)
- [yfinance 官方文件](https://github.com/ranaroussi/yfinance)
- [Google Cloud Run 教學](https://cloud.google.com/run/docs)
- [Gemini AI 開發指南](https://ai.google.dev/tutorials)

### 相關專案

- [FinTA - 技術分析庫](https://github.com/peerchemist/finta)
- [Backtrader - 回測框架](https://github.com/mementum/backtrader)
- [QuantLib - 量化金融](https://www.quantlib.org/)

---

## 🙋 常見問題

<details>
<summary><b>Q: 可以用於實際交易嗎？</b></summary>

不建議。本專案為教學用途，數據延遲且未經嚴格測試，不適用於實際交易決策。
</details>

<details>
<summary><b>Q: 為什麼不使用即時數據？</b></summary>

即時金融數據需要付費授權（通常每月數百至數千美元）。本專案使用免費的延遲數據，適合學習但不適合交易。
</details>

<details>
<summary><b>Q: 可以商業化使用嗎？</b></summary>

不可以。yfinance 和 Gemini 免費版均不允許商業用途。若要商業化，需：
1. 購買即時數據授權
2. 升級至 Gemini 付費方案
3. 遵守所有相關法規
</details>

---

## 📧 聯絡方式

- 💬 GitHub Issues: [提問](https://github.com/Phyllis9783/FinTech-Lab-101.git/issues)
- 📧 Email: Phyllis.strategy@gmail.com
---

<div align="center">

Made with ❤️ for Learning by **Phyllis**

⭐ 如果這個教學專案對你有幫助，請給一個 Star！

**投資有風險，學習需謹慎** 📚

[⬆ Back to Top](#-finbot-pro---ai-投資學習助理教學版)

</div>
