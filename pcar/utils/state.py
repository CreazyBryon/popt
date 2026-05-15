from datetime import datetime, timezone
import logging 
logger = logging.getLogger(__name__)

class AutoRunTask:
    def __init__(self):
        self.map_name = "" 
        self.counting_succeed = True
        self.total_round = 0
        self.finished_round = 0
        self.succeed_round = 0

        #read only, set when task start
        self.startedAt = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        self.completedAt = None
 

class GlobalState:
    def __init__(self):
        self.current_account = None
 
        self.fish_target_area_start_x = 0
        self.fish_target_area_end_x = 0
        self.fish_cusor_start_x_time = None
        self.fish_cusor_speed = 0

        self.current_task = None
        self.task_history = []


    def start_run_task(self, map_name, total_round, counting_succeed=True):
        task = AutoRunTask()
        task.map_name = map_name
        task.total_round = total_round
        task.counting_succeed = counting_succeed

        if self.current_task is not None:
            self.task_history.append(self.current_task)

        self.current_task = task
 
        logger.critical(f'Starting [{self.current_account}],total:{total_round},isfinish:{counting_succeed}')

 

    def refresh_run_task(self, succeed):
        if self.current_task is None:
            logger.warning("No current task to refresh")
            return True

        task = self.current_task

        if task.completedAt is not None:
            return True

        task.finished_round += 1
        if succeed:
            task.succeed_round += 1

        logger.info(
            f'[{self.current_account}],'
            f'round:{task.finished_round},'
            f'success:{task.succeed_round},'
            f'total:{task.total_round}'
        )

        rounds_finished = task.finished_round >= task.total_round
        all_succeeded = task.succeed_round >= task.total_round

        is_completed = rounds_finished and (
            all_succeeded if task.counting_succeed else True
        )

        if is_completed:
            task.completedAt = datetime.now(timezone.utc).isoformat(
                timespec="milliseconds"
            ).replace("+00:00", "Z")
            logger.critical(
                f'Autorun task completed for account:{self.current_account}, '
                f'total rounds: {task.total_round}, '
                f'successful rounds: {task.succeed_round}'
            )

        return is_completed    
    
    def check_run_task(self):
        if self.current_task is None:
            logger.error("No current task to check")
            return False
         
        logger.error(f'[{self.current_account}],round:{self.current_task.finished_round},success:{self.current_task.succeed_round},total:{self.current_task.total_round}')
 

global_state = GlobalState()