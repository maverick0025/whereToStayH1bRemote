# whereToStayH1bRemote

levels are determined by BLS Areas in each state
each bls area is associated with atleast one county from the state
Each bls can be overlapped with multiple states

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