import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

# Ganti dengan URI MongoDB Anda
MONGO_URI = "mongodb+srv://mylodirgantara:JELPOT@cluster0.sq6kh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(MONGO_URI)
    db = client['data_collection']
    dht11_collection = db['dht11']
    ldr_collection = db['ldr']
    print("Koneksi ke MongoDB berhasil!")
except Exception as e:
    print("[ERROR] Gagal terhubung ke MongoDB:", e)

@app.route('/')
def index():
    return "Hello, World!"

# DHT11
@app.route('/kirim_data_dht', methods=['POST'])
def sensor1():
    data = request.get_json()
    if not data or 'temperature' not in data or 'humidity' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Temperature and humidity are required!'}), 400

    try:
        temperature = float(data['temperature'])
        kelembapan = float(data['humidity'])
    except ValueError:
        return jsonify({'error': 'Bad Request', 'message': 'Temperature and humidity must be numeric!'}), 400
    
    sensor_data = {
        'temperature': temperature,
        'kelembapan': kelembapan,
        'timestamp': datetime.utcnow() + timedelta(hours=7) 
    }

    result = dht11_collection.insert_one(sensor_data)  
    return jsonify({'message': 'DHT11 data inserted successfully!', 'id': str(result.inserted_id)}), 201

# LDR
@app.route('/kirim_data_ldr', methods=['POST'])
def send_ldr():
    data = request.get_json()
    if not data or 'light_value' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'light_value is required!'}), 400

    try:
        light_value = float(data['light_value'])  
    except ValueError:
        return jsonify({'error': 'Bad Request', 'message': 'light_value must be numeric!'}), 400
    
    sensor_data = {
        'light_value': light_value, 
        'timestamp': datetime.utcnow() + timedelta(hours=7)
    }

    result = ldr_collection.insert_one(sensor_data)  
    return jsonify({'message': 'LDR data inserted successfully!', 'id': str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
