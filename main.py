import pyautogui
import keyboard
import time
import autoit
import tkinter as tk
import threading
import win32api
import win32con

region1 = (497, 587, 253, 225)
reroll = (638, 855)
exit = (1384, 200)
pop_up = (854, 636)
enchant = "V.png"
enchant_iv = "IV.png"
popup = "close.png"
attempts = 0

running = False
clicking = False
check_iv = False

def toggle_loop():
    global running
    running = not running
    if running:
        status_label.config(text="Running", bg="green")
        start_thread()
    else:
        status_label.config(text="Stopped", bg="red")
    print(f"Running: {running}")

def toggle_clicker():
    global clicking
    clicking = not clicking
    if clicking:
        clicker_label.config(text="Auto clicker: Running", bg="green")
        start_clicker_thread()
    else:
        clicker_label.config(text="Auto clicker: Stopped", bg="red")
    print(f"Clicker running: {clicking}")

def toggle_iv():
    global check_iv
    check_iv = not check_iv
    iv_button.config(relief=tk.SUNKEN if check_iv else tk.RAISED)
    print(f"Check IV enabled: {check_iv}")

def click():
    x, y = autoit.mouse_get_pos()
    autoit.mouse_move(x + 10, y, 1)
    autoit.mouse_move(x, y, 1)
    autoit.mouse_click()

def check_popup():
    try:
        result = pyautogui.locateOnScreen(popup, confidence=0.85)
        if result:
            print("Popup detected")
            pyautogui.moveTo(pop_up)
            click()
            return True
    except pyautogui.ImageNotFoundException:
        return False

def find_enchant():
    try:
        result = pyautogui.locateOnScreen(enchant, confidence=0.95, region=region1)
        if result:
            print("Found V")
            return True
        if check_iv:
            result_iv = pyautogui.locateOnScreen(enchant_iv, confidence=0.9, region=region1)
            if result_iv:
                print("Found IV")
                return True
    except pyautogui.ImageNotFoundException:
        return False

def main_loop():
    global attempts, running
    while running:
        enchant_found = find_enchant()
        if enchant_found:
            pyautogui.moveTo(exit)
            click()
            time.sleep(0.01)
            click()
            print(f"Enchant found after {attempts} attempts.")
            status_label.config(text="Stopped", bg="red")
            running = False 
        else:
            attempts += 1
            pyautogui.moveTo(reroll)
            click()
            time.sleep(0.01)
            check_popup()

            if attempts % 5 == 0:
                attempts_label.config(text=f"Attempts: {attempts}")
        time.sleep(0.01)
    print(f"Total attempts: {attempts}")

def autoclick_loop():
    while True:
        if clicking:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.01)

def start_thread():
    thread = threading.Thread(target=main_loop)
    thread.daemon = True
    thread.start()

def start_clicker_thread():
    thread = threading.Thread(target=autoclick_loop)
    thread.daemon = True
    thread.start()

root = tk.Tk()
root.title("enchanter")
root.geometry("400x300")

keyboard.add_hotkey('F8', toggle_loop)
keyboard.add_hotkey('F6', toggle_clicker)

status_label = tk.Label(root, text="F8 to start/stop", font=("Arial", 14), fg="white", bg="red", width=20, height=2)
status_label.pack(pady=10)

clicker_label = tk.Label(root, text="F6 to toggle auto clicker", font=("Arial", 14), fg="white", bg="red", width=25, height=2)
clicker_label.pack(pady=10)

attempts_label = tk.Label(root, text="Attempts: 0", font=("Arial", 12), fg="white", bg="black", width=20, height=2)
attempts_label.pack(pady=10)

iv_button = tk.Button(root, text="Toggle IV Search", font=("Arial", 12), command=toggle_iv)
iv_button.pack(pady=5)

root.mainloop()
