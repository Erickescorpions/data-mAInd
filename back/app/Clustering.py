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
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator

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

        data_np = np.array(data[columnas])
        new_data = data[columnas]

        if estandarizacion == 'StandardScaler': 
            estandarizar = StandardScaler() 
        else:
            estandarizar = MinMaxScaler()


        MEstandarizada = estandarizar.fit_transform(data_np)
        MJerarquico = AgglomerativeClustering(n_clusters=int(numero_clusters), linkage='complete', metric=metrica)
        MJerarquico.fit_predict(MEstandarizada)

        new_data['clusterH'] = MJerarquico.labels_
        centroidesH = new_data.groupby('clusterH').mean()

        return {
            "sucess": True,
            "centroides": centroidesH.to_json(orient='records')
        }
    
    @staticmethod
    def obtenerCodo(estandarizacion, columnas, file=None, dataset="datos_prueba/apriori/movies.csv"):         
        if file:
            #print('recibiendo archivo')
            data = pd.read_csv(file)
        else:
            #print('default')
            data = pd.read_csv(dataset)
        
        # agarramos solo las columnas que seleccionamos
        data = np.array(data[columnas])

        if estandarizacion == 'StandardScaler': 
            estandarizar = StandardScaler() 
        else:
            estandarizar = MinMaxScaler()

        MEstandarizada = estandarizar.fit_transform(data)
        
        #Definición de k clusters para K-means
        #Se utiliza random_state para inicializar el generador interno de números aleatorios
        SSE = []
        for i in range(2, 12):
            km = KMeans(n_clusters=i, random_state=0)
            km.fit(MEstandarizada)
            SSE.append(km.inertia_)

        #Se grafica SSE en función de k
        plt.figure(figsize=(10, 7))
        plt.plot(range(2, 12), SSE, marker='o')
        plt.xlabel('Cantidad de clusters *k*')
        plt.ylabel('SSE')
        plt.title('Elbow Method')

        temp_file = f'{Clustering.generar_hash_aleatorio()}.png'
        # Guardar la figura en un archivo de imagen
        plt.savefig(f'image_tmp/{temp_file}')
        plt.close()

        kl = KneeLocator(range(2, 12), SSE, curve="convex", direction="decreasing")
        plt.style.use('ggplot')
        temp_file2 = f'{Clustering.generar_hash_aleatorio()}.png'
        # Guardar la figura en un archivo de imagen
        kl.plot_knee()
        plt.savefig(f'image_tmp/{temp_file2}')
        plt.close()

        return {
            "sucess": True,
            "data": {
                "image": f"http://localhost:8000/api/clustering/image/{temp_file}",
                "knee_point": f"http://localhost:8000/api/clustering/image/{temp_file2}"
            }
        }
    
    def obteniendoClustersParticional(numero_clusters, estandarizacion, columnas, file=None, dataset="datos_prueba/apriori/movies.csv"):
        if file:
            #print('recibiendo archivo')
            data = pd.read_csv(file)
        else:
            #print('default')
            data = pd.read_csv(dataset)

        data_np = np.array(data[columnas])
        new_data = data[columnas]

        if estandarizacion == 'StandardScaler': 
            estandarizar = StandardScaler() 
        else:
            estandarizar = MinMaxScaler()


        MEstandarizada = estandarizar.fit_transform(data_np)
        MParticional = KMeans(n_clusters=int(numero_clusters), random_state=0).fit(MEstandarizada)
        MParticional.predict(MEstandarizada)

        new_data['clusterP'] = MParticional.labels_
        centroidesP = new_data.groupby('clusterP').mean()

        return {
            "sucess": True,
            "centroides": centroidesP.to_json(orient='records')
        }
    