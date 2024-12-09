import socket
import json
import utime as time
from local_dht import get_temp, get_humidity
import machine
from relay import Relay


# Initialize relays
heat_relay = Relay(33)
cool_relay = Relay(25)
fan_relay = Relay(27)

# Default settings
temperature_unit = "F"  # 'F' for Fahrenheit, 'C' for Celsius
default_temperature = 68
current_temperature = None
current_humidity = None
mode = "off"  # "heat", "cool", or "off"


# Read temperature from DHT11
def read_temperature():
    global current_temperature
    try:
        temp_c = get_temp() 
        temp_f = temp_c * 9 / 5 + 32
        current_temperature = temp_f if temperature_unit == "F" else temp_c
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

        if mode == "heat":
            if current_temperature < default_temperature:
                print(f"Heating: Turning on heat relay. Current temp: {current_temperature}°{temperature_unit}")
                heat_relay.on()
                fan_relay.on()
            else:
                print(f"Heating: Current temp ({current_temperature}°{temperature_unit}) >= set temp ({default_temperature}°{temperature_unit}). Turning off heat relay.")
                heat_relay.off()
                fan_relay.off()

        elif mode == "cool":
            if current_temperature > default_temperature:
                print(f"Cooling: Turning on cool relay. Current temp: {current_temperature}°{temperature_unit}")
                cool_relay.on()
                fan_relay.on()
            else:
                print(f"Cooling: Current temp ({current_temperature}°{temperature_unit}) <= set temp ({default_temperature}°{temperature_unit}). Turning off cool relay.")
                cool_relay.off()
                fan_relay.off()

        elif mode == "off":
            print("System is off. Turning off all relays.")
            heat_relay.off()
            cool_relay.off()
            fan_relay.off()
    except Exception as e:
        print("Error updating relays:", e)


# Handle API requests
def handle_request(request):
    global temperature_unit, default_temperature, mode

    try:
        print(f"Received request: {request}")

        if not request:
            return {"error": "Empty request"}

        if request.startswith("/api/status"):
            return {"status": "hello! Server is running!"}

        if request.startswith("/api/heat/"):
            temp_value = int(request.split("/api/heat/")[-1])
            mode = "heat"
            default_temperature = temp_value
            return {"mode": "heat", "set_temperature": temp_value}

        elif request.startswith("/api/cool/"):
            temp_value = int(request.split("/api/cool/")[-1])
            mode = "cool"
            default_temperature = temp_value
            return {"mode": "cool", "set_temperature": temp_value}

        elif request.startswith("/api/off"):
            mode = "off"
            return {"mode": "off", "set_temperature": None}

        elif request.startswith("/api/relay/test"):
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
            return {"test": "success"}

        elif request.startswith("/api/temp"):
            temp = read_temperature()
            if temp is not None:
                return {"temperature": temp, "unit": temperature_unit}
            return {"error": "Temperature reading failed"}

        elif request.startswith("/api/humidity"):
            hum = read_humidity()
            if hum is not None:
                return {"humidity": hum}
            return {"error": "Humidity reading failed"}

        elif request.startswith("/api/unit/f"):
            temperature_unit = "F"
            return {"unit": "F"}

        elif request.startswith("/api/unit/c"):
            temperature_unit = "C"
            return {"unit": "C"}

        elif request.startswith("/api/default/"):
            temp_value = int(request.split("/api/default/")[-1])
            default_temperature = temp_value
            return {"default_temperature": default_temperature}

        else:
            return {"error": "Invalid endpoint"}
    except Exception as e:
        print("Error handling request:", e)
        return {"error": str(e)}


# Web server with periodic temperature logging and relay updates
def web_server(ip_address):
    try:
        addr = socket.getaddrinfo(ip_address, 80)[0][-1]
        server = socket.socket()
        server.bind(addr)
        server.listen(1)
        print(f"Web server running on http://{ip_address}:80")

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
