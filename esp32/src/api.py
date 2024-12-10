import socket
import json
import utime as time
from local_dht import get_temp, get_humidity
import machine
from relay import Relay
from settings import (
    heat_relay_pin,
    cool_relay_pin,
    fan_relay_pin,
    default_temperature_unit,
    default_temperature,
    default_dht11_offset,
)

# Initialize relays
heat_relay = Relay(heat_relay_pin)
cool_relay = Relay(cool_relay_pin)
fan_relay = Relay(fan_relay_pin)

# Default settings
temperature_unit = default_temperature_unit  # 'F' for Fahrenheit, 'C' for Celsius
default_temperature = default_temperature
current_temperature = None
dht11_offset = default_dht11_offset
current_humidity = None
mode = "off"  # "heat", "cool", or "off"


# Read temperature from DHT11
def read_temperature():
    global current_temperature
    global dht11_offset
    try:
        temp_c = get_temp()
        temp_f = temp_c * 9 / 5 + 32
        current_temperature = (
            temp_f + dht11_offset if temperature_unit == "F" else temp_c
        )
        return current_temperature
    except Exception as e:
        print("Error reading DHT11:", e)
        return None


def read_humidity():
    global current_humidity
    try:
        humidity = get_humidity()
        current_humidity = humidity
        return current_humidity
    except Exception as e:
        print("Error reading DHT11:", e)
        return None


# System test
def system_test():
    global default_temperature, mode, dht11_offset

    test_results = {
        "temperature": read_temperature(),
        "humidity": read_humidity(),
        "unit": temperature_unit,
        "default_temperature": default_temperature,
        "current_mode": mode,
        "dht11_offset": dht11_offset,
    }

    # Test relays
    try:
        heat_relay.on()
        time.sleep(1)
        heat_relay.off()
        time.sleep(1)
        cool_relay.on()
        time.sleep(1)
        cool_relay.off()
        time.sleep(1)
        fan_relay.on()
        time.sleep(1)
        fan_relay.off()
        test_results["relays"] = "success"
    except Exception as e:
        test_results["relays"] = f"failed: {str(e)}"

    return test_results


# Automatically update relay states based on mode and temperature
def update_relay():
    global current_temperature, default_temperature, mode

    try:
        if current_temperature is None:
            print("No valid temperature reading. Relays will remain off.")
            heat_relay.off()
            cool_relay.off()
            fan_relay.off()
            return

        if mode == "heat" and current_temperature < default_temperature:
            heat_relay.on()
            fan_relay.on()
            cool_relay.off()
        elif mode == "cool" and current_temperature > default_temperature:
            cool_relay.on()
            fan_relay.on()
            heat_relay.off()
        else:
            heat_relay.off()
            cool_relay.off()
            fan_relay.off()

        if mode == "off":
            heat_relay.off()
            cool_relay.off()
            fan_relay.off()

    except Exception as e:
        print("Error updating relays:", e)


# Handle API requests
def handle_request(request):
    global temperature_unit, default_temperature, mode, dht11_offset

    try:
        print(f"Received request: {request}")

        if not request:
            return {"status": 400, "error": "Empty request"}

        # System Status
        if request.startswith("/api/system/status"):
            return {
                "status": 200,
                "temperature": read_temperature(),
                "humidity": read_humidity(),
                "unit": temperature_unit,
                "default_temperature": default_temperature,
                "current_mode": mode,
                "dht11_offset": dht11_offset,
            }

        # Temperature Controls
        elif request.startswith("/api/control/heat/"):
            temp_value = int(request.split("/api/control/heat/")[-1])
            mode = "heat"
            default_temperature = temp_value
            return {
                "status": 200,
                "mode": "heat",
                "set_temperature": temp_value,
            }

        elif request.startswith("/api/control/cool/"):
            temp_value = int(request.split("/api/control/cool/")[-1])
            mode = "cool"
            default_temperature = temp_value
            return {
                "status": 200,
                "mode": "cool",
                "set_temperature": temp_value,
            }

        # DHT11 Offset
        elif request.startswith("/api/system/set_dht11_offset/"):
            dht11_offset = int(request.split("/api/system/set_dht11_offset/")[-1])
            return {
                "status": 200,
                "message": "DHT11 offset updated successfully",
                "dht11_offset": dht11_offset,
            }

        elif request.startswith("/api/system/read_dht11_offset/"):
            return {
                "status": 200,
                "dht11_offset": dht11_offset,
            }

        # System Modes
        elif request.startswith("/api/system/off"):
            mode = "off"
            return {
                "status": 200,
                "mode": "off",
                "set_temperature": None,
            }

        elif request.startswith("/api/system/test"):
            system_test()
            return {
                "status": 200,
                "message": "System test initiated",
            }

        elif request.startswith("/api/system/restart"):
            mode = "off"
            machine.reset()
            return {
                "status": 200,
                "message": "System restarting...",
            }

        # Status Queries
        elif request.startswith("/api/status/temp"):
            temp = read_temperature()
            if temp is not None:
                return {
                    "status": 200,
                    "temperature": temp,
                    "unit": temperature_unit,
                }
            return {"status": 500, "error": "Temperature reading failed"}

        elif request.startswith("/api/status/humidity"):
            hum = read_humidity()
            if hum is not None:
                return {
                    "status": 200,
                    "humidity": hum,
                }
            return {"status": 500, "error": "Humidity reading failed"}

        # Set Unit
        elif request.startswith("/api/system/unit/"):
            unit_value = request.split("/api/system/unit/")[-1].lower()
            if unit_value in ["f", "c"]:
                temperature_unit = unit_value.upper()
                return {
                    "status": 200,
                    "unit": temperature_unit,
                    "message": f"Temperature unit set to {temperature_unit}",
                }
            else:
                return {
                    "status": 400,
                    "error": "Invalid unit. Use 'f' for Fahrenheit or 'c' for Celsius.",
                }

        # Default Temperature
        elif request.startswith("/api/system/set_default_temp/"):
            temp_value = int(request.split("/api/system/set_default_temp/")[-1])
            default_temperature = temp_value
            return {
                "status": 200,
                "default_temperature": default_temperature,
            }

        # Invalid Endpoint
        else:
            return {"status": 404, "error": "Invalid endpoint"}

    except Exception as e:
        print("Error handling request:", e)
        return {"status": 500, "error": str(e)}


# API with periodic temperature logging and relay updates
def rest_api(ip_address):
    try:
        addr = socket.getaddrinfo(ip_address, 80)[0][-1]
        server = socket.socket()
        server.bind(addr)
        server.listen(1)
        print(f"Thermostat API running on http://{ip_address}:80")

        last_temp_log = time.ticks_ms()

        while True:
            # Log temperature and update relays every 5 seconds
            if time.ticks_diff(time.ticks_ms(), last_temp_log) >= 5000:
                temp = read_temperature()
                if temp is not None:
                    print(f"Current Temperature: {temp}°{temperature_unit}")
                update_relay()
                last_temp_log = time.ticks_ms()

            # Handle client requests
            cl, addr = server.accept()
            print(f"Client connected: {addr}")

            request = cl.recv(1024).decode()
            if not request:
                print("Empty request received")
                cl.close()
                continue

            path = request.split(" ")[1].strip()
            print(f"Processing path: {path}")
            response = handle_request(path)

            cl.send("HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
            cl.send(json.dumps(response))
            cl.close()
    except Exception as e:
        print("Error in web server:", e)
        machine.reset()
