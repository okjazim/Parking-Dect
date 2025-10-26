# Initial Setup Guide (Work In Progress)

This document guides you through setting up the development environment for the **Parking Detection System on OX64**, from installing WSL to building your first Buildroot image.

## 1. Install WSL (Windows Subsystem for Linux)

1. Open **PowerShell** as Administrator.  
2. Run:
'''bash
wsl --install
'''
3. Restart your system if prompted.  
4. After reboot, open **Ubuntu** (or your chosen Linux distro) from the Start menu and complete the initial user setup.  
5. Update your package list:
'''bash
sudo apt update && sudo apt upgrade -y
'''

## 2. Install Development Dependencies

Run the following in your WSL terminal:
'''bash
sudo apt install -y git make gcc g++ libncurses5-dev libssl-dev bc wget unzip rsync cpio python3
'''

These are required for compiling Buildroot and working with GNU toolchains.

## 3. Clone Buildroot Repository

Clone the **Buildroot** source code (you can adjust version/tag as needed):
git clone https://git.busybox.net/buildroot
cd buildroot
git checkout 2025.11-git

text

If using a specific stable release, adjust the tag accordingly.

---

## 4. Prepare Project Directory

Keep Buildroot separate from custom project files for a clean setup:
mkdir -p ~/projects/ox64-setup
cd ~/projects/ox64-setup

text

You may later clone or link your OX64 project files here (e.g. configs, external trees, patches).

---

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
