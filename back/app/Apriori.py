import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt     # Para la generación de gráficas a partir de los datos
import apyori

class Apriori():
    
    @staticmethod
    def frecuencia(file=None, dataset='datos_prueba/apriori/movies.csv'):
        if file:
            #print('recibiendo archivo')
            data = pd.read_csv(file)
        else:
            #print('default')
            data = pd.read_csv(dataset)

        transacciones = data.values.reshape(-1).tolist()
        lista = pd.DataFrame(transacciones)
        lista['Frecuencia'] = 1

        #Se agrupa los elementos
        lista = lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
        lista = lista.rename(columns={0 : 'Item'})
        lista = lista.to_numpy().tolist()

        # Convertimos las frecuencias a json
        frecuencias = []
        labels = []

        for item in lista:
            labels.append(item[0])
            frecuencias.append(item[1])
        
        return {
            'sucess': True,
            'frecuencias': frecuencias,
            'labels': labels
        }

    @staticmethod
    def execute(parametros, file=None, dataset="datos_prueba/apriori/movies.csv"):         
        #ejecucion del algoritmo 
        
        if file:
            #print('recibiendo archivo')
            data = pd.read_csv(file)
        else:
            #print('default')
            data = pd.read_csv(dataset)

        #Se crea una lista de listas a partir del dataframe y se remueven los 'NaN'
        data_lista = data.stack().groupby(level=0).apply(list).tolist()

        # Datos de regla de asocicion se obtienen de la clase
        # por el memonto se los asignamos asi cmo asi
        soporte_minimo = parametros['soporte']
        confianza_minima = parametros['confianza']
        elevacion_minima = parametros['elevacion']

        reglas = apyori.apriori(data_lista, 
            min_support=soporte_minimo, 
            min_confidence=confianza_minima, 
            min_lift=elevacion_minima)  
        
        lista_reglas = list(reglas)
        df_reglas = pd.DataFrame(lista_reglas)

        #se guardan las reglas en la clase 
        reglas = {}
        index = 0

        for regla in lista_reglas:
            items = []
            parametros = {}
            
            for item in regla[0]:
                items.append(item)

            reglas[index] = {
                "regla": ' | '.join(items),
                "confianza": regla[2][0][2],
                "elevacion": regla[2][0][3],
                "soporte": regla[1]
            }

            index = index + 1

        return {
            "sucess": True,
            "reglas": reglas
        }