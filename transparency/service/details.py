
def show_information(detail):
    for i in ["summary", "description", "path"]:
        print("{:12}: {}".format(i.capitalize(),detail[i]))
    
    if "parameters" in detail:
        print("\nAll parameters\n")
        for i in detail["parameters"]:
            type_ = "*required" if i["required"] else "optional" 
            print("{:12}: {} ({})\nDescription: {} - (Type: {})\n".format("Name",i["name"],type_, i["description"], i["format"]))

            
            
    
def create_link(detail, payload):
    if "parameters" in detail:
        query="?"
        nth = 0 
        for param in detail["parameters"]:
            if param["required"] == True:    
                key = param["name"]
                if nth != 0:
                    query +="&"
                if key not in payload:
                    print("There are missing parameters.")
                    print("\nRequired parameters")
                    for i in detail["parameters"]:
                        type_ = "*required" if i["required"] else "optional" 
                        print("{:12}: {} ({})\nDescription: {} - (Type: {})\n".format("Name",i["name"],type_, i["description"], i["format"]))

                    return None
                query += "{}={}".format(key, payload[key])
                nth += 1
        res = detail["path"]+query
    else:
        res = detail["path"]
    return res 

