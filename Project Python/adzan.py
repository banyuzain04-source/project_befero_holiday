import requests
import json
from datetime import datetime, timedelta
from tabulate import tabulate

# --- Konfigurasi dan Konstanta ---
# Aladhan Prayer Times API
API_URL = "https://api.aladhan.com/v1/timingsByCity"
# Metode perhitungan (20: Egyptian General Authority of Survey)
CALCULATION_METHOD = 20

def get_prayer_times(city, country, date_offset=0):
    """
    Mengambil jadwal sholat dari Aladhan API untuk kota dan negara tertentu.
    
    Args:
        city (str): Nama kota.
        country (str): Nama negara.
        date_offset (int): Selisih hari dari hari ini (0=Hari ini, 1=Besok, dst).
        
    Returns:
        dict or None: Data jadwal sholat jika berhasil, None jika gagal.
    """
    
    # Hitung tanggal yang diminta
    requested_date = datetime.now() + timedelta(days=date_offset)
    formatted_date = requested_date.strftime("%d-%m-%Y")
    
    print(f"Mengambil jadwal sholat untuk {city.title()}, {country.title()} pada tanggal {formatted_date}...")
    
    # Parameter query untuk API
    params = {
        'city': city,
        'country': country,
        'method': CALCULATION_METHOD,
        'date': formatted_date  # Menggunakan parameter 'date' untuk spesifik tanggal
    }
    
    try:
        # 1. Permintaan data (HTTP GET)
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()  # Memunculkan HTTPException jika kode status adalah 4xx atau 5xx
        
        # 2. Parsing JSON
        data = response.json()
        
        # Cek status API
        if data.get('code') == 200:
            return data['data']
        else:
            print(f"🚨 Gagal mendapatkan data dari API. Pesan: {data.get('status')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Terjadi kesalahan saat membuat permintaan HTTP: {e}")
        return None
    except json.JSONDecodeError:
        print("❌ Gagal memproses respons JSON.")
        return None
        
def display_prayer_times(data):
    """
    Menampilkan data jadwal sholat dalam format tabel.
    
    Args:
        data (dict): Data jadwal sholat yang sudah diparsing.
    """
    
    if not data:
        print("Tidak ada data untuk ditampilkan.")
        return

    # Ambil data Waktu Sholat dan Tanggal
    timings = data['timings']
    date_info = data['date']
    
    city_name = input_city.title()
    country_name = input_country.title()

    # Data yang akan ditampilkan
    prayer_times = {
        "Subuh": timings.get('Fajr'),
        "Dzuhur": timings.get('Dhuhr'),
        "Ashar": timings.get('Asr'),
        "Maghrib": timings.get('Maghrib'),
        "Isya": timings.get('Isha'),
        # Tambahkan waktu lain jika diperlukan, contoh: Sunrise: timings.get('Sunrise')
    }

    # Persiapan data untuk tabel
    table_data = []
    # Urutan waktu sholat yang ingin ditampilkan
    prayer_order = ["Subuh", "Dzuhur", "Ashar", "Maghrib", "Isya"]
    
    for prayer in prayer_order:
        table_data.append([prayer, prayer_times.get(prayer, '-')])

    # 3. Menampilkan data dalam bentuk list / tabel
    print("\n" + "="*50)
    print(f"📅 JADWAL SHOLAT UNTUK KOTA {city_name}, {country_name}")
    print(f"   Tanggal Masehi: {date_info.get('readable')}")
    print(f"   Tanggal Hijriah: {date_info['hijri'].get('day')} {date_info['hijri'].get('month').get('en')} {date_info['hijri'].get('year')}")
    print("="*50)

    # Gunakan tabulate untuk membuat tabel yang rapi
    print(tabulate(table_data, headers=["Waktu Sholat", "Jam"], tablefmt="fancy_grid"))
    print("="*50 + "\n")


# --- Main Program ---
if __name__ == "__main__":
    print("🕌 Selamat Datang di Aplikasi Jadwal Sholat")
    print("------------------------------------------")

    # 1. Input nama kota dari user (Fitur Tambahan 1)
    input_city = input("Masukkan Nama Kota (contoh: Jakarta): ").strip()
    input_country = input("Masukkan Nama Negara (contoh: Indonesia): ").strip()
    
    if not input_city or not input_country:
        print("Kota dan Negara tidak boleh kosong. Program dihentikan.")
    else:
        # Ambil jadwal sholat untuk Hari Ini
        data_today = get_prayer_times(input_city, input_country, date_offset=0)
        display_prayer_times(data_today)
        
        # 2. Menampilkan jadwal sholat untuk hari berikutnya (Fitur Tambahan 2)
        # Fitur tambahan ini lebih baik daripada hanya menampilkan 1 spesifik data, 
        # karena memanggil endpoint dengan data yang berbeda (tanggal yang berbeda).
        
        print("\n--- Fitur Tambahan: Jadwal Sholat Hari Besok ---")
        data_tomorrow = get_prayer_times(input_city, input_country, date_offset=1)
        display_prayer_times(data_tomorrow)