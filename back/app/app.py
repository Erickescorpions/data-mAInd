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
        if not request.json['confianza'] or not request.json['elevacion'] or not request.json['soporte']:
            return {
                "sucess": False,
                "mensaje": "Es necesario proporcionar los parametros para ejecutar el algoritmo."
            }
        
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

'''
    ruta para obtener las distancias, recibe el tipo de 
    metrica y el archivo y regresa un json con los datos
    estandarizados y la matriz de distancias
'''
# @app.route('/api/metricas', methods=['GET'])
def executeMetricas():
    valores_metricas = ['euclidean', 'chebyshev', 'cityblock', 'minkowski']
    metrica = request.json['metrica']
    
    if metrica not in valores_metricas: 
        return {
            "sucess": False,
            "message": f"No se reconoce la metrica {metrica}, por favor envia una metrica que este dentro de los siguiente valores: {valores_metricas}"
        }

    res = MetricasDistancia.execute(metrica)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, port=8000)