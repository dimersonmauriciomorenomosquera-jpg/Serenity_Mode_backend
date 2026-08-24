from flask import Blueprint, request, jsonify
from src.models.envio import Envio
from src.models.factura import Factura
from src.models.clientes import Cliente

from datetime import datetime

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from src.utils.decorators import admin_required


Envio_bp = Blueprint('Envio', __name__)


# ==========================================================
# OBTENER TODOS LOS ENVÍOS
# SOLO ADMINISTRADORES
# ==========================================================

@Envio_bp.route('/', methods=['GET'])
@admin_required
def get_envios():

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

    envios, total = Envio.get(
        page=page,
        per_page=per_page
    )

    total_pages = (total + per_page - 1) // per_page

    lista = []

    for envio in envios:

        lista.append({

            'id_envio': envio.id_envio,

            'fecha_factura': str(
                envio.fecha_factura
            ),

            'destino': envio.destino,

            'direccion_envio':
                envio.direccion_envio,

            'empresa_envio':
                envio.empresa_envio,

            'numero_guia':
                envio.numero_guia,

            'id_factura':
                envio.id_factura,

            'estado_envio':
                envio.estado_envio
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
# OBTENER UN ENVÍO
# CLIENTE DUEÑO DEL ENVÍO O ADMINISTRADOR
# ==========================================================

@Envio_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_envio(id):

    envio = Envio.get_by_id(id)

    if not envio:

        return jsonify({
            'message': 'Envio no encontrado'
        }), 404

    # ======================================================
    # OBTENER FACTURA
    # ======================================================

    factura = Factura.get_by_id(
        envio.id_factura
    )

    if not factura:

        return jsonify({
            'message': 'Factura asociada no encontrada'
        }), 404

    # ======================================================
    # OBTENER TIPO DE USUARIO
    # ======================================================

    claims = get_jwt()

    tipo = claims.get("tipo")

    # ======================================================
    # SI ES ADMINISTRADOR
    # PUEDE CONSULTAR EL ENVÍO
    # ======================================================

    if tipo == "administrador":

        return jsonify({

            'id_envio':
                envio.id_envio,

            'fecha_factura':
                str(envio.fecha_factura),

            'destino':
                envio.destino,

            'direccion_envio':
                envio.direccion_envio,

            'empresa_envio':
                envio.empresa_envio,

            'numero_guia':
                envio.numero_guia,

            'id_factura':
                envio.id_factura,

            'estado_envio':
                envio.estado_envio

        }), 200

    # ======================================================
    # SI ES CLIENTE
    # SOLO PUEDE VER SU PROPIO ENVÍO
    # ======================================================

    id_cliente = get_jwt_identity()

    if str(factura.id_cliente) != str(id_cliente):

        return jsonify({
            'message':
                'No tienes permiso para consultar este envío.'
        }), 403

    # ======================================================
    # RESPUESTA PARA EL CLIENTE
    # ======================================================

    return jsonify({

        'id_envio':
            envio.id_envio,

        'fecha_factura':
            str(envio.fecha_factura),

        'destino':
            envio.destino,

        'direccion_envio':
            envio.direccion_envio,

        'empresa_envio':
            envio.empresa_envio,

        'numero_guia':
            envio.numero_guia,

        'id_factura':
            envio.id_factura,

        'estado_envio':
            envio.estado_envio

    }), 200


# ==========================================================
# CREAR ENVÍO AUTOMÁTICAMENTE
#
# ESTA FUNCIÓN NO ES UNA RUTA.
#
# DEBE SER LLAMADA CUANDO LA FACTURA CAMBIE A "Pagada".
# ==========================================================

def crear_envio_factura(id_factura):

    factura = Factura.get_by_id(
        id_factura
    )

    if not factura:

        return None, {
            'message': 'Factura no encontrada.'
        }, 404

    # ======================================================
    # LA FACTURA DEBE ESTAR PAGADA
    # ======================================================

    if factura.estado_factura != "Pagada":

        return None, {
            'message':
                'El envío solo puede generarse cuando la factura está pagada.'
        }, 400

    # ======================================================
    # EVITAR CREAR DOS ENVÍOS PARA LA MISMA FACTURA
    # ======================================================

    envios, total = Envio.get(
        page=1,
        per_page=1000
    )

    for envio in envios:

        if envio.id_factura == id_factura:

            return envio, None, 200

    # ======================================================
    # BUSCAR CLIENTE
    # ======================================================

    cliente = Cliente.get_by_id(
        factura.id_cliente
    )

    if not cliente:

        return None, {
            'message':
                'Cliente asociado a la factura no encontrado.'
        }, 404

    # ======================================================
    # CREAR ENVÍO
    # ======================================================

    envio = Envio(

        fecha_factura=datetime.now().date(),

        destino=cliente.direccion_cliente,

        direccion_envio=cliente.direccion_cliente,

        # Tu BD no permite NULL
        empresa_envio="Pendiente",

        # Tu BD no permite NULL
        numero_guia="Pendiente",

        id_factura=id_factura,

        estado_envio="Preparando"
    )

    envio.save()

    return envio, None, 201


# ==========================================================
# ACTUALIZAR ENVÍO
# SOLO ADMINISTRADORES
# ==========================================================

@Envio_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_envio(id):

    envio = Envio.get_by_id(id)

    if not envio:

        return jsonify({
            'message': 'Envio no encontrado'
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            'message': 'Debe enviar información.'
        }), 400

    # ======================================================
    # ACTUALIZAR FECHA
    # ======================================================

    if 'fecha_factura' in data:

        try:

            envio.fecha_factura = datetime.strptime(
                data['fecha_factura'],
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                'message': 'Fecha inválida'
            }), 400

    # ======================================================
    # ACTUALIZAR DESTINO
    # ======================================================

    if 'destino' in data:

        envio.destino = data['destino']

    # ======================================================
    # ACTUALIZAR DIRECCIÓN
    # ======================================================

    if 'direccion_envio' in data:

        envio.direccion_envio = \
            data['direccion_envio']

    # ======================================================
    # ACTUALIZAR EMPRESA
    # ======================================================

    if 'empresa_envio' in data:

        envio.empresa_envio = \
            data['empresa_envio']

    # ======================================================
    # ACTUALIZAR NÚMERO DE GUÍA
    # ======================================================

    if 'numero_guia' in data:

        envio.numero_guia = \
            data['numero_guia']

    # ======================================================
    # NO PERMITIMOS CAMBIAR id_factura
    #
    # El envío ya pertenece a una factura.
    # ======================================================

    # NO hacer:
    #
    # if 'id_factura' in data:
    #     envio.id_factura = data['id_factura']

    # ======================================================
    # ACTUALIZAR ESTADO
    # ======================================================

    if 'estado_envio' in data:

        envio.estado_envio = \
            data['estado_envio']

    # ======================================================
    # GUARDAR
    # ======================================================

    envio.update()

    return jsonify({

        'message':
            'Envio actualizado exitosamente'

    }), 200


# ==========================================================
# ELIMINAR ENVÍO
# SOLO ADMINISTRADORES
# ==========================================================

@Envio_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_envio(id):

    envio = Envio.get_by_id(id)

    if not envio:

        return jsonify({
            'message': 'Envio no encontrado'
        }), 404

    envio.delete()

    return jsonify({

        'message':
            'Envio eliminado exitosamente'

    }), 200