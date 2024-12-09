
# ESP32 Setup Script

This project provides a convenient Bash script to prepare, flash, and set up an ESP32 board with MicroPython. It automates the process of erasing the flash, flashing MicroPython firmware, and transferring project files to the ESP32.

## Prerequisites

Before using the script, ensure the following are installed and accessible on your system:

1. **Python 3** and `pip`
   - Used to install tools like `esptool.py` and `rshell`.
2. **esptool.py**
   - For flashing firmware to the ESP32.
   - Install with:
     ```bash
     pip install esptool
     ```
3. **rshell**
   - For communicating with the ESP32 and transferring files.
   - Install with:
     ```bash
     pip install rshell
     ```

1. **Make the script executable**:
   ```bash
   chmod +x setup.sh
   ```

2. **Run the script**:
   ```bash
   # Make sure you run this from the esp32 directory!
   ./setup.sh
   ```

3. The script performs the following steps:
   - Erases the ESP32 flash memory.
   - Flashes the specified MicroPython firmware.
   - Connects to the ESP32 using `rshell`.
   - Copies all files from the `src/` directory to the ESP32.

## Configuration

### ESP32 Port
The default serial port for the ESP32 is `/dev/ttyUSB0`. If your ESP32 is connected to a different port, modify the `ESP_PORT` variable in the `setup.sh` script:

```bash
ESP_PORT="/dev/ttyUSB1"  # Update with your port
```

### Firmware File
Ensure the correct firmware file is placed in the `firmware/` directory and update the `FIRMWARE` variable in the script if necessary:

```bash
FIRMWARE="firmware/ESP32_GENERIC-20241129-v1.24.1.bin"
```

### Source Directory
The script copies all files from the `src/` directory to the ESP32. Update the `SRC_DIR` variable if your source files are located elsewhere:

```bash
SRC_DIR="src/*"
```

## Troubleshooting

### Permission Denied
If you encounter a "Permission denied" error when accessing the ESP32 serial port, ensure your user has access to the serial device:

```bash
sudo usermod -a -G dialout $USER
```

Then log out and back in for the changes to take effect.

### Missing Dependencies
Ensure that `esptool.py` and `rshell` are installed and in your system's PATH.

---
