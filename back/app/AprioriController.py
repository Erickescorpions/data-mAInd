from Singleton import Singleton
from Apriori import Apriori
import json

class AprioriController(metaclass=Singleton):
    
    def __init__(self) -> None:
        self.apriori = Apriori()

    def setParametros(self, request):
        try:
            parametros = {
                "confianza": float(request.json['confianza']),
                "elevacion": float(request.json['elevacion']),
                "soporte": float(request.json['soporte'])
            }
        
            self.apriori.setSoporte(parametros['soporte'])
            self.apriori.setConfianza(parametros['confianza'])
            self.apriori.setElevacion(parametros['elevacion'])

            params = self.apriori.getParametros()

            return {
                "success": True,
                "message": "Se han asignado correctamente los parametros.",
                "params": params
            }
        
        except ValueError:
            return {
                "sucess": False,
                "message": "Los parametros deben de ser de tipo flotante."
            }

    
    def getParametros(self):
        return self.apriori.getParametros()

    def execute(self):
        if not self.apriori.confianza or not self.apriori.elevacion or not self.apriori.soporte:
            return {
                "sucess": False,
                "mensaje": "Es necesario proporcionar los parametros para ejecutar el algoritmo."
            }
        
        Apriori.execute(self.apriori)
        reglas = self.apriori.reglas
        frecuencia = self.apriori.frecuencia
        return {
            "reglas" : reglas,
            "frecuencia": frecuencia
        }
        

