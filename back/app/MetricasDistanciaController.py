from Singleton import Singleton
from MetricasDistancia import MetricasDistancia

class MetricasDistanciaController(metaclass=Singleton):
    
    def __init__(self) -> None:
        self.metricas = MetricasDistancia()

    def setMetrica(self, request):
        valores_metricas = ['euclidean', 'chebyshev', 'cityblock', 'minkowski']
        metrica = request.json['metrica']
        
        if metrica not in valores_metricas: 
            return {
                "sucess": False,
                "message": f"No se reconoce la metrica {metrica}, por favor envia una metrica que este dentro de los siguiente valores: {valores_metricas}"
            }

        self.metricas.setMetrica(metrica)
        return {
            "sucess": True,
            "message": f"Se ha agregado la metrica '{self.metricas.metrica}' correctamente"
        }

    def execute(self):
        res = MetricasDistancia.execute(self.metricas)
        return {
            "sucess": True,
            "distancias": self.metricas.distancias
        }
        

