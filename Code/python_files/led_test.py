#!/usr/bin/env python3
"""
LED test script for Ox64 using libgpiod
"""

import time
import gpiod

# The GPIO lines you want to test
LED_PINS = [15, 12, 13]

# Which GPIO chip to use
CHIP = "gpiochip0"

chip = gpiod.Chip(CHIP)

# Request each pin as output
lines = [chip.get_line(pin) for pin in LED_PINS]
for line in lines:
    line.request(consumer="led-test", type=gpiod.LINE_REQ_DIR_OUT)

print("\nTesting LEDs on GPIO pins:", LED_PINS)
print("Press Ctrl+C to stop.\n")

try:
    # Blink each LED separately
    for index, line in enumerate(lines):
        print(f"Testing GPIO {LED_PINS[index]}")
        for i in range(5):
            line.set_value(1)
            print(f"  GPIO {LED_PINS[index]} ON")
            time.sleep(0.5)
            line.set_value(0)
            print(f"  GPIO {LED_PINS[index]} OFF")
            time.sleep(0.5)
        print()

    # Blink all together
    print("Blinking all LEDs together...\n")
    for _ in range(5):
        for line in lines:
            line.set_value(1)
        time.sleep(0.5)
        for line in lines:
            line.set_value(0)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nLED test stopped by user.")

finally:
    for line in lines:
        line.set_value(0)
        line.release()
    chip.close()
    print("\nGPIO cleanup done. All LEDs off.")
