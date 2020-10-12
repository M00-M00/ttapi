
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




","latitude":50.394006,"longitude":-4.082748,"distance":5616924.3107357,"shortAddress":"Coypool Park and Ride, Plymouth, PL7 4TB",
"address":{"id":748,"name":"Coypool Park and Ride","address1":"Coypool Park and Ride","address2":"","town":"Plymouth","postcode":"PL7 4TB","slug":
"coypool-park-and-ride-e75y"},"slug":"jeff-luke"},{"scope":"POD POINT","id":3539,"name":"Luke-Roxy","latitude":51.469688,"longitude":-0.452818,"distance
":5723326.6161293,"shortAddress":"London Heathrow Airport, Middlesex, TW6 1AP","address":{"id":780,"name":"Heathrow Airport T2","address1":"London Heathrow
 Airport","address2":"Hounslow","town":"Middlesex","postcode":"TW6 1AP","slug":"heathrow-airport-t2-5zew"},"slug":"luke-roxy"},{"scope":"POD POINT","id":3206
 ,"name":"Luke-Jeff","latitude":51.522584,"longitude":-0.678844,"distance":5729405.343486,"shortAddress":"Bath Road, Slough, SL6 0NX","address
 ":{"id":138,"name":"The Bishop Centre","address1":"Bath Road","address2":"Taplow","town":"Slough","postcode":"SL6 0XN","slug":"the-bishop-centre-nxd"}
 ,"slug":"luke-jeff"},{"scope":"POD POINT","id":2912,"name":"Luke-June","latitude":51.522778,"longitude":-0.678889,"distance":5729426.9599488,"shortAddress":"Bath Road, Slough, SL6 0NX","address":{"id":138,"name":"The Bishop Centre","address1":"Bath Road","address2":"Taplow","town":"Slough","postcode":"SL6 0NX","slug":"the-bishop-centre-nxd"},"slug":"luke-june"},{"scope":"POD POINT","id":3660,"name":"Luke-Abby","latitude":51.536569,"longitude":-0.125452,"distance":5730617.1412095,"shortAddress":"3 Canal Reach, London, N1C 4AB","address":{"id":918,"name":"Argent LLP - Canal Reach","address1":"3 Canal Reach","address2":"Kings Cross","town":"London","postcode":"N1C 4AB","slug":"argent-llp-canal-reach-wgpe"},"slug":"luke-abby"},{"scope":"POD POINT","id":2184,"name":"Anne-Luke","latitude":52.55598505,"longitude":1.7130896,"distance":5846139.1450588,"shortAddress":"Gorleston, Norfolk, NR31 7RA","address":{"id":141,"name":"Beacon Innovation Centre","address1":"Gorleston","address2":"Great Yarmouth","town":"Norfolk","postcode":"NR31 7RA","slug":"beacon-innovation-centre-165"},"slug":"anne-luke"},{"scope":"POD POINT","id":2815,"name":"Kirk-Carl","latitude":52.636232,"longitude":-2.139199,"distance":5856271.4674367,"shortAddress":"Engine Manufacturing Centre, Wolverhampton, WV9 5GB","address":{"id":351,"name":"JLR EMC-UK","address1":"Engine Manufacturing Centre","address2":"Innovation Drive Coven","town":"Wolverhampton","postcode":"WV9 5GB","slug":"jlr-emc-uk-05m"},"slug":"kirk-carl"},{"scope":"POD POINT","id":3578,"name":"Gabe-Abby","latitude":52.636284,"longitude":-2.138997,"distance":5856276.6033048,"shortAddress":"Engine Manufacturing Centre, Wolverhampton, WV9 5GB","address":{"id":351,"name":"JLR EMC-UK","address1":"Engine Manufacturing Centre","address2":"Innovation Drive Coven","town":"Wolverhampton","postcode":"WV9 5GB","slug":"jlr-emc-uk-05m"},"slug":"gabe-abby"},{"scope":"POD POINT","id":3672,"name":"Hugo-Phil","latitude":52.636301,"longitude":-2.13977,"distance":5856280.9405593,"shortAddress":"Engine Manufacturing Centre, Wolverhampton, WV9 5GB","address":{"id":351,"name":"JLR EMC-UK","address1":"Engine Manufacturing Centre","address2":"Innovation Drive Coven","town":"Wolverhampton","postcode":"WV9 5GB","slug":"jlr-emc-uk-05m"},"slug":"hugo-phil"},{"scope":"POD POINT","id":3671,"name":"Eddy-Emma","latitude":52.636329,"longitude":-2.139468,"distance":5856283.0936797,"shortAddress":"Engine Manufacturing Centre, Wolverhampton, WV9 5GB","address":{"id":351,"name":"JLR EMC-UK","address1":"Engine Manufacturing Centre","address2":"Innovation Drive Coven","town":"Wolverhampton","postcode":"WV9 5GB","slug":"jlr-emc-uk-05m"},"slug":"eddy-emma"}],"meta":{"paginatio