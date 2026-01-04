#!/usr/bin/env python3
"""
HC-SR04 Distance Sensor with Color-Coded LED Indicators
Red (GPIO 15)    = Very Close (< 10 cm)
Yellow (GPIO 12) = Close (10-20 cm)
Green (GPIO 13)  = Far (20-30 cm)
All Off          = Very Far (> 30 cm)
"""

import time
import gpiod

CHIP = "gpiochip0"
TRIG_PIN = 30
ECHO_PIN = 31

# LED Pin Assignments
RED_LED = 15      # Very Close
YELLOW_LED = 12   # Close
GREEN_LED = 13    # Far

chip = gpiod.Chip(CHIP)
trig = chip.get_line(TRIG_PIN)
echo = chip.get_line(ECHO_PIN)

# Setup LEDs
red = chip.get_line(RED_LED)
yellow = chip.get_line(YELLOW_LED)
green = chip.get_line(GREEN_LED)

trig.request(consumer="trig", type=gpiod.LINE_REQ_DIR_OUT)
echo.request(consumer="echo", type=gpiod.LINE_REQ_DIR_IN)
red.request(consumer="red", type=gpiod.LINE_REQ_DIR_OUT)
yellow.request(consumer="yellow", type=gpiod.LINE_REQ_DIR_OUT)
green.request(consumer="green", type=gpiod.LINE_REQ_DIR_OUT)

def all_leds_off():
    """Turn off all LEDs"""
    red.set_value(0)
    yellow.set_value(0)
    green.set_value(0)

def set_led_by_distance(distance):
    """Control LEDs based on distance ranges"""
    all_leds_off()
    
    if distance < 10:
        # Very Close - RED
        red.set_value(1)
        return "🔴 VERY CLOSE"
    elif distance < 20:
        # Close - YELLOW
        yellow.set_value(1)
        return "🟡 CLOSE"
    elif distance < 30:
        # Far - GREEN
        green.set_value(1)
        return "🟢 FAR"
    else:
        # Very Far - All Off
        return "⚫ VERY FAR"

def distance_cm():
    """Measure distance using HC-SR04"""
    # Send trigger pulse
    trig.set_value(0)
    time.sleep(0.000002)
    trig.set_value(1)
    time.sleep(0.00001)
    trig.set_value(0)
    
    # Wait for echo to go HIGH
    t0 = None
    t1 = None
    timeout_start = time.time()
    
    while echo.get_value() == 0:
        t0 = time.time()
        if time.time() - timeout_start > 0.1:  # 100ms timeout
            return -1
    
    # Wait for echo to go LOW
    timeout_start = time.time()
    while echo.get_value() == 1:
        t1 = time.time()
        if time.time() - timeout_start > 0.1:  # 100ms timeout
            return -1
    
    # Check if we got valid readings
    if t0 is None or t1 is None:
        return -1
    
    # Calculate distance
    duration = t1 - t0
    return round(duration * 17150, 2)

# Main Program
print("=" * 60)
print("HC-SR04 Distance Sensor with Color-Coded LED Indicators")
print("=" * 60)
print(f"TRIG: GPIO {TRIG_PIN}")
print(f"ECHO: GPIO {ECHO_PIN}")
print()
print("LED Color Indicators:")
print(f"  🔴 RED (GPIO {RED_LED})    → VERY CLOSE (< 10 cm)")
print(f"  🟡 YELLOW (GPIO {YELLOW_LED}) → CLOSE (10-20 cm)")
print(f"  🟢 GREEN (GPIO {GREEN_LED})  → FAR (20-30 cm)")
print(f"  ⚫ ALL OFF         → VERY FAR (> 30 cm)")
print("=" * 60)
print("\nPress Ctrl+C to stop\n")

try:
    while True:
        d = distance_cm()
        
        if d < 0:
            print("⚠️  Measurement timeout")
            all_leds_off()
        else:
            status = set_led_by_distance(d)
            print(f"Distance: {d:6.2f} cm  →  {status}")
        
        time.sleep(0.2)
        
except KeyboardInterrupt:
    print("\n\n⏹️  Stopping sensor...")
    
finally:
    all_leds_off()
    trig.release()
    echo.release()
    red.release()
    yellow.release()
    green.release()
    chip.close()
    print("✅ Clean exit. All LEDs off, GPIO released.")

