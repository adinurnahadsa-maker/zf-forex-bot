import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

# Konfigurasi
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

# KITA GUNAKAN FILE SEBAGAI "MEMORI" AGAR PESAN HANYA DIKIRIM SEKALI
MEM_FILE = "bot_init.txt"

def send_once(message):
    if not os.path.exists(MEM_FILE):
        try:
            bot.send_message(CHAT_ID, message)
            with open(MEM_FILE, "w") as f:
                f.write("sent")
        except:
            pass

def get_data(symbol):
    try:
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
        return f"📊 Peringatan Bearish Divergence! RSI: {current_rsi:.2f}"
    return None

def main():
    # Pesan ini hanya akan terkirim SEKALI SEUMUR HIDUP bot
    send_once("🤖 Bot Trading Aktif dan Memantau Pasar...")
    
    while True:
        symbols = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'USDJPY=X']
        for symbol in symbols:
            df = get_data(symbol)
            if df is not None:
                alert = check_divergence(df)
                if alert:
                    try:
                        bot.send_message(CHAT_ID, f"Pair: {symbol}\n{alert}")
                    except:
                        pass
        time.sleep(3600) # Jeda 1 jam

if __name__ == '__main__':
    main()
