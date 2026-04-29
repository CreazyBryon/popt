
import subprocess
import pyautogui
import time 
import random
import os
from datetime import datetime

from utils.state import global_state
from utils.d4 import d4ocr
import utils.constants as pop_consts
 
import logging
from utils.logging_config import setup_logging
logger = logging.getLogger(__name__)


def findSlider():
  
    with open(r'pics\tag.png', 'rb') as f:
        target_bytes = f.read()
  
    with open(r'pics\bg0.png', 'rb') as f:
        background_bytes = f.read()
  
    res = d4ocr.slide_match(target_bytes, background_bytes, simple_target=True)
  
    logger.debug("OCR result: %s", res)

    return res['target']


def slideYzm():

    start_x=883
    start_y=376+random.randint(-5,5)
    pyautogui.moveTo(start_x, start_y, duration=0.1 + random.uniform(0, 0.1))
    time.sleep(0.2)

    pyautogui.mouseDown()
    time.sleep(1)    

    pyautogui.screenshot(r"pics\bg0.png", region=(906, 253, 177, 108))
    tagPos = findSlider()
  
    xTag = 33+tagPos[0]
 
    human_horizontal_slide(xTag)

    time.sleep(0.5)
    pyautogui.mouseUp()
    time.sleep(0.5)


def human_horizontal_slide(dist1):
    start_x = 883
    start_y = 376
    end_x=start_x +dist1
  
    time.sleep(random.uniform(0.1, 0.3)) # Pause before starting the pull
    
    # 3. The Slide (with variable speed and potential overshoot)
    # Decide if we are going to accidentally overshoot the target (like real humans do)
    will_overshoot = random.random() > 0.5 # 50% chance to overshoot
    
    if will_overshoot:
        # Calculate an overshoot target (e.g., 5 to 15 pixels past the real target)
        direction = 1 if end_x > start_x else -1
        overshoot_x = end_x + (random.randint(5, 15) * direction)
        
        # Fast, confident slide past the target
        slide_duration = random.uniform(0.5, 0.9)
        pyautogui.moveTo(overshoot_x, start_y, duration=slide_duration, tween=pyautogui.easeInOutSine)
        
        # Oops went too far! Tiny pause to realize the mistake
        time.sleep(random.uniform(0.2, 0.4))
        
        # Pull back slowly to the exact correct spot
        correction_duration = random.uniform(0.3, 0.6)
        pyautogui.moveTo(end_x, start_y, duration=correction_duration, tween=pyautogui.easeOutCubic)
        
    else:
        # Normal, careful slide directly to the target
        slide_duration = random.uniform(0.7, 1.2)
        pyautogui.moveTo(end_x, start_y, duration=slide_duration, tween=pyautogui.easeInOutSine)

    # 4. Final pause before releasing the mouse button
    time.sleep(random.uniform(0.1, 0.3))


def doYzm():
    for i in range(20):
        slideYzm()
        time.sleep(1)
        loc0 = pyautogui.locateOnScreen(r'pics\cw.png',confidence=0.9)

        if(loc0==None):
            logger.debug('yzm passed')
            return True
        else:
            logger.debug('yzm failed retry: %d', i)

    logger.debug('yzm failed after 20 retries')
    return False

def is_karter_up():              
    pop_px = pyautogui.pixel(*pop_consts.POP_ICON_POS)       
    return pop_px == pop_consts.POP_ICON_COLOR

 
def is_tc_game_up():
    tc_px = pyautogui.pixel(*pop_consts.LOGIN_WINDOW_CHECK_POS)       
    return tc_px == pop_consts.LOGIN_WINDOW_CHECK_COLOR


def launchPP():
    for i in range(30):
        time.sleep(1)
        pix = pyautogui.pixel(*pop_consts.LOGIN_LAUNCH_BUTTON_POS)
        logger.debug('launch button pixel color: %s', pix)
 
        if(pix==pop_consts.LOGIN_LAUNCH_BUTTON_RUNNING_COLOR):
            logger.debug('running, stop first')
            pyautogui.click(*pop_consts.LOGIN_LAUNCH_BUTTON_POS)# stop pp
            time.sleep(0.1)
            pyautogui.press('enter')# que ren 
  
        elif(pix==pop_consts.LOGIN_LAUNCH_BUTTON_READY_COLOR):      
            logger.debug('launch button found, login success, click launch')

            pyautogui.click(*pop_consts.LOGIN_LAUNCH_BUTTON_POS)#qi dong

            logger.debug('login process finished, launch clicked, waiting for game to showup')
            for i in range(60):
                time.sleep(1)    
                if(is_karter_up()):
                    logger.debug('karter started running')
                    return 1;      
                else:
                    logger.debug('not running yet')
            logger.debug('karter win not show up after 60s, something wrong, retry click launch')
            return -1;
        else:
            logger.debug('launch button color not matched, retry: %d', i)
                  
    
    logger.debug('launch button not found after 30 retries, something wrong, retry login')  
    return -1;

def login0(acid):
    ppp = 'yy123456'
    nnn = acid[-2]

    if(acid=='hsmsyy91' or acid=='hsmsyy92' or acid=='hsmsyy99'):
        ppp='yuy@2023'

    if(acid=='hsmsyy06'):
        ppp='yu@2017'

    if(acid=='hsmsyy03'):
        ppp='ezc@202512'

    if(acid=='hsmsyy94'):
        ppp='rxv@qq2025'

    if(acid=='hsmsyy97'):
        ppp='ubm@2025ww'

    if(acid=='hsmsyy98'):
        ppp='inm@2025qw'



    if(acid=='hsmsyy2003' or acid=='hsmsyy2008'):
        ppp='qq123456'
    
 
    pyautogui.doubleClick(1000,307,button='left')
    pyautogui.typewrite(acid,0.1)
    pyautogui.click(1000,337)    
    pyautogui.typewrite(ppp,0.1)
    
    isYzm = doYzm()

    if(isYzm==False):
        logger.debug('yzm failed, retry login')
        return -1;
 
    logger.debug('yzm passed, click login')
    pyautogui.click(975,459)#login button
    
    isLaunch = launchPP()

    if(isLaunch==1):
        return 1;

    if(isLaunch==-1):
        logger.debug('login failed, retry')
        return -1;


  
    logger.debug('karter start failed, something wrong, retry click launch')
    return launchPP()
 
  
def clear_login():
    for i in range(10):
        time.sleep(0.5)
        pyautogui.press('esc')
        pyautogui.click(750,613)# guoqi
        pyautogui.click(684,571)
        pyautogui.click(684,587) 
        pyautogui.click(684,630)         
        pyautogui.click(679,607)   
        pyautogui.click(1109,103)#dafuweng    


def kill_kt():
    os.system(r'taskkill /IM KartRider.exe /F ')

def kill_tc_game():
    os.system(r'taskkill /IM TCGame.exe /F ')

def callup_tc_game():
    pyautogui.click(*pop_consts.TC_GAME_BAR_POS)

def callup_karter():
    pyautogui.click(*pop_consts.KARTER_BAR_POS)

def is_login_window_up():
    loc = pyautogui.locateOnScreen(r'pics\slider.png',confidence=0.9)
    return loc!=None;
 

def return_login():
    logger.debug('stop karter if running')
    kill_kt()
    logger.debug('try to switch account')
    
    if(is_login_window_up()):
        logger.debug('login window show up')
        return True;

    if is_tc_game_running() and not is_tc_game_up():
        logger.debug('tc game is running but not up, click tc game bar to wake it up')
        callup_tc_game()
        time.sleep(3)

    if not is_tc_game_up(): 
        logger.debug('tc game is not up even after click, something wrong, retry by kill tc game and click again')
        kill_tc_game()
        time.sleep(1)
        callup_tc_game()
        for i in range(30):
            time.sleep(1)
            if is_tc_game_up():
                logger.debug('tc game is up, switch account')
                pyautogui.click(1057,129)#click user
                time.sleep(2)
                pyautogui.click(1097,261)#switch account
                time.sleep(3)
                break
             

    if is_tc_game_up():
        logger.debug('tc game is up, switch account')
        pyautogui.click(1057,129)#click user
        time.sleep(2)
        pyautogui.click(1097,261)#switch account


    logger.debug('start to check if login window show up')
    for i in range(60):
        time.sleep(1)
        if(is_login_window_up()):
            logger.debug('login window show up')
            return True;

        logger.debug('login window not show up, retry: %d', i)

    return False;
 

def reset_login():
    logger.debug('reset login, kill tc game and karter')
    kill_kt()    
    kill_tc_game()
    time.sleep(3)
    callup_tc_game()
    for i in range(30):
        time.sleep(1)
        if is_tc_game_up():
            logger.debug('tc game is still up, switch account')   
            pyautogui.click(1057,129)#click user
            time.sleep(2)
            pyautogui.click(1097,261)#switch account
            time.sleep(3)
            break
        else:
            if(is_login_window_up()):
                logger.debug('login window show up')
                return True;

 
    logger.debug('start to check if login window show up')
    for i in range(60):
        time.sleep(1)
        if(is_login_window_up()):
            logger.debug('login window show up')
            return True;

        logger.debug('login window not show up, retry: %d', i)

    return False;
 


def get_pid(name):
    result = subprocess.run(
        ["tasklist"], capture_output=True, text=True
    )

    for line in result.stdout.splitlines():
        if name in line:
            return int(line.split()[1])
    
    return None


def is_running():  
    return get_pid("KartRider.exe") != None

def is_tc_game_running():  
    return get_pid("TCGame.exe") != None

def is_already_login(acid):
    account_name_pic= rf'pics\{acid}.png'  

    if is_running():
        if not is_karter_up():  
             logger.debug('karter running, but not at front, close it first')
             callup_karter()

        if is_karter_up():         
            logger.debug('karter is up, check login state')          
            if global_state.current_account == acid:
                logger.debug(f"already logged in with account: {acid}")
                return True;
        
            if global_state.current_account is not None:
                logger.debug(f"currently logged in with account: {global_state.current_account}, but expected: {acid}, close it first")
                return False;
            else:
                logger.debug('karter running, but global state not updated, check if already logged in with account: %s', acid)

                if not os.path.exists(account_name_pic):
                    logger.debug("Account name image not found: %s", account_name_pic)
                    return False;   
                else:
                    loc = pyautogui.locateOnScreen(rf'pics\{acid}.png',confidence=0.8,region=pop_consts.UI_ACCOUNT_NAME_AREA_REGION)
                    if(loc!=None):
                        logger.debug('already logged in with account: %s', acid)
                        global_state.current_account = acid
                        return True;
                    else:
                        logger.debug('logged in with other account, close it first')
                        return False;
        else:
            logger.debug('karter running, but not show up even after click, something wrong, close it first')
            return False;
       
    else:
        logger.debug('karter not running, no account logged in')
        return False



def login2(acid, forced=False):
 
    if not forced and is_already_login(acid):
        return True;
    
    is_login_up = return_login()

    logger.critical('start to login with account: %s', acid) 
    time.sleep(3)
    startT = str(datetime.now())
 
    if(is_login_up):
        logger.debug('start to login since login window is up')        
        time.sleep(2)
        lres = login0(acid)
        
        if(lres==-1):#retry
            time.sleep(3)
            logger.debug('login failed, retry once')
            lres = login0(acid)
 
        if (lres==1): 
            global_state.current_account = acid
            time.sleep(5)#wait pop statble after login
            clear_login()
            pyautogui.screenshot(rf'pics\{acid}.png', region=pop_consts.UI_ACCOUNT_NAME_AREA_REGION)
            logger.critical('login succeed for account: %s; start: %s; end: %s', acid, startT, str(datetime.now()))
            return True;    

    logger.critical('login failed for account: %s; start: %s; end: %s', acid, startT, str(datetime.now()))
    return False;


def login_st(acid):
    time.sleep(1)
    is_login_up = return_login()
 
    if(is_login_up): 
        logger.debug('start to login for ST since login window is up')        
        time.sleep(2)
        lres = login0(acid)
        
        if(lres==-1):#retry
            logger.debug('login failed for ST, retry once')
            time.sleep(3)
            lres = login0(acid)
        
        if (lres==1): 
            logger.critical('login st succeed for account: %s', acid)
            time.sleep(5)
            return True;
 
    return False;
 

if __name__ == '__main__':
    setup_logging()
    logger.debug('start')
    login2("qq")