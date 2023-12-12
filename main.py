import sys
import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, List

sys.path.append('./src/')
import KG
import KG_types

app = FastAPI()

@app.post("/KG")
async def query_knowledge_graph(json_query: KG.Query):
    username, password, connection_string = get_credentials()
    db = KG.db_connect(connection_string,username,password)
    result = KG.Query_KG_all(json_query,db)
    return(result)

@app.get("/KG_types")
async def get_types():
    username, password, connection_string = get_credentials()
    db = KG.db_connect(connection_string,username,password)
    result = KG_types.get_KG_types(db)
    return(result)

def get_credentials():
    with open('/Users/katiechristensen/Desktop/credentials.json', 'r') as f:
        data = json.load(f)

    username = data['username']
    password = data['password']
    connection_string = data['connection_string']

    return username, password, connection_string
