import argparse
from general import TomTomApi
import data_structures as ds
from pytz import utc



api = TomTomApi("availability_config.json")

if api.search_type == "by_index_keys":
    api.ev_availability_by_index(api.index_keys, api.availability_data_filename)
elif api.search_type == "by_availability_ids":
    print("checking")
    api.ev_availability_by_availabilty_id(api.availability_ids, api.availability_data_filename)


