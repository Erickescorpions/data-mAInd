import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt     # Para la generación de gráficas a partir de los datos
import apyori

class Apriori():
    def __init__(self) -> None:
        self.frecuencia = None
        self.dataset = "datos_prueba/apriori/movies.csv"
        self.soporte = None
        self.elevacion = None
        self.confianza = None
        self.reglas = None

    def setFrecuencia(self, frecuencia):
        self.frecuencia = {}
        index = 0
        
        for item in frecuencia:
            self.frecuencia[index] = {
                "pelicula": item[0],
                "frecuencia": item[1],
                "porcentaje": item[2]
            }
            index = index + 1

    def setSoporte(self, soporte: float):
        self.soporte = soporte

    def setConfianza(self, confianza: float):
        self.confianza = confianza

    def setElevacion(self, elevacion: float):
        self.elevacion = elevacion

    def setReglasAsociacion(self, reglas):
        self.reglas = {}
        index = 0

        for regla in reglas:
            items = []
            parametros = {}
            
            for item in regla[0]:
                items.append(item)
            
            parametros = {
                "confianza": regla[2][0][2],
                "elevacion": regla[2][0][3],
                "soporte": regla[1]
            }

            self.reglas[index] = {
                "regla": items,
                "parametros": parametros
            }

            index = index + 1


    def setDataset(self, dataset: str):
        self.dataset = dataset

    def getParametros(self):
        return {
            'confianza': self.confianza,
            'elevacion': self.elevacion,
            'soporte': self.soporte
        }

    @staticmethod
    def execute(apriori):         
        #ejecucion del algoritmo 
        data = pd.read_csv(apriori.dataset)

        transacciones = data.values.reshape(-1).tolist()
        lista = pd.DataFrame(transacciones)
        lista['Frecuencia'] = 1

        #Se agrupa los elementos
        lista = lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
        lista['Porcentaje'] = (lista['Frecuencia'] / lista['Frecuencia'].sum()) #Porcentaje
        lista = lista.rename(columns={0 : 'Item'})
        lista = lista.to_numpy().tolist()
        # Se guarda la frecuencia en la clase
        # aqui
        apriori.setFrecuencia(lista)

        #Se crea una lista de listas a partir del dataframe y se remueven los 'NaN'
        data_lista = data.stack().groupby(level=0).apply(list).tolist()

        # Datos de regla de asocicion se obtienen de la clase
        # por el memonto se los asignamos asi cmo asi
        soporte_minimo = apriori.soporte
        confianza_minima = apriori.confianza
        elevacion_minima = apriori.elevacion

        reglas = apyori.apriori(data_lista, 
            min_support=soporte_minimo, 
            min_confidence=confianza_minima, 
            min_lift=elevacion_minima)  
        
        lista_reglas = list(reglas)
        df_reglas = pd.DataFrame(lista_reglas)
        #se guardan las reglas en la clase 
        apriori.setReglasAsociacion(lista_reglas)