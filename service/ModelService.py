
import joblib

from schema.WattsDesagregado import WattsDesagregado, example_WattsDesagregado
from schema.WattsTotal import WattsTotal
import pandas as pd
import numpy as np
class ModelService:
    def __init__(self):
        self.modelo = self.cargar_modelo()
        pass
    def cargar_modelo(self):
        try:
            modelo = joblib.load(r"C:\Users\user2\Documents\azul\Backend\service\modelo.h5")
            return modelo
        except Exception as e:
            print('Error al cargar el : {}'.format(e))
            return None
    def transformInputData(self, df):
        try:
               # Convertir la columna 'Fecha' a tipo datetime si no lo está
            df['Fecha'] = pd.to_datetime(df['Fecha'])

            # Dividir la columna 'Fecha' en mes, día, hora y minuto
            df['Mes'] = df['Fecha'].dt.month
            df['Dia'] = df['Fecha'].dt.day
            df['Hora'] = df['Fecha'].dt.hour
            df['Minuto'] = df['Fecha'].dt.minute

            # Agregar una nueva columna para el día de la semana en formato de texto
            df['Dia_semana'] = df['Fecha'].dt.day_name()

            # Convertir la columna 'Dia_semana' en variables dummy
            df = pd.get_dummies(df, columns=['Dia_semana'])

            # Aplicar función seno al medidor
            df['Medidor [W]_seno'] = np.sin(2 * np.pi * df['Medidor [W]'] / 24)

            # Crear un DataFrame con todas las columnas necesarias
            features = ['Mes', 'Dia', 'Hora', 'Minuto', 'Medidor [W]_seno', 
                        'Dia_semana_Friday', 'Dia_semana_Monday', 'Dia_semana_Saturday', 
                        'Dia_semana_Sunday', 'Dia_semana_Thursday', 'Dia_semana_Tuesday', 
                        'Dia_semana_Wednesday']

            # Reindexar para asegurar que todas las columnas estén presentes y rellenar con ceros si es necesario
            df = df.reindex(columns=features, fill_value=0)
            # Devolver los datos transformados
            return df
        
        except Exception as e:
            print('Error al transformar los datos de entrada: {}'.format(e))
            return None
        
    def convertirJson(self, dataFrames):
        return [dataFrames[0].to_dict(orient='records'), dataFrames[1].to_dict(orient='records')]

    def predecirDataFrame(self, inputPandasDataFrame):
        try:
            dataAlterada = self.transformInputData(inputPandasDataFrame.copy())
            prediccion = self.modelo.predict(dataAlterada)
            
            df_prediccion = np.arcsin(prediccion)
            df_prediccion = np.where(df_prediccion < 0, -df_prediccion, df_prediccion)

            columnas = ['Refrigerator','Clothes washer','Clothes Iron','Computer','Oven','Play','TV','Sound system']
            prediccionEncendidos = np.where(df_prediccion > 1, 1, 0)
            df_prediccion = pd.DataFrame(df_prediccion, columns=columnas)
            prediccionEncendidos = pd.DataFrame(prediccionEncendidos, columns=columnas)

            PrediccionesWattsDataFrame = inputPandasDataFrame.join(df_prediccion)
            PrediccionesEncendidosDataFrame = inputPandasDataFrame.join(prediccionEncendidos)
            result = self.convertirJson([PrediccionesWattsDataFrame, PrediccionesEncendidosDataFrame])
            return result
        except Exception as e:
            print(e)
            return 

    