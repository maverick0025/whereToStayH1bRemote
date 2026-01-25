# whereToStayH1bRemote

levels are determined by BLS Areas in each state
each bls area is associated with atleast one county from the state
Each bls can be overlapped with multiple states

```json
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
```


table: state
- state name
- state notation
- List<bls area>
- List<County>

table: BLS Area
- bls area name
- area code

table: Soc code (type of work)
- soc code (eg., 15-1252)
- work name (eg., software development, software testing)

table: salary
- area code
- soc code
- level 1 sal
- level 2 sal
- level 3 sal
- level 4 sal
- avg sal