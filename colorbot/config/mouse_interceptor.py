import socket
import time
import evdev
from evdev import InputDevice, categorize, ecodes

# virtual HID device file
HID_DEV = '/dev/hidg0'

# TCP server settings
HOST = ''  # accept connections from any IP address
PORT = 5005

# find the physical mouse input device on the pi
def find_mouse():
    devices = [InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if 'HID-compliant mouse' in device.name: 
            return device
    return None


def send_hid_report(report):
    with open(HID_DEV, 'wb+') as fd:
        fd.write(report)

# HID report
def create_hid_report(x, y, btn1=0):
    buttons = btn1 & 0x01  # Only LMB
    return bytes([buttons, x & 0xff, y & 0xff, 0])

# mouse forwarding and click interception
def handle_mouse_input(mouse, click_override=False):
    for event in mouse.read_loop():
        x_movement = y_movement = btn1 = 0

        # relative movements (X, Y) and button events
        if event.type == ecodes.EV_REL:
            if event.code == ecodes.REL_X:
                x_movement = event.value
            elif event.code == ecodes.REL_Y:
                y_movement = event.value

            # create HID report for movement
            report = create_hid_report(x_movement, y_movement)
            send_hid_report(report)

        elif event.type == ecodes.EV_KEY:
            # override button event if click_override is True
            if click_override:
                btn1 = 1
            else:
                if event.code == ecodes.BTN_LEFT:
                    btn1 = event.value  # 1 for press, 0 for release

            # send button press to host
            report = create_hid_report(0, 0, btn1)
            send_hid_report(report)

# TCP listener for receiving click override signal
def listen_for_override_signal():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print("Waiting for connection...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode()
                if data == "True":
                    print("Received click override signal")
                    return True
                else:
                    return False

def main():
    mouse = find_mouse()
    if mouse is None:
        print("Mouse not found")
        return

    print(f"Using mouse: {mouse.name}")

    # Loop to handle mouse input and listen for TCP override signal
    while True:
        click_override = listen_for_override_signal()  # Check if click override is enabled
        handle_mouse_input(mouse, click_override)      # Forward or intercept input based on override

if __name__ == "__main__":
    main()