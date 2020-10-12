
from ev import EV_Search
import data_structures as ds
from pytz import utc
from datetime import datetime
 
 
api = EV_Search()
api.temporary_ev_availability([8898,7654], "availability_test.json")