
import json

db_area={}
db_wage={}
hours_in_year=2080

def extractGeographyInfo(file_geography):

    with open(file_geography, 'r', encoding='utf-8-sig') as geo_file:
        geography_data = geo_file.readlines()
        for line in geography_data[:]:
            values = line.strip().split(',')
            area_code =   values[0][1:-1]
            area_name =   values[1][1:-1]
            state_code=  values[-3][1:-1]
            state_name = values[-2][1:-1]
            county_name= values[-1][1:-1]
            if(len(values)>5):
                # state_code != values[2]
                area_name = area_name+"," + ",".join(values[2:-3]) 
                
            if(area_code.__contains__("Area")):
                continue
            else:
                
                # print(area_code, area_name, state_code, state_name, county_name)
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
    
    #saving extracted json to a file
    with open('db_area.json', 'w') as f:
        json.dump(db_area, f, indent=4)

def extractWageInfo(file_wages, expected_occupation_code):
    with open(file_wages, 'r', encoding='utf-8-sig') as wage_file:
        wage_data = wage_file.readlines()
        for line in wage_data[:]:
            values = line.strip().split(',')

            area_code =       values[0][1:-1]
            occupation_code = values[1][1:-1]
            wage_level_1 =    values[3][1:-1]
            wage_level_2 =    values[4][1:-1]
            wage_level_3 =    values[5][1:-1]
            wage_level_4 =    values[6][1:-1]
            wage_level_avg =  values[7][1:-1]
                            
            if(area_code.__contains__("Area")):
                continue
            else:
                if(db_wage.get(area_code) is None):
                    db_wage[area_code] = []
                if(occupation_code.__contains__(expected_occupation_code)): # focusing on software development occupations
                    db_wage[area_code].append({
                                            # "socCode":occupation_code,
                                            # "wageLevel1":wage_level_1,
                                            # "wageLevel2":wage_level_2,
                                            # "wageLevel3":wage_level_3,
                                            # "wageLevel4":wage_level_4,
                                            # "wageLevelAvg":wage_level_avg,
                                            "level1_salary": str(round(float(wage_level_1)*hours_in_year,2)) if wage_level_1 !='' else '',
                                            "level2_salary": str(round(float(wage_level_2)*hours_in_year,2)) if wage_level_2 !='' else '',
                                            "level3_salary": str(round(float(wage_level_3)*hours_in_year,2)) if wage_level_3 !='' else '',
                                            "level4_salary": str(round(float(wage_level_4)*hours_in_year,2)) if wage_level_4 !='' else '',
                                            "avg_salary": str(round(float(wage_level_avg)*hours_in_year,2)) if wage_level_avg !='' else ''
                                            })

    #save db_wage to a file
    with open('db_wage_software_dev.json', 'w') as f:
        json.dump(db_wage, f, indent=4)    
            
def __main__():        
    file_geography= "OFLC_Wages_2025-26_Updated/Geography.csv"
    file_wages="OFLC_Wages_2025-26_Updated/ALC_Export.csv"
    software_dev_occupation_code= "15-1252"  # SOC code for Software Developers and Software Quality Assurance Analysts and Testers
            
    # extractGeographyInfo(file_geography)        
    extractWageInfo(file_wages, software_dev_occupation_code)
        

__main__()