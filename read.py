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




a = input("a")
