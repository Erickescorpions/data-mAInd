import pandas as pd                         # Para la manipulación y análisis de datos
import numpy as np                          # Para crear vectores y matrices n dimensionales
from scipy.spatial.distance import cdist    # Para el cálculo de distancias
from sklearn.preprocessing import StandardScaler, MinMaxScaler  

class MetricasDistancia():
    @staticmethod
    def execute(metrica, file=None, dataset="datos_prueba/metricas/Hipoteca.csv"):         
        # ejecucion del algoritmo 
        if file:
            #print('recibiendo archivo')
            data = pd.read_csv(file)
        else:
            #print('default')
            data = pd.read_csv(dataset)

        # eliminando columnas no numericas
        columnas_no_numericas = data.select_dtypes(exclude='number').columns
        data_df = data.drop(columnas_no_numericas, axis=1)

        # estandarizacion de datos
        estandarizar = StandardScaler()
        data_estandarizada = estandarizar.fit_transform(data_df)

        #print(data_estandarizada)

        # matriz de distancias
        dst = cdist(data_estandarizada, data_estandarizada, metric=metrica)
        dst = dst.tolist()

        return {
            "sucess": True,
            "distancias": dst
        }
