from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

app = FastAPI(
    title="HEI API_evaluation final",
    description="API pour la gestion de vehicules et leur caracteristiques",
    version="1.0.0",
)

class Caracteristique(BaseModel):
    max_speed: float
    max_fuel_capacity: float


class Car(BaseModel):
    id: int
    brand: str
    model: str
    caracteristiques: Optional[Caracteristique] = None

in_memory_db: Dict[str, Car] = {}

@app.get("/ping")
def pong():
    return {"message": "pong"}

@app.post("/cars", response_model=Car, status_code=status.HTTP_201_CREATED, summary="Créer un nouveau véhicule")
async def create_car(id, brand: str, model: str):
    if id in in_memory_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Car with this ID already exists"
        )
    new_car = Car(id=id, brand=brand, model=model)
    in_memory_db[id] = new_car
    return new_car

@app.get("/cars",response_model=List[Car], summary="Get all cars")
async def get_all_cars():
    return list(in_memory_db.values())

@app.get("/cars/{id}", response_model=Car, summary="Get a car by ID")
async def get_car_by_id(id: str):
    car = in_memory_db.get(id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

@app.put("/cars/{id}/caracteristiques", response_model=Car, summary="Update car characteristics")
async def update_caracteristiques(id: int, caracteristiques: Caracteristique):
    if id not in in_memory_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    
    car = in_memory_db[id]
    car.caracteristiques = caracteristiques
    in_memory_db[id] = car
    return car