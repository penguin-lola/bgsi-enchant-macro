import pyautogui
import time
import keyboard
#reroll = 638, 855
#exit = 1384, 200

#press f9 to print mouse position of reroll and exit button


def print_mouse_position():
    x, y = pyautogui.position()
    print(f"Current mouse position: ({x}, {y})")
keyboard.add_hotkey("f9", print_mouse_position)

image = "reroll.png"
image2 = "exit.png"

location = pyautogui.locateOnScreen(image, confidence=0.9)
print(location)

a = input("")



