from flask import Flask, request, jsonify
from AprioriController import AprioriController
from MetricasDistanciaController import MetricasDistanciaController

## creamos la aplicacion
app = Flask(__name__)
aprioriController = None
metricasController = None

@app.route('/')
def index():
    return '¡Hola mundo!'

''' 
    ruta para agregar los parametros que utiliza el 
    algoritmo apriori (elevacion, confianza y soporte)  
 '''
@app.route('/api/apriori/parametros', methods=['POST'])
def agregarParametrosApriori():
    aprioriController = AprioriController()
    res = aprioriController.setParametros(request)

    return jsonify(res)

'''
    ruta para obtener los parametros del algoritmo apriori
'''
@app.route('/api/apriori/parametros', methods=['GET'])
def getParametrosApriori():
    aprioriController = AprioriController()
    res = aprioriController.getParametros()
    return jsonify(res)

'''
    ruta para obtener los resultados del algoritmo apriori
    regresa un json con la frecuencia de todas los registros
    y regresa las reglas generadas
'''
@app.route('/api/apriori/execute', methods=['GET'])
def executeApriori():
    aprioriController = AprioriController()
    res = aprioriController.execute()
    return jsonify(res)

'''
    ruta para agregar un valor a la metrica
'''
@app.route('/api/metricas/metrica', methods=['POST'])
def agregarMetrica():
    metricasController = MetricasDistanciaController()
    res = metricasController.setMetrica(request)
    return jsonify(res)

'''
    ruta para obtener las distancias
'''
@app.route('/api/metricas/execute', methods=['GET'])
def executeMetricas():
    metricasController = MetricasDistanciaController()
    res = metricasController.execute()
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, port=8000)