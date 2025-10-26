#!/usr/bin/env python3
"""
Smart Parking Detection System - Simple HTTP Server
"""

import time
import gpiod
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import os

CHIP = "gpiochip0"
TRIG_PIN = 30
ECHO_PIN = 31

# Setup GPIO
chip = gpiod.Chip(CHIP)
trig = chip.get_line(TRIG_PIN)
echo = chip.get_line(ECHO_PIN)
trig.request(consumer="trig", type=gpiod.LINE_REQ_DIR_OUT)
echo.request(consumer="echo", type=gpiod.LINE_REQ_DIR_IN)

latest_distance = 0

def distance_cm():
    """Measure distance using HC-SR04"""
    trig.set_value(0)
    time.sleep(0.000002)
    trig.set_value(1)
    time.sleep(0.00001)
    trig.set_value(0)
    
    t0 = None
    t1 = None
    timeout_start = time.time()
    
    while echo.get_value() == 0:
        t0 = time.time()
        if time.time() - timeout_start > 0.1:
            return -1
    
    timeout_start = time.time()
    while echo.get_value() == 1:
        t1 = time.time()
        if time.time() - timeout_start > 0.1:
            return -1
    
    if t0 is None or t1 is None:
        return -1
    
    duration = t1 - t0
    return round(duration * 17150, 2)

def sensor_loop():
    """Continuously read sensor"""
    global latest_distance
    while True:
        d = distance_cm()
        if d > 0:
            latest_distance = d
        time.sleep(0.2)

class ParkingHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/data':
            # Send JSON distance data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = json.dumps({'distance': latest_distance})
            self.wfile.write(data.encode())
            return
        
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        # Suppress log messages
        pass

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    # Change to /www directory
    os.chdir('/www')
    
    # Start sensor reading in background
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()
    
    print("=" * 60)
    print("🚗 Smart Parking Detection System")
    print("=" * 60)
    print(f"Server running on http://0.0.0.0:8080")
    print(f"Access from your phone:")
    print(f"  Find your Ox64 IP address with: ip addr show bleth0")
    print(f"  Then open: http://<ox64-ip>:8080")
    print("=" * 60)
    
    server = ThreadedHTTPServer(('0.0.0.0', 8080), ParkingHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
