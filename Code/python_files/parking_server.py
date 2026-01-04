#!/usr/bin/env python3
import time
import gpiod
import json
import os
import threading
import atexit
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

CHIP = "gpiochip0"
TRIG_PIN = 30
ECHO_PIN = 31
LED_RED_PIN = 15
LED_YELLOW_PIN = 12
LED_GREEN_PIN = 13

latest_distance = 999
running = True
led_red = None
led_yellow = None
led_green = None
last_print_distance = -1

def cleanup_leds():
    """Turn all LEDs OFF when script exits"""
    global led_red, led_yellow, led_green
    if led_red:
        led_red.set_value(0)
    if led_yellow:
        led_yellow.set_value(0)
    if led_green:
        led_green.set_value(0)
    print("✅ All LEDs turned OFF")

def setup_gpio():
    global led_red, led_yellow, led_green
    chip = gpiod.Chip(CHIP)

    trig = chip.get_line(TRIG_PIN)
    echo = chip.get_line(ECHO_PIN)
    trig.request(consumer="trig", type=gpiod.LINE_REQ_DIR_OUT)
    echo.request(consumer="echo", type=gpiod.LINE_REQ_DIR_IN)

    led_red = chip.get_line(LED_RED_PIN)
    led_yellow = chip.get_line(LED_YELLOW_PIN)
    led_green = chip.get_line(LED_GREEN_PIN)

    led_red.request(consumer="led_red", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    led_yellow.request(consumer="led_yellow", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    led_green.request(consumer="led_green", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

    led_red.set_value(0)
    led_yellow.set_value(0)
    led_green.set_value(0)

    atexit.register(cleanup_leds)

    return trig, echo, led_red, led_yellow, led_green

def measure_distance(trig, echo):
    trig.set_value(0)
    time.sleep(0.00001)
    trig.set_value(1)
    time.sleep(0.00001)
    trig.set_value(0)

    timeout = time.time() + 0.1
    while echo.get_value() == 0 and time.time() < timeout:
        pass
    if time.time() >= timeout:
        return -1

    start = time.time()
    timeout = time.time() + 0.1
    while echo.get_value() == 1 and time.time() < timeout:
        pass
    end = time.time()

    duration = end - start
    distance = duration * 17150
    return round(distance, 1)

def get_status(distance):
    if distance < 0:
        return "NO SIGNAL"
    elif distance <= 15:
        return "RED (0-15cm)"
    elif distance <= 25:
        return "YELLOW (16-25cm)"
    elif distance <= 45:
        return "GREEN (26-45cm)"
    else:
        return "FAR (>45cm)"

def update_leds(led_red, led_yellow, led_green, distance):
    led_red.set_value(0)
    led_yellow.set_value(0)
    led_green.set_value(0)

    if distance < 0:
        pass
    elif distance <= 15:
        led_red.set_value(1)
    elif distance <= 25:
        led_yellow.set_value(1)
    elif distance <= 45:
        led_green.set_value(1)

def print_live_update(distance):
    global last_print_distance
    if distance != last_print_distance and distance > 0:
        status = get_status(distance)
        print(f"📏 LIVE: {distance}cm - {status}")
        last_print_distance = distance

def sensor_loop(trig, echo, led_red, led_yellow, led_green):
    global latest_distance, running
    print("🔄 Sensor loop started - Live updates every motion...")
    while running:
        dist = measure_distance(trig, echo)
        if dist > 0:
            latest_distance = dist
            update_leds(led_red, led_yellow, led_green, dist)
            print_live_update(dist)
        time.sleep(0.2)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='/park_dect', **kwargs)

    def log_message(self, format, *args):
        """Disable all web logs"""
        pass

    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'distance': latest_distance}).encode())
            return
        if self.path == '/':
            self.path = '/index.html'
        super().do_GET()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    os.makedirs('/park_dect', exist_ok=True)
    trig, echo, led_red, led_yellow, led_green = setup_gpio()

    thread = threading.Thread(target=sensor_loop, args=(trig, echo, led_red, led_yellow, led_green))
    thread.daemon = True
    thread.start()

    server = ThreadedHTTPServer(('0.0.0.0', 8080), Handler)
    print("🚗 Ox64 Parking Server - http://0.0.0.0:8080")
    print("🎯 RANGES: RED=0-15cm | YELLOW=16-25cm | GREEN=26-45cm")
    print("📱 Web: http://172.20.10.2:8080")
    print("Ctrl+C to stop (ALL LEDs OFF)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        running = False
        cleanup_leds()
        server.shutdown()
        print("✅ Server stopped, all LEDs OFF")

