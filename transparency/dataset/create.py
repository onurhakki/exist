

from json import dump, loads
from requests import get 
import os

def json_file(export=False):
    r = get("https://seffaflik.epias.com.tr/transparency/technical/swagger.json")

    parsed_json = r.json()


    service_path = parsed_json["schemes"][0]+"://" + parsed_json["host"] + parsed_json["basePath"]

    final_json = dict()
    final_json["main_path"] = service_path

    for k,i in parsed_json["paths"].items():
        tag = i["get"]["tags"][0]
        if tag in final_json:
            pass
        else:
            final_json[tag] = dict()
        operationId = i["get"]["operationId"]
        final_json[tag][operationId] = dict()

        final_json[tag][operationId]["summary"] = i["get"]["summary"]
        final_json[tag][operationId]["description"] = i["get"]["description"]
        final_json[tag][operationId]["consumes"] = i["get"]["consumes"]
        final_json[tag][operationId]["produces"] = i["get"]["produces"]
        final_json[tag][operationId]["responses"] = i["get"]["responses"]
        final_json[tag][operationId]["path"] = service_path+k

        if "parameters" in i["get"]:
            final_json[tag][operationId]["parameters"] = i["get"]["parameters"]
    if export == True:    
        with open("final_data.json", "w", encoding="utf8") as outfile:
            dump(final_json, outfile)
    return final_json

def read_json(export = False):
    if os.path.isfile(os.path.join(os.getcwd(), "final_data.json")) == True:
        print("Reading from local file.")
        with open(os.path.join(os.getcwd(), "final_data.json"), encoding="utf8") as user_file:
            file_contents = user_file.read()
            res = loads(file_contents)


    else:
        print("Downloading from EPİAŞ.")
        res = json_file(export=export)
    return res

