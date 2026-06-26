import requests
import time

# === 🔑 KONFIGURASI UTAMA ===
TOKEN = "8804489887:AAE3oxnfvdQ3MkdSXzXNabrAVBA47nkEJ6Y"
CHAT_ID = "1074189996"

def ambil_harga_xauusd():
    """Mengambil harga emas realtime menggunakan API publik CoinGecko (PAX-GOLD) yang lolos proxy gratisan"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd"
    try:
        respon = requests.get(url, timeout=7).json()
        return float(respon['pax-gold']['usd'])
    except Exception as e:
        print(f"❌ Gagal mengambil harga market: {e}")
        return None

def kirim_telegram(harga, aksi, keterangan):
    """Mengirim struktur sinyal tangga kustom ke Telegram"""
    # Struktur kalkulator target otomatis (SL 30 pips, TP 60 pips)
    sl = harga - 30.0 if aksi == "BUY" else harga + 30.0
    tp = harga + 60.0 if aksi == "BUY" else harga - 60.0

    pesan = f"""<code>🔶 {keterangan}
├── 📈 Harga Realtime: {harga:.2f}
├── 💥 Rekomendasi: {aksi}
├── 📦 Lot: 0.01 | ✅ AMAN
├── 🛑 SL: {sl:.2f}
└── 💰 TP: {tp:.2f}</code>"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=5)
        print(f"🔥 Sinyal {aksi} Berhasil Dikirim ke Telegram pada harga {harga:.2f}!")
    except Exception as e:
        print(f"❌ Gagal mengirim sinyal ke Telegram: {e}")

# === ⚙️ SISTEM UTAMA MENYALAKAN ROBOT ===
if __name__ == "__main__":
    print("==================================================")
    print("🤖 Robot Pemantau Momentum XAUUSD Mulai Bekerja...")
    print("Bot memantau pergerakan pasar secara ketat per 5 detik.")
    print("==================================================")

    # Ambil harga patokan awal saat bot baru dinyalakan
    harga_lama = ambil_harga_xauusd()

    while True:
        time.sleep(5)  # Jeda 5 detik agar bot aman dari blokir spam Telegram
        harga_baru = ambil_harga_xauusd()

        # Validasi jika data internet sempat terputus
        if not harga_lama or not harga_baru:
            if harga_baru:
                harga_lama = harga_baru
            continue

        # Hitung kalkulasi pergeseran harga desimal market
        selisih = harga_baru - harga_lama

        # 🚀 TRIGGER BUY: Jika harga benar-benar melonjak naik
        if selisih > 0.00:
            kirim_telegram(harga_baru, "BUY", f"🚀 MOMENTUM BULLISH (+${selisih:.2f})")
            harga_lama = harga_baru

        # 🩸 TRIGGER SELL: Jika harga benar-benar terjun bebas
        elif selisih < 0.00:
            kirim_telegram(harga_baru, "SELL", f"🩸 MOMENTUM BEARISH (-${abs(selisih):.2f})")
            harga_lama = harga_baru

        # Jika selisih == 0.00 (harga tenang/sideways), bot diam siaga tanpa spam
