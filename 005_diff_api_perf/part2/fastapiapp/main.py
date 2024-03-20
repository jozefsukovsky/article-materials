import json

from fastapi import FastAPI, Request


test_data = {}
with open('./test_data.json', encoding='utf8') as fd:
    test_data = json.loads(fd.read())

app = FastAPI()

@app.get("/children")
def read_children(_request: Request):
    return test_data
