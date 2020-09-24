
key = "BEAUFvC8jzPyPYNBotRrEIlaOi0fBRPo"
base_url = "api.tomtom.com"
categories_url = "https://" + base_url + "/search/2/poiCategories.json?key=" + key + "&[language=EN]"

#any coordinates in the UK are fine, since country is set to GB & radius is 2400000000
lat  = 55.978923
lon = -3.186007
radius = 240000000

locId = 0

poiCode = 0

failed_ids = []

query = ""

gas_station_Id = 7311
ev_station_id = 7309


detailed_search = f"https://{base_url}/search/2/poiDetails.json?key={key}&id={locId}"

#json_chargingAvailability = ["results"][0]["dataSources"]["chargingAvailability"]["id"]

#charging_availabilty = f"https://{base_url}/search/2/chargingAvailability.json?key={key}&chargingAvailability={charging_availability_id}"


search_request = f"https://api.tomtom.com/search/2/categorySearch/{query}.json?&countrySet={country}&lat={lat}&lon={lon}&radius=240000000&categorySet={poiCode}&ofs={ofset}&limit=100&key={key}"

url_petrol =  f"https://api.tomtom.com/search/2/categorySearch/petrol.json?&countrySet={country}&lat={lat}&lon={lon}&radius=240000000&categorySet=7311&ofs={ofset}&limit=100&key={key}"


#total_results = s.get(search_request).json()["summary"]["totalResults"]


uk_search_1 = {"lat" :51.208795, "lon" : -4.067991,  "radius" : 200000 }

uk_search_2 = {"lat" : 51.926424, "lon" : 0.491915, "radius" : 130000}

uk_search_3 = {"lat" :53.654690, "lon" :  -1.395234,  "radius" : 130000}

uk_search_4 = {"lat" :56.132649, "lon" : -3.426368, "radius" : 185000}

uk_search_5 = {"lat" :54.738375, "lon" :-6.759626, "radius" : 100000}

all_uk_brands = ['Asda', 'BP', 'Shell', 'JET', 'Morrisons', "Sainsbury's", 
'Esso', 'Asda', 'BP', 'Shell', 'JET', 'Morrisons', "Sainsbury's", 'Esso', 'Tesco',
'Gulf', 'Gleaner', 'Pace', 'Coop Mineraloel', 'Scottish Fuels', 'Murco', 'Rix', 
'Texaco', 'Harvest Energy', 'Regency Oils', 'Solo', 'Major', 'Maxol', 'Emo', 
'Star', 'Applegreen', 'EuroOil',]