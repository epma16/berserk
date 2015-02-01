"""The client side of the I/O-bound Berserk benchmark"""

from datetime import datetime

import requests

from log import log
from berserk import finalize

def run_from_conf(conf):
    log("------------------\nBERSERK BENCHMARK\n------------------")
    dt1 = datetime.now()
    log("#start %s" % (str(dt1)))

    # send requests to berserk-server and collect the results
    # TODO: server-side

    dt2 = datetime.now()
    log("#end %s" % (str(dt2)))
    dt_runtime = dt2-dt1
    log("#runtime %s (%d s)" % (str(dt_runtime), dt_runtime.seconds))
    #results = {"dt_runtime": dt_runtime, "runtime": duration}
    results = (dt1, dt2)
    try:
        finalize(results)
    except:
        log("Warning: Can't notify the benchmark master of the outcome.")

if __name__ == "__main__":
    #sample_run()
    import conf
    run_from_conf(conf)
