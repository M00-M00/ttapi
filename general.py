import requests
import json
import asyncio
import time
from datetime import datetime
import pandas as pd
import data_structures as ds
import os




class TomTomApi():

    def __init__(self, config_file):

        #self.key = "BEAUFvC8jzPyPYNBotRrEIlaOi0fBRPo"
        #self.key = "p9QAG7A754ZSfW21em3XPfDdfoaZls1x"
        self.base_url = "api.tomtom.com"
        self.s = requests.Session()
        self.failed_brand_search = []
        self.nearby_results = {}
        self.failed_nearby_ids = []
        self.detailed_results = {}
        self.failed_detailed_search_id = []
        self.poi_results = []
        self.availability_data = {}

        #self.poi_categories_json = self.s.get(self.categories_url).json()["poiCategories"]

        config = ds.load_from_json(config_file)

        self.country = config["country"]

        self.key = config["key"]

        self.locId = 0

        self.poi_code = config["poi_code"]

        self.failed_ids = []

        self.query = config["query"]

        self.data_type = config["data_type"]

        self.days_of_week = config["scheduled_days_of_week"]

        self.hours = config["scheduled_hour"]

        self.search_type = config["search_type"]

        self.availability_ids = config["availability_ids"]

        self.index_keys = config["index_keys"]

        self.poi_results_filename = config["poi_results_filename"]

        self.availability_data_filename = config["availability_data_filename"]

        self.categories_url = "https://" + self.base_url + "/search/2/poiCategories.{self.data_type}?key=" + self.key + "&[language=EN]"





    def get_total_poi_results_for_country(self):

        ofset = 0
        url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.{self.data_type}?&countrySet={self.country}&categorySet={self.poi_code}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url_petrol)
        total_results = search_request.json()["summary"]["totalResults"]
        self.poi_results.extend(search_request.json()["results"])





    def get_results_poi(self,start):

        ofset = 0
        url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.{self.data_type}?&countrySet={self.country}&categorySet={self.poi_code}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url_petrol)
        total_results = search_request.json()["summary"]["totalResults"]
        self.poi_results.extend(search_request.json()["results"])

        for ofset in range(start, total_results, 100):
            print(ofset)
            url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.{self.data_type}?&countrySet={self.country}&categorySet={self.poi_code}&ofs={ofset}&limit=100&key={self.key}"
            search_request = self.s.get(url_petrol)
            time.sleep(0.5)
            try:
                self.poi_results.extend(search_request.json()["results"])
            except:
                print("error at: " + str(ofset) + " trying again")
                search_request = self.s.get(url_petrol)
                time.sleep(0.5)
                self.poi_results.extend(search_request.json()["results"])


    def get_total_for_brand(self, brand):
        ofset = 0
        url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.{self.data_type}?&countrySet={self.country}&categorySet={self.poi_code}&brandSet={brand}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url)
        total = search_request.json()["summary"]["totalResults"]
        self.total_by_brand[brand] = total




    def get_total_by_brand(self, brands: list):
        self.failed_brand_search = []
        self.total_by_brand = {}
        for brand in brands:
            ofset = 0
            url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.{self.data_type}?&countrySet={self.country}&categorySet={self.poi_code}&brandSet={brand}&ofs={ofset}&limit=100&key={self.key}"
            search_request = self.s.get(url)
            total = search_request.json()["summary"]["totalResults"]
            self.total_by_brand[brand] = total
            print(brand + ": " + str(total) + "pois")
            for ofset in range(0, total, 100):
                print(ofset)
                url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.{self.data_type}?&countrySet={self.country}&brandSet={brand}&categorySet={self.poi_code}&ofs={ofset}&limit=100&key={self.key}"
                search_request = self.s.get(url_petrol)
                time.sleep(1)
                try:
                    self.poi_results.extend(search_request.json()["results"])
                except:
                    try:
                        print("error at: " + str(ofset) + " trying again")
                        time.sleep(1)
                        search_request = self.s.get(url_petrol)
                        self.poi_results.extend(search_request.json()["results"])
                    except:
                        self.failed_brand_search.append(ofset)
                        print("request " + str(ofset) + " failed, added to failed list")
        self.ids = [a["id"] for a in self.poi_results]
        self.results_dict = ds.list_to_dict_with_key(self.poi_results, "id")
        if len(brands) == 1:
            filename = str(self.country) + "_" + str(brands[0]) + "_" + str(self.poi_code) + ".json"
        else:
            filename = str(self.country) + "_" + str(self.poi_code) + ".json"
        ds.save_json(filename, self.results_dict)



    def get_detailed_search_for_poi(self, id):
        url = f"https://{self.base_url}/search/2/poiDetails.{self.data_type}?key={self.key}&id={id}"
        search_requests = self.s.get(url)
        self.detailed_results[id] = search_requests.json()


    def search_nearby(self, id, radius):
        lat = self.results_dict[id]["position"]["lat"]
        lon = self.results_dict[id]["position"]["lon"]
        url = f"https://{self.base_url}/search/2/nearbySearch/.{self.data_type}?key={self.key}&lat={lat}&lon={lon}&radius={radius}"
        request = self.s.get(url)
        self.nearby_results[id]= request.json()



    def search_all_nearbies(self, radius, ids):
        n = 0
        for id in ids:
            self.search_nearby(id, radius)
            time.sleep(0.5) 
            if n % 50 == 0:
                print(f"Done {n} out of {len(self.results_dict)}")
            n += 1


        
    def search_all_detailed(self, ids):
        n = 0
        for id in ids:
            try:
                self.get_detailed_search_for_poi(id)
                time.sleep(1)
            except:
                try:
                    self.get_detailed_search_for_poi(id)
                    time.sleep(1)
                except:
                    print(str(id) + " parsing failed, adding to failed list")
                    self.failed_detailed_search_id.append(id)
            if n % 5 == 0:
                print(f"Done {n} out of {len(self.results_dict)}")
            n += 1    
            

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
            url  = f"https://{self.base_url}/search/2/chargingAvailability.{self.data_type}?key={self.key}&chargingAvailability={charging_availability_id}"
            search_request = self.s.get(url)





    def get_charger_availability_for_one_poi_num(self, num):

        charging_availability_id = self.results_dict[str(num)]["dataSources"]["chargingAvailability"]["id"]
        url  = f"https://{self.base_url}/search/2/chargingAvailability.{self.data_type}?key={self.key}&chargingAvailability={charging_availability_id}"
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
                url  = f"https://{self.base_url}/search/2/chargingAvailability.{self.data_type}?key={self.key}&chargingAvailability={charging_availability_id}"
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
                url  = f"https://{self.base_url}/search/2/chargingAvailability.{self.data_type}?key={self.key}&chargingAvailability={charging_availability_id}"
                search_request = self.s.get(url)
                availability_data[id] = search_request.json()
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
                url  = f"https://{self.base_url}/search/2/chargingAvailability.{self.data_type}?key={self.key}&chargingAvailability={charging_availability_id}"
                search_request = self.s.get(url)
                availability_data[num] = search_request.json()
            except KeyError:
                print (f"No Charging Availability id for station with id {num}, moving to the next id")
                continue
        return dictionary



    def ev_availability_by_index(self, numbers, availability_data_filename):
        self.load_results_dict(self.poi_results_filename)
        filename = availability_data_filename
        if os.path.exists(filename):
            self.availability_data = ds.load_from_json(filename)
        self.get_charger_availability_by_index_number(numbers)
        ds.save_json(filename, self.availability_data)
        
    def ev_availability_by_availabilty_id(self, ids, availability_data_filename):
        filename = availability_data_filename
        if os.path.exists(filename):
            self.availability_data = ds.load_from_json(filename)
        self.get_charger_availability_by_availability_id(ids)
        ds.save_json(filename, self.availability_data)




    def get_first_100_ev(self):
        ofset = 0    
        url =  f"https://api.tomtom.com/search/2/categorySearch/station.{self.data_type}?&countrySet={self.country}&lat={self.lat}&lon={self.lon}&radius={self.radius}&categorySet=7309&ofs={ofset}&limit=100&key={self.key}"
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




            


            
