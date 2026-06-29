import os
import yfinance as yf
import telebot
import time

# Konfigurasi dari Environment Variables Railway
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

# Instrumen yang dipantau (GC=F adalah Gold Futures untuk menggantikan XAUUSD)
INSTRUMENTS = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'GC=F']

def get_market_data(symbol):
    try:
        # Mengambil data 5 hari terakhir dengan timeout agar stabil
        df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=10)
        if df is None or df.empty or len(df) < 5:
            return None
        return df
    except Exception:
        return None

def check_price_action(df):
    try:
        # Pastikan data tersedia untuk dianalisis
        if len(df) < 2:
            return None
            
        current_close = float(df['Close'].iloc[-1])
        prev_high = float(df['High'].iloc[-2])
        prev_low = float(df['Low'].iloc[-2])
        
        # Deteksi Break of Structure (BoS)
        if current_close > prev_high:
            return f"⚡ STRUCTURE BREAK (BULLISH): {current_close:.2f}"
        elif current_close < prev_low:
            return f"⚡ STRUCTURE BREAK (BEARISH): {current_close:.2f}"
            
    except Exception:
        return None
    return None

def main():
    # Loop utama bot yang berjalan terus menerus
    while True:
        for symbol in INSTRUMENTS:
            df = get_market_data(symbol)
            if df is not None:
                alert = check_price_action(df)
                if alert:
                    try:
                        bot.send_message(CHAT_ID, f"🎯 Radar {symbol}\n{alert}")
                    except: 
                        pass
        
        # Jeda 1 jam sebelum scan ulang agar server Railway tetap tenang
        time.sleep(3600) 

if __name__ == '__main__':
    # Menjalankan fungsi utama
    main()
