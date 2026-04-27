import global_state
import time
import com_Keyboard as ckb


def findTargetArea():
    target_start_x=0
    target_end_x=0

    for i in range(global_state.fish_bar_start_x, global_state.fish_bar_end_x, 1):
        pix = ckb.get_pixel(i, global_state.fish_bar_y)
        
        if target_start_x==0 and pix == global_state.fish_target_area_color: 
                print('target area start found')
                target_start_x = i
        
        if target_start_x>0 and pix != global_state.fish_target_area_color:
            print('target area end found')
            target_end_x = i
            break
 
        time.sleep(0.01)

    return target_start_x, target_end_x


def trackCursor():

    start_x_time=None
    end_x_time=None

    while True:
        pix1 = ckb.get_pixel(global_state.fish_bar_start_x, global_state.fish_bar_y)

        if pix1 == global_state.fish_cusor_color:
            print('target area found')
            start_x_time = time.time()   
  
        pix2 = ckb.get_pixel(global_state.fish_bar_end_x, global_state.fish_bar_y)

        if pix2 == global_state.fish_cusor_color:
            print('target area found')
            end_x_time = time.time()

        if start_x_time and end_x_time:
            break

    if start_x_time and end_x_time:
        global_state.fish_cusor_start_x_time=start_x_time
        global_state.fish_cusor_speed = (global_state.fish_bar_end_x - global_state.fish_bar_start_x) / abs(end_x_time - start_x_time)
        print('cursor speed:', global_state.fish_cusor_speed, 'start time:', global_state.fish_cusor_start_x_time)
        return True
    
    return False


def hitting():
    t_x_start,t_x_end = findTargetArea()
    if t_x_start==0 or t_x_end==0:
        print('target area not found, stop fishing')
        return False

    print('target area:', t_x_start, t_x_end)
    isTracked=trackCursor()

    if isTracked:
        print('start to hitting target area')
        #predict when will cursor come to target area, and hit space then, the cusor is moving back and forth between bar start and end, so we can predict when it will come to target area
        while True:
            current_time = time.time()
            elapsed_time = current_time - global_state.fish_cusor_start_x_time
            current_x = global_state.fish_bar_start_x + (elapsed_time * global_state.fish_cusor_speed) % (global_state.fish_bar_end_x - global_state.fish_bar_start_x)

            if t_x_start <= current_x <= t_x_end:
                print('hitted, current x:', current_x)
                ckb.pressKey(0x20) # space
                time.sleep(3)
                print('finished')
                return True
            
            time.sleep(0.01)

    return False
 

def fishing():
    print('press space to start fishing')
    ckb.pressKey(0x20) # space
  
    hitted = hitting()

    if hitted:
        print('hook bite, start to fighting')
        
        for i in range(10):
            time.sleep(0.5)
            hitted = hitting()
            if hitted:
                print('reel good, continue')
            else:
                print('fish catched')
                break

        time.sleep(3)
        ckb.pressKey(0x20) # space
        print('finished')
        return True

    return False


if __name__ == '__main__':
    print('start fishing')
    time.sleep(2)

    for i in range(10):
        print('fishing round:', i+1)
        success = fishing()
        if not success:
            print('fishing failed, try again')
            time.sleep(2)
        else:
            print('fishing success, wait for next round')
            time.sleep(5)




