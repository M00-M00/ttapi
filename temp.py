import requests
import json
import asyncio
import time
from datetime import datetime
import pandas as pd
import data_structures as ds
import os
from general import TomTomApi



class Check_EVs(TomTomApi):

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
        self.output_pois = []


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

        self.hours = config["scheduled_hours"]

        self.search_type = config["search_type"]

        self.availability_ids = config["availability_ids"]

        self.index_keys = config["index_keys"]

        self.poi_results_filename = config["poi_results_filename"]

        self.availability_data_filename = config["availability_data_filename"]

        self.categories_url = "https://" + self.base_url + "/search/2/poiCategories.{self.data_type}?key=" + self.key + "&[language=EN]"

        self.poi_results = ds.load_from_json(self.poi_results_filename)

        """

self.poi_results = dict( [ (self.poi_results[a]["id"] , self.poi_results[a]) for a in self.poi_results] )

 dict( [ (nearby_dict_2[a]["results"][0]["id"] , nearby_dict_2[a]) for a in nearby_dict_2] )


ids = [id for id in self.poi_results]

self.search_all_nearbies_for_petrol_station(25, new_ids, self.poi_results, "uk_ev_nearby2_25.json" )

self.check_poi_for_nearby_petrol(self.poi_results, ids, "uk_ev_nearby_25.json")
print(self.output_pois)
        """


    def search_nearby_for_petrol(self, radius, id, poi_dict):
        lat = poi_dict[id]["position"]["lat"]
        lon = poi_dict[id]["position"]["lon"]
        url = f"https://{self.base_url}/search/2/nearbySearch/.{self.data_type}?key={self.key}&lat={lat}&lon={lon}&radius={radius}"
        request = self.s.get(url)
        results = request.json()["results"]
        for n in results:
            if n["poi"]["categories"] == ["petrol station"]:
                self.output_pois.append(str(id))
        self.nearby_results[id]= request.json()
        return  self.nearby_results



    def search_all_nearbies_for_petrol_station(self, radius, ids, poi_dict, output_filename):
        n = 0
        for id in ids:
            self.search_nearby_for_petrol(radius, id, poi_dict)
            time.sleep(0.5) 
            if n % 50 == 0:
                print(f"Done {n} out of {len(ids)}")
                ds.save_json(output_filename, self.nearby_results)
            n += 1


    def test_pois(self, poi_dict, input_filename, output_filename):

        test_results = self.test_availability_of_each_poi(poi_dict ,output_filename)

        test = ds.load_from_json(input_filename)

        tested_pois = self.sort_availability_data(test_results)
        self.tested_pois = tested_pois

    def print_total(test):
        w = len(tested_pois["types"]["working"])
        u = len(tested_pois["types"]["unknown"])
        o =  len(tested_pois["types"]["out_of_service"])

        Total = w + u + o

        print( "Total: " + str(Total) + 
        "\n" +  "Working: "+ str(len(tested_pois["types"]["working"]))+ 
        "\n" + "All Connector Types Working: " + str(len(tested_pois["fully_working"])) + 
        "\n" + "Unknown: " +  str(len(tested_pois["types"]["unknown"])) + 
        "\n" + "Out of Service: " + str( len(tested_pois["types"]["out_of_service"])))  


    def get_ids_from_tested(self):
        ids = [id for id in self.tested_pois["types"]["working"]]
        return ids



    def check_nearby_for_petrol(self, nearby_dict):
        output_pois = []
        for a in nearby_dict:
            for n in nearby_dict[a]["results"]:
                if n["poi"]["categories"] == ["petrol station"]:
                        output_pois.append(str(a))
        return output_pois


    def check_poi_for_nearby_petrol(self, ev_dict, ids_to_test, output_filename):



        self.search_all_nearbies_for_petrol_station(25, ids_to_test, self.poi_results)
        ds.save_json(output_filename, self.nearby_results)
        

        #print(self.nearby)

        #d = check_nearby_for_petrol(nearby_dict)


