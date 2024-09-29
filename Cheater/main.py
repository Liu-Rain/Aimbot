# Load a model
from ultralytics import YOLO
from mss import mss
import cv2
from PIL import Image
import numpy as np
#from time import time
import pygetwindow as gw
import pyautogui
import win32api
import time
import pydirectinput

# Load a model
model = YOLO("C:/Users/85876/Desktop/Machinelearning/Cheater/best.pt")  # load an official model
pyautogui.FAILSAFE = False
mouse_state = win32api.GetKeyState(0x70)  # Right button down = 0 or 1. Button up = -127 or -128
f8_state = win32api.GetKeyState(0x77)  # Right button down = 0 or 1. Button up = -127 or -128



def get_window_coordinates(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]  # Get the first window with the given title
        if window:
            return {
                'top': window.top,
                'left': window.left,
                'width': window.width,
                'height': window.height
            }
    except IndexError:
        print(f"No window found with title: {title}")
        return None

# Title of the window to capture
window_title = "C​a​l​l​ ​o​f​ ​D​u​t​y​®​ ​H​Q​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​"  # Change this to the title of your target window

# Get the window coordinates
mon = get_window_coordinates(window_title)

# Ensure the window was found
if mon:
    # Initialize the mss instance
    sct = mss()

    while True:
        #begin_time = time()
        
        # Capture the window
        sct_img = sct.grab(mon)
        
        # Create an image from the screen capture
        img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        
        # Convert the image to BGR (for OpenCV)
        
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Display the image
        #cv2.imshow('test', img_bgr)
        results = model(img_bgr)  # predict on an image
        keypoints = results[0].keypoints
        data = keypoints[0].data[0]
        mouse_click = win32api.GetKeyState(0x70)
        if mouse_click != mouse_state:  # Button state changed
            mouse_state = mouse_click
            if mouse_click < 0:
                if len(data) == 0:
                    pass
                else:
                    for i in range(4):
                        if data[i][0].item() != 0 and data[i][1].item() != 0:
                            pydirectinput.moveTo(int(data[i][0].item()), int(data[i][1].item()), duration = 0)
                            pydirectinput.click(button='left')
                            break
                print('Middle Button Pressed')
            else:
                print('Middle Button Released')

        
        # Print the time taken for this frame
        #print('This frame takes {:.4f} seconds.'.format(time() - begin_time))
        
        # Exit if 'q' is pressed
        f8_click = win32api.GetKeyState(0x77)
        if f8_click != f8_state:  # Button state changed
            f8_state = f8_click
            if f8_click < 0:
                break
            else:
                print('Middle Button Released')
        time.sleep(0.001)
else:
    print("Target window not found. Please ensure the window title is correct.")

# Predict with the model


