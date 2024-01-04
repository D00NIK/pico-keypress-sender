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

# Convert character to it's USB usage ID equivalent
# https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html
def char_to_keycode(c):
    c_num = ord(c)

    if (c >= 'a' and c <= 'z'):
        return c_num - ord('a') + 4
    if (c == '0'):
        return 0x27
    if (c >= '1' and c <= '9'):
        return c_num - ord('1') + 0x1E
    return False
 
while True:
    if supervisor.runtime.serial_bytes_available:
        val = input()[0]
        c = char_to_keycode(val)

        if val == '' or not c:
            print("ERROR! This character isn't supported yet")

        led.value = USE_LED and True
        keyboard.press(c)
        
        time.sleep(UNTIL_RELEASED)
        
        keyboard.release(c)
        led.value = False

        print("Pressed " + val)