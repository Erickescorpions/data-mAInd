from flask import Flask, request, jsonify
from Apriori import Apriori
from MetricasDistancia import MetricasDistancia

## creamos la aplicacion
app = Flask(__name__)

@app.route('/')
def index():
    return '¡Hola mundo!'

'''
    ruta para obtener los resultados del algoritmo apriori,
    recibe el archivo y los parametros y regresa un json 
    con la frecuencia de todas los registros
    y regresa las reglas generadas
'''
@app.route('/api/apriori', methods=['POST'])
def executeApriori():

    try:
        parametros = {
            "confianza": float(request.json['confianza']),
            "elevacion": float(request.json['elevacion']),
            "soporte": float(request.json['soporte'])
        }

        # file = 

        res = Apriori.execute(parametros)
        return jsonify(res)
        
    
    except ValueError:
        return {
            "sucess": False,
            "message": "Los parametros ['confianza', 'elevacion' y 'soporte'] deben de ser de tipo flotante."
        }

# '''
#     ruta para agregar un valor a la metrica
# '''
# @app.route('/api/metricas/metrica', methods=['POST'])
# def agregarMetrica():
#     metricasController = MetricasDistanciaController()
#     res = metricasController.setMetrica(request)
#     return jsonify(res)

'''
    ruta para obtener las distancias, recibe el tipo de 
    metrica y el archivo y regresa un json con los datos
    estandarizados y la matriz de distancias
'''
# @app.route('/api/metricas', methods=['GET'])
# def executeMetricas():
#     metricasController = MetricasDistanciaController()
#     res = metricasController.execute()
#     return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, port=8000)