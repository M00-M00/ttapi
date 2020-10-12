import argparse
from ev import EV_Search
import data_structures as ds
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour="3-20", minute = "51")
def scheduled_job():
    api = EV_Search()
    api.temporary_ev_availability([8898,7654], "availability_test.json")


sched.start()