import dxcam
import numpy as np

import keyboard
import win32api
import sys
from ctypes import WinDLL
import serial

import time
import random



user32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

# config - link w/ userinput GUI or .json

hz = 120

zone = 5

r, g, b = (250, 100, 250) # trigger color
margin = 70 # for trigger mask

trigger_toggle = False # switch between toggle and hold modes for trigger.py
trigger_hotkey = int("0x12",16) # alt key

quit_key = 'q' # keybind for quitting program


# setup

shcore.SetProcessDpiAwareness(2)
xres, yres = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

region = ((xres//2)-zone, (yres//2)-zone, (xres//2)+zone, (yres//2)+zone)


# initalization

camera = dxcam.create(output_color='RGB', max_buffer_len=64)
camera.start(region=region, target_fps=hz)

def shut_down():  # shutdown for compiling to exe
    try:
        camera.stop()  # Stop the camera before shutting down
        sys.exit()
    except SystemExit:
        pass  # Exit normally
    except Exception as e:
        print(f"Error during shutdown: {e}")
        raise SystemExit

def send_bool():
    activated = False  # boolean flag for one-time logic
    quit_flag = False  # flag to manage program quit

    try:
        while not quit_flag:
            while win32api.GetAsyncKeyState(trigger_hotkey) < 0:
                if not activated:  # one-time logic when key is pressed
                    activated = True
                    print("activated")

                try:
                    image = camera.get_latest_frame()
                    rgb_vals = image.reshape(-1, 3)  # assuming RGB with 3 channels
                    mask = (
                        (rgb_vals[:, 0] > r - margin) & (rgb_vals[:, 0] < r + margin) &
                        (rgb_vals[:, 1] > g - margin) & (rgb_vals[:, 1] < g + margin) &
                        (rgb_vals[:, 2] > b - margin) & (rgb_vals[:, 2] < b + margin)
                    )
                    target_rgb_vals = rgb_vals[mask]

                    if len(target_rgb_vals) > 0:
                        keyboard.press_and_release(";")
                        print('click')
                except Exception as e:
                    print(f"Error processing frame: {e}")
                    continue

            # Check if `trigger_hotkey` was released
            if activated:
                activated = False
                print("deactivated")

            # Check for quit key
            if keyboard.is_pressed(quit_key):
                quit_flag = True
                print("Quitting...")

            time.sleep(0.1)  # Pause to reduce CPU usage
    finally:
        camera.stop()  # Ensure the camera stops before exiting

if __name__ == "__main__":
    print(f'Started! x, y: {xres}, {yres}')
    send_bool()
    shut_down()