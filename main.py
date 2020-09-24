
import argparse
from petrol import PetrolTomTomApi


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




if __name__ == "__main__":
    api = PetrolTomTomApi()

    if mode == "Brand":
        if brand == None:
            print("No Brand selected, enter brand")
            brand = str(input())
            api.get_total_by_brand(brand)
    else:    
        if json == None:
            print("No json selected, enter what brand to search first")
            brand = str(input())
            api.get_total_by_brand([brand])
        else:
            results_dict = api.load_petrol_stations(json)
            api.ids = [a for a in results_dict]

        if mode == "Detailed":
            if detailed == None:
                api.search_all_detailed(api.ids)
            else: 
                api.detailed_results = api.load_detailed_results(detailed)
                start = len(api.detailed_results)
                if stop != None:
                    stop = start + stop
                    ids_to_scrape = api.ids[start:stop]
                else:
                    ids_to_scrape = api.ids[start:]
                api.search_all_detailed(ids_to_scrape)

        elif mode =="Nearby":
            if radius == None:
                print("Enter radius for nearby search") 
                radius = str(input())
            else:
                api.search_all_nearbies(radius = radius, ids = api.ids)

        

        
    
