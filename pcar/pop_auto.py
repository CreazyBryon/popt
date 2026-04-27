import time
from utils import win32_native as mykb
from utils.state import global_state

#scan codes
SC_UP    = 0x48
SC_LEFT  = 0x4B
SC_RIGHT = 0x4D
SC_DOWN  = 0x50

SC_F5 = 0x3F 
SC_CTRL=0x1D
SC_SPACE=0x39
SC_ESC=0x01
SC_ENTER=0x1C
SC_SHIFT=0x2A

 

def run9_blind():
    
    mykb.press(SC_F5)
    time.sleep(10)
    print('start running, hold up')
    global_state.check_run_task()
    time.sleep(5)
    mykb.hold(SC_UP) #hold up
    time.sleep(2)

    # --- PHASE 1: THE SPIRAL (0 to 85) ---
    print('Entering spiral...')
    for i in range(86): 
        mykb.hold(SC_RIGHT)
        time.sleep(0.5)#turn right for 0.5s
        mykb.release(SC_RIGHT)
        time.sleep(0.4)#run straight for 0.4s

    # --- PHASE 2: THE STRAIGHTAWAY (86 to 91) ---
    # (These slight right taps might be correcting for drift)
    print('Entering straightaway...')
    for i in range(6): 
        mykb.hold(SC_RIGHT)
        time.sleep(0.3)#turn right for 0.3s
        mykb.release(SC_RIGHT)
        time.sleep(1.5)#run straight for 1.5s

    print('route finished, stop turning, waiting 10 seconds')
    time.sleep(10)
    mykb.release(SC_UP)#drive end
    print('drive end, release up, checking result')




def isHit9RoadSign(duration):

    start_time = time.monotonic()
    while time.monotonic() - start_time < duration:
        color = mykb.get_pixel(535, 70)
        if color == (255, 0, 0): # Red color
            return True
        time.sleep(0.05)  # Check every 50ms

    return False

def run9_eye():
    
    mykb.press(SC_F5)
    time.sleep(15)
    print('start running, hold up')
    mykb.hold(SC_UP) #hold up
    time.sleep(2)

    # --- PHASE 1: THE SPIRAL (0 to 85) ---
    print('Entering spiral...')

    for i in range(80): 
        mykb.hold(SC_RIGHT)
        time.sleep(0.5)#turn right for 0.5s
        mykb.release(SC_RIGHT)
        time.sleep(0.4)#run straight for 0.4s

    # --- PHASE 2: CHECK COLOR AND DECIDE WHETHER TO BREAK THE SPIRAL ---
    for i in range(10): 
        mykb.hold(SC_RIGHT)
        isHitColor = isHit9RoadSign(0.5)#check if hit the color while turning for 0.5s
        mykb.release(SC_RIGHT)

        if(isHitColor):
            print('hit color, break the spiral, entering straightaway...')
            break

        isHitColor = isHit9RoadSign(0.4)

        if(isHitColor):
            print('hit color, break the spiral, entering straightaway...')
            break
        

    # --- PHASE 3: THE STRAIGHTAWAY (86 to 91) ---
    # (These slight right taps might be correcting for drift)
    print('Entering straightaway...')
    for i in range(6): 
        mykb.hold(SC_RIGHT)
        time.sleep(0.3)#turn right for 0.3s
        mykb.release(SC_RIGHT)
        time.sleep(1.5)#run straight for 1.5s

    print('route finished, stop turning, waiting 10 seconds')
    time.sleep(10)
    mykb.release(SC_UP)#drive end
    print('drive end, release up, checking result')
  




def isRunFinished():
    # Check if th color at (100, 200) is red, which indicates the run has finished
    color = mykb.get_color(100, 200)
    return color == 789516 # RGB(12, 12, 12) in decimal


def isApproachingLeftWall():
    # Check if the color at (50, 300) is a specific shade of gray, which indicates approaching left wall
    color = mykb.get_color(50, 300)
    return color == 789516 # RGB(12, 12, 12) in decimal

def isApproachingRightWall():
    # Check if the color at (200, 300) is a specific shade of gray, which indicates approaching right wall
    color = mykb.get_color(200, 300)
    return color == 789516 # RGB(12, 12, 12) in decimal


def runLvZhou_blind():

    mykb.press(SC_F5)
    time.sleep(15)
    print('start running, hold up')
    mykb.hold(SC_UP) #hold up
    time.sleep(2)

    print('Entering route...')

    for i in range(150): 
        mykb.press(SC_CTRL)      
        mykb.press(SC_SPACE)
        time.sleep(1)#attack every 1s

    print('route finished, stop turning, waiting 10 seconds')
    time.sleep(10)
    mykb.release(SC_UP)#drive end
    print('drive end, release up, checking result');



def runLvZhou_eye():

    mykb.press(SC_F5)
    time.sleep(15)
    print('start running, hold up')
    mykb.hold(SC_UP) #hold up
    time.sleep(2)

    print('Entering route...')

    turn_start_time = time.monotonic() - 2 # Initialize to allow immediate turning

    for i in range(150): 
        if i>100 and isRunFinished():
            print('run finished, break the loop')
            mykb.release(SC_UP)#drive end
            break

        if isApproachingLeftWall():
            print('approaching left wall, turn right, only turn 1 time inside a second, in case of over turning')

            if time.monotonic() - turn_start_time > 1: # Only turn if more than 1 second has passed since last turn
                mykb.hold(SC_RIGHT)
                time.sleep(0.3)
                mykb.release(SC_RIGHT)
                turn_start_time = time.monotonic() # Update last turn time
                
        elif isApproachingRightWall():
            print('approaching right wall, turn left, only turn 1 time inside a second, in case of over turning')

            if time.monotonic() - turn_start_time > 1: # Only turn if more than 1 second has passed since last turn
                mykb.hold(SC_LEFT)
                time.sleep(0.3)
                mykb.release(SC_LEFT)
                turn_start_time = time.monotonic() # Update last turn time

        mykb.press(SC_CTRL)      
        mykb.press(SC_SPACE)
        time.sleep(0.5)#attack every 1s

    print('route finished, stop turning, waiting 10 seconds')

    print('drive end, release up, checking result');


if __name__ == "__main__":
    time.sleep(5) # Time to switch to the game window
    runLvZhou_blind()