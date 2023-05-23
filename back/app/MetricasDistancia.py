import pandas as pd                         # Para la manipulación y análisis de datos
import numpy as np                          # Para crear vectores y matrices n dimensionales
from scipy.spatial.distance import cdist    # Para el cálculo de distancias
from sklearn.preprocessing import StandardScaler, MinMaxScaler  

class MetricasDistancia():
    @staticmethod
    def execute(metrica, dataset="datos_prueba/metricas/Hipoteca.csv"):         
        # ejecucion del algoritmo 
        data = pd.read_csv(dataset)

        # estandarizacion de datos
        estandarizar = StandardScaler()
        # Se calculan la media y desviación y se escalan los datos
        data_estandarizada = estandarizar.fit_transform(data)

        print(data_estandarizada)

        # matriz de distancias
        dst = cdist(data_estandarizada, data_estandarizada, metric=metrica)
        dst = dst.tolist()

        return {
            "sucess": True,
            "distancias": dst
        }
