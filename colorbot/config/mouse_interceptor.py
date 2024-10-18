import os
import time
import evdev
from evdev import InputDevice, categorize, ecodes

# USB HID gadget device virtual mouse
HID_DEV = '/dev/hidg0'

# write to HID device file
def send_hid_report(report):
    with open(HID_DEV, 'wb+') as fd:
        fd.write(report)

# findthe physical mouse input device on pi
def find_mouse():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if 'HID-compliant mouse' in device.name: # verify with device manager
            return device
    return None

def create_hid_report(x, y, btn1=0, btn2=0, btn3=0):
    # HID report structure for a mouse: buttons, X, Y, wheel
    buttons = (btn1 << 0) | (btn2 << 1) | (btn3 << 2)
    return bytes([buttons, x & 0xff, y & 0xff, 0])

def main():
    mouse = find_mouse()
    if mouse is None:
        print("Mouse not found")
        return

    print(f"Using mouse: {mouse.name}")

    # read mouseevents with evdev
    for event in mouse.read_loop():
        if event.type == ecodes.EV_REL:
            if event.code == ecodes.REL_X:
                x_movement = event.value
            elif event.code == ecodes.REL_Y:
                y_movement = event.value
            else:
                x_movement = 0
                y_movement = 0

            # double sensitivity
            x_movement = x_movement * 2
            y_movement = y_movement * 2

            # create HID report
            report = create_hid_report(x_movement, y_movement)
            send_hid_report(report)

        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_LEFT:
                btn1 = event.value  # 1 for press, 0 for release
            elif event.code == ecodes.BTN_RIGHT:
                btn2 = event.value
            elif event.code == ecodes.BTN_MIDDLE:
                btn3 = event.value

            # send button press to host
            report = create_hid_report(0, 0, btn1, btn2, btn3)
            send_hid_report(report)

if __name__ == "__main__":
    main()