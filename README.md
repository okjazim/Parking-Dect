# **Parking Dect**

![Ox64\_board](https://github.com/user-attachments/assets/95ccf921-083b-4a0c-8ff2-a3b6ef4544fe)

The **Parking Detection System on OX64** is an embedded project that uses the **HC-SR04 ultrasonic sensor** to detect the presence of vehicles in a parking slot. The **Raspberry Pi Pico 2** acts as a **USB-to-UART sensor interface**, reading ultrasonic measurements and sending processed distance data directly to the **OX64** over UART.

This project demonstrates real-world embedded system concepts including sensor interfacing, microcontroller communication, Buildroot-based Linux development, and hardware bring-up.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [File Structure](#file-structure)
- [Contribution](#contribution)
- [Important Note](#important-note)
- [License](#license)
- [References](#references)

---

## Tech Stack

### Hardware
- **OX64 board** - Main processing unit
- **Raspberry Pi Pico 2** - UART sensor interface
- **HC-SR04 Ultrasonic Sensor** - Vehicle detection
- Breadboard and jumper wires for prototyping

### Software
- **Buildroot Linux system** - Embedded Linux distribution for OX64
- **OpenBouffalo** - Firmware development tools
- **Python** - Utilities for LED control, motion tests, and debugging
- **Bash scripts** - Buildroot automation and serial session handling
- **WSL 2 (Ubuntu 24.04)** - Development environment

---

## Features

* **Vehicle detection** using HC-SR04 ultrasonic sensor
* **Pico 2 → UART → OX64 communication pathway**
* OX64 processes distance values sent from Pico
* Firmware and root filesystem built entirely from **Buildroot**
* Minimalist project structure for easy onboarding
* Python utilities for LED control, motion tests, and debugging
* Bash scripts for auto-login and PuTTY / serial automation
* Clean modular wiring using jumper wires & breadboard

---

## Setup Instructions

This guide walks you through setting up the development environment for the **Parking Detection System on OX64**, from installing WSL to building your first Buildroot image.

### 1. Install WSL (Windows Subsystem for Linux)

Before installation, make sure your system meets these requirements:
- OS: Windows 10 (version 21H2+) or Windows 11 (recommended)
- Virtualization: Must be enabled in BIOS/UEFI
- PowerShell Access: Run commands as Administrator

Open PowerShell as Administrator, then verify virtualization:

```bash
systeminfo | find "Virtualization"
```

If virtualization or WSL are not enabled, run this in PowerShell:

```bash
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

Reboot your system if prompted.

Then install Ubuntu 24.04 with:

```bash
wsl --install -d Ubuntu-24.04
```

Restart your system again if needed.

After reboot, launch Ubuntu from Start Menu, create your UNIX username and password, and update packages:

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Development Dependencies

Install all required packages for Buildroot and development:

```bash
sudo apt install -y which sed make binutils build-essential diffutils gcc g++ bash patch gzip bzip2 perl tar cpio unzip rsync file bc findutils gawk wget python3 libncurses5-dev libncurses-dev qtbase5-dev libglib2.0-dev libgtk2.0-dev libglade2-dev git bzr curl cvs mercurial subversion default-jdk asciidoc w3m dblatex graphviz python3-matplotlib python3-aiohttp
```

### 3. Clone Buildroot Repositories

Create a workspace and clone Buildroot and Bouffalo repositories:

```bash
mkdir -p ~/ox64
cd ~/ox64
git clone https://github.com/buildroot/buildroot
git clone https://github.com/openbouffalo/buildroot_bouffalo
```

### 4. Configure Buildroot for OX64

Use the provided defconfig or create your own configuration:

```bash
make ox64_defconfig
```

If you have a custom configuration file:

```bash
make configs/ox64_custom_defconfig
```

To adjust options via the interactive menu:

```bash
make menuconfig
```

Here you can:
- Enable or disable specific packages
- Choose the toolchain or compiler options
- Modify root filesystem contents

### 5. Build the Image

Run:

```bash
make
```

Buildroot will automatically download, extract, compile, and assemble the entire embedded Linux system for the OX64 board. Compilation may take several minutes depending on your hardware.

If you encounter errors, verify toolchain accessibility:

```bash
echo $PATH
which make
which gcc
```

### 6. Locate Build Output

Once complete, the build artifacts will be found in:

```
output/images/
```

This directory typically contains:
- Bootloader binaries
- Kernel image (`Image` or `zImage`)
- Device Tree Blob (`.dtb`)
- Root filesystem image (`rootfs.ext4` or similar)

### 7. Flashing

Flash the built Buildroot image to the OX64 using balenaEtcher:

1. Download and install [balenaEtcher](https://www.balena.io/etcher/)
2. Insert an SD card into your computer
3. Open balenaEtcher and select the built image file (`output/images/sdcard.img`)
4. Select your target SD card
5. Click "Flash" and wait for the process to complete
6. Safely eject the SD card and insert it into the OX64 board

---

## Usage

To use the Parking Detection System:

1. **Start the listener script**: Run `listener.py` in the background on your laptop/PC that is connected to the same network as the OX64 board.

2. **Connect via PuTTY**: Open PuTTY and connect with the correct baud rate (2000000) and COM port assigned to the OX64 (you can check the assigned COM port using Device Manager).

3. **Automatic boot sequence**: The initialization scripts will automatically run during the OX64 boot sequence.

4. **Access the web interface**: The webpage will automatically open in your default browser, providing a graphical interface for monitoring the parking detection system.

The system will display real-time parking slot occupancy data, with the HC-SR04 ultrasonic sensor measuring distances and the Pico 2 relaying data to the OX64 for processing.

---

## Screenshots

### Web Interface Overview

The system includes a responsive web interface that automatically opens in the default browser upon system startup. The web interface provides real-time monitoring and visualization of the parking detection system.

### Light Theme
![Light Theme](assests/Screenshot%20(130).png)

The light theme offers a clean, bright interface suitable for well-lit environments, displaying parking slot status, distance measurements, and system diagnostics.

### Dark Theme
![Dark Theme](assests/image.png)

The dark theme provides an eye-friendly alternative for low-light conditions or extended monitoring sessions, featuring the same comprehensive data display with reduced screen glare.

### Frontend Features

- **Real-time Status Display**: Live parking slot occupancy indicators
- **Distance Measurements**: Continuous ultrasonic sensor readings from HC-SR04
- **Theme Switching**: Automatic or manual light/dark theme selection
- **Responsive Design**: Optimized for various screen sizes and devices
- **System Diagnostics**: Connection status and sensor health monitoring
- **Historical Data**: Optional logging and trend visualization
---

## File Structure

```
Parking-Dect/
├── assests/           # Screenshots and images for documentation
│   ├── image.png          # Dark theme screenshot
│   └── Screenshot (130).png # Light theme screenshot
├── Code/              # Main application code
│   ├── python_files/      # Python utilities and server
│   │   ├── led_test.py        # LED testing utilities
│   │   ├── listener.py        # Network listener for sensor data
│   │   ├── motion.py          # Motion detection scripts
│   │   └── parking_server.py # Main parking detection server
│   └── webpage/          # Web interface files
│       ├── index.html        # Main web page
│       ├── script.js         # Frontend JavaScript
│       └── styles.css        # CSS styling
├── Diagrams/          # Wiring diagrams and documentation
│   ├── Ox64_pinout.png   # OX64 board pinout diagram
│   ├── pin_pic3.webp     # Additional pin diagrams
│   └── serial_connect.png # Serial connection diagram
├── Init Scripts/      # System initialization scripts
│   ├── S40wifi_connect    # WiFi connection setup
│   └── S50parking_server # Parking server startup
├── LICENSE            # Project license file
└── README.md          # Main documentation (this file)
```

---

## Contribution

We welcome contributions to the Parking Detection System! Here's how you can help:

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature-name`
7. Submit a pull request

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python code and consistent formatting for other languages
- **Documentation**: Update documentation for any new features or changes
- **Testing**: Test your changes on actual hardware when possible
- **Commits**: Write clear, descriptive commit messages

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Ensure all tests pass and code lints without errors
3. Request review from maintainers
4. Address any feedback from reviewers

### Reporting Issues

- Use GitHub Issues to report bugs
- Include detailed steps to reproduce the issue
- Provide system information and hardware details
- Suggest potential solutions if possible

### Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

---

## Important Note

### Common Issues

| Problem                    | Likely Cause            | Fix                                     |
| -------------------------- | ----------------------- | --------------------------------------- |
| No serial output from Pico | Wrong firmware or cable | Reflash Pico, check dmesg               |
| OX64 not booting           | SD partitions incorrect | Reformat, ensure boot files are present |
| No UART data               | TX/RX swapped           | Reverse UART lines                      |
| HC-SR04 unstable           | Power noise             | Ensure stable 5V and proper ground      |
| Buildroot errors           | Missing packages        | Reinstall dependencies                  |

### System Architecture

```
        USB                     UART                       GPIO
+------------------+   +-----------------------+   +---------------------------+
|     PC Host      |   | Raspberry Pi Pico 2   |   | HC-SR04 Ultrasonic Sensor |
| (WSL Buildroot)  |   | (UART Sensor Bridge)  |   +---------------------------+
+------------------+   | - Reads HC-SR04       |
                       | - Computes distance   |
                       | - Sends data to OX64  |
                       +-----------v-----------+
                                   | UART
                                   v
                           +------------------+
                           |      OX64        |
                           | Parses distance  |
                           | Parking logic    |
                           +------------------+
```

### Sensor Flow

1. Pico triggers HC-SR04
2. Pico measures echo and computes distance
3. Pico sends formatted data over UART → OX64
4. OX64 interprets distance → determines occupancy

### Wiring Overview

Complete diagram is located in:
**`/Diagrams/serial_connect.png`**

#### Pico → HC-SR04

```
Pico GPIO (Trigger) → HC-SR04 TRIG
Pico GPIO (Echo)    → HC-SR04 ECHO
Pico 5V / VBUS      → HC-SR04 VCC
Pico GND            → HC-SR04 GND
```

#### Pico UART → OX64

```
Pico TX → OX64 RX
Pico RX → OX64 TX
GND     → GND
```

---

## License

This project is licensed under the **MIT License**.
See [`LICENSE`](LICENSE) for details.

---

## References

* Buildroot Manual: [https://buildroot.org/downloads/manual/manual.html#requirement](https://buildroot.org/downloads/manual/manual.html#requirement)
* OX64 Wiki: [https://wiki.pine64.org/wiki/Ox64](https://wiki.pine64.org/wiki/Ox64)
