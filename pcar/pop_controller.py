
import pyautogui
import time 
import os
from datetime import datetime 
from utils.d4 import d4ocr
import pop_auto
from utils.state import global_state
import utils.constants as pop_consts

import logging
from utils.logging_config import setup_logging
logger = logging.getLogger(__name__)

AUTORUN9_TASK_NAME = "saidao9"
AUTORUN9_TASK_DESCRIPTION = "Running autorun 9"
MAX_CONSECUTIVE_FAILURES = 10
 
class NeedRelaunchError(Exception):
    pass
 
def goto_main_page():
    main_pixel = pyautogui.pixel(*pop_consts.UI_ICON_MAIN_POS)

    if main_pixel == pop_consts.UI_ICON_COLOR:
        logger.debug('main icon visible, click the main icon')
        pyautogui.click(*pop_consts.UI_ICON_MAIN_POS)#main
        time.sleep(0.5)
        pyautogui.press('return')
        time.sleep(2)
        return True
    else:
        logger.debug('main icon invisible, stopping')
        return False

def goto_duoren_channel():
    duoren_pixel = pyautogui.pixel(*pop_consts.UI_ICON_POS_DUOREN)
 
    if duoren_pixel == pop_consts.UI_ICON_COLOR:
        logger.debug('duoren icon is visible, click to enter duoren channel')
        pyautogui.click(*pop_consts.UI_ICON_POS_DUOREN)#duoren icon in ribbon
        pyautogui.press('return')
        time.sleep(2)
        return True
    else:
        logger.debug('duoren icon invisible, stopping')
    
    return False



def select_map_in_fav(map_index=1):
    pyautogui.click(*pop_consts.UI_POS_ROOM_MAP_BUTTON)#saidao
    time.sleep(1)
    pyautogui.click(*pop_consts.UI_POS_MAP_FAVORITE_TAB)#xingbiao
    time.sleep(0.5)
    pyautogui.click(*pop_consts.UI_POS_MAP_FIRST)#saidao9
    time.sleep(0.5)        
    pyautogui.click(*pop_consts.UI_POS_MAP_CONFIRM_BUTTON)#queren
    time.sleep(1)       

def open_room_9():
    if not goto_duoren_channel():
        return False

    pyautogui.click(*pop_consts.UI_POS_JINGSU)#jingsu
    time.sleep(1)    
    pyautogui.click(*pop_consts.UI_POS_WUXIAN_DANREN)#wuxian
    time.sleep(3)    
    pyautogui.click(*pop_consts.UI_POS_NEW_GAME_BUTTON)#chuangjian
    time.sleep(1)    
    pyautogui.moveTo(*pop_consts.UI_POS_NEW_GAME_JIAMI_CHECKBOX,duration=0.3)#jiami
    pyautogui.click()
    time.sleep(0.5)    
    pyautogui.click(*pop_consts.UI_POS_NEW_GAME_AI_CHECKBOX,duration=0.3)#ai
    pyautogui.click()
    time.sleep(0.5)    
    pyautogui.click(*pop_consts.UI_POS_NEW_GAME_PASSWORD_FIELD)#mima
    time.sleep(0.5)        
    pyautogui.typewrite('qq1',0.1)
    pyautogui.click(*pop_consts.UI_POS_NEW_GAME_CONFIRM_BUTTON)#queding
    time.sleep(4)        
    select_map_in_fav()
    time.sleep(4)
    return True



 
def autorun9(round_limit=5,is_limit_finish=True):
 
    account = global_state.current_account
    failed_rounds_consecutive = 0

    global_state.start_run_task(AUTORUN9_TASK_NAME, round_limit, counting_succeed=is_limit_finish)

    opened = open_room_9()
    if not opened:
        logger.critical('failed to open room 9, stop autorun for account:%s', account)
        return False

    try:
        while True:
           
            run_finished = run9()

            if run_finished:
                failed_rounds_consecutive = 0
            else:
                failed_rounds_consecutive += 1
                logger.debug(f'9 run failed for account:{account}, consecutive failed rounds: {failed_rounds_consecutive}')
                if failed_rounds_consecutive >= MAX_CONSECUTIVE_FAILURES:
                    logger.critical(f'Max consecutive failures reached for account:{account}, stopping autorun9')
                    break
 
            if global_state.refresh_run_task(run_finished): 
                break
  
 
    except NeedRelaunchError:
        logger.debug('need relaunch, stop autorun, account:%s', account)
        return False
    except Exception:
        logger.exception('unknown exception, stop autorun, account:%s', account)
        return False
 
    logger.critical(f'autorun9 end for account:{account}, round limit: {round_limit}, consecutive failed rounds: {failed_rounds_consecutive}')
    return True


def wait_until_room_ready():

    for i in range(50):
        loc1 = pyautogui.locateOnScreen(r'pics\dklj.png',confidence=0.9)
        if loc1!=None:
            logger.debug('connection failed, need to restart')
            pyautogui.click(693,465)#queding
            raise NeedRelaunchError()

        pyautogui.click(750,613)#guoqi
        pyautogui.click(657,544)#qiandao 1     
        time.sleep(1)        
        pyautogui.click(1110,123)#qiandao 2
        pyautogui.click(685,574)

        loc2 = pyautogui.locateOnScreen(r'pics\zbing.png',confidence=0.9)
        if loc2!=None:
            logger.debug('play is ready')
            return True
            
        time.sleep(1)
    
    return False

def wait_until_rush_finish():

    for rrr in range(20):
        loc = pyautogui.locateOnScreen(r'pics\kl.png',confidence=0.8)    
        if loc!=None:
            logger.debug(f'found kl.png at location: {loc}')
            return True
            
        time.sleep(1)
    
    return False

def run9():
    
    if not wait_until_room_ready():
        logger.debug('room is not ready, return')
        return False
 
    pop_auto.run9_blind()
  
    return wait_until_rush_finish()


 
def goumai(slot,lv1=0,lv2=0, scrolls=0):
    pyautogui.click(*pop_consts.UI_ICON_POS_SHOP)
    time.sleep(3)

    #level 1
    if(lv1>0):
        lv1x=pop_consts.UI_SHOP_LV_BASE_POS_X + (lv1-1)*pop_consts.UI_SHOP_LV_BASE_POS_OFFSET_X
        pyautogui.click(lv1x,pop_consts.UI_SHOP_LV1_BASE_POS_Y)#720/790/860
        time.sleep(0.5)
 
    #level 2
    if(lv2>0):
        lv2x=pop_consts.UI_SHOP_LV_BASE_POS_X + (lv2-1)*pop_consts.UI_SHOP_LV_BASE_POS_OFFSET_X
        pyautogui.click(lv2x,pop_consts.UI_SHOP_LV2_BASE_POS_Y)
        time.sleep(0.5)

    if(scrolls>0):
        pyautogui.click(*pop_consts.UI_SHOP_GOODS_SCROLL_POS)#bottom scroll
        time.sleep(0.5)

    slot_x = pop_consts.UI_SHOP_SLOT_BASE_POS_X + ((slot-1)%3)*pop_consts.UI_SHOP_SLOT_BASE_POS_OFFSET_X
    slot_y = pop_consts.UI_SHOP_SLOT_BASE_POS_Y + ((slot-1)//3)*pop_consts.UI_SHOP_SLOT_BASE_POS_OFFSET_Y    

    pyautogui.click(slot_x, slot_y)   
    time.sleep(0.5)
    
    time.sleep(0.3)
    pyautogui.click(*pop_consts.UI_SHOP_PRICE_POS)#price
    time.sleep(0.3)
    pyautogui.click(*pop_consts.UI_SHOP_PRICE_FIRST_POS)#first price
    time.sleep(0.3)
    pyautogui.click(*pop_consts.UI_SHOP_BUY_BUTTON_POS)#goumai
    time.sleep(0.3)
    pyautogui.press('return')
    time.sleep(0.1)
    pyautogui.press('return')
    time.sleep(0.1)
    pyautogui.press('return')
    time.sleep(1)

def jianglixiang():
    pyautogui.click(*pop_consts.UI_ICON_POS_BOX)
    time.sleep(0.5)    
    pyautogui.click(*pop_consts.UI_BOX_ALL_BUTTON_POS)
    time.sleep(3)      
    pyautogui.press('esc')    
    time.sleep(0.5)      
    pyautogui.press('esc')
    time.sleep(1)      
    pyautogui.press('esc')    
    time.sleep(1)     


def dafuweng():
    for i in range(1000):
        time.sleep(1)
        loc = None
        if(i%5==0):
            logger.debug('checking wdsz')
            loc = pyautogui.locateOnScreen(r'pics\wdsz.png')
        
        if(loc==None):
            logger.debug('dafuweng runing:'+str(i))
            pyautogui.click(978,566)
            pyautogui.press('return')
        else:
            break
    
    logger.debug('dafuweng finished')


def lingqu_shenmi(acc,hh):
    pyautogui.click(250,734)#shenmi
    time.sleep(3)
 
    takeTimes()
    time.sleep(1)
    tt = readTimes()
    logger.debug(f'Shenmi times: {tt}')
 
    if tt==[0,0]:
        logger.debug('shenmi time reached..................')
          
        pyautogui.click(684,585)
        time.sleep(10)
        #jieguo
        npath = os.path.join('pics','shenmi',acc+'#'+str(hh)+'@'+str(datetime.now()).replace(':','')+'.png')
        pyautogui.screenshot(npath)
        pyautogui.click(684,585)
        time.sleep(1)
        takeTimes()
        time.sleep(1)
        tt = readTimes()
        
        if 1==2:#(tt==[0,30]):
            pyautogui.click(684,585)
            time.sleep(0.5)
            pyautogui.click(614,493)#kaiqi        
            time.sleep(10)
            
            loc = pyautogui.locateOnScreen(r'pics\clbz.png',confidence=0.9)
            
            if loc==None:
                #jieguo
                npath = os.path.join('pics','shenmi',acc+'#'+str(hh)+'@'+str(datetime.now()).replace(':','')+'.png')
                pyautogui.screenshot(npath)
                pyautogui.click(684,585)
                time.sleep(1)
                takeTimes()
                time.sleep(1)
                tt = readTimes()                
            else:
                pyautogui.click(685,459)#queding
                
        
        logger.debug(f'Shenmi times after processing: {tt}')
    
    pyautogui.click(1335,50)
 
    return tt

def takeTimes():
    pyautogui.screenshot(r"pics\xs.png", region=(518, 460, 73, 53))
    pyautogui.screenshot(r"pics\fz.png", region=(685, 460, 81, 53))    
   
def readTimes():
    xs=0
    fz=0
    with open(r'pics\xs.png','rb') as f:
        imb = f.read()
        result = d4ocr.classification(imb)
        
        if result.isdigit():
            xs=int(result)
 
    with open(r'pics\fz.png','rb') as f:
        imb = f.read()
        result = d4ocr.classification(imb)
        
        if result.isdigit():
            fz=int(result)        
 
    return [xs,fz]
 




if __name__ == '__main__':
    setup_logging()
    time.sleep(3)
    #goumai(slot=9,lv1=5,lv2=6,scrolls=1)
    #autorun9(6)
    #dafuweng()
    autorun9(round_limit=10,is_limit_finish=True)
    #logger.debug(f'autorun9 completed, current round:{current_round}, success round: {finish_round}, round limit: {round_limit}')
    time.sleep(2)



