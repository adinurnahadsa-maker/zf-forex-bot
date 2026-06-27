import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

# Daftar Pair yang dipantau
INSTRUMENTS = ['XAUUSD=X', 'EURUSD=X', 'GBPUSD=X', 'USDJPY=X']

def get_data(symbol):
    try:
        # Menambahkan timeout agar tidak menggantung/crash
        df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=15)
        if df.empty or len(df) < 20: 
            return None
        
        # Tambahkan indikator RSI
        df['RSI'] = ta.rsi(df['Close'], length=14)
        return df
    except Exception:
        # Jangan kirim pesan ke Telegram agar tidak spam
        return None

def check_signal(df):
    try:
        current_rsi = df['RSI'].iloc[-1]
        # Contoh strategi: Sinyal sederhana RSI
        if current_rsi < 30: return "📈 Sinyal BUY (Oversold)"
        if current_rsi > 70: return "📉 Sinyal SELL (Overbought)"
    except: pass
    return None

def main():
    # Menghapus pesan inisialisasi (Anti-Spam)
    while True:
        for symbol in INSTRUMENTS:
            df = get_data(symbol)
            if df is not None:
                alert = check_signal(df)
                if alert:
                    try:
                        bot.send_message(CHAT_ID, f"🎯 Radar {symbol}\n{alert}")
                    except: pass
            # Jika data None, kita diam saja, jangan kirim pesan error
        
        # Jeda 1 jam agar bot tidak terdeteksi spam oleh sistem
        time.sleep(3600)

if __name__ == '__main__':
    main()
