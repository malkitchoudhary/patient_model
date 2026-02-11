from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Literal
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "patients.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calc_bmi(h, w):
    return round(w/(h*h),2) if h>0 else 0

def verdict(bmi):
    if bmi<18.5: return "Underweight"
    elif bmi<25: return "Normal"
    elif bmi<30: return "Overweight"
    else: return "Obese"

class Patient(BaseModel):
    id:str
    name:str
    city:str
    age:int
    gender:Literal["male","female","others"]
    height:float
    weight:float

@app.get("/api/view")
def view():
    data=load_data()
    result={}
    for pid,p in data.items():
        bmi=calc_bmi(p["height"],p["weight"])
        result[pid]={**p,"bmi":bmi,"verdict":verdict(bmi)}
    return result

@app.post("/api/create")
def create(p:Patient):
    data=load_data()
    if p.id in data:
        raise HTTPException(400,"ID already exists")

    data[p.id]={
        "name":p.name,
        "city":p.city,
        "age":p.age,
        "gender":p.gender,
        "height":p.height,
        "weight":p.weight
    }
    save_data(data)
    return {"message":"Added successfully"}

@app.put("/api/update/{pid}")
def update(pid:str,p:Patient):
    data=load_data()
    if pid not in data:
        raise HTTPException(404,"Not found")

    data[pid]={
        "name":p.name,
        "city":p.city,
        "age":p.age,
        "gender":p.gender,
        "height":p.height,
        "weight":p.weight
    }
    save_data(data)
    return {"message":"Updated successfully"}

@app.delete("/api/delete/{pid}")
def delete(pid:str):
    data=load_data()
    if pid not in data:
        raise HTTPException(404,"Not found")
    del data[pid]
    save_data(data)
    return {"message":"Deleted successfully"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
