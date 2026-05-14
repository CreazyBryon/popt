import pop_login
import pop_controller
import time
  
from utils.logging_config import setup_logging

setup_logging()

def play(acc):
    if not acc:
        print('cancel play, empty account provided')
        return
 
    logged = pop_login.login2(acc)

    if not logged:
        print(f'cancel play, login failed for account: {acc}')
        return
    
    print('lingqu jiangli')
    pop_controller.jianglixiang()
    #print('gou mai')
    #pop_controller.goumai(slot=4,lv1=1,lv2=0,scrolls=1)
    pop_controller.autorun9(5)
    #print('shen mi')
    #pop_shm.shenmi()
    time.sleep(5)


def plays(accs):

    for acc in accs:
        play(acc)

    #print('shen mi')
    #pop_shm.shenmi()

def play2(acc_num):
    acc = get_acc_from_num(acc_num)
    play(acc)

def play2s(acc_nums):
    for acc_num in acc_nums:
        play2(acc_num)

def st(accs):

    for acc in accs:
        pop_login.loginST(acc)
    print('st finished')

def st2(acc_nums):

    for acc_num in acc_nums:
        acc = get_acc_from_num(acc_num)
        pop_login.loginST(acc)
        
    print('st finished')


#tools
def get_acc_from_num(acc_num):
    if acc_num == 5 or acc_num == 6: 
        return f'hsmsyy0{acc_num}'
    else:  
        return f'hsmsyy9{acc_num}'


if __name__ == '__main__':
    print('hello world')
    time.sleep(3)
    # Example usage
    #pop_login.login2('1234567890')
    pop_controller.autorun9(5)
    time.sleep(3)