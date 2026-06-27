import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

# Konfigurasi dari Railway Variables
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def scan_market(symbol):
    try:
        # Mengambil data harga
        df = yf.download(symbol, period='5d', interval='1h', progress=False)
        if df.empty or len(df) < 14:
            return None
        
        # Hitung RSI
        df['RSI'] = ta.rsi(df['Close'], length=14)
        last_rsi = df['RSI'].iloc[-1]
        
        # Logika Sinyal sederhana
        action = None
        if last_rsi < 30:
            action = "BUY (Oversold)"
        elif last_rsi > 70:
            action = "SELL (Overbought)"
            
        return last_rsi, action
    except:
        return None, None

def main():
    bot.send_message(CHAT_ID, "🚀 Bot Radar Sinyal Sempurna Aktif!")
    
    while True:
        symbols = ['EURUSD=X', 'GBPUSD=X']
        for symbol in symbols:
            rsi, action = scan_market(symbol)
            
            if action:
                msg = f"📊 {symbol}\nRSI: {rsi:.2f}\nSinyal: {action}"
                bot.send_message(CHAT_ID, msg)
        
        # Tunggu 1 jam agar tidak spam
        time.sleep(3600)

if __name__ == '__main__':
    main()
