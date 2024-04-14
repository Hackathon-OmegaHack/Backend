from fastapi import FastAPI
from schema.WattsTotal import WattsTotal, example_WattsTotal 
from schema.WattsDesagregado import WattsDesagregado, example_WattsDesagregado
from schema.ResultadoCSV import ResultadoCSV
from fastapi import Body
from fastapi import UploadFile, File
from io import StringIO
from service.ModelService import ModelService
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/", response_model= WattsDesagregado)
def read_root(wattsTotal: WattsTotal = Body(example =example_WattsTotal )):
    print(Path().absolute())
    wattsTotal_dicta = wattsTotal.dict()
    return example_WattsDesagregado
@app.post("/upload-csv/", response_model = ResultadoCSV)
async def upload_csv(file: UploadFile = File(...), ):
    contents = await file.read()
    csv_string = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    jsons = ModelService().predecirDataFrame(df)
    response =  ResultadoCSV(
        csv_predicciones_watts = jsons[0],
        csv_predicciones_encendidos = jsons[1],
    )
    return response
