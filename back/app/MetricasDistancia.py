import pandas as pd                         # Para la manipulación y análisis de datos
import numpy as np                          # Para crear vectores y matrices n dimensionales
from scipy.spatial.distance import cdist    # Para el cálculo de distancias
from sklearn.preprocessing import StandardScaler, MinMaxScaler  

class MetricasDistancia():
    def __init__(self) -> None:
        self.dataset = "datos_prueba/metricas/Hipoteca.csv"
        self.data_estandarizada = None
        self.metrica = 'euclidean'
        self.distancias = None

    def setDistancias(self, distancias):
        self.distancias = distancias

    def setDataset(self, dataset: str):
        pass

    def setDataEstandarizada(self, data_estandarizada):
        self.data_estandarizada = data_estandarizada

    def setMetrica(self, metrica):
        self.metrica = metrica

    @staticmethod
    def execute(metricas):         
        # ejecucion del algoritmo 
        data = pd.read_csv(metricas.dataset)

        # estandarizacion de datos
        estandarizar = StandardScaler()
        # Se calculan la media y desviación y se escalan los datos
        data_estandarizada = estandarizar.fit_transform(data)

        metricas.setDataEstandarizada(data_estandarizada)

        # matriz de distancias
        dst = cdist(data_estandarizada, data_estandarizada, metric=metricas.metrica)
        metricas.setDistancias(dst.tolist())
