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
    while not sta_if.isconnected():
        time.sleep(1)
        print("Menunggu koneksi WiFi...")
    print("Terhubung ke WiFi:", sta_if.ifconfig())

# API endpoints
API_BASE_URL = "http://192.168.43.14:5000" 
DHT11_ENDPOINT = f"{API_BASE_URL}/send_dht11"
LDR_ENDPOINT = f"{API_BASE_URL}/send_ldr"

# Inisialisasi pin untuk DHT11
DHT_PIN = Pin(21)
dht_sensor = dht.DHT11(DHT_PIN)

# Inisialisasi pin untuk LDR
LDR_PIN = Pin(34)  
ldr_sensor = m.ADC(Pin(LDR_PIN))  

def send_ldr_data(ldr_value):
    payload = {
        "light_value": ldr_value
    }
    
    print("Payload LDR yang akan dikirim:", payload)  
    
    try:
        req = urequests.post(LDR_ENDPOINT, json=payload)
        print("LDR Status Code:", req.status_code)
        if req.status_code == 200:
            print("LDR Response:", req.json())
        else:
            print("[ERROR] Gagal mengirim data LDR:", req.text)
    except Exception as e:
        print("[ERROR] Gagal mengirim data LDR:", e)

def send_dht_data(temperature, humidity):
    payload = {
        "temperature": temperature,
        "humidity": humidity
    }
    
    print("Payload DHT yang akan dikirim:", payload) 
    
    try:
        req = urequests.post(DHT11_ENDPOINT, json=payload)
        print("DHT Status Code:", req.status_code)
        if req.status_code == 200:
            print("DHT Response:", req.json())
        else:
            print("[ERROR] Gagal mengirim data DHT:", req.text)
    except Exception as e:
        print("[ERROR] Gagal mengirim data DHT:", e)
        
def main():
    checkwifi()  # Memeriksa koneksi WiFi
    while True:
        try:
            # Membaca nilai dari LDR
            ldr_value = ldr_sensor.read()  
            print(f"Light Value: {ldr_value}")  # Menampilkan nilai LDR
            send_ldr_data(ldr_value)  # Mengirim data LDR ke server Flask
            
            # Membaca data dari DHT11
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            print(f"Temperature: {temperature} C, Humidity: {humidity} %")  # Menampilkan data DHT
            send_dht_data(temperature, humidity)  # Mengirim data DHT ke server Flask
            
        except OSError as e:
            print("[ERROR] Gagal membaca sensor.")
        time.sleep(5)  # Kirim data setiap 5 detik

if __name__ == '__main__':
    main()  # Menjalankan fungsi utama
