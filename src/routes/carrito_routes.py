from flask import Blueprint, request, jsonify
from src.models.carrito import Carrito
from datetime import datetime

Carrito_bp = Blueprint('Carrito', __name__)

@Carrito_bp.route('/', methods=['GET'])
def get_carritos():
    carritos = Carrito.get()
    lista = []

    for carrito in carritos:
        lista.append({
            'id_carrito': carrito.id_carrito,
            'fecha_creacion': str(carrito.fecha_creacion),
            'total_carrito': float(carrito.total_carrito),
            'id_cliente': carrito.id_cliente
        })

    return jsonify(lista), 200

@Carrito_bp.route('/<int:id>', methods=['GET'])
def get_carrito(id):
    carrito = Carrito.get_by_id(id)

    if not carrito:
        return jsonify({'message': 'Carrito no encontrado'}), 404

    return jsonify({
        'id_carrito': carrito.id_carrito,
        'fecha_creacion': str(carrito.fecha_creacion),
        'total_carrito': float(carrito.total_carrito),
        'id_cliente': carrito.id_cliente
    }), 200

@Carrito_bp.route('/', methods=['POST'])
def create_carrito():
    data = request.get_json()

    # VALIDACIONES PRIMERO
    required = ['fecha_creacion', 'total_carrito', 'id_cliente']

    for field in required:
        if not data.get(field):
            return jsonify({'message': f'{field} es obligatorio'}), 400

    try:
        fecha = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'message': 'Formato de fecha inválido (YYYY-MM-DD)'}), 400

    try:
        total = float(data['total_carrito'])
    except ValueError:
        return jsonify({'message': 'Total debe ser numérico'}), 400

    carrito = Carrito(
        fecha_creacion=fecha,
        total_carrito=total,
        id_cliente=data['id_cliente']
    )

    carrito.save()

    return jsonify({
        'message': 'Carrito creado exitosamente',
        'carrito': {
            'fecha_creacion': str(carrito.fecha_creacion),
            'total_carrito': float(carrito.total_carrito),
            'id_cliente': carrito.id_cliente
        }
    }), 201

@Carrito_bp.route('/<int:id>', methods=['DELETE'])
def delete_carrito(id):
    carrito = Carrito.get_by_id(id)

    if not carrito:
        return jsonify({'message': 'Carrito no encontrado'}), 404

    carrito.delete()

    return jsonify({'message': 'Carrito eliminado exitosamente'}), 200

@Carrito_bp.route('/<int:id>', methods=['PUT'])
def update_carrito(id):
    carrito = Carrito.get_by_id(id)

    if not carrito:
        return jsonify({'message': 'Carrito no encontrado'}), 404

    data = request.get_json()

    if 'fecha_creacion' in data:
        try:
            carrito.fecha_creacion = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'message': 'Fecha inválida'}), 400

    if 'total_carrito' in data:
        try:
            carrito.total_carrito = float(data['total_carrito'])
        except ValueError:
            return jsonify({'message': 'Total inválido'}), 400

    if 'id_cliente' in data:
        carrito.id_cliente = data['id_cliente']

    carrito.save()

    return jsonify({
        'message': 'Carrito actualizado exitosamente',
        'carrito': {
            'fecha_creacion': str(carrito.fecha_creacion),
            'total_carrito': float(carrito.total_carrito),
            'id_cliente': carrito.id_cliente
        }
    }), 200