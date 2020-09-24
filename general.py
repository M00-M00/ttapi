import requests
import json
import asyncio
import time
import data_structures as ds
import xmltodict





class TomTomApi():

    def __init__(self, query, country, poiCode):

        #self.key = "BEAUFvC8jzPyPYNBotRrEIlaOi0fBRPo"
        self.key = "p9QAG7A754ZSfW21em3XPfDdfoaZls1x"
        self.base_url = "api.tomtom.com"
        self.categories_url = "https://" + self.base_url + "/search/2/poiCategories.json?key=" + self.key + "&[language=EN]"
        self.s = requests.Session()
        self.failed_brand_search = []
        self.nearby_results = {}
        self.failed_nearby_ids = []
        self.detailed_results = {}
        self.failed_detailed_search_id = []
        self.poi_results = []

        #self.poi_categories_json = self.s.get(self.categories_url).json()["poiCategories"]

        self.gas_station_Id = 7311
        self.ev_station_id = 7309

        self.country = country

        self.locId = 0

        self.poiCode = poiCode

        self.failed_ids = []

        self.query = query



    def get_total_poi_results_for_country(self):

        ofset = 0
        url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url_petrol)
        total_results = search_request.json()["summary"]["totalResults"]
        self.poi_results.extend(search_request.json()["results"])





    def get_results_petrol(self,start):

        ofset = 0
        url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url_petrol)
        total_results = search_request.json()["summary"]["totalResults"]
        self.poi_results.extend(search_request.json()["results"])

        for ofset in range(start, total_results, 100):
            print(ofset)
            url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
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
        url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&brandSet={brand}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url)
        total = search_request.json()["summary"]["totalResults"]
        self.total_by_brand[brand] = total




    def get_total_by_brand(self, brands: list):
        self.failed_brand_search = []
        self.total_by_brand = {}
        for brand in brands:
            ofset = 0
            url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&brandSet={brand}&ofs={ofset}&limit=100&key={self.key}"
            search_request = self.s.get(url)
            total = search_request.json()["summary"]["totalResults"]
            self.total_by_brand[brand] = total
            print(brand + ": " + str(total) + "pois")
            for ofset in range(0, total, 100):
                print(ofset)
                url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&brandSet={brand}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
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
            filename = str(self.country) + "_" + str(brands[0]) + "_" + str(self.poiCode) + ".json"
        else:
            filename = str(self.country) + "_" + str(self.poiCode) + ".json"
        ds.save_json(filename, self.results_dict)



    def get_detailed_search_for_poi(self, id):
        url = f"https://{self.base_url}/search/2/poiDetails.json?key={self.key}&id={id}"
        search_requests = self.s.get(url)
        self.detailed_results[id] = search_requests.json()


    def search_nearby(self, id, radius):
        lat = self.results_dict[id]["position"]["lat"]
        lon = self.results_dict[id]["position"]["lon"]
        url = f"https://{self.base_url}/search/2/nearbySearch/.json?key={self.key}&lat={lat}&lon={lon}&radius={radius}"
        request = self.s.get(url)
        self.nearby_results[id]= request.json()


    def search_all_nearbies(self, radius, ids):
        for id in ids:
            self.search_nearby(id, radius)
            time.sleep(0.5)
        ds.save_json("Nearby_Search.json", self.nearby_results)

    
        
    def search_all_detailed(self, ids):
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
        ds.save_json("Detailed_Search.json", self.detailed_results)






            


            
