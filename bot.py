import os
import yfinance as yf
import telebot
import time

# Konfigurasi
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)
INSTRUMENTS = ['XAUUSD=X', 'EURUSD=X', 'GBPUSD=X', 'USDJPY=X']

def get_market_data(symbol):
    try:
        # Mengambil data harga OHLC
        df = yf.download(symbol, period='5d', interval='1h', progress=False)
        return df
    except: return None

def check_price_action(df):
    # Logika mendeteksi pergerakan impulsif (Gap besar)
    # Jika harga penutupan candle terakhir > High candle sebelumnya + threshold
    current_close = df['Close'].iloc[-1]
    prev_high = df['High'].iloc[-2]
    prev_low = df['Low'].iloc[-2]
    
    # Deteksi Breakout Impulsif (Potensi BoS)
    if current_close > prev_high:
        return f"⚡ STRUCTURE BREAK (BULLISH): Harga menembus {current_close:.2f}"
    elif current_close < prev_low:
        return f"⚡ STRUCTURE BREAK (BEARISH): Harga menembus {current_close:.2f}"
    
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
                    except: pass
        time.sleep(1800) # Scan tiap 30 menit

if __name__ == '__main__':
    main()
