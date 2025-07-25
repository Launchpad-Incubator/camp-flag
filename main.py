import network
import socket
import time
from machine import Pin, PWM

FLAG_PIN = 2
SSID = "IoT"
PASSWORD = "launchRob0t$"
UP_PULSE = 1200
DOWN_PULSE = 1500
LED = Pin("LED", Pin.OUT)
current_state = False
wlan = None
ip = None

def connect_wifi(ssid: str, password: str):
    """Connects to a Wi-Fi network.
    
    Args:
        ssid: Wi-Fi SSID
        password: Wi-Fi password
    
    Returns:
        IP address as a string
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        LED.toggle()
        time.sleep(0.25)
    
    LED.on()
    ip = wlan.ifconfig()[0]
    print(f"Connected. IP address: {ip}")
    return ip, wlan


def set_pulse(microseconds: int) -> None:
    """Sets a PWM duty cycle based on a pulse width.
        
    Args:
        microseconds: Duration of the high pulse in microseconds (1000-2000 typical).
    """
    duty = int(microseconds / 20000 * 65535)
    Self.pwm.duty_u16(duty)
def wifi_connect():
    while not wlan.isconnected():
        LED.toggle()
        time.sleep(0.25)

    LED.on()
    ip = wlan.ifconfig()[0]
    print(f"Connected to {SSID} IP address: {ip}")
    return ip, wlan


def handle_api_request():
    try:
        print(f"Incoming request: {request}")
        query = request.split('GET /api?')[1]
        if query == "move":
            current_state = not current_state
    except Exception as e:
        print("Parsing Error:", e)

def main() -> None:
    connect_wifi("Iot", "launchRob0t$")
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
                handle_api_request(request)
                cl.send("HTTP/1.1 204 No Content\r\n\r\n")
            else:
                cl.send("HTTP/1.1 404 Not Found\r\n\r\n")
        except Exception as e:
            print("Request error:", e)
        finally:
            cl.close()

            
main()