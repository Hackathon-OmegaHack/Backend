
from pydantic import BaseModel
from schema.WattsDesagregado import WattsDesagregado, example_WattsDesagregado

class ResultadoCSV(BaseModel):
    csv_predicciones_watts: list[dict]
    csv_predicciones_encendidos: list[dict]
    
