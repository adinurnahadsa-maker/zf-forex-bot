import os
import yfinance as yf
import telebot
import time

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

INSTRUMENTS = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'GC=F']

def get_market_data(symbol):
    try:
        df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=10)
        if df is None or df.empty or len(df) < 15: return None
        # Tambahkan RSI untuk deteksi Sideways
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    except: return None

def check_hybrid_signal(df):
    try:
        # A. LOGIKA TREN (Price Action)
        close = float(df['Close'].iloc[-1])
        prev_h = float(df['High'].iloc[-2])
        prev_l = float(df['Low'].iloc[-2])
        
        if close > prev_h: return f"⚡ TREN: Bullish Breakout {close:.2f}"
        if close < prev_l: return f"⚡ TREN: Bearish Breakout {close:.2f}"
        
        # B. LOGIKA SIDEWAYS (Mean Reversion)
        rsi = float(df['RSI'].iloc[-1])
        if rsi > 75: return f"↔️ SIDEWAYS: Overbought (Potensi SELL) RSI:{rsi:.1f}"
        if rsi < 25: return f"↔️ SIDEWAYS: Oversold (Potensi BUY) RSI:{rsi:.1f}"
        
    except: return None
    return None

def main():
    while True:
        for symbol in INSTRUMENTS:
            df = get_market_data(symbol)
            if df is not None:
                alert = check_hybrid_signal(df)
                if alert:
                    try:
                        bot.send_message(CHAT_ID, f"🎯 Radar {symbol}\n{alert}")
                    except: pass
        time.sleep(3600)

if __name__ == '__main__':
    main()
