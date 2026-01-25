import json


#input: state name, current salary, level 1 or 2 or 3 or 4
#output: list of counties sorted as per input wage level only if current salary >= input wage level's salary in the county
def fetch_counties_by_wage(state_name, current_salary, wage_level):
    # Load area data
    with open('db_area.json', 'r') as f:
        db_area = json.load(f)

    # Load wage data
    with open('db_wage_software_dev.json', 'r') as f:
        db_wage = json.load(f)

    if state_name not in db_area:
        return []

    result_counties = []
    wage_level_key = f'{wage_level}_salary'

    for area_entry in db_area[state_name]['blsCodesAndCounties']:
        for area_code, area_info in area_entry.items():
            if area_code in db_wage:
                wage_info = db_wage[area_code][0]
                if wage_level_key in wage_info:
                    wage_value = float(wage_info[wage_level_key])
                    if current_salary >= wage_value:
                        result_counties.extend(area_info['counties'])

    return sorted(result_counties)

def __main__():
    # Load area data
    with open('db_area.json', 'r') as f:
        db_area = json.load(f)
        
    states = db_area.keys()
    
    # Example input 1
    # state = "Oklohoma"
    salary = 100000
    level = "level3" #options can be level1, level2, level3, avg

    for state in states:
        
        counties = fetch_counties_by_wage(state, salary, level)
        if(len(counties)>0):
            print(f"State: {state}")
            print(counties)
            print("-----------------------------------")
    
__main__()