import json
import csv
import os




def save_json(filename, data):
    with open(filename,"w") as outfile:
        json.dump(data, outfile)
        

def create_dict_to_csv(filename, dict_data):
    with open(filename, "w") as outfile:
        w = csv.DictWriter(outfile, dict_data[0].keys())
        w.writeheader()
        for a in dict_data:
            w.writerow(dict_data[a])

def append_dict_to_csv(filename, data):
    with open(filename, "ab") as outfile:
        w = csv.DictWriter(outfile, data.keys())
        w.writerow(data)


# Removes duplicates 
def list_to_dict(list):
    result_dict = {}
    for n in string:
        result_dict[string.index(n)] = n
    return result_dict

def list_to_dict_with_key(list, key):
    result_dict = {}
    for n in list:    
        k = n[key]
        result_dict[k] = n
    return result_dict



def parse_results(res):
    parsed_results = []
    for n in res:
        parse_res = {   "id": res[n]["id"], 
                        "name" : res[n]["poi"]["name"], 
                        "lat": res[n]["position"]["lat"],
                        "lat": res[n]["position"]["lat"],

                    }
        parsed_results.extend([parse_res])
    return parsed_results


def load_from_json(filename):
    if os.path.exists(filename) == False:
        print("File doesn't exist")
    else:
        with open(filename) as j:
            json_data = json.load(j)
            return(json_data)

def dictionary_from_dictionary_with_key(old_dict: dict, key) -> dict :
    new_dict = dict( [ (old_dict[a][key] , old_dict[a]) for a in old_dict] )
    return new_dict
