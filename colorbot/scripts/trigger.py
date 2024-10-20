import dxcam
import numpy as np

import keyboard
import win32api
import sys
from ctypes import WinDLL

import winsound
import time
import json
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

def shut_down(): # shutdown for compiling to exe
    try:
        sys.exit()
    except:
        raise SystemExit

def send_bool():
    activated = False # boolean flag for one-time logic
    while True:
        while win32api.GetAsyncKeyState(trigger_hotkey) < 0:
            if not activated: # one time logic
                activated = True
            try:
                image = camera.get_latest_frame()
            except:
                continue
            rgb_vals = image.reshape(-1,4)
            mask = (
                (rgb_vals[:,0] > r -  margin) & (rgb_vals[:,0] < r +  margin) &
                (rgb_vals[:,1] > g -  margin) & (rgb_vals[:,1] < g +  margin) &
                (rgb_vals[:,2] > b -  margin) & (rgb_vals[:,2] < b +  margin)
            )
            target_rgb_vals = rgb_vals[mask]
            if len(target_rgb_vals) > 0:
                time.sleep(0.01)
                keyboard.press_and_release(";")
                print('trigger')
                random_sleep = random.uniform(0.08, 0.14)
                time.sleep(random_sleep)
        else:
            if activated:
                activated = False
            time.sleep(0.1)

            if keyboard.is_pressed(quit_key):
                break

if __name__ == "__main__":
    send_bool()
    shut_down()