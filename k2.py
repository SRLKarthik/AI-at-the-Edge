#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
from sense_hat import SenseHat
import threading
import tkinter as tk
from tkinter import ttk

# Initialize Sense HAT
sense = SenseHat()

# Threshold values for energy-saving recommendations
TEMP_THRESHOLD = 22  # Temperature in Celsius
HUMIDITY_THRESHOLD = 60  # Humidity percentage

# Data log storage
data_log = []

# Function to get sensor data from Sense HAT
def get_sensor_data():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    # Package the data in a dictionary
    data = {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'timestamp': timestamp
    }
    return data

# Function to evaluate recommendations based on sensor data
def get_recommendations(data):
    recommendations = []
    if data['temperature'] > TEMP_THRESHOLD:
        recommendations.append("Reduce heating, temperature exceeds 22°C.")
    if data['humidity'] > HUMIDITY_THRESHOLD:
        recommendations.append("Consider using a dehumidifier, humidity is above 60%.")
    return recommendations

# Function to log data
def log_data(data):
    data_log.append(data)
    if len(data_log) > 100:  # Keep log size manageable
        data_log.pop(0)

# Function to periodically fetch and process sensor data
def run_system():
    while True:
        data = get_sensor_data()
        recommendations = get_recommendations(data)
        log_data(data)
        update_ui(data, recommendations)
        time.sleep(5)

# Function to update UI with sensor data and recommendations
def update_ui(data, recommendations):
    # Update sensor data
    temp_label['text'] = f"Temperature: {data['temperature']:.2f} °C"
    humidity_label['text'] = f"Humidity: {data['humidity']:.2f} %"
    pressure_label['text'] = f"Pressure: {data['pressure']:.2f} hPa"
    timestamp_label['text'] = f"Timestamp: {data['timestamp']}"
    
    # Update recommendations
    recommendations_text.set('\n'.join(recommendations))

# Create the Tkinter GUI
root = tk.Tk()
root.title("Sense HAT Monitoring System")

# Create UI elements
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

temp_label = ttk.Label(frame, text="Temperature: -- °C", font=("Helvetica", 14))
temp_label.grid(row=0, column=0, sticky=tk.W)

humidity_label = ttk.Label(frame, text="Humidity: -- %", font=("Helvetica", 14))
humidity_label.grid(row=1, column=0, sticky=tk.W)

pressure_label = ttk.Label(frame, text="Pressure: -- hPa", font=("Helvetica", 14))
pressure_label.grid(row=2, column=0, sticky=tk.W)

timestamp_label = ttk.Label(frame, text="Timestamp: --", font=("Helvetica", 12))
timestamp_label.grid(row=3, column=0, sticky=tk.W)

recommendations_label = ttk.Label(frame, text="Recommendations:", font=("Helvetica", 14, "bold"))
recommendations_label.grid(row=4, column=0, sticky=tk.W, pady=(10, 0))

recommendations_text = tk.StringVar()
recommendations_value = ttk.Label(frame, textvariable=recommendations_text, font=("Helvetica", 12), wraplength=400)
recommendations_value.grid(row=5, column=0, sticky=tk.W)

# Start the background monitoring thread
monitoring_thread = threading.Thread(target=run_system)
monitoring_thread.daemon = True
monitoring_thread.start()

# Run the Tkinter event loop
try:
    root.mainloop()
except KeyboardInterrupt:
    print("System interrupted by user")

