from flask import Blueprint, request, jsonify
from src.models.factura import Factura
from datetime import datetime

from flask_jwt_extended import jwt_required
from src.utils.decorators import admin_required


Factura_bp = Blueprint('Factura', __name__)


# ==========================================================
# OBTENER TODAS LAS FACTURAS
# SOLO ADMINISTRADORES
# ==========================================================

@Factura_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_facturas():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if page < 1:
        return jsonify({
            'message': 'La página debe ser mayor o igual a 1'
        }), 400

    if per_page < 1:
        return jsonify({
            'message': 'La cantidad por página debe ser mayor o igual a 1'
        }), 400

    facturas, total = Factura.get(
        page=page,
        per_page=per_page
    )

    total_pages = (total + per_page - 1) // per_page

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
# OBTENER UNA FACTURA POR ID
# SOLO ADMINISTRADORES
# ==========================================================

@Factura_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@admin_required
def get_factura(id):

    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    return jsonify({
        'id_factura': factura.id_factura,
        'fecha_factura': str(factura.fecha_factura),
        'total_pagar': float(factura.total_pagar),
        'estado_pago': factura.estado_pago,
        'id_cliente': factura.id_cliente,
        'id_carrito': factura.id_carrito
    }), 200


# ==========================================================
# CREAR FACTURA
# SOLO ADMINISTRADORES
# ==========================================================

@Factura_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
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

    except (ValueError, TypeError):
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


# ==========================================================
# ELIMINAR FACTURA
# SOLO ADMINISTRADORES
# ==========================================================

@Factura_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
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


# ==========================================================
# ACTUALIZAR FACTURA
# SOLO ADMINISTRADORES
# ==========================================================

@Factura_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
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

        except (ValueError, TypeError):
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