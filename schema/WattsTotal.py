from datetime import datetime as date
from pydantic import BaseModel

class WattsTotal(BaseModel):
    Fecha:date
    Medidor: float

example_WattsTotal = WattsTotal(
    Fecha = date(2021, 1, 1, 1,1),
    Medidor = 0.0
)

