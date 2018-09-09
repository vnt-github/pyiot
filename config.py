import json

with open('./config.json') as configF:
    config = json.load(configF)

with open('./testClient.json') as testClientF:
    testClient = json.load(testClientF)