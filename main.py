import machine
import utime
import _thread
import urequests as requests
import json
import network

# Wi-Fi setup
SSID = "RedeCASD-H8I-110"
PASSWORD = "borarede"

# Initialize WLAN interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print(f"Connecting to Wi-Fi network: {SSID}...")

# Attempt to connect
wlan.connect(SSID, PASSWORD)

# Wait for connection
max_attempts = 10
attempts = 0
while not wlan.isconnected() and attempts < max_attempts:
    print(f"Waiting for connection... ({attempts+1}/{max_attempts})")
    utime.sleep(1)
    attempts += 1

if wlan.isconnected():
    print("Wi-Fi connected successfully!")
    print("IP address:", wlan.ifconfig()[0])
else:
    print("Failed to connect to Wi-Fi.")
    print("Current status:", wlan.status())

# Generator constants
NUM_MAGNETS = 2
CALC_PERIOD_S = 1
UA_PER_RPM = 100 # Non-reducted motors

global rpm
rpm = 0.0

# Backend data
LOCAL_IP = "192.168.10.110" # ipconfig getifaddr en0 
PORT = 3000
ENDPOINT = "/reading"
URL = "http://" + LOCAL_IP + ":" + str(PORT) + ENDPOINT

def requests_thread():
    global rpm
    while True:
        utime.sleep(1)
        current = rpm*UA_PER_RPM
        payload = {
            "value": float(current),
            "epoch": utime.time()
        }
        post_data = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}

        res = requests.post(URL, headers=headers, data = post_data)
        
        print(res.json()) # Requests not working

_thread.start_new_thread(requests_thread, ())

led = machine.Pin("LED", machine.Pin.OUT)

led_ext = machine.Pin(15, machine.Pin.OUT)

a0_pin = machine.Pin(6, machine.Pin.IN) # useless for now
d0_pin = machine.Pin(17, machine.Pin.IN)

while True:
    start_time = utime.time()
    rotations = 0
    signals = 0
    
    while utime.time() <= start_time + CALC_PERIOD_S:
        utime.sleep(0.01)
            
        if d0_pin.value() == 0:
            signals += 1
            led_ext.value(1)
        else:
            led_ext.value(0)
    
    rotations = signals / NUM_MAGNETS
    global rpm
    rpm = rotations / CALC_PERIOD_S
    print(rpm)
