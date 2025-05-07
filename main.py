from machine import Pin, Timer
import urequests
import utime

# === CONFIGURATION ===
REFRESH_RATE_HZ = 10
NUM_MAGNETS = 4
# TODO: Check Pin attached to hall sensor
HALL_PIN = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO 15 with pull-up resistor TODO: Check pull-up

# === VARIABLES ===
pulse_count = 0
rpm = 0

# === INTERRUPT HANDLER ===
def on_hall_trigger(pin):
    global pulse_count
    pulse_count += 1

# === TIMER TO COMPUTE RPM EVERY SECOND ===
def calc_rpm(timer):
    global pulse_count, rpm
    rpm = (pulse_count / NUM_MAGNETS) * 60  # Convert to RPM
    pulse_count = 0
    print("RPM:", rpm)

def rpm_to_ma(rpm: int):
    # TODO: Implement
    pass

# TODO: Send data to server
# === SETUP ===
HALL_PIN.irq(trigger=Pin.IRQ_FALLING, handler=on_hall_trigger)  # Detect falling edge
rpm_timer = Timer()
rpm_timer.init(period=(1/REFRESH_RATE_HZ)*1000, mode=Timer.PERIODIC, callback=calc_rpm)

# === MAIN LOOP ===
while True:
    utime.sleep(1)  # Nothing needed here, logic runs via interrupts and timer
