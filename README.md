# **Parking Detection System on OX64 (Work In Progress)**

![Ox64\_board](https://github.com/user-attachments/assets/95ccf921-083b-4a0c-8ff2-a3b6ef4544fe)

The **Parking Detection System on OX64** is an embedded project that uses the **HC-SR04 ultrasonic sensor** to detect the presence of vehicles in a parking slot. The **Raspberry Pi Pico 2** acts as a **USB-to-UART sensor interface**, reading ultrasonic measurements and sending processed distance data directly to the **OX64** over UART.

This project demonstrates real-world embedded system concepts including sensor interfacing, microcontroller communication, Buildroot-based Linux development, and hardware bring-up.

---

# **Table of Contents**

* [Features](#features)
* [Project Structure](#project-structure)
* [System Architecture](#system-architecture)
* [Hardware Components](#hardware-components)
* [Software Components](#software-components)
* [Wiring Overview](#wiring-overview)
* [Initial Setup (WSL + Buildroot)](#initial-setup-wsl--buildroot)
* [Buildroot Configuration & Image Build](#buildroot-configuration--image-build)
* [Flashing & Booting OX64](#flashing--booting-ox64)
* [Usage](#usage)
* [Work In Progress Notes](#work-in-progress-notes)
* [Common Issues](#common-issues)
* [License](#license)
* [References](#references)

---

# **Features**

* **Vehicle detection** using HC-SR04 ultrasonic sensor
* **Pico 2 → UART → OX64 communication pathway**
* OX64 processes distance values sent from Pico
* Firmware and root filesystem built entirely from **Buildroot**
* Minimalist project structure for easy onboarding
* Python utilities for LED control, motion tests, and debugging
* Bash scripts for auto-login and PuTTY / serial automation
* Clean modular wiring using jumper wires & breadboard

---

# **Project Structure**

```
Parking-Dect/
├── Code/              # Python, Bash scripts, UART tools (WIP)
├── Diagrams/          # Wiring diagrams, block diagrams
├── Initial Setup/     # WSL, Buildroot, environment preparation
└── README.md          # Main documentation (this file)
```

---

# **System Architecture**

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

### **Sensor Flow**

1. Pico triggers HC-SR04
2. Pico measures echo and computes distance
3. Pico sends formatted data over UART → OX64
4. OX64 interprets distance → determines occupancy

---

# **Hardware Components**

* **OX64 board**
* **Raspberry Pi Pico 2** (used *exclusively* as a UART + sensor interface)
* **HC-SR04 Ultrasonic Sensor**
* Breadboard
* Jumper wires
* Micro-USB to USB-C adapter
* PC for flashing & serial monitoring

---

# **Software Components**

* **Buildroot Linux system** for OX64
* **OpenBouffalo** tooling
* **Pico firmware** as UART sensor adapter (Picoprobe or custom Python/C firmware)
* **Python utilities** for LED control, motion simulation, and debugging
* **Bash scripts** for Buildroot automation and PuTTY serial session handling
* Environment built under **WSL 2 (Ubuntu 24.04)**

---

# **Wiring Overview**

Complete diagram is located in:
**`/Diagrams/serial_connect.png`**

### **Pico → HC-SR04**

```
Pico GPIO (Trigger) → HC-SR04 TRIG
Pico GPIO (Echo)    → HC-SR04 ECHO
Pico 5V / VBUS      → HC-SR04 VCC
Pico GND            → HC-SR04 GND
```

### **Pico UART → OX64**

```
Pico TX → OX64 RX
Pico RX → OX64 TX
GND     → GND
```

---

# **Initial Setup (WSL + Buildroot)**

*(This section incorporates content from `Initial_Setup.md`.)*

## **1. Install WSL (Windows Subsystem for Linux)**

Check virtualization:

```powershell
systeminfo | find "Virtualization"
```

Enable features:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

Install Ubuntu 24.04:

```powershell
wsl --install -d Ubuntu-24.04
```

Update environment:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## **2. Install Development Dependencies**

```
sudo apt install -y which sed make binutils build-essential diffutils gcc g++ bash patch \
gzip bzip2 perl tar cpio unzip rsync file bc findutils gawk wget python3 \
libncurses5-dev libncurses-dev qtbase5-dev libglib2.0-dev libgtk2.0-dev \
libglade2-dev git bzr curl cvs mercurial subversion default-jdk asciidoc \
w3m dblatex graphviz python3-matplotlib python3-aiohttp
```

---

## **3. Clone Repositories**

```
mkdir -p ~/ox64
cd ~/ox64
git clone https://github.com/buildroot/buildroot
git clone https://github.com/openbouffalo/buildroot_bouffalo
```

---

# **Buildroot Configuration & Image Build**

## **5. Configure Buildroot**

Use provided OX64 defconfig:

```
make ox64_defconfig
```

For a custom config:

```
make configs/ox64_custom_defconfig
```

Interactive configuration:

```
make menuconfig
```

---

## **6. Build Image**

```
make
```

If issues occur:

```
echo $PATH
which make
which gcc
```

---

## **7. Build Output Location**

Build artifacts:

```
output/images/
```

Includes:

* Bootloaders
* Kernel (`Image`)
* DTB
* Root filesystem (`rootfs.ext4`, etc.)

---

# **Flashing & Booting OX64**

*(This portion will be expanded as firmware flashing steps mature.)*

Basic steps:

1. Format SD card (FAT32)
2. Copy Buildroot images into boot partition
3. Insert card into OX64
4. Connect via Pico UART → PuTTY (115200 baud)

---

# **Usage**

*(Work in progress — final usage instructions will be added as software stabilizes.)*

Current expectations:

* Pico gathers distance
* Pico sends UART stream:

  ```
  DIST: 23.4cm
  DIST: 24.1cm
  ```
* OX64 receives and interprets
* Python utilities test LEDs, motion, etc.

---

# **Work In Progress Notes**

Areas still under development:

* Parking detection logic
* Threshold calibration
* Python-side utilities
* Automated boot service
* LED and indicator behavior
* Data logging
* Real-time notification system
* Documentation for Python & Bash scripts

---

# **Common Issues**

| Problem                    | Likely Cause            | Fix                                     |
| -------------------------- | ----------------------- | --------------------------------------- |
| No serial output from Pico | Wrong firmware or cable | Reflash Pico, check dmesg               |
| OX64 not booting           | SD partitions incorrect | Reformat, ensure boot files are present |
| No UART data               | TX/RX swapped           | Reverse UART lines                      |
| HC-SR04 unstable           | Power noise             | Ensure stable 5V and proper ground      |
| Buildroot errors           | Missing packages        | Reinstall dependencies                  |

---

# **License**

This project is licensed under the **MIT License**.
See [`LICENSE`](LICENSE) for details.

---

# **References**

* Buildroot Manual
* [https://buildroot.org/downloads/manual/manual.html#requirement](https://buildroot.org/downloads/manual/manual.html#requirement)
* OX64 Wiki
* [https://wiki.pine64.org/wiki/Ox64](https://wiki.pine64.org/wiki/Ox64)
