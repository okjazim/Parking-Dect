# Parking-Dect (Work In Progress)

![Ox64_board](https://github.com/user-attachments/assets/95ccf921-083b-4a0c-8ff2-a3b6ef4544fe)

This project is a simple parking detection system built around the OX64. Peripheral devices such as the Raspberry Pi Pico 2  and the HC-SR04 ultrasonic sensor helps accurately detect the presence of vehicles in parking spaces are what have been integrated. Jumper wires are used to establish reliable connections between these components, ensuring efficient communication and operation. 

The system combines hardware interfacing and sensor data processing to provide a practical solution for automated parking management, utilizing the strengths of both the OX64 platform and the Raspberry Pi Pico 2 for enhanced control and flexibility.

This setup is for demonstrating embedded system applications in real-world scenarios.

## Features
- Object detection using HC-SR04 ultrasonic sensor
- Control and data processing on OX64 embedded platform
- Peripheral integration with Raspberry Pi Pico 2
- Simple wiring and hardware setup with jumper wires
- Modular design for easy adaptation and extension

## Hardware Components
- OX64 
- Raspberry Pi Pico 2
- HC-SR04 ultrasonic sensor
- Jumper wires for connections
- Micro Usb to Usb Type-C adapter
- Bread Board
- Power supply from Personal Computer
  
## Software Components
- Firmware for OX64 (OpenBouffalo)
- Firmware for Pico (Picoprobe)
- Build environment: Buildroot (version), toolchain details, etc.
- WSL 2 (Windows Subsystem for Linux)
- Terminal/Powershell
- PuTTY

## Instructions
1. Connect all the peripherals (Pico, Ox64,etc.) using jumper wires as per the wiring diagram in the docs folder.
2. Have them all attached on the breadboard
3. Flash the firmware for Pico.
4. Build the firmware for OX64 using the provided setup folder.
5. Flash the firmware onto a sd card on your PC.
6. Insert the card on the OX64
7. Power on the system and verify connections.
(not done)

## Usage
in progress

## Screenshots and Images
in progress

## Common Issues
in progress

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References
[Builroot Requirements](https://buildroot.org/downloads/manual/manual.html#requirement)

[OX64 Wiki](https://wiki.pine64.org/wiki/Ox64)
