# Initial Setup Guide (Work In Progress)

This document guides you through setting up the development environment for the **Parking Detection System on OX64**, from installing WSL to building your first Buildroot image.

---

## 1. Install WSL (Windows Subsystem for Linux)

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

---

## 2. Install Development Dependencies

Install all required packages for Buildroot and development:
```bash
sudo apt install -y which sed make binutils build-essential diffutils gcc g++ bash patch gzip bzip2 perl tar cpio unzip rsync file bc findutils gawk wget python3 libncurses5-dev libncurses-dev qtbase5-dev libglib2.0-dev libgtk2.0-dev libglade2-dev git bzr curl cvs mercurial subversion default-jdk asciidoc w3m dblatex graphviz python3-matplotlib python3-aiohttp
```

---

## 3. Clone Buildroot Repositories

Create a workspace and clone Buildroot and Bouffalo repositories:
```bash
mkdir -p ~/ox64
cd ~/ox64
git clone https://github.com/buildroot/buildroot
git clone https://github.com/openbouffalo/buildroot_bouffalo
```

---

## 4. In Progress

## 5. Configure Buildroot for OX64

Use the provided defconfig or create your own configuration:
make ox64_defconfig

text

If you have a custom configuration file:
make configs/ox64_custom_defconfig

text

To adjust options via the interactive menu:
make menuconfig

text

Here you can:
- Enable or disable specific packages  
- Choose the toolchain or compiler options  
- Modify root filesystem contents  

---

## 6. Build the Image

Run:
make

text

Buildroot will automatically download, extract, compile, and assemble the entire embedded Linux system for the OX64 board.  
Compilation may take several minutes depending on your hardware.

If you encounter errors, verify toolchain accessibility:
echo $PATH
which make
which gcc

text

---

## 7. Locate Build Output

Once complete, the build artifacts will be found in:
output/images/

text

This directory typically contains:
- Bootloader binaries  
- Kernel image (`Image` or `zImage`)  
- Device Tree Blob (`.dtb`)  
- Root filesystem image (`rootfs.ext4` or similar)  

---

## 8. Next Steps

After generating the firmware images, the next phase involves integrating peripherals such as the **Raspberry Pi Pico 2** and **HC-SR04 ultrasonic sensor**, and preparing for flashing.
