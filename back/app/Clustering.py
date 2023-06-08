import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns             # Para la visualización de datos basado en matplotlib
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
import secrets
import hashlib
import json

class Clustering():
    @staticmethod
    def generar_hash_aleatorio():
        # Genera una cadena aleatoria
        cadena_aleatoria = secrets.token_hex(16)  # Genera una cadena hexadecimal de 16 bytes (32 caracteres)

        # Calcula el hash SHA256 de la cadena aleatoria
        sha256_hash = hashlib.sha256(cadena_aleatoria.encode()).hexdigest()
        return sha256_hash

    
    @staticmethod
    def generaMatrizCorrlaciones(file=None, dataset='datos_prueba/clustering/Hipoteca.csv'):
        if file:
            data = pd.read_csv(file)
        else:
            data = pd.read_csv(dataset)

        # eliminando columnas no numericas
        columnas_no_numericas = data.select_dtypes(exclude='number').columns
        data = data.drop(columnas_no_numericas, axis=1)
        columnas = data.columns.values.tolist()

        Correlaciones = data.corr(method='pearson')

        MatrizInf = np.triu(Correlaciones)
        heatmap = sns.heatmap(Correlaciones, cmap='RdBu_r', annot=True, mask=MatrizInf)

        # Ajusta el tamaño de la figura del mapa de calor
        fig = heatmap.get_figure()
        fig.set_size_inches(10, 8) 

        # Guarda el mapa de calor en un archivo temporal
        temp_file = f'{Clustering.generar_hash_aleatorio()}.png'
        fig.savefig(f'image_tmp/{temp_file}')

        # Cierra la figura para liberar recursos
        plt.close(fig)

        return {
            "sucess": True,
            "data": {
                "image": f"http://localhost:8000/api/clustering/image/{temp_file}",
                'columnas': columnas
            }
        }

    @staticmethod
    def obtenerArbol(metrica, estandarizacion, columnas, file=None, dataset="datos_prueba/apriori/movies.csv"):         
        if file:
            #print('recibiendo archivo')
            data = pd.read_csv(file)
        else:
            #print('default')
            data = pd.read_csv(dataset)
        
        data = np.array(data[columnas])

        print(columnas)

        if estandarizacion == 'StandardScaler': 
            estandarizar = StandardScaler() 
        else:
            estandarizar = MinMaxScaler()

        MEstandarizada = estandarizar.fit_transform(data)
        
        # Crear una figura
        
        plt.figure(figsize=(8, 7))
        
        plt.title("Dendograma")
        Arbol = shc.dendrogram(shc.linkage(MEstandarizada, method='complete', metric=metrica))
        temp_file = f'{Clustering.generar_hash_aleatorio()}.png'
        # Guardar la figura en un archivo de imagen
        plt.savefig(f'image_tmp/{temp_file}')
        plt.close()

        return {
            "sucess": True,
            "data": {
                "image": f"http://localhost:8000/api/clustering/image/{temp_file}"
            }
        }
    
    def obteniendoClusters(numero_clusters, metrica, estandarizacion, columnas, file=None, dataset="datos_prueba/apriori/movies.csv"):
        if file:
            #print('recibiendo archivo')
            data = pd.read_csv(file)
        else:
            #print('default')
            data = pd.read_csv(dataset)

        columnas_no_numericas = data.select_dtypes(exclude='number').columns
        data = data.drop(columnas_no_numericas, axis=1)
        nombre_columnas = data.columns.values.tolist()
        data_np = np.array(data[nombre_columnas])

        if estandarizacion == 'StandardScaler': 
            estandarizar = StandardScaler() 
        else:
            estandarizar = MinMaxScaler()

        MEstandarizada = estandarizar.fit_transform(data_np)
        MJerarquico = AgglomerativeClustering(n_clusters=int(numero_clusters), linkage='complete', metric=metrica)
        MJerarquico.fit_predict(MEstandarizada)

        new_data = data[columnas]

        new_data['clusterH'] = MJerarquico.labels_
        centroidesH = new_data.groupby('clusterH').mean()

        return {
            "sucess": True,
            "centroides": centroidesH.to_json(orient='records')
        }