import time
import keyboard

import dxcam
import numpy as np
import cv2
import scipy.spatial
import win32api
import serial
# config - color ranges

# purple
lower = np.array([110, 20, 80], dtype='uint8') 
upper = np.array([250, 90, 250], dtype='uint8')



#self found
#lower = np.array([82, 42, 105], dtype='uint8') 
#upper = np.array([212, 145, 214], dtype='uint8')


# setup - link w/ userinput

xres = 2560
yres = 1440

xmult = 10
ymult = 10


width = int((1/xmult)* xres)
height = int((1/ymult)* yres)

pt = (width, height) # screen center; pointer position: # win32api.GetCursorPos()
region = ((xres//2)-width, (yres//2)-height, (xres//2)+width, (yres//2)+height)

camera = dxcam.create(output_color='BGR', max_buffer_len=64)
hz = 60

activated = False # bool flag for on/off
hotkey = 'alt' # keybind for toggling
quit_key = 'q' # keybind for quitting program


# function definitions
def find_closest_point(image, pt):
    close_points = []
    mask = cv2.inRange(image, lower, upper)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        if cv2.contourArea(c) > 1:  # Adjust size threshold as needed
            x1, y1, w1, h1 = cv2.boundingRect(c)
            close_points.append((round(x1 + (w1 / 2)), round(y1 + (h1 / 2))))
            cv2.rectangle(image, (x1, y1), (x1+w1, y1+h1), (255, 255, 255), 1)

    if close_points:
        closest = close_points[scipy.spatial.KDTree(close_points).query(pt)[1]]
        return closest
    return None


# one-time start logic
camera.start(region=region, target_fps=hz)


while True:
    if keyboard.is_pressed(hotkey):
        if not activated: # one-time logic
            activated = True
            print('activated')


        # loop logic
        image = camera.get_latest_frame()

        #closest function
        close_points = []
        mask = cv2.inRange(image, lower, upper)
        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for c in contours:
            if cv2.contourArea(c) > 1:  # Adjust size threshold as needed
                x1, y1, w1, h1 = cv2.boundingRect(c)
                close_points.append((round(x1 + (w1 / 2)), round(y1 + (h1 / 2))))
                cv2.rectangle(thresh, (x1, y1), (x1+w1, y1+h1), (255, 255, 255), 1)

        if close_points:
            closest = close_points[scipy.spatial.KDTree(close_points).query(pt)[1]]

            if closest is not None:
                cv2.circle(thresh, (closest[0], closest[1]), radius=2, color=(255, 255, 255), thickness=-1)
                cv2.line(thresh, pt, (closest[0], closest[1]), (255, 255, 255), 1)

        resize = cv2.resize(thresh, (960, 540))
        cv2.imshow('Real-Time Color Detection', resize)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        if activated: # one-time logic
            activated = False
            print('deactivated')
            cv2.destroyAllWindows()


        # loop logic
        if keyboard.is_pressed(quit_key):
            print(f'{quit_key} was pressed: shutting down') # one-time quit logic

            camera.stop()


            break


        #image = camera.grab(region=region)
        #image = cv2.cvtColor(np.array(temp), cv2.COLOR_RGB2BGR)