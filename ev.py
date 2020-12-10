import requests
import json
import asyncio
import time
from datetime import datetime
from general import TomTomApi
import pandas as pd
import json
import asyncio
import time
import data_structures as ds
from general import TomTomApi
import os


class EV_Search(TomTomApi):

    def __init__(self):

                #self.key = "BEAUFvC8jzPyPYNBotRrEIlaOi0fBRPo"
        self.key = "p9QAG7A754ZSfW21em3XPfDdfoaZls1x"
        self.base_url = "api.tomtom.com"
        self.categories_url = "https://" + self.base_url + "/search/2/poiCategories.json?key=" + self.key + "&[language=EN]"
        self.s = requests.Session()
        

        # nearby search results
        self.nearby_results = {}
        # detailed search results 
        self.detailed_results = {}

        self.ev_stations = []

        self.results_dict = {}

        self.failed_brand_search = []
        self.failed_nearby_ids = []
        self.failed_detailed_search_id = []

        #self.poi_categories_json = self.s.get(self.categories_url).json()["poiCategories"]

        self.gas_station_Id = 7311
        self.ev_station_id = 7309

        self.country = "GB"

        self.locId = 0

        self.poiCode = self.ev_station_id 

        self.failed_ids = []

        self.query = "station"

        self.ev_results = []

        self.availability_data = {}


        self.locations = {

            "search_1" : {"lat" :51.208795, "lon": -4.067991,  "radius": 200000 }

            ,"search_2"  : {"lat" :51.046315, "lon": -0.505211, "radius" : 45000}

            ,"search_11" : {"lat": 52.013485,"lon" :-0.341636 ,"radius":50000}

            ,"search_7" : {"lat":51.583442, "lon":0.723850, "radius" :  55000}

            ,"search_8" : {"lat":51.835858, "lon":-0.666779, "radius" : 45000}

            ,"search_9" : {"lat" :52.470408, "lon": 0.949150, "radius": 80000}

            ,"search_3" : {"lat" :53.654690, "lon":  -1.395234  ,"radius": 115000}

            ,"search_6" : {"lat":52.198257, "lon" :-1.093577, "radius":70000}

            ,"search_4" : {"lat" :56.132649, "lon": -3.426368 ,"radius": 190000}

            ,"search_5" : {"lat" :54.738375, "lon":-6.759626 ,"radius": 100000}

            , "search_12" : {"lat":52.199665, "lon":-1.616336, "radius":65000}
            
           , }


        self.results_count = {}
        self.ev_results = []




    def get_ev_stations_for_country(self):

        ofset = 0
        url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url)
        total_results = search_request.json()["summary"]["totalResults"]
        self.ev_stations.extend(search_request.json()["results"])





    def get_results_by_location(self, location):

        ofset = 0
        lat = location["lat"]
        lon = location["lon"]
        radius = location["radius"]
        url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&lat={lat}&lon={lon}&radius={radius}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url)
        total_results = search_request.json()["summary"]["totalResults"]
        self.ev_stations.extend(search_request.json()["results"])

        for ofset in range(0, total_results, 100):
            print(ofset)
            url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&lat={lat}&lon={lon}&radius={radius}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
            search_request = self.s.get(url)
            time.sleep(0.5)
            try:
                self.ev_stations.extend(search_request.json()["results"])
            except:
                print("error at: " + str(ofset) + " trying again")
                search_request = self.s.get(url)
                time.sleep(0.5)
                self.ev_stations.extend(search_request.json()["results"])
        self.results_dict = ds.list_to_dict(self.ev_stations)


    def get_total_per_location(self,location):
        ofset = 0
        lat = location["lat"]
        lon = location["lon"]
        radius = location["radius"]
        url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&lat={lat}&lon={lon}&radius={radius}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url)
        search_total_count = search_request.json()["summary"]["totalResults"]
        self.results_count["search_" + str(len(self.results_count)+1)] = search_total_count


    def results_all_location(self):
        for a in self.locations:
            self.get_results_by_location(self.locations[a])




    def get_total_of_location_search(self):
        count = 0
        for a in self.results_count:
            if a != "total":
                count += self.results_count[a] 
                return count 


    def get_brands_from_results(self,data):
        df = pd.DataFrame.from_dict(data, orient = "index")


    def load_results_dict(self, filename: str) :
        self.results_dict = ds.load_from_json(filename)


    def get_charger_availability_for_poi_for_all(self):
        ids = [self.results_dict[a]["id"] for a in self.results_dict]  
        for num in range(0, len(self.results_dict)):
            charging_availability_id = self.results_dict[ids[num]]["dataSources"]["chargingAvailability"]["id"]
            url  = f"https://{self.base_url}/search/2/chargingAvailability.json?key={self.key}&chargingAvailability={charging_availability_id}"
            search_request = self.s.get(url)





    def get_charger_availability_for_one_poi_num(self, num):

        charging_availability_id = self.results_dict[str(num)]["dataSources"]["chargingAvailability"]["id"]
        url  = f"https://{self.base_url}/search/2/chargingAvailability.json?key={self.key}&chargingAvailability={charging_availability_id}"
        search_request = self.s.get(url)
        return search_request.json()



    def get_charger_availability_by_index_number(self, numbers):
        now = datetime.now()
        time_now = now.strftime("%m/%d, %H:%M")
        self.availability_data[time_now] ={}
        availability_data = self.availability_data[time_now]
        for num in numbers:
            try:
                charging_availability_id = self.results_dict[str(num)]["dataSources"]["chargingAvailability"]["id"]
                url  = f"https://{self.base_url}/search/2/chargingAvailability.json?key={self.key}&chargingAvailability={charging_availability_id}"
                search_request = self.s.get(url)
                availability_data[num] = search_request.json()
            except KeyError:
                print (f"No Charging Availability id for station with id {num}, moving to the next id")
                continue

        def get_charger_availability_by_availability_id(self, ids):
            now = datetime.now()
            time_now = now.strftime("%m/%d, %H:%M")
            self.availability_data[time_now] ={}
            availability_data = self.availability_data[time_now]
            for id in ids:
                try:
                    charging_availability_id = id
                    url  = f"https://{self.base_url}/search/2/chargingAvailability.json?key={self.key}&chargingAvailability={charging_availability_id}"
                    search_request = self.s.get(url)
                    availability_data[num] = search_request.json()
                except KeyError:
                    print (f"No Charging Availability id for station with id {num}, moving to the next id")
                    continue


    
    def get_charger_availability_by_index_key(self, numbers, dictionary):
        now = datetime.now()
        time_now = now.strftime("%m/%d, %H:%M")
        dictionary[time_now] ={}
        availability_data = dictionary[time_now]
        for num in numbers:
            try:
                charging_availability_id = self.results_dict[str(num)]["dataSources"]["chargingAvailability"]["id"]
                url  = f"https://{self.base_url}/search/2/chargingAvailability.json?key={self.key}&chargingAvailability={charging_availability_id}"
                search_request = self.s.get(url)
                availability_data[num] = search_request.json()
            except KeyError:
                print (f"No Charging Availability id for station with id {num}, moving to the next id")
                continue
        return dictionary



    def temporary_ev_availability(self, numbers, availability_data_filename):
        self.load_results_dict("uk_ev.json")
        filename = availability_data_filename
        if os.path.exists(filename):
            self.availability_data = ds.load_from_json(filename)
        self.get_charger_availability_by_index_number(numbers)
        ds.save_json(filename, self.availability_data)
        




    def get_first_100_ev(self):
        ofset = 0    
        url =  f"https://api.tomtom.com/search/2/categorySearch/station.json?&countrySet={self.country}&lat={self.lat}&lon={self.lon}&radius={self.radius}&categorySet=7309&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url)
        self.ev_total_results = search_request.json()["summary"]["totalResults"]

        self.total_by_brand = {}




    def index_to_ids(self, dictionary):
        ids = [dictionary[a]["id"] for a in dictionary]
        return ids

    def results_dict_to_ids(self):
        self.ids =  self.index_to_ids(self.results_dict)
        return self.ids




    def parse_results(self, res):
        parsed_results = []
        for n in res:
            parse_res = {   "id": n["id"], 
                            "name" : n["poi"]["name"], 
                            "position": 
                                        {
                                        "lat": n["position"]["lat"],
                                        "lon": n["position"]["lon"], 
                                        },
                        }
            parsed_results.extend([parse_res])
            self.parsed_results = parsed_results
        return parsed_results

        
                
            


            
