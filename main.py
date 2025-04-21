import pyautogui
import keyboard
import time
import autoit
import tkinter as tk
import win32api
import win32con
import threading

reroll = (613, 851)
exit = (1385, 213)
pop_up = (852, 636)
enchant = "V.png"
enchant_iv = "IV.png"
popup = "close.png"
attempts = 0

running = False
check_iv = False
auto_clicker = False
auto_clicker_thread = None

def click():
    x, y = pyautogui.position()
    autoit.mouse_move(x + 5, y, speed=1)
    autoit.mouse_click()

def check_popup():
    try:
        if pyautogui.locateOnScreen(popup, confidence=0.85):
            print("popup")
            pyautogui.moveTo(pop_up)
            click()
            return True
    except pyautogui.ImageNotFoundException:
        return False

def find_enchant():
    try:
        found = pyautogui.locateOnScreen(enchant, confidence=0.93)
        print("found" if found else "not found")
        return found is not None
    except pyautogui.ImageNotFoundException:
        print("not found")
        return False

def find_enchant2():
    try:
        found = pyautogui.locateOnScreen(enchant_iv, confidence=0.93)
        print("found" if found else "not found")
        return found is not None
    except pyautogui.ImageNotFoundException:
        print("not found")
        return False

def exit_sequence():
    for _ in range(3):
        pyautogui.moveTo(exit)
        click()
        time.sleep(0.1)

def main_loop():
    global running, attempts
    print("running")
    while running:
        if check_popup():
            time.sleep(0.05)
            continue

        if find_enchant():
            exit_sequence()
            break

        pyautogui.moveTo(reroll)
        click()
        attempts += 1
        update_attempts()
        time.sleep(0.05)

def alt_loop():
    global running, attempts
    print("running")
    while running:
        if check_popup():
            time.sleep(0.05)
            continue

        if find_enchant() or find_enchant2():
            exit_sequence()
            break

        pyautogui.moveTo(reroll)
        click()
        attempts += 1
        update_attempts()
        time.sleep(0.05)

def toggle_loop():
    global running, check_iv
    if running:
        running = False
        update_status()
        return
    running = True
    update_status()
    loop = alt_loop if check_iv else main_loop
    threading.Thread(target=loop, daemon=True).start()

def update_status():
    if running:
        status_label.config(text="RUNNING", bg="green")
    else:
        status_label.config(text="STOPPED", bg="red")

def update_attempts():
    attempts_label.config(text=f"Attempts: {attempts}")

def alt_button_action():
    global check_iv
    check_iv = not check_iv
    alt_button.config(
        text=f"Enchant 2: {'ON' if check_iv else 'OFF'}",
        bg="green" if check_iv else "SystemButtonFace"
    )


def normal_button_action():
    global check_iv
    check_iv = False
    toggle_loop()

def auto_clicker_task():
    while auto_clicker:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(1)

def toggle_auto_clicker():
    global auto_clicker, auto_clicker_thread
    auto_clicker = not auto_clicker
    if auto_clicker:
        auto_clicker_label.config(text="Auto Clicker: ON", bg="green")
        auto_clicker_thread = threading.Thread(target=auto_clicker_task, daemon=True)
        auto_clicker_thread.start()
    else:
        auto_clicker_label.config(text="Auto Clicker: OFF", bg="red")

root = tk.Tk()
root.title("Auto Enchanter")
root.geometry("300x300")
root.resizable(False, False)

status_label = tk.Label(root, text="STOPPED", bg="red", fg="white", width=20, height=2)
status_label.pack(pady=5)

normal_button = tk.Button(root, text="Start Normally", command=normal_button_action)
normal_button.pack(pady=5)

alt_button = tk.Button(root, text="Enchant 2: OFF", command=alt_button_action)
alt_button.pack(pady=5)


attempts_label = tk.Label(root, text="Attempts: 0", bg="white", fg="black", width=20, height=2)
attempts_label.pack(pady=5)

auto_clicker_label = tk.Label(root, text="Auto Clicker: OFF", bg="red", fg="white", width=20, height=2)
auto_clicker_label.pack(pady=5)

tk.Label(root, text="F8 to Start/Stop").pack()
tk.Label(root, text="F6 to toggle Auto Clicker").pack()

keyboard.add_hotkey("f8", toggle_loop)
keyboard.add_hotkey("f6", toggle_auto_clicker)

root.mainloop()
