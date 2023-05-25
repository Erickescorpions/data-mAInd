from flask import Flask, request, jsonify
from Apriori import Apriori
from MetricasDistancia import MetricasDistancia
from flask_cors import CORS

## creamos la aplicacion
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

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
        if not request.form['confianza'] or not request.form['elevacion'] or not request.form['soporte']:
            return {
                "sucess": False,
                "mensaje": "Es necesario proporcionar los parametros para ejecutar el algoritmo."
            }
        
        parametros = {
            "confianza": float(request.form['confianza']),
            "elevacion": float(request.form['elevacion']),
            "soporte": float(request.form['soporte'])
        }
        
        file = None
        
        if 'file' in request.files:
            file = request.files['file']

        if not file:
            res = Apriori.execute(parametros)
        else: 
            res = Apriori.execute(parametros, file)
        
        return jsonify(res)
        
    except KeyError:
        return jsonify({
            "sucess": False,
            "message": "Los parametros que se necesitan recibir son ['confianza', 'elevacion', 'soporte' y opcionalmente un archivo como 'file']."
        })

    except ValueError:
        return jsonify({
            "sucess": False,
            "message": "Los parametros ['confianza', 'elevacion' y 'soporte'] deben de ser de tipo flotante."
        })

'''
    ruta para obtener las distancias, recibe el tipo de 
    metrica y el archivo y regresa un json con los datos
    estandarizados y la matriz de distancias
'''
@app.route('/api/metricas', methods=['POST'])
def executeMetricas():
    try:
        valores_metricas = ['euclidean', 'chebyshev', 'cityblock', 'minkowski']
        
        metrica = ''

        if 'metrica' in request.form:
            metrica = request.form['metrica']
        
        if metrica not in valores_metricas: 
            return jsonify({
                "sucess": False,
                "message": f"No se reconoce la metrica {metrica}, por favor envia una metrica que este dentro de los siguiente valores: {valores_metricas}"
            });

        file = None
            
        if 'file' in request.files:
            file = request.files['file']

        if not file:
            res = MetricasDistancia.execute(metrica)
        else: 
            res = MetricasDistancia.execute(metrica, file=file)

        return jsonify(res)
    except KeyError:
        return jsonify({
            "sucess": False,
            "message": "Los parametros que se necesitan recibir son ['metrica' y opcionalmente un archivo como 'file]"
        })

if __name__ == '__main__':
    app.run(debug=True, port=8000)