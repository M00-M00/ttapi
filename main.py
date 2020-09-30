
import argparse
from petrol import PetrolTomTomApi
import data_structures as ds


parser = argparse.ArgumentParser()

parser.add_argument("-B" ,"--brand", type =str)
parser.add_argument("-M", "--mode", type = str)
parser.add_argument("-D", "--detailed_results", type = str)
parser.add_argument("-S", "--detailed_stop", type = int)
parser.add_argument("-J" ,"--json", type = str)
parser.add_argument("-R", "--radius", type =str)
args = parser.parse_args()

brand = args.brand
mode = args.mode
detailed = args.detailed_results
json= args.json
radius = args.radius
stop = args.detailed_stop

def name_json():
    if mode == "Nearby":
        if json == None:
            filename = brand + "_" + str(radius) +  "_Nearby_Petrol.json"
        else:
            filename = json.split(".")[0] + "_" + str(radius) +  "_Nearby_Petrol.json"

    elif mode == "Detailed":
        if json == None:
            filename = brand  +  "_Detailed_Petrol.json"
        else:
            filename = json.split(".")[0]  +  "_Detailed_Petrol.json"
    return filename






if __name__ == "__main__":
    api = PetrolTomTomApi()

    if mode == "Brand":
        if brand == None:
            print("No Brand selected, enter brand")
            brand = str(input())
        api.get_total_by_brand(brand)
        filename = brand + ".json"
        ds.save_json(filename, api.results_dict)
    else:    
        if json == None:
            if brand == None:
                print("No json selected, enter what brand to search first")
                brand = str(input())
            api.get_total_by_brand([brand])
        else:
            api.results_dict = api.load_petrol_stations(json)
            api.ids = [a for a in api.results_dict]

        if mode == "Detailed":
            if detailed == None:
                api.search_all_detailed(api.ids)
                filename = name_json()
                ds.save_json(filename, api.detailed_results)
            else: 
                api.detailed_results = api.load_detailed_results(detailed)
                start = len(api.detailed_results)
                if stop != None:
                    stop = start + stop
                    ids_to_scrape = api.ids[start:stop]
                else:
                    ids_to_scrape = api.ids[start:]
                api.search_all_detailed(ids_to_scrape)
                filename = name_json()
                ds.save_json(filename, api.detailed_results)

        elif mode =="Nearby":
            if radius == None:
                print("Enter radius for nearby search") 
                radius = str(input())
                api.search_all_nearbies(radius = radius, ids = api.ids)
                filename = name_json()
                ds.save_json(filename, api.nearby_results)
            else:
                api.search_all_nearbies(radius = radius, ids = api.ids)
                filename = name_json()
                ds.save_json(filename, api.nearby_results)

        

        
    
