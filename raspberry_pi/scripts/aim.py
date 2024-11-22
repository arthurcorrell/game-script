import dxcam
import numpy as np
import cv2
import scipy.spatial

import keyboard
import win32api
import sys
from ctypes import WinDLL

import time
import json

user32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

# config - link w/ userinput GUI or .json

hz = 120

x_fov = 128
y_fov = 72

lower = np.array([110, 20, 80], dtype='uint8') # color range for aim
upper = np.array([250, 90, 250], dtype='uint8')

aim_hotkey =  int("0x11",16) # ctrl key

# alt key: "0x12"

quit_key = 'q' # keybind for quitting program


# setup

shcore.SetProcessDpiAwareness(2)
xres, yres = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

pt = (x_fov, y_fov) # center of captured window; pointer position: # win32api.GetCursorPos()
region = ((xres//2)-x_fov, (yres//2)-y_fov, (xres//2)+x_fov, (yres//2)+y_fov)


# initalization

camera = dxcam.create(output_color='BGR', max_buffer_len=64)
camera.start(region=region, target_fps=hz)


# function definitions

def shut_down(): # shutdown for compiling to exe
    try:
        sys.exit()
    except:
        raise SystemExit
    
def find_lowest_y(image, pt):
    mask = cv2.inRange(image, lower, upper)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    lowest_y = float('inf')
    lowest_point = None

    for c in contours:
        if cv2.contourArea(c) > 1:
            x1, y1, w1, h1 = cv2.boundingRect(c)

            point = (round(x1 + (w1 / 2)), round(y1 + (h1 / 2)))
            
            if y1 < lowest_y:
                lowest_y = y1
                lowest_point = point

            # visual DEBUG
            #cv2.rectangle(image, (x1, y1), (x1+w1, y1+h1), (255, 255, 255), 1) 

    if lowest_point:
        return lowest_point
    return None

# not in use - for later reference
def find_closest_point(image, pt):
    close_points = []
    mask = cv2.inRange(image, lower, upper)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        if cv2.contourArea(c) > 1:  # Adjust size threshold as needed
            x1, y1, w1, h1 = cv2.boundingRect(c)
            close_points.append((round(x1 + (w1 / 2)), round(y1 + (h1 / 2))))

            # for visual debugging:
            #cv2.rectangle(image, (x1, y1), (x1+w1, y1+h1), (255, 255, 255), 1) 

    if close_points:
        closest = close_points[scipy.spatial.KDTree(close_points).query(pt)[1]]
        return closest
    return None
    '''
        if closest is not None:
            cv2.circle(thresh, (closest[0], closest[1]), radius=2, color=(255, 255, 255), thickness=-1)
            cv2.line(thresh, pt, (closest[0], closest[1]), (255, 255, 255), 1)

        resize = cv2.resize(thresh, (960, 540))
        cv2.imshow('Real-Time Color Detection', resize)
    '''



def send_coordinates():
    activated = False # bool flag for on/off
    while True:
        while win32api.GetAsyncKeyState(aim_hotkey) < 0:
            if not activated: # one-time logic
                activated = True
                print('activated')

            # loop logic
            image = camera.get_latest_frame()
            lowest_point = find_lowest_y(image, pt)

            # visual DEBUG
            """
            if lowest_point is not None:
                cv2.circle(image, (lowest_point[0], lowest_point[1]), radius=2, color=(255, 255, 255), thickness=-1)
                cv2.line(image, pt, (lowest_point[0], lowest_point[1]), (255, 255, 255), 1) 
            resize = cv2.resize(image, (960, 540))
            cv2.imshow('Real-Time Color Detection', resize)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            """

        else:
            if activated: # one-time logic
                activated = False
                print('deactivated')

                # visual DEBUG
                cv2.destroyAllWindows()
            
            time.sleep(0.1) # limits windows api calls


            # loop logic
            if keyboard.is_pressed(quit_key):
                print(f'{quit_key} was pressed: shutting down') # one-time quit logic

                camera.stop()


                break

if __name__ == "__main__":
    send_coordinates()