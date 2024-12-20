
import json
import os

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)
        
spells = os.listdir("../Armors")
for seed in spells:
        
    with open("../Armors"+"/"+seed, 'r') as file:
        d = json.load(file)
        code = seed.split(".")
        code = code[0]
        code = code+".json"
        print(code)
        encode_to_file(d,"../Armors"+"/"+code)

