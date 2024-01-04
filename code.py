import time
import board
import digitalio
import usb_hid
import supervisor
 
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

USE_LED = True # Will flash when pressing
UNTIL_RELEASED = 0.1 # The time between pressing and releasing

# Initialise LED
if (USE_LED):
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

# Initialise Keyboard 
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard) 
 
while True:
    if supervisor.runtime.serial_bytes_available:
        # https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html
        val = input()[0]
        c = getattr(Keycode, val.upper())

        if val == '' or not c:
            print("ERROR! This character isn't supported yet")

        led.value = USE_LED and True
        keyboard.press(c)
        
        time.sleep(UNTIL_RELEASED)
        
        keyboard.release(c)
        led.value = False

        print("Pressed " + val)
