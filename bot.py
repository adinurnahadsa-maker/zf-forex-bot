import os
import yfinance as yf
import telebot
import time
import pandas as pd

# Konfigurasi dari Environment Variables Railway
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

# Daftar instrumen yang dipantau
INSTRUMENTS = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'GC=F', 'BTC-USD']

def get_market_data(symbol):
    try:
        # Mengambil data 5 hari terakhir dengan interval 1 jam
        df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=20)
        if df is None or df.empty or len(df) < 5:
            return None
        return df
    except Exception:
        return None

def check_price_action(df):
    try:
        # Memastikan data memiliki cukup baris agar tidak error
        if len(df) < 2: return None
            
        # Mengambil data harga penutupan dan level high/low sebelumnya
        current_close = float(df['Close'].iloc[-1])
        prev_high = float(df['High'].iloc[-2])
        prev_low = float(df['Low'].iloc[-2])
        
        # Logika Deteksi Break of Structure (BoS)
        if current_close > prev_high:
            return f"⚡ BULLISH BREAKOUT: {current_close:.2f}"
        elif current_close < prev_low:
            return f"⚡ BEARISH BREAKOUT: {current_close:.2f}"
            
    except Exception:
        return None
    return None

def main():
    # Notifikasi awal agar Anda tahu bot sudah hidup dan memantau
    try:
        bot.send_message(CHAT_ID, "✅ ZF Core Trading Bot telah dimulai dan memantau pasar.")
    except: 
        pass
    
    # Loop utama bot
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
        # Jeda 1 jam sebelum memantau kembali
        time.sleep(3600) 

if __name__ == '__main__':
    main()
