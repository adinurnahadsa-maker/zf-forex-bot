import os
import yfinance as yf
import telebot
import time

# Pastikan TOKEN dan CHAT_ID ada di Railway Variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

# Instrumen yang dipantau
INSTRUMENTS = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'GC=F', 'BTC-USD']

def get_market_data(symbol):
    try:
        # Menambahkan timeout agar tidak hang/crash
        df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=20)
        if df is None or df.empty or len(df) < 5:
            return None
        return df
    except Exception:
        return None

def check_price_action(df):
    try:
        if len(df) < 2: return None
        # Strategi: Jika harga saat ini menembus High atau Low candle sebelumnya
        current_close = float(df['Close'].iloc[-1])
        prev_high = float(df['High'].iloc[-2])
        prev_low = float(df['Low'].iloc[-2])
        
        if current_close > prev_high:
            return f"⚡ BULLISH BREAKOUT: {current_close:.2f}"
        elif current_close < prev_low:
            return f"⚡ BEARISH BREAKOUT: {current_close:.2f}"
    except:
        return None
    return None

def main():
    # Bot hanya mengirim pesan jika ada sinyal, tidak akan mengirim error
    while True:
        for symbol in INSTRUMENTS:
            df = get_market_data(symbol)
            if df is not None:
                alert = check_price_action(df)
                if alert:
                    try:
                        bot.send_message(CHAT_ID, f"🎯 Radar {symbol}\n{alert}")
                    except: pass
        time.sleep(3600) # Jeda 1 jam agar stabil

if __name__ == '__main__':
    main()
