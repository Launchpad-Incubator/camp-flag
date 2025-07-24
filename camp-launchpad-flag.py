"""
FLAG CODE FOR CAMP LAUNCHPAD V0

- Connects to Raspberry Pi Pico W to control a servo motor.

Update notes: Init commit

Author: Aidan McMillan
"""

import keyboard
import socket
import requests
import time


# INSERT IP INFO HERE
PICO_IP = "10.10.20.82"

def send_command(command: str) -> None:
    url = f"http://{PICO_IP}/api?{command}"
    try:
        response = requests.get(url, timeout=10)
        print(f"Sent: {command} - Status: {response.status_code}")
    except Exception as e:
        print(f"Failed to send: {command} - Error: {e}")
    
def main():
    print("Initialized flag control. Press SPACE to move flag.")
    last_cmd = None

    while True:
        if keyboard.is_pressed('space'):
            move_cmd = "move"

        else:
            move_cmd = "hold"

        command = f"cmd={move_cmd}"

        if command != last_cmd:
            send_command(command)

        time.sleep(0.02)

main()
        