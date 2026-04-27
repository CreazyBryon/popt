import pop_login
import pop_controller
import time
  
from utils.logging_config import setup_logging

setup_logging()

def play(acc):
 
    pop_login.login2(acc)
    print('lingqu jiangli')
    pop_controller.jianglixiang()
    #print('gou mai')
    #pop_controller.goumai(slot=4,lv1=1,lv2=0,scrolls=1)
    pop_controller.autorun9(10)
    print('shen mi')
    #pop_shm.shenmi()


def plays(accs):

    for acc in accs:
        play(acc)

    #print('shen mi')
    #pop_shm.shenmi()

def st(accs):

    for acc in accs:
        pop_login.loginST(acc)
    print('st finished')


if __name__ == '__main__':
    print('hello world')
    # Example usage
    #pop_login.login2('1234567890')
    #pop_controller.run9()