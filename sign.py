from PIL import ImageGrab
import pyautogui
import cv2
import numpy as np
import time

while True:
    try:
        # Capture the whole screen
        screenshot = ImageGrab.grab()

        # Convert the screenshot to a numpy array and then to grayscale
        img = np.array(screenshot)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Read the template image in grayscale
        template = cv2.imread('metamask.png', 0)

        # Perform template matching
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            # Get the screen coordinates of the arrow down button
            arrow_down_button_x = 1236  # Replace with the actual x-coordinate of the arrow down button
            arrow_down_button_y = 627  # Replace with the actual y-coordinate of the arrow down button

            # Click on the arrow down button
            pyautogui.click(arrow_down_button_x, arrow_down_button_y)
            print("arrow down")
            time.sleep(1)
            pyautogui.scroll(-10)  # Negative value for scrolling down

            time.sleep(2)  # Wait for 2 seconds for the interface to respond

            # Get the screen coordinates of the sign button
            sign_button_x = 1220  # Replace with the actual x-coordinate of the sign button
            sign_button_y = 616  # Replace with the actual y-coordinate of the sign button

            # Click on the sign button
            pyautogui.click(sign_button_x, sign_button_y)
            print("sign")
        else:
            print("Element not found, waiting for 5 seconds before trying again")
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)
