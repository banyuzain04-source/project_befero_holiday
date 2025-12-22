import requests
import json
from datetime import datetime, timedelta
# Hapus baris 'from tabulate import tabulate'

# --- Konfigurasi ---
API_URL = "https://api.aladhan.com/v1/timingsByCity"
CALCULATION_METHOD = 20

def get_prayer_times(city, country, date_offset=0):
    requested_date = datetime.now() + timedelta(days=date_offset)
    formatted_date = requested_date.strftime("%d-%m-%Y")
    
    print(f"⏳ Mengambil data untuk {city.title()} tanggal {formatted_date}...")
    
    params = {
        'city': city,
        'country': country,
        'method': CALCULATION_METHOD,
        'date': formatted_date
    }
    
    try:
        # Tambahkan timeout agar tidak hang jika internet lemot
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 200:
            return data['data']
        else:
            print(f"🚨 Gagal: {data.get('status')}")
            return None
    except Exception as e:
        print(f"❌ Terjadi kesalahan koneksi: {e}")
        return None

def display_prayer_times(data, city, country):
    if not data:
        return

    timings = data['timings']
    date_info = data['date']
    
    city_name = city.title()
    country_name = country.title()

    # Urutan waktu sholat
    prayer_order = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    # Nama Indonesia untuk ditampilkan
    prayer_names = {
        "Fajr": "Subuh", 
        "Dhuhr": "Dzuhur", 
        "Asr": "Ashar", 
        "Maghrib": "Maghrib", 
        "Isha": "Isya"
    }

    print("\n" + "="*40)
    print(f"📅 JADWAL SHOLAT: {city_name.upper()}")
    print(f"   Tanggal: {date_info.get('readable')}")
    print("="*40)

    # --- MEMBUAT TABEL MANUAL (TANPA TABULATE) ---
    # Header Tabel
    # :<15 artinya beri ruang 15 karakter rata kiri
    print(f"| {'Waktu Sholat':<15} | {'Jam':<15} |")
    print("-" * 40)

    # Isi Tabel
    for key in prayer_order:
        waktu_indo = prayer_names.get(key)
        jam = timings.get(key)
        print(f"| {waktu_indo:<15} | {jam:<15} |")

    print("="*40 + "\n")

# --- Main Program ---
if __name__ == "__main__":
    print("🕌 Aplikasi Jadwal Sholat Sederhana")
    
    input_city = input("Masukkan Kota: ").strip()
    input_country = input("Masukkan Negara: ").strip()
    
    if input_city and input_country:
        # Jadwal Hari Ini
        data = get_prayer_times(input_city, input_country)
        display_prayer_times(data, input_city, input_country)
    else:
        print("Kota/Negara tidak boleh kosong.")