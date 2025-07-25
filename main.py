import network
import socket
import time
from machine import Pin

FLAG_PIN = 2
SSID = "IoT"
PASSWORD = "launchRob0t$"
LED = Pin("LED", Pin.OUT)
current_state = [0, 0]
wlan = None
ip = None
request = None

def connect_wifi():
    global ip, wlan
    """Connects to a Wi-Fi network.
    
    Args:
        ssid: Wi-Fi SSID
        password: Wi-Fi password
    
    Returns:
        IP address as a string
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        LED.toggle()
        time.sleep(0.25)
    
    LED.on()
    ip = wlan.ifconfig()[0]
    print(f"Connected. IP address: {ip}")
    return ip, wlan

def handle_api_request():
    global current_state
    global request
    try:
        print(f"Incoming request: {request}")
        query = request.split('GET /api?')[1]
        if query == "all":
            current_state = [1,1]
        elif query == "right":
            current_state[1] = not current_state[1]
        elif query == "left":
            current_state[0] = not current_state[0]
    except Exception as e:
        print("Parsing Error:", e)

def main() -> None:
    global request
    ip = connect_wifi()[0]
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(1)
    print(f"Server listening on http://{ip}/api?cmd=...")
    while True:
        cl, addr = sock.accept()
        try:
            request = cl.recv(1024).decode()
            print("Request received:")
            print(request)
            if 'GET /api?' in request:
                handle_api_request()
                cl.send("HTTP/1.1 204 No Content\r\n\r\n")
            else:
                cl.send("HTTP/1.1 404 Not Found\r\n\r\n")
        except Exception as e:
            print("Request error:", e)
        finally:
            cl.close()

            
main()
