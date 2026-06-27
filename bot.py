import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

# Konfigurasi
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

# Variabel status untuk mencegah spam pesan aktif
is_initialized = False

def get_data(symbol):
    try:
        # Mengambil data 5 hari terakhir
        df = yf.download(symbol, period='5d', interval='1h', progress=False)
        if df.empty or len(df) < 20:
            return None
        df['RSI'] = ta.rsi(df['Close'], length=14)
        return df
    except:
        return None

def check_divergence(df):
    current_rsi = df['RSI'].iloc[-1]
    prev_rsi = df['RSI'].iloc[-5:-1].max()
    
    if current_rsi < prev_rsi and current_rsi > 60:
        return f"📊 Peringatan: Potensi Bearish Divergence (Pucuk Terdeteksi!) \nRSI: {current_rsi:.2f}"
    return None

def main():
    global is_initialized
    if not is_initialized:
        try:
            bot.send_message(CHAT_ID, "🤖 Bot Trading Aktif dan Memantau Pasar...")
            is_initialized = True
        except:
            pass
    
    while True:
        symbols = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'USDJPY=X']
        for symbol in symbols:
            df = get_data(symbol)
            if df is not None:
                alert = check_divergence(df)
                if alert:
                    bot.send_message(CHAT_ID, f"Pair: {symbol}\n{alert}")
        
        # Jeda 1 jam sebelum scan ulang
        time.sleep(3600)

if __name__ == '__main__':
    main()
