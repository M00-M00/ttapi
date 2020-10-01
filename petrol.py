import requests
import json
import asyncio
import time
import data_structures as ds
import xmltodict

class PetrolTomTomApi():

    def __init__(self):

        #self.key = "BEAUFvC8jzPyPYNBotRrEIlaOi0fBRPo"
        self.key = "p9QAG7A754ZSfW21em3XPfDdfoaZls1x"
        self.base_url = "api.tomtom.com"
        self.categories_url = "https://" + self.base_url + "/search/2/poiCategories.json?key=" + self.key + "&[language=EN]"
        self.s = requests.Session()
        self.failed_brand_search = []

        # nearby search results
        self.nearby_results = {}
        # detailed search results 
        self.detailed_results = {}
    
        self.petrol_stations = []

        self.failed_nearby_ids = []
        self.failed_detailed_search_id = []

        #self.poi_categories_json = self.s.get(self.categories_url).json()["poiCategories"]

        self.gas_station_Id = 7311
        self.ev_station_id = 7309

        self.country = "GB"

        self.locId = 0

        self.poiCode = self.gas_station_Id

        self.failed_ids = []

        self.query = "petrol"



        self.all_uk_brands = ['Asda', 'BP', 'Shell', 'JET', 'Morrisons', "Sainsbury's", 'Esso', 'Asda', 'BP', 'Shell', 'JET', 'Morrisons',
         "Sainsbury's", 'Esso', 'Tesco', 'Gulf', 'Gleaner', 'Pace', 'Coop Mineraloel', 'Scottish Fuels', 'Murco', 'Rix', 'Texaco', 
         'Harvest Energy', 'Regency Oils', 'Solo', 'Major', 'Maxol', 'Emo', 'Star', 'Applegreen', 'EuroOil',]


    
    def get_total_petrol_stations_for_country(self):

        ofset = 0
        url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url_petrol)
        total_results = search_request.json()["summary"]["totalResults"]
        self.petrol_stations.extend(search_request.json()["results"])





    def get_results_petrol(self,start):

        ofset = 0
        url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url_petrol)
        total_results = search_request.json()["summary"]["totalResults"]
        self.petrol_stations.extend(search_request.json()["results"])

        for ofset in range(start, total_results, 100):
            print(ofset)
            url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&ofs={ofset}&limit=100&key={self.key}"
            search_request = self.s.get(url_petrol)
            time.sleep(0.5)
            try:
                self.petrol_stations.extend(search_request.json()["results"])
            except:
                print("error at: " + str(ofset) + " trying again")
                search_request = self.s.get(url_petrol)
                time.sleep(0.5)
                self.petrol_stations.extend(search_request.json()["results"])


    #Number of POI for each brand
    def get_total_for_brand(self, brand):
        ofset = 0
        url =  f"https://api.tomtom.com/search/2/categorySearch/{self.query}.json?&countrySet={self.country}&categorySet={self.poiCode}&brandSet={brand}&ofs={ofset}&limit=100&key={self.key}"
        search_request = self.s.get(url)
        total = search_request.json()["summary"]["totalResults"]
        self.total_by_brand[brand] = total




    def get_total_by_brand(self, brand: str):
        self.failed_brand_search = []
        self.total_by_brand = {}
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
                self.petrol_stations.extend(search_request.json()["results"])
            except:
                try:
                    print("error at: " + str(ofset) + " trying again")
                    time.sleep(1)
                    search_request = self.s.get(url_petrol)
                    self.petrol_stations.extend(search_request.json()["results"])
                except:
                    self.failed_brand_search.append(ofset)
                    print("request " + str(ofset) + " failed, added to failed list")
        self.ids = [a["id"] for a in self.petrol_stations]
        self.results_dict = ds.list_to_dict_with_key(self.petrol_stations, "id")



    def load_results_dict_from_json(self,filename):
        self.results_dict = ds.load_from_json(filename)


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


        


    def get_poi_categories(self):
        self.poi_categories_json = self.s.get(self.categories_url).json()["poiCategories"]



    def find_category_id(self, categories_json, category):
        self.get_poi_categories()
        for c in categories_json:
            if c["name"] == category  or category in c["synonyms"]:
                return c["id"]



    def load_detailed_results(self, filename):
        detailed= ds.load_from_json(filename)
        return detailed
    
    def load_petrol_stations(self, filename):
        results_dict = ds.load_from_json(filename)
        return results_dict

    def load_nearby_results(self, filename):
        nearby_results = ds.load_from_json(filename)
        return nearby_results




            
