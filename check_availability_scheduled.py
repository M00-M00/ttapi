import argparse
from general import TomTomApi
import data_structures as ds
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()


parser = argparse.ArgumentParser()

parser.add_argument("-C" ,"--config", type =str)
args = parser.parse_args()

config = args.config

api = TomTomApi(config)

@sched.scheduled_job('cron', day_of_week=api.days_of_week, hour=api.hours, minute = "0, 15, 30, 45")
def scheduled_job():
    if api.search_type == "by_index_keys":
        api.ev_availability_by_index(api.index_keys, api.availability_data_filename)
    elif api.search_type == "by_availability_ids":
        api.ev_availability_by_availabilty_id(api.availability_ids, api.availability_data_filename)


sched.start()