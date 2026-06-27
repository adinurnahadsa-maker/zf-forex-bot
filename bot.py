import os
import yfinance as yf
import pandas_ta as ta
import telebot
import time

# Konfigurasi
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def scan_market(symbol):
    try:
        df = yf.download(symbol, period='5d', interval='1h', progress=False)
        if df.empty or len(df) < 14:
            return None, None
        
        df['RSI'] = ta.rsi(df['Close'], length=14)
        last_rsi = df['RSI'].iloc[-1]
        
        action = None
        if last_rsi < 30:
            action = "BUY (Oversold)"
        elif last_rsi > 70:
            action = "SELL (Overbought)"
            
        return last_rsi, action
    except:
        return None, None

def main():
    # Pesan inisialisasi hanya dikirim sekali saat bot pertama kali menyala
    bot.send_message(CHAT_ID, "✅ Bot Radar Sinyal Aktif dan Siap Memantau Pasar!")
    
    while True:
        symbols = ['EURUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'USDJPY=X']
        for symbol in symbols:
            rsi, action = scan_market(symbol)
            if action:
                msg = f"📊 Sinyal {symbol}\nRSI: {rsi:.2f}\nSinyal: {action}"
                bot.send_message(CHAT_ID, msg)
        
        # Jeda 1 jam (3600 detik) untuk pemantauan berikutnya
        time.sleep(3600)

if __name__ == '__main__':
    main()
