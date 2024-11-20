import json

with open('jeu.json', 'r') as file:
    data = json.load(file)

x = {"carte1" : "test 123"}

data.update(x)

print(data["carte1"])