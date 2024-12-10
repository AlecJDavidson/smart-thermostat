import machine
import utime as time
from api import rest_api 
from wifi import load_wifi_credentials, connect_wifi


# Main execution
def main():
    try:
        ssid, password = load_wifi_credentials()
        ip = connect_wifi(ssid, password)
        rest_api(ip)
    except Exception as e:
        print("Critical error:", e)
        machine.reset()

# Production
main()

# # Development Mode
# if __name__ == "__main__":
#     main()

