import time 
import pyautogui

def is_any_card_empty():
    loc = pyautogui.locateOnScreen(r'pics\card_empty.png', confidence=0.7, region=(278, 676, 520, 32))
    return loc

while True:
    time.sleep(0.5)
    pos = pyautogui.position()
    print(pos)
    
    mp = pyautogui.pixel(pos.x, pos.y)
 
    print(mp)

    mp = pyautogui.pixel(243, 184)
 
    print(mp)
    print(is_any_card_empty())


#25,122,255
#10,47,96
    #pyautogui.screenshot(r'pics\caiquan111.png', region=(278, 676, 520, 32))
    #pyautogui.screenshot(r'pics\caiquan111.png', region=(539, 683, 28, 25))
    #loc = pyautogui.locateOnScreen(r'pics\bao.png',confidence=0.9,region=(265, 90, 250, 80))
    #print(loc)
 


 