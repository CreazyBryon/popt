import sys

import pyautogui
import time

import pop_login
import pop_controller

from datetime import datetime, timedelta

from utils.d4 import d4ocr
import logging
from utils.logging_config import setup_logging
logger = logging.getLogger(__name__)


def readHistory():
    logger.debug('readHistory....................')
    text_file = open("smt.txt", "r")
    lines = text_file.readlines()
    text_file.close()
    
    accounts={}
 
    for line in lines:
        aitem=line.strip()
        if(len(aitem)>0):
            acc, dt, hh = aitem.split('@')
            accounts[acc]=[datetime.strptime(dt,'%Y-%m-%d %H:%M:%S.%f'),int(hh)]
    
    return accounts

 
shm_account_states=readHistory()

  
def saveHistory():
    logger.debug('saveHistory....................')
    with open('smt.txt', 'w') as file:
        for key, value in shm_account_states.items():
            file.write(f'{key}@{value[0]}@{value[1]}\n')    



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
 

def do_lingqu(acc,ttt,hh):
    
    current_datetime = datetime.now()
 
    if(ttt<current_datetime):
        logger.debug('time reached, start lingqu, account:%s', acc)
  
        pyautogui.press('ctrl')#active screen
        isLoged = pop_login.login2(acc)
        if not isLoged:
            logger.debug('login failed, account:%s', acc)
            return -1
        

        logger.debug('lingqu jiangli')
        pop_controller.jianglixiang()
        #pop_controller.goumai(slot=4,lv1=1,lv2=0,scrolls=1)

        #lingqu shenmi
        logger.debug('lingqu shenmi, account:%s, ttt:%s, hh:%s', acc, ttt, hh)
        h1,m1=lingqu_shenmi(acc,hh)
        
        if(h1==0 and m1==0):
            logger.critical('linqu failed, account:%s', acc)
            return -1
        
        new_time = datetime.now() + timedelta(hours=h1,minutes=(m1+1))
        shm_account_states[acc]=[new_time,h1]
        logger.critical('lingqu success, account:%s, next time:%s', acc, new_time)
 
        return 0
    else:
        time_left=ttt-current_datetime
        logger.debug('%s, left:%s, hh:%s', acc, time_left, hh)
        return time_left.total_seconds()
    

 

def shenmi_start(is_close=False):
    shm_round=0
    shm_box_count=0
    logger.debug('shenmi_start, is_close:%s', is_close)

    while True:
        shm_round=shm_round+1
        logger.debug('round:%s;box:%s', shm_round, shm_box_count)
        open_count=0
        last_account=None
        min_left_time=9999999
        
        for acc in shm_account_states:
            dt,hh = shm_account_states[acc]
            box_left_time = do_lingqu(acc,dt,hh)

            if box_left_time==0:
                open_count=open_count+1
                shm_box_count = shm_box_count+1
                last_account = acc
                saveHistory()
            elif box_left_time>0:
                if box_left_time<min_left_time:
                    min_left_time=box_left_time

       
        if(last_account!=None):
            logger.debug('last account=%s', last_account)    
            if is_close:
                logger.debug('close after one time lingqu, break')
                pop_login.kill_kt()
        
        #if min_left_time>1200:
        if 1==2:
            logger.debug('start auto run......')
            pop_controller.autorun9(round_limit=5,is_limit_finish=True)
   
        logger.debug('finished, open box:%s; total box:%s, next time:%s', open_count, shm_box_count, min_left_time)
    
        time.sleep(60)



if __name__ == '__main__':
    setup_logging()
    time.sleep(2)
    auto_round_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    is_close_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    logger.debug(f'Input arguments: auto_round={auto_round_arg}, is_close={is_close_arg}')

    if auto_round_arg > 0:
        pop_controller.autorun9(round_limit=auto_round_arg,is_limit_finish=True)

    shenmi_start(is_close=(is_close_arg == 1))