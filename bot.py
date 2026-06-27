import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

# Daftar instrumen yang fokus pada Forex & XAU
INSTRUMENTS = ['XAUUSD=X', 'EURUSD=X', 'GBPUSD=X', 'USDJPY=X']

def get_data(symbol):
    try:
        # Menambah timeout agar tidak sering gagal
        df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=10)
        if df.empty or len(df) < 20: 
            return None
        df['RSI'] = ta.rsi(df['Close'], length=14)
        bb = ta.bbands(df['Close'], length=20, std=2)
        df = df.join(bb)
        return df
    except Exception as e:
        print(f"Error mengambil data {symbol}: {e}")
        return None

def check_combined_signal(df):
    try:
        close = df['Close'].iloc[-1]
        upper = df['BBU_20_2.0'].iloc[-1]
        lower = df['BBL_20_2.0'].iloc[-1]
        current_rsi = df['RSI'].iloc[-1]
        prev_rsi = df['RSI'].iloc[-5:-1].max()
        
        if close >= upper: return "📉 SIDEWAYS: Harga di Upper Band (Potensi SELL)"
        if close <= lower: return "📈 SIDEWAYS: Harga di Lower Band (Potensi BUY)"
        if (current_rsi < prev_rsi and current_rsi > 65): return "🔥 TREN: Potensi Bearish Divergence (Pucuk)"
    except: pass
    return None

def main():
    # Menghapus pesan inisialisasi agar TIDAK SPAM
    while True:
        for symbol in INSTRUMENTS:
            df = get_data(symbol)
            if df is not None:
                alert = check_combined_signal(df)
                if alert:
                    try:
                        bot.send_message(CHAT_ID, f"🎯 Radar {symbol}\n{alert}")
                    except: pass
            else:
                # Jangan kirim pesan "Data Gagal" ke Telegram agar tidak spam
                print(f"Gagal memuat data untuk {symbol}")
        
        time.sleep(1800) # Scan tiap 30 menit

if __name__ == '__main__':
    main()
