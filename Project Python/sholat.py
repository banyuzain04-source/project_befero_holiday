
import requests
# pip --version (cek versi pip terinstall)
# pip install requests (install requests jika belum ada)
target_url = "https://api.aladhan.com/v1/timingsByCity/09-12-2025?city=Jakarta&country=Indonesia&method=20"
print (f"target urlnya adalah {target_url}")

# HTTP GET request (ambil data dari url)
response = requests.get(target_url)
#  Konvesi data ke format JSON
data_json = response.json()
# print (f"response data: {data_json}")
print("Jadwal Sholat")
print("=" * 20)
jadwal = data_json["data"]["timings"]
shubuh = jadwal["Fajr"]
dzuhur = jadwal["Dhuhr"]
print (f"-Shubuh: {shubuh}")
print (f"-Dzuhur: {dzuhur}")
