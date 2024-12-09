import utime as time
import json
from network import WLAN, STA_IF

# Load Wi-Fi credentials
def load_wifi_credentials(filename="wifi_config.json"):
    try:
        with open(filename, "r") as file:
            config = json.load(file)
            return config.get("ssid"), config.get("password")
    except Exception as e:
        print("Error reading Wi-Fi configuration:", e)
        raise RuntimeError("Failed to load Wi-Fi credentials")


# Connect to Wi-Fi
def connect_wifi(ssid, password):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print(f"Connecting to Wi-Fi with SSID: {ssid}...")
    timeout = 30  # Timeout in seconds
    while not wlan.isconnected() and timeout > 0:
        print(f"Waiting for connection... {timeout}s remaining")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("Connected to Wi-Fi!")
        print("IP Address:", wlan.ifconfig()[0])
        return wlan.ifconfig()[0]
    else:
        print("Failed to connect to Wi-Fi. Please check your credentials.")
        raise RuntimeError("Wi-Fi connection failed")


