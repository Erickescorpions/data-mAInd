import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering

class Clustering():
    
    @staticmethod
    def generaMatrizCorrlaciones(file=None, dataset='datos_prueba/clustering/Hipoteca.csv'):
        if file:
            data = pd.read_csv(file)
        else:
            data = pd.read_csv(dataset)

        # eliminando columnas no numericas
        columnas_no_numericas = data.select_dtypes(exclude='number').columns
        data = data.drop(columnas_no_numericas, axis=1)

        Correlaciones = data.corr(method='pearson')

        plt.subplots(figsize=(10, 8))

        MatrizInf = np.triu(Correlaciones)
        heatmap = sns.heatmap(Correlaciones, cmap='RdBu_r', annot=True, mask=MatrizInf)

        # Guarda el mapa de calor en un archivo temporal
        temp_file = 'heatmap.png'
        heatmap.figure.savefig(temp_file)

        # Cierra la figura para liberar recursos
        plt.close(heatmap.figure)

        return temp_file

    @staticmethod
    def executeJerarquico(parametros, file=None, dataset="datos_prueba/apriori/movies.csv"):         
        pass