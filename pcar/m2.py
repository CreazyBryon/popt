import time 
import pyautogui


while True:
    time.sleep(1)
    pos = pyautogui.position()
    print(pos)
    
    mp = pyautogui.pixel(pos.x, pos.y)
 
    print(mp)

    mp = pyautogui.pixel(581, 702)
 
    print(mp)

    #pyautogui.screenshot(r'pics\cq_jian_bao.png', region=(265, 90, 250, 80))
    #loc = pyautogui.locateOnScreen(r'pics\bao.png',confidence=0.9,region=(265, 90, 250, 80))
    #print(loc)
 


 