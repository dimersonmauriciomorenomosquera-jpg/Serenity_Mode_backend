from flask import Blueprint, request, jsonify
from src.models.factura import Factura
from datetime import datetime

Factura_bp = Blueprint('Factura', __name__)

@Factura_bp.route('/', methods=['GET'])
def get_facturas():
    facturas = Factura.get()
    lista = []

    for factura in facturas:
        lista.append({
            'id_factura': factura.id_factura,
            'fecha_factura': str(factura.fecha_factura),
            'total_pagar': float(factura.total_pagar),
            'estado_pago': factura.estado_pago,
            'id_cliente': factura.id_cliente,
            'id_carrito': factura.id_carrito
        })

    return jsonify(lista), 200

@Factura_bp.route('/<int:id>', methods=['GET'])
def get_factura(id):
    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404

    return jsonify({
        'id_factura': factura.id_factura,
        'fecha_factura': str(factura.fecha_factura),
        'total_pagar': float(factura.total_pagar),
        'estado_pago': factura.estado_pago,
        'id_cliente': factura.id_cliente,
        'id_carrito': factura.id_carrito
    }), 200


@Factura_bp.route('/', methods=['POST'])
def create_factura():
    data = request.get_json()

    required = [
        'fecha_factura',
        'total_pagar',
        'estado_pago',
        'id_cliente',
        'id_carrito'
    ]

    for field in required:
        if not data.get(field):
            return jsonify({
                'message': f'{field} es obligatorio'
            }), 400

    try:
        fecha = datetime.strptime(
            data['fecha_factura'],
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return jsonify({
            'message': 'Formato de fecha inválido (YYYY-MM-DD)'
        }), 400

    try:
        total = float(data['total_pagar'])
    except ValueError:
        return jsonify({
            'message': 'El total debe ser numérico'
        }), 400

    factura = Factura(
        fecha_factura=fecha,
        total_pagar=total,
        estado_pago=data['estado_pago'],
        id_cliente=data['id_cliente'],
        id_carrito=data['id_carrito']
    )

    factura.save()

    return jsonify({
        'message': 'Factura creada exitosamente'
    }), 201

@Factura_bp.route('/<int:id>', methods=['DELETE'])
def delete_factura(id):
    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    factura.delete()

    return jsonify({
        'message': 'Factura eliminada exitosamente'
    }), 200

@Factura_bp.route('/<int:id>', methods=['PUT'])
def update_factura(id):
    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    data = request.get_json()

    if 'fecha_factura' in data:
        try:
            factura.fecha_factura = datetime.strptime(
                data['fecha_factura'],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                'message': 'Fecha inválida'
            }), 400

    if 'total_pagar' in data:
        try:
            factura.total_pagar = float(data['total_pagar'])
        except ValueError:
            return jsonify({
                'message': 'Total inválido'
            }), 400

    if 'estado_pago' in data:
        factura.estado_pago = data['estado_pago']

    if 'id_cliente' in data:
        factura.id_cliente = data['id_cliente']

    if 'id_carrito' in data:
        factura.id_carrito = data['id_carrito']

    factura.update()

    return jsonify({
        'message': 'Factura actualizada exitosamente'
    }), 200