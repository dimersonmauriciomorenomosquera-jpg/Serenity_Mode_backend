from flask import Blueprint, request, jsonify
from src.models.pago import Pago
from datetime import datetime

from flask_jwt_extended import jwt_required
from src.utils.decorators import admin_required


Pago_bp = Blueprint('Pago', __name__)


# ==========================================================
# OBTENER TODOS LOS PAGOS
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_pagos():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Validar página
    if page < 1:
        return jsonify({
            'message': 'La página debe ser mayor o igual a 1'
        }), 400

    # Validar cantidad por página
    if per_page < 1:
        return jsonify({
            'message': 'La cantidad por página debe ser mayor o igual a 1'
        }), 400

    pagos, total = Pago.get(
        page=page,
        per_page=per_page
    )

    total_pages = (total + per_page - 1) // per_page

    lista = []

    for pago in pagos:
        lista.append({
            'id_pago': pago.id_pago,
            'fecha_pago': str(pago.fecha_pago),
            'monto': float(pago.monto),
            'metodo_pago': pago.metodo_pago,
            'estado_pago': pago.estado_pago,
            'id_factura': pago.id_factura,
            'id_cliente': pago.id_cliente
        })

    return jsonify({
        'data': lista,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': total_pages
        }
    }), 200


# ==========================================================
# OBTENER UN PAGO POR ID
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@admin_required
def get_pago(id):

    pago = Pago.get_by_id(id)

    if not pago:
        return jsonify({
            'message': 'Pago no encontrado'
        }), 404

    return jsonify({
        'id_pago': pago.id_pago,
        'fecha_pago': str(pago.fecha_pago),
        'monto': float(pago.monto),
        'metodo_pago': str(pago.metodo_pago),
        'estado_pago': str(pago.estado_pago),
        'id_factura': pago.id_factura,
        'id_cliente': pago.id_cliente
    }), 200


# ==========================================================
# CREAR PAGO
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
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
            return jsonify({
                'message': f'{field} es obligatorio'
            }), 400

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

    except (ValueError, TypeError):
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


# ==========================================================
# ELIMINAR PAGO
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_pago(id):

    pago = Pago.get_by_id(id)

    if not pago:
        return jsonify({
            'message': 'Pago no encontrado'
        }), 404

    pago.delete()

    return jsonify({
        'message': 'Pago eliminado exitosamente'
    }), 200


# ==========================================================
# ACTUALIZAR PAGO
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_pago(id):

    pago = Pago.get_by_id(id)

    if not pago:
        return jsonify({
            'message': 'Pago no encontrado'
        }), 404

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

        except (ValueError, TypeError):
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