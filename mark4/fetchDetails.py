import json
from selective_county_mapper import SelectiveCountyMapper

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


def visualize(statesAndCounties):

    mapper = SelectiveCountyMapper()
    selections = {}

    for(state, counties) in statesAndCounties.items():
        selections[state] = counties
    # print(selections)
            
    if selections:
        is_valid, msg = mapper.validate_selection(selections)
        if(not is_valid):
            print(msg)
        if is_valid:
            locations = mapper.get_selected_locations(selections)
            mapper.print_locations_table(locations)
            mapper.export_locations_json(locations, 'my_selection.json')
            mapper.create_selective_map(selections, 'my_selection_map.html')


def __main__():
    with open('./db_area.json', 'r') as f:
        db_area = json.load(f)

    '''
    state = "Oklohoma"
    counties = fetch_counties_by_wage("Texas", salary, level)
    result = list(map(lambda x: x.split(" County")[0] , counties))
    print(", ".join(result))
    '''    
    
    salary = 100000
    level = "level3" #options can be level1, level2, level3, avg
    statesAndCounties={}    
    states = db_area.keys()
    for state in states:
        counties = fetch_counties_by_wage(state, salary, level)
        # if(len(counties)>0 and state == "Colorado"):
        if(len(counties)>0):
            state_counties = list(map(lambda x: x.split(" County")[0] , counties))
            statesAndCounties[db_area[state]["stateCode"]]=state_counties
    
    # print("Selected States and Counties:")
    # print("-----------------------------")
    # for(state, counties) in statesAndCounties.items():
    #     print(state)
    #     print(db_area[state]["stateCode"])
    #     print(counties)
    #     print("-----------------------------")
        # print(f"{state}: {', '.join(counties)}")
    
    visualize(statesAndCounties)

__main__()