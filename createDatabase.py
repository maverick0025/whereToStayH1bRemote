
file_geography= "OFLC_Wages_2025-26_Updated/Geography.csv"
file_wages="OFLC_Wages_2025-26_Updated/ALC_Export.csv"



db_area={}
db_wage={}

with open(file_geography, 'r', encoding='utf-8-sig') as geo_file:
    geography_data = geo_file.readlines()
    for line in geography_data[:]:
        values = line.strip().split(',')
        area_code = values[0]
        area_name = values[1]
        state_code= values[-3]
        state_name = values[-2]
        county_name= values[-1]
        if(len(values)>5):
            # state_code != values[2]
            area_name = area_name + " " + "".join(values[2:-3]) 
            
        if(area_code.__contains__("Area")):
            continue
        else:
            if(db_area.get(state_name) is None):
                db_area[state_name] = {"stateCode":{}, "blsCodesAndCounties":[]}
                db_area[state_name]["stateCode"]= state_code
            blsCodesAndCounties= db_area[state_name]["blsCodesAndCounties"]
            
            entry_found= False
            entry_index= -1
            for entry in blsCodesAndCounties:
                entry_index+=1
                if area_code in entry:
                    entry_found= True        
                    break
                
            if(entry_found==False):
                db_area[state_name]["blsCodesAndCounties"].append({
                    area_code:{"blsName":area_name, "counties":[]},
                })
                entry_index= len(db_area[state_name]["blsCodesAndCounties"])-1

            db_area[state_name]["blsCodesAndCounties"][entry_index][area_code]["counties"].append(county_name)
        
#save db_area to a file
import json
with open('db_area.json', 'w') as f:
    json.dump(db_area, f, indent=4)
    
# #save db_wage to a file
# with open('db_wage.json', 'w') as f:
#     json.dump(db_wage, f, indent=4)