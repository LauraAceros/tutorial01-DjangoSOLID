from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['POST'])
def realizar_compra():
    data = request.get_json()
    # Simulación de lógica de negocio extraída [cite: 26]
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad', 1)

    if not producto_id:
        return jsonify({"error": "Falta el ID del producto"}), 400 [cite: 29]

    return jsonify({
        "mensaje": "Compra procesada exitosamente por el Microservicio Flask (v2)", [cite: 30]
        "producto_id": producto_id, [cite: 32]
        "cantidad": cantidad, [cite: 33]
        "status": "Aprobado" [cite: 34]
    }), 200 [cite: 36]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) [cite: 40]