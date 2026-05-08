import pop_player 
import sched
import time
from datetime import datetime, timedelta

scheduler = sched.scheduler(time.time, time.sleep)

def do_task():
    print(f'Starting scheduled autorun9 task at {datetime.now()}')
    pop_player.st(['hsmsyy91','hsmsyy92','hsmsyy94','hsmsyy05','hsmsyy06','hsmsyy97','hsmsyy98','hsmsyy99'])
    print(f'Finished scheduled autorun9 task at {datetime.now()}')

if __name__ == '__main__': 
    #pop_player.st(['hsmsyy91','hsmsyy92','hsmsyy94','hsmsyy05','hsmsyy06','hsmsyy97','hsmsyy98','hsmsyy99'])
    # Choose a time today
    run_time = datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)

    # If time already passed, schedule for tomorrow
    if run_time < datetime.now():
        run_time += timedelta(days=1)

    scheduler.enterabs(run_time.timestamp(), 1, do_task)
    scheduler.run()
