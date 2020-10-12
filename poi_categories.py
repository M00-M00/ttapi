import requests
import json


class Categories_POI():

    def __init__(self):
        self.s = requests.Session()
        self.key = "p9QAG7A754ZSfW21em3XPfDdfoaZls1x"
        self.base_url = "api.tomtom.com"
        self.categories_url = "https://" + self.base_url + "/search/2/poiCategories.json?key=" + self.key + "&[language=EN]"

    def get_poi_categories(self):
        self.poi_categories_json = self.s.get(self.categories_url).json()["poiCategories"]

    def find_category_id(self, categories_json, category):
        self.get_poi_categories()
        for c in categories_json:
            if c["name"] == category  or category in c["synonyms"]:
                return c["id"]
