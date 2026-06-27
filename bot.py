import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

INSTRUMENTS = ['XAUUSD=X', 'EURUSD=X', 'GBPUSD=X', 'USDJPY=X']

def get_data(symbol):
    try:
        df = yf.download(symbol, period='5d', interval='1h', progress=False)
        if df.empty or len(df) < 20: return None
        # Indikator Tren
        df['RSI'] = ta.rsi(df['Close'], length=14)
        # Indikator Sideways (Bollinger Bands)
        bb = ta.bbands(df['Close'], length=20, std=2)
        df = df.join(bb)
        return df
    except: return None

def check_combined_signal(df):
    close = df['Close'].iloc[-1]
    upper = df['BBU_20_2.0'].iloc[-1]
    lower = df['BBL_20_2.0'].iloc[-1]
    current_rsi = df['RSI'].iloc[-1]
    prev_rsi = df['RSI'].iloc[-5:-1].max()
    
    # 1. Deteksi Tren (Divergensi & Breakout)
    is_divergence = (current_rsi < prev_rsi and current_rsi > 65)
    
    # 2. Deteksi Sideways (Bollinger Bands)
    if close >= upper:
        return "📉 SIDEWAYS: Harga di Upper Band (Potensi SELL)"
    elif close <= lower:
        return "📈 SIDEWAYS: Harga di Lower Band (Potensi BUY)"
    elif is_divergence:
        return "🔥 TREN: Potensi Bearish Divergence (Sinyal Pucuk)"
        
    return None

def main():
    while True:
        for symbol in INSTRUMENTS:
            df = get_data(symbol)
            if df is not None:
                alert = check_combined_signal(df)
                if alert:
                    try:
                        bot.send_message(CHAT_ID, f"🎯 Radar {symbol}\n{alert}")
                    except: pass
        time.sleep(1800) # Scan tiap 30 menit

if __name__ == '__main__':
    main()
