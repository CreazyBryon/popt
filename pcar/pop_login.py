
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

def launchPP():
    for i in range(20):
        logger.debug('logging in, waiting...')
        time.sleep(1)

        loc = pyautogui.locateOnScreen(r'pics\mmcw.png',confidence=0.9)
        
        if(loc!=None):
            logger.debug('Login failed due to incorrect password, retry!!!')
            return -1;

        loc = pyautogui.locateOnScreen(r'pics\zzyx.png',confidence=0.9)
 
        if(loc!=None):
            logger.debug('running, stop first')
            pyautogui.click(1257,726)# stop pp
            time.sleep(1)
            pyautogui.click(629,465)# que ren 

        
        logger.debug('start to check if launch button existing')
        loc2 = pyautogui.locateOnScreen(r'pics\qd.png',confidence=0.9)
        
        if(loc2!=None):      
            loc = pyautogui.locateOnScreen(r'pics\duodi.png',confidence=0.8)
            
            if(loc!=None):
                logger.debug('Login failed due to multiple login attempts, retry!!!')
                pyautogui.click(500,500)
                return -1;            
        
            logger.debug('launch button found, login success, click launch')
            pyautogui.click(1025,638)#qi dong
            return 1
    
    logger.debug('launch button not found after 20 retries, something wrong, retry login')  
    return -1;

def login0(acid,isSlow=True):
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

    if(isLaunch==-1):
        logger.debug('login failed, retry')
        return -1;

    logger.debug('login process finished, launch clicked, waiting for game to showup')
    for i in range(20):
        time.sleep(1)
        loc = pyautogui.locateOnScreen(r'pics\kr.png',confidence=0.7)
        
        if(loc==None):
            logger.debug('not running yet')
        else:
            logger.debug('karter started running')
            return 1; 


    logger.debug('karter start failed, something wrong, retry click launch')
    launchPP()
 
    return 0;

def wait_until_pop_running(is_clear_login=True):
    for i in range(100):
        time.sleep(1)
        loc = pyautogui.locateOnScreen(r'pics\kr.png',confidence=0.7)
        
        if(loc==None):
            logger.debug('not running yet')
        else:
            logger.debug('karter running')
            if(is_clear_login):
                time.sleep(5)
                clear_login()
            
            break

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


def killkt():
    os.system(r'taskkill /F /IM KartRider.exe')

def closeKarter():
    loc = pyautogui.locateOnScreen(r'pics\kr.png',confidence=0.6)
    
    if(loc==None):
        logger.debug('no running')
    else:
        logger.debug('karter running, stop first')
        killkt()
        time.sleep(2)
        pyautogui.click(1057,129)#click user
        time.sleep(3)
        pyautogui.click(1097,261)#switch account

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

def login2(acid, forced=False):

    account_name_pic= rf'pics\{acid}.png'  

    if is_running():
        logger.debug('karter running, check if already logged in with account: %s', acid)
        loc = pyautogui.locateOnScreen(r'pics\kr.png',confidence=0.6) 

        if(loc!=None):                   
            if global_state.current_account == acid:
                logger.debug(f"already logged in with account: {acid}")
                return True;
   
            logger.debug('karter running, but global state not updated, check if already logged in with account: %s', acid)

            if not os.path.exists(account_name_pic):
                logger.debug("Account name image not found: %s", account_name_pic)
                closeKarter()   
            else:
                loc = pyautogui.locateOnScreen(rf'pics\{acid}.png',confidence=0.8,region=pop_consts.UI_ACCOUNT_NAME_AREA_REGION)
                if(loc!=None):
                    logger.debug('already logged in with account: %s', acid)
                    global_state.current_account = acid
                    return True;
                else:
                    logger.debug('logged in with other account, close it first')
                    closeKarter()
        else:
            logger.debug('karter running, but not at front, close it')
            closeKarter()            

    logger.critical('start to login with account: %s', acid)
 
    time.sleep(3)
    startT = str(datetime.now())
 
    for i in range(20):
        time.sleep(1)
        loc = pyautogui.locateOnScreen(r'pics\slider.png',confidence=0.9)
        
        if(loc==None):
            logger.debug('no login window')
        else:    
            logger.debug('logining')        
            time.sleep(2)
            lres = login0(acid)
            
            if(lres==-1):#retry
                time.sleep(3)
                lres = login0(acid)
             
            global_state.current_account = acid
            wait_until_pop_running(is_clear_login=True)
            pyautogui.screenshot(account_name_pic, region=pop_consts.UI_ACCOUNT_NAME_AREA_REGION)
            logger.critical('login succeed for account: %s; start: %s; end: %s', acid, startT, str(datetime.now()))
            return True;

    logger.critical('login failed for account: %s; start: %s; end: %s', acid, startT, str(datetime.now()))
    return False;


def loginST(acid):
    time.sleep(1)
    closeKarter()
    for i in range(20):
        time.sleep(1)
        loc = pyautogui.locateOnScreen(r'pics\slider.png',confidence=0.9)
        
        if(loc==None):
            logger.debug('no login window')
        else:
            logger.debug('logining')        
            time.sleep(2)
            login0(acid,False)
                     
            wait_until_pop_running(is_clear_login=False)

            time.sleep(5)
 
            break
 

if __name__ == '__main__':
    setup_logging()
    logger.debug('start')
    login2("qq")