import glob
import os
import time
import pyautogui

from utils.state import global_state
import utils.constants as pop_consts

import logging
from utils.logging_config import setup_logging
logger = logging.getLogger(__name__)

_spare_card=''
_target_level=5
_is_quit_on_draw=False

 
def do_caiquan():
    time.sleep(2)
    logger.critical('caiquan started, will run 100 times')
    for i in range(100):
        caiquan0(i+1)
        if i%10==0:
            logger.critical(f'caiquan time {i} completed')

    logger.critical('caiquan finished all times')


def caiquan0(play_time=1):
    pyautogui.click(390,200)#x_offset=80,y_offset=80
    time.sleep(1)

    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear, something may be wrong')
        return False
    
    logger.debug('caiquan start to play the {} time'.format(play_time))

    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#jixu
    time.sleep(2)
    caiquan_return()
    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug('caiquan result dialog did not appear, something may be wrong')
        return False
 
    for i in range(50):
        logger.debug(f'caiquan round {i+2} start')
        is_continue = play_rally()
        if not is_continue:
            break
 


def play_rally():
    time.sleep(2)
    logger.debug(f'play rally with target level {_target_level} and quit on draw={_is_quit_on_draw}')
    is_win = caiquan_return()
    dig = wait_caiquan_dialog_up()
    if not dig:
        logger.debug(f'caiquan result dialog did not appear, something may be wrong')
        return False 
        
    if (is_hit_level(_target_level) and is_win) or (_is_quit_on_draw and not is_win):
        logger.debug(f'caiquan level is hitting {_target_level} or draw, is win={is_win}, quit and lingqu bonus')
        pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_CANCEL_POS)#cancel
        time.sleep(1)
        pyautogui.click(*pop_consts.RPS_RESULT_BONUS_POS)#lingqu
        time.sleep(1)   
        return False     
        
    logger.debug(f'caiquan result is {"win" if is_win else "draw"}, not hit level {_target_level} yet, continue')  
    pyautogui.click(*pop_consts.RPS_RESULT_DIALOG_OK_POS)#ok    
    return True


def is_hit_level(target_level):
    pix = pyautogui.pixel(1000,445-30*(target_level-1))
    return pix==(8,61,105)

def wait_caiquan_dialog_up():
    for i in range(30):
        time.sleep(1)
        pix = pyautogui.pixel(*pop_consts.RPS_RESULT_DIALOG_POS)
        if pix==pop_consts.RPS_RESULT_DIALOG_COLOR:
            logger.debug('caiquan dialog is up')  
            return True

    logger.debug('caiquan dialog is not up')  
    return False
   
 
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
                logger.debug('caiquan result is draw') 
                return False
            
            if pix==pop_consts.RPS_RESULT_WIN_COLOR:
                logger.debug('caiquan result is win') 
                return True
    
    print('caiquan result is unknown, something may be wrong, stopping')
    return False

 


if __name__ == '__main__':
    setup_logging()
    time.sleep(3)
    logger.debug('start to run caiquan')
    do_caiquan()
    time.sleep(2)