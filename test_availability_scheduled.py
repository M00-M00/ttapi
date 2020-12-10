import argparse
from general import TomTomApi
import data_structures as ds
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

api = TomTomApi()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour="8-20")
def scheduled_job():
    api = EV_Search()
    api.temporary_ev_availability([8898,7654], "availability_test.json")


sched.start()