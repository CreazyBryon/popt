import time 
import pyautogui


while True:
    time.sleep(1)
    pos = pyautogui.position()
    print(pos)
    
    mp = pyautogui.pixel(pos.x, pos.y)
 
    print(mp)

    mp = pyautogui.pixel(1361, 42)
 
    print(mp)
 
 


 