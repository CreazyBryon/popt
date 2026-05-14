import glob

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
 
_spare_card=''

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

def goto_jingsu_channel():
    jingsu_pixel = pyautogui.pixel(*pop_consts.UI_POS_DUOREN_TITLE)

    if jingsu_pixel == pop_consts.UI_POS_DUOREN_TITLE_COLOR:
        logger.debug('jingsu icon is visible, click to enter jingsu channel')
        pyautogui.click(*pop_consts.UI_POS_JINGSU)#jingsu
        time.sleep(2)
        return True
    else:
        logger.debug('jingsu icon invisible, stopping')
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

    if not goto_jingsu_channel():
        return False

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
        pyautogui.click(686,575)#shengji tongzhi

        pix = pyautogui.pixel(1063, 678)
        if pix==(40,136,255):
            logger.debug('play is ready')
            return True
            
        time.sleep(1)
    
    return False


def run9():
    
    if not wait_until_room_ready():
        logger.debug('room is not ready, return')
        return False
 
    return pop_auto.run9_blind()
   
 
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
        
        if (tt==[0,30]):
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
    time.sleep(1)
 
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
 
def do_caiquan0():
    time.sleep(2)

    for i in range(100):
        caiquan3()
 
def do_caiquan():
    time.sleep(2)
    logger.critical('caiquan started, will run 100 rounds')
    for i in range(100):
        caiquan0()
        if i%10==0:
            logger.critical(f'caiquan round {i} completed')

    logger.critical('caiquan finished all rounds')

def caiquan_return():

    robo_possibles = rps_robot_throwing()
    click_pos = pop_consts.RPS_SHI_POS # default shi

    if robo_possibles is not None:
        logger.debug(f'caiquan robot possibles: {robo_possibles}')
        if 'jian' == robo_possibles:
            if 'jian' == _spare_card:
                logger.debug('caiquan has spare jian card, click jian to draw')
                click_pos = pop_consts.RPS_JIAN_POS
            else:
                click_pos = pop_consts.RPS_SHI_POS
        elif 'shi' == robo_possibles:
            if 'shi' == _spare_card:
                logger.debug('caiquan has spare shi card, click shi to draw')
                click_pos = pop_consts.RPS_SHI_POS
            else:
                click_pos = pop_consts.RPS_BU_POS
        elif 'bu' == robo_possibles:
            if 'bu' == _spare_card:
                logger.debug('caiquan has spare bu card, click bu to draw')
                click_pos = pop_consts.RPS_BU_POS
            else:
                click_pos = pop_consts.RPS_JIAN_POS
        elif 'shi_bu' == robo_possibles:
            click_pos = pop_consts.RPS_BU_POS      
        elif 'jian_bu' == robo_possibles:
            click_pos = pop_consts.RPS_JIAN_POS
        elif 'jian_shi' == robo_possibles:
            click_pos = pop_consts.RPS_SHI_POS

    if click_pos is not None:
        logger.debug(f'caiquan click position: {click_pos}')
        pyautogui.click(click_pos)

        for i in range(10):
            time.sleep(0.5)
            pix = pyautogui.pixel(*pop_consts.RPS_RESULT_POS)
            if pix==pop_consts.RPS_RESULT_DRAW_COLOR:
                logger.debug('caiquan result is draw, give up and return') 
                return False
            
            if pix==pop_consts.RPS_RESULT_WIN_COLOR:
                logger.debug('caiquan result is win, continue to next round') 
                return True
    
    print('caiquan result is unknown, something may be wrong, stopping')
    return False

def caiquan_return0():
    robo_possibles = rps_robot_throwing()
    click_pos = pop_consts.RPS_SHI_POS # default shi

    if robo_possibles is not None:
        logger.debug(f'caiquan robot possibles: {robo_possibles}')
        if 'jian' == robo_possibles:
            click_pos = pop_consts.RPS_SHI_POS
        elif 'shi' == robo_possibles:
            click_pos = pop_consts.RPS_BU_POS
        elif 'bu' == robo_possibles:
            click_pos = pop_consts.RPS_JIAN_POS
        elif 'shi_bu' == robo_possibles:
            click_pos = pop_consts.RPS_BU_POS      
        elif 'jian_bu' == robo_possibles:
            click_pos = pop_consts.RPS_JIAN_POS
        elif 'jian_shi' == robo_possibles:
            click_pos = pop_consts.RPS_SHI_POS

    if click_pos is not None:
        logger.debug(f'caiquan click position: {click_pos}')
        pyautogui.click(click_pos)

        for i in range(10):
            time.sleep(0.5)
            pix = pyautogui.pixel(*pop_consts.RPS_RESULT_POS)
            if pix==pop_consts.RPS_RESULT_DRAW_COLOR:
                logger.debug('caiquan result is draw, give up and return') 
                return False
            
            if pix==pop_consts.RPS_RESULT_WIN_COLOR:
                logger.debug('caiquan result is win, continue to next round') 
                return True
    
    print('caiquan result is unknown, something may be wrong, stopping')
    return False

def wait_caiquan_dialog_up():
    for i in range(30):
        time.sleep(1)
        pix = pyautogui.pixel(*pop_consts.RPS_RESULT_DIALOG_POS)
        if pix==pop_consts.RPS_RESULT_DIALOG_COLOR:
            logger.debug('caiquan dialog is up')  
            return True

    logger.debug('caiquan dialog is not up')  
    return False

def is_rps_level_5():
    pix = pyautogui.pixel(1000,321)
    return pix==(8,61,105)

def is_any_card_empty():
    loc = pyautogui.locateOnScreen(r'pics\card_empty.png', confidence=0.7, region=(278, 676, 520, 32))
    return loc is None


def caiquan3():
    pyautogui.click(390,200)#x_offset=80,y_offset=80
    time.sleep(1)

    #if is_any_card_empty():
      #  print('card empty')
    #    return False
 
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#jixu
    time.sleep(2)
  
    caiquan_return()

    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear, something may be wrong')
        return False
    
    logger.debug('caiquan result 1 is out')  
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok
    time.sleep(2)    
 
    caiquan_return()

    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear for round 2, something may be wrong')
        return False
 
    logger.debug('caiquan result 2 is out')  
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok
     
    for i in range(20):
        time.sleep(2)
        cres= caiquan_return()
        dig = wait_caiquan_dialog_up()
        if not dig:
            logger.debug(f'caiquan result dialog did not appear for round {i+3}, something may be wrong')
            return False 

        if is_rps_level_5() and cres:
            logger.debug(f'caiquan level is 5, quit and lingqu bonus')
            pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_CANCEL_POS)#cancel
            time.sleep(1)
            pyautogui.click(*pop_consts.RPS_RESULT_BONUS_POS)#lingqu
            time.sleep(1)   
            return True     
            
        logger.debug(f'caiquan result {i+3} result is {"win" if cres else "draw"}, continue')  
        pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok

    return True

def caiquan():
    pyautogui.click(390,200)#x_offset=80,y_offset=80
    time.sleep(1)
 
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#jixu
    time.sleep(2)
  
    caiquan_return()

    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear, something may be wrong')
        return False
    
    logger.debug('caiquan result 1 is out')  
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok
    time.sleep(2)    
 
    caiquan_return()

    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear for round 2, something may be wrong')
        return False
 
    logger.debug('caiquan result 2 is out')  
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok
       
    
    for i in range(3):
        time.sleep(2)
        cres= caiquan_return()
        dig = wait_caiquan_dialog_up()
        if not dig:
            logger.debug(f'caiquan result dialog did not appear for round {i+3}, something may be wrong')
            return False 

        if not cres or i==2:
            logger.debug(f'caiquan result {i+3} is draw, quit and lingqu bonus')
            pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_CANCEL_POS)#cancel
            time.sleep(1)
            pyautogui.click(*pop_consts.RPS_RESULT_BONUS_POS)#lingqu
            time.sleep(1)   
            return          
        else:             
            logger.debug(f'caiquan result {i+3} is win')  
            pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok
  
 


def caiquan2():
    pyautogui.click(390,200)#x_offset=80,y_offset=80
    time.sleep(0.5)
    global_state.caiquan_current_level=1

    while caiquan_go():
        pass

    logger.debug('caiquan finished') 

def caiquan_go():

    pix = pyautogui.pixel(*pop_consts.RPS_RESULT_DIALOG_POS)
    if pix==pop_consts.RPS_RESULT_DIALOG_COLOR:
        logger.debug('caiquan waiting for click') 
        pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#jixu
        time.sleep(1)

    rps_lv = rps_level()
    logger.debug(f'caiquan level: {rps_lv}')
    is_quit=False

    if global_state.caiquan_current_level==rps_lv:
        logger.debug('caiquan level is the same as current level, need to quit')
        is_quit=True
    else:
        global_state.caiquan_current_level = rps_lv

    robo_possibles = rps_robot_throwing()
    click_pos = None

    if robo_possibles is not None:
        logger.debug(f'caiquan robot possibles: {robo_possibles}')
        if 'jian' == robo_possibles:
            click_pos = pop_consts.RPS_SHI_POS
        elif 'shi' == robo_possibles:
            click_pos = pop_consts.RPS_BU_POS
        elif 'bu' == robo_possibles:
            click_pos = pop_consts.RPS_JIAN_POS
        elif 'shi_bu' == robo_possibles:
            click_pos = pop_consts.RPS_BU_POS      
        elif 'jian_bu' == robo_possibles:
            click_pos = pop_consts.RPS_JIAN_POS
        elif 'jian_shi' == robo_possibles:
            click_pos = pop_consts.RPS_SHI_POS

    if click_pos is not None:
        logger.debug(f'caiquan click position: {click_pos}')
        pyautogui.click(click_pos)

        for i in range(30):
            time.sleep(1)
            pix = pyautogui.pixel(*pop_consts.RPS_RESULT_DIALOG_POS)
            if pix!=pop_consts.RPS_RESULT_DIALOG_COLOR:
                logger.debug('caiquan result is out, checking level') 
                if is_quit or rps_lv==5:
                    logger.debug(f'caiquan quit or reach level 5, click jixu to quit, current level: {rps_lv}')
                    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_CANCEL_POS)#cancel
                    time.sleep(1)
                    pyautogui.click(*pop_consts.RPS_RESULT_BONUS_POS)#lingqu
                    return False 
                else:
                    logger.debug(f'caiquan continue to next level, current level: {rps_lv}')
                    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok
                    time.sleep(1)
                    return True
    
    return False


def rps_level(): 
    for i in range(9):
        time.sleep(1)
        pix = pyautogui.pixel(1000,445+30*i)
        if pix==(8,61,105):
            return i+1

    return None
    
def rps_robot_throwing():
    img = pyautogui.screenshot(region=pop_consts.RPS_ROBOT_AREA)   

    cqfiles = glob.glob(os.path.join('pics','cq_*.png'))

    for cqfile in cqfiles:
        loc = pyautogui.locate(cqfile, img, confidence=0.9)
        if loc is not None:
            logger.debug(f'Found match for {cqfile} at location {loc}')
            robo_res = cqfile[8:-4]

            return robo_res
        
        logger.debug('No match found for any cq image')
    
    return None

def caiquan0():
    pyautogui.click(390,200)#x_offset=80,y_offset=80
    time.sleep(1)
 
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#jixu
    time.sleep(2)
  
    caiquan_return()

    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear, something may be wrong')
        return False
    
    logger.debug('caiquan result 1 is out')  
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok
    time.sleep(2)    
 
    caiquan_return()

    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear for round 2, something may be wrong')
        return False
 
    logger.debug('caiquan result 2 is out')  
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_CANCEL_POS)#cancel
    time.sleep(1)
    pyautogui.click(*pop_consts.RPS_RESULT_BONUS_POS)#lingqu
    time.sleep(1)


if __name__ == '__main__':
    setup_logging()
    time.sleep(3)
    #run9()
    #goumai(slot=9,lv1=5,lv2=6,scrolls=1)
    #autorun9(5)
    #dafuweng()
    #autorun9(round_limit=3,is_limit_finish=True)
    #logger.debug(f'autorun9 completed, current round:{current_round}, success round: {finish_round}, round limit: {round_limit}')
    do_caiquan()
    
    time.sleep(2)