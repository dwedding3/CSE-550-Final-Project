import os
import json

def startInit():
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd):
        for filename in files:
            if(filename.lower().endswith(".json")):
                with open(f'{root}/{filename}', 'r') as configs:
                    return json.load(configs)
