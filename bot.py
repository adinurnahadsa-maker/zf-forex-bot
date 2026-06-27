import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def get_data(symbol):
    try:
        # Mengambil data lebih banyak (30 candle) untuk membandingkan puncak/lembah
        df = yf.download(symbol, period='5d', interval='1h', progress=False)
        if df.empty or len(df) < 20:
            return None
        df['RSI'] = ta.rsi(df['Close'], length=14)
        return df
    except:
        return None

def check_divergence(df):
    # Logika sederhana: Membandingkan RSI puncak terbaru dengan sebelumnya
    # Ini adalah deteksi dasar, ideal untuk bot Telegram notifikasi
    current_rsi = df['RSI'].iloc[-1]
    prev_rsi = df['RSI'].iloc[-5:-1].max()
    
    # Jika harga naik tapi RSI melemah (Bearish Divergence sederhana)
    if current_rsi < prev_rsi and current_rsi > 60:
        return "⚠️ Potensi Bearish Divergence (Pucuk Terdeteksi!)"
    return None

def main():
    bot.send_message(CHAT_ID, "🤖 Bot Divergensi Aktif!")
    while True:
        symbols = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'USDJPY=X']
        for symbol in symbols:
            df = get_data(symbol)
            if df is not None:
                divergence = check_divergence(df)
                if divergence:
                    msg = f"📊 {symbol}\n{divergence}\nRSI Sekarang: {df['RSI'].iloc[-1]:.2f}"
                    bot.send_message(CHAT_ID, msg)
        time.sleep(3600)

if __name__ == '__main__':
    main()
