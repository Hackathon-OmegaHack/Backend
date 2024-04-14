from datetime import datetime as date
from pydantic import BaseModel

class WattsDesagregado(BaseModel):
    Fecha: date
    Medidor: float
    Refrigator: float
    ClothesWasher: float
    ClothesIron: float
    Computer: float
    Oven: float
    Play: float
    TV: float
    SoundSystem: float

example_WattsDesagregado = WattsDesagregado(
    Fecha = date(2021, 1, 1, 1,1),
    Medidor = 0.0,
    Refrigator = 0.0,
    ClothesWasher = 0.0,
    ClothesIron = 0.0,
    Computer = 0.0,
    Oven = 0.0,
    Play = 0.0,
    TV = 0.0,
    SoundSystem = 0.0
)