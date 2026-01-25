
file_geography= "OFLC_Wages_2025-26_Updated/Geography.csv"
file_wages="OFLC_Wages_2025-26_Updated/ALC_Export.csv"


db_area_sample={
  "Delaware": {
    "statecode": "DE",
    "blsareacodes": [
      {
        "1000005": {
          "blsareaName": "Sussex Delaware Non metropolitan area",
          "counties": ["county1", "county20"]
        }
      },
      {
        "323232": {
          "blsareaName": "del metro area",
          "counties": ["county3", "county4"]
        }
      }
    ]
  }
}


db_wage_sample = {
  "areacode": [
    {
      "soccode1": {
        "level_1": 15.0,
        "level_2": 18.0,
        "level_3": 20.0,
        "level_4": 25.0,
        "avg": 30.0
      }
    },
    {
      "soccode2": {
        "level_1": 16.0,
        "level_2": 19.0,
        "level_3": 21.0,
        "level_4": 26.0,
        "avg": 31.0
      }
    }
  ]
}

db_area=db_area_sample
db_wage=db_wage_sample

with open(file_geography, 'r', encoding='utf-8-sig') as geo_file:
    geography_data = geo_file.readlines()
    for line in geography_data[:5]:
        print(line.strip().split(','))
        
#save db_area to a file
import json
with open('db_area.json', 'w') as f:
    json.dump(db_area, f, indent=4)
    
#save db_wage to a file
with open('db_wage.json', 'w') as f:
    json.dump(db_wage, f, indent=4)