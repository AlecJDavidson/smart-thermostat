#!/bin/bash

# Variables
ESP_PORT="/dev/ttyUSB0"
FIRMWARE="firmware/ESP32_GENERIC-20241129-v1.24.1.bin"
SRC_DIR="src/*"

# Step 1: Erase flash
echo "Erasing flash on ESP32..."
esptool.py --chip esp32 --port "$ESP_PORT" erase_flash
if [ $? -ne 0 ]; then
  echo "Failed to erase flash. Exiting."
  exit 1
fi

# Step 2: Flash MicroPython firmware
echo "Flashing MicroPython firmware..."
esptool.py --chip esp32 --port "$ESP_PORT" --baud 460800 write_flash -z 0x1000 "$FIRMWARE"
if [ $? -ne 0 ]; then
  echo "Failed to flash firmware. Exiting."
  exit 1
fi

# Step 3: Connect and mount the board
echo "Connecting to the ESP32 with rshell..."
rshell -p "$ESP_PORT" -b 115200 <<EOF
# Step 4: Copy files to the board
cp $SRC_DIR /pyboard
EOF

if [ $? -ne 0 ]; then
  echo "Failed to copy files to the board. Exiting."
  exit 1
fi

echo "ESP32 setup complete!"
