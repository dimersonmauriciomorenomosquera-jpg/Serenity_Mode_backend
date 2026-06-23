from flask import Blueprint, request, jsonify
from src.models.carrito import Carrito
from datetime import datetime

Pago_bp = Blueprint('Pago', __name__)

@Pago_bp.route('/', methods=['GET'])
def get_carritos():
    pagos = Pago.get()
    lista = []

    for pago in pagos:
        lista.append({
            'id_pago': pago.id_pago,
            'fecha_pago': str(pago.fecha_pago),
            'monto': float(pago.monto),
            'metodo_pago': str(pago.metodo_pago),
            'estado_pago': str(pago.estado_pago),
            'id_factura': pago.id_factura,
            'id_cliente': pago.id_cliente
        })

    return jsonify(lista), 200

@Pago_bp.route('/<int:id>', methods=['GET'])
def get_pago(id):
    pago = Pago.get_by_id(id)

    if not pago:
        return jsonify({'message': 'pago no encontrado'}), 404

    return jsonify({
            'id_pago': pago.id_pago,
            'fecha_pago': str(pago.fecha_pago),
            'monto': float(pago.monto),
            'metodo_pago': str(pago.metodo_pago),
            'estado_pago': str(pago.estado_pago),
            'id_factura': pago.id_factura,
            'id_cliente': pago.id_cliente
    }), 200

@Pago_bp.route('/', methods=['POST'])
def create_pago():
    data = request.get_json()

    required = [
        'fecha_pago',
        'monto',
        'metodo_pago',
        'estado_pago',
        'id_factura',
        'id_cliente'
    ]

    for field in required:
        if not data.get(field):
            return jsonify({'message': f'{field} es obligatorio'}), 400

    try:
        fecha = datetime.strptime(
            data['fecha_pago'],
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return jsonify({
            'message': 'Formato de fecha inválido (YYYY-MM-DD)'
        }), 400

    try:
        monto = float(data['monto'])
    except ValueError:
        return jsonify({
            'message': 'El monto debe ser numérico'
        }), 400

    pago = Pago(
        fecha_pago=fecha,
        monto=monto,
        metodo_pago=data['metodo_pago'],
        estado_pago=data['estado_pago'],
        id_factura=data['id_factura'],
        id_cliente=data['id_cliente']
    )

    pago.save()

    return jsonify({
        'message': 'Pago creado exitosamente',
        'pago': pago.to_dict()
    }), 201


@Pago_bp.route('/<int:id>', methods=['DELETE'])
def delete_pago(id):
    pago = Pago.get_by_id(id)

    if not pago:
        return jsonify({'message': 'Pago no encontrado'}), 404

    pago.delete()

    return jsonify({'message': 'Pago eliminado exitosamente'}), 200


@Pago_bp.route('/<int:id>', methods=['PUT'])
def update_pago(id):
    pago = Pago.get_by_id(id)

    if not pago:
        return jsonify({'message': 'Pago no encontrado'}), 404

    data = request.get_json()

    if 'fecha_pago' in data:
        try:
            pago.fecha_pago = datetime.strptime(
                data['fecha_pago'],
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({
                'message': 'Fecha inválida'
            }), 400

    if 'monto' in data:
        try:
            pago.monto = float(data['monto'])
        except ValueError:
            return jsonify({
                'message': 'Monto inválido'
            }), 400

    if 'metodo_pago' in data:
        pago.metodo_pago = data['metodo_pago']

    if 'estado_pago' in data:
        pago.estado_pago = data['estado_pago']

    if 'id_factura' in data:
        pago.id_factura = data['id_factura']

    if 'id_cliente' in data:
        pago.id_cliente = data['id_cliente']

    pago.save()

    return jsonify({
        'message': 'Pago actualizado exitosamente',
        'pago': pago.to_dict()
    }), 200