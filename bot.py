import os
import yfinance as yf
import telebot
import time

# Pastikan variabel ini ada di Railway Variables (TOKEN dan CHAT_ID)
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

# Daftar instrumen yang stabil
INSTRUMENTS = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'GC=F', 'BTC-USD']

def get_market_data(symbol):
    try:
        # Mengambil data dengan timeout agar tidak menggantung/crashed
        df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=15)
        # Cek apakah data valid
        if df is None or df.empty or len(df) < 5:
            return None
        return df
    except Exception:
        # Jika gagal, bot akan diam, tidak mengirim error ke Telegram
        return None

def check_price_action(df):
    try:
        # Memastikan data memiliki cukup baris agar tidak IndexError
        if len(df) < 2: return None
            
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
        # Jeda 1 jam agar bot tidak spam & hemat resource
        time.sleep(3600) 

if __name__ == '__main__':
    main()
