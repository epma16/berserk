"""The client side of the I/O-bound Berserk benchmark"""

from datetime import datetime

import requests

from log import log
from berserk import finalize, cpu

def send_requests(tasks, task_size):
    params = {'tasks': tasks, 'task_size': task_size}
    response = requests.get(conf.berserk_server_url, params=params)
    result = response.json()['result']
    log(result)

def run_from_conf(conf):
    log("------------------\nBERSERK BENCHMARK\n------------------")
    dt1 = datetime.now()
    log("#start %s" % (str(dt1)))

    tasks, task_size = conf.tasks, conf.task_size
    tasks_remote = int(round(tasks * conf.remote_task_ratio))
    tasks_local =  tasks - tasks_remote

    done_tasks_local = 0
    done_tasks_remote = 0
    tasks_remote_round = tasks_remote / conf.local_remote_rounds
    tasks_local_round = tasks_local / conf.local_remote_rounds

    # interlace local and remote tasks
    while done_tasks_local< tasks_local and done_tasks_remote< tasks_remote:
        # send requests to berserk-server and collect the results
        log('Sending {} remote tasks'.format(tasks_remote_round))
        send_requests(tasks_remote_round, task_size)
        done_tasks_remote += tasks_remote_round
        log('Doing {} local tasks'.format(tasks_local_round))
        cpu(tasks_local_round, task_size)
        done_tasks_local += tasks_local_round

    dt2 = datetime.now()
    log("#end %s" % (str(dt2)))
    dt_runtime = dt2-dt1
    log("#runtime %s (%d s)" % (str(dt_runtime), dt_runtime.seconds))
    #results = {"dt_runtime": dt_runtime, "runtime": duration}
    results = (dt1, dt2)
    try:
        finalize(results)
    except Exception as e:
        log("Warning: Can't notify benchmark master. {}".format(str(e)))

if __name__ == "__main__":
    import conf
    run_from_conf(conf)
