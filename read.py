import pyautogui
import time
#reroll = 638, 855
#exit = 1384, 200

#if you cant get it to work add my discord just2good4u.

#make sure autoit is downloaded this is official site: https://www.autoitscript.com/cgi-bin/getfile.pl?autoit3/autoit-v3-setup.zip
#once downloaded run this in terminal pip install pyautogui keyboard autoit pywin32
#this should work for 1920x1080 but if it doesnt you can just remove the region


screenshot = pyautogui.screenshot(region = (497, 587, 253, 225))
screenshot.save("screenshot.png")

while True:
    print(pyautogui.position())
    time.sleep(3)

#top left 501 643 left 500 687 right 746 683 bottom right 744 758

#region=(501, 643, 243, 115)

#region=(497, 587, 253, 225)


