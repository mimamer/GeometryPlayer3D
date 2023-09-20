import json

def read_data(path):
    with open(path) as file:
        data=json.load(file)
        return data