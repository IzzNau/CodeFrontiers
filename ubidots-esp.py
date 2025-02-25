import network
import machine as m
import time
import urequests
import dht
from machine import Pin

# Konfigurasi WiFi
SSID = "SBSN"
PASSWORD = "*#aulaSBSN#"
sta_if = network.WLAN(network.STA_IF)

def connect_wifi():
    if sta_if.isconnected():
        sta_if.disconnect()
        time.sleep(1)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)

def checkwifi():
    connect_wifi()
    timeout = 10  # detik
    start_time = time.time()
    while not sta_if.isconnected():
        if time.time() - start_time > timeout:
            print("[ERROR] Gagal terhubung ke WiFi dalam waktu yang ditentukan.")
            return
        time.sleep(1)
        print("Menunggu koneksi WiFi...")
    print("Terhubung ke WiFi:", sta_if.ifconfig())

# API endpoints
API_BASE_URL = "http://192.168.229.59:5000"  # Ganti dengan alamat IP server Flask Anda
DHT11_ENDPOINT = f"{API_BASE_URL}/kirim_data"  # Endpoint untuk mengirim data DHT11 dan LDR

# Inisialisasi pin untuk DHT11
DHT_PIN = Pin(21)
dht_sensor = dht.DHT11(DHT_PIN)

# Inisialisasi pin untuk LDR
LDR_PIN = 34  # 
ldr_sensor = m.ADC(Pin(LDR_PIN))  # Inisialisasi ADC

def send_sensor_data(temperature, humidity, ldr_value):
    payload = {
        'temperature': temperature,
        'kelembapan': humidity,
        'cahaya': ldr_value 
    }
    
    try:
        req = urequests.post(DHT11_ENDPOINT, json=payload)
        print("Status Code:", req.status_code)
        print("Response:", req.json())
    except Exception as e:
        print("[ERROR] Gagal mengirim data:", e)

def main():
    checkwifi()  # Memeriksa koneksi WiFi
    while True:
        try:
            # Membaca data dari DHT11
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            print(f"Suhu: {temperature} C, Kelembapan: {humidity} %")  # Menampilkan data DHT
            
            # Membaca nilai dari LDR
            ldr_value = ldr_sensor.read()
            ldr_value_scaled = (ldr_value / 4095) * 100  
            print(f"Cahaya: {ldr_value_scaled:.2f}%")  # Menampilkan nilai LDR yang sudah diskalakan
            
            # Mengirim data ke server Flask
            send_sensor_data(temperature, humidity, ldr_value_scaled)  # Mengirim data DHT dan LDR
            
        except OSError as e:
            print("[ERROR] Gagal membaca sensor.")
        time.sleep(5)  # Kirim data setiap 5 detik

if _name_ == '_main_':
    main()  # Menjalankan fungsi utama
