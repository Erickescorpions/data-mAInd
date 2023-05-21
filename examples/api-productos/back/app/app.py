# importamos funciones y clases de flask 
from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify({"message": "hello"})

@app.route('/products', methods=['GET'])
def gerProducts():
    return jsonify({"products": products, "message": "Products list"})

@app.route('/products/<string:product_name>', methods=['GET'])
def getProduct(product_name):
    print(product_name)
    products_found = [product for product in products if product['name'] == product_name]
    if(len(products_found) >0):
        return jsonify({"product": products_found})

    return jsonify({"message": "Product not found"})

@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }

    products.append(new_product)
    return jsonify({
        "message": "Producto agregado correctamente.",
        "products": products
    })

@app.route('/products/<string:product_name>', methods=["PUT"])
def editProduct(product_name):
    products_found = [product for product in products if product['name'] == product_name]
    if(len(products_found) >0):
        products_found[0]['name'] = request.json['name']
        products_found[0]['price'] = request.json['price']
        products_found[0]['quantity'] = request.json['quantity']

        return jsonify({
            "message": "Product actualizado",
            "product": products_found[0]
        })
    
    return jsonify({"message": "Product not found"})

@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    products_found = [product for product in products if product['name'] == product_name]
    if(len(products_found) >0):
        products.remove(products_found[0])

        return jsonify({
            "message": "Producto eliminado",
            "products": products
        })
    
    return jsonify({"message": "Product not found"})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
