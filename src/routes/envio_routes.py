from flask import Blueprint, request, jsonify
from src.models.envio import Envio
from datetime import datetime

Envio_bp = Blueprint('Envio', __name__)

@Envio_bp.route('/', methods=['GET'])
def get_envios():
    envios = Envio.get()
    lista = []

    for envio in envios:
        lista.append({
            'id_envio': envio.id_envio,
            'fecha_factura': str(envio.fecha_factura),
            'destino': envio.destino,
            'direccion_envio': envio.direccion_envio,
            'empresa_envio': envio.empresa_envio,
            'numero_guia': envio.numero_guia,
            'id_factura': envio.id_factura,
            'estado_envio': envio.estado_envio
        })

    return jsonify(lista), 200


@Envio_bp.route('/<int:id>', methods=['GET'])
def get_envio(id):
    envio = Envio.get_by_id(id)

    if not envio:
        return jsonify({'message': 'Envio no encontrado'}), 404

    return jsonify({
        'id_envio': envio.id_envio,
        'fecha_factura': str(envio.fecha_factura),
        'destino': envio.destino,
        'direccion_envio': envio.direccion_envio,
        'empresa_envio': envio.empresa_envio,
        'numero_guia': envio.numero_guia,
        'id_factura': envio.id_factura,
        'estado_envio': envio.estado_envio
    }), 200


@Envio_bp.route('/', methods=['POST'])
def create_envio():
    data = request.get_json()

    required = [
        'fecha_factura',
        'destino',
        'direccion_envio',
        'empresa_envio',
        'numero_guia',
        'id_factura',
        'estado_envio'
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

    envio = Envio(
        fecha_factura=fecha,
        destino=data['destino'],
        direccion_envio=data['direccion_envio'],
        empresa_envio=data['empresa_envio'],
        numero_guia=data['numero_guia'],
        id_factura=data['id_factura'],
        estado_envio=data['estado_envio']
    )

    envio.save()

    return jsonify({
        'message': 'Envio creado exitosamente'
    }), 201


@Envio_bp.route('/<int:id>', methods=['DELETE'])
def delete_envio(id):
    envio = Envio.get_by_id(id)

    if not envio:
        return jsonify({
            'message': 'Envio no encontrado'
        }), 404

    envio.delete()

    return jsonify({
        'message': 'Envio eliminado exitosamente'
    }), 200

@Envio_bp.route('/<int:id>', methods=['PUT'])
def update_envio(id):
    envio = Envio.get_by_id(id)

    if not envio:
        return jsonify({
            'message': 'Envio no encontrado'
        }), 404

    data = request.get_json()

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

    if 'destino' in data:
        envio.destino = data['destino']

    if 'direccion_envio' in data:
        envio.direccion_envio = data['direccion_envio']

    if 'empresa_envio' in data:
        envio.empresa_envio = data['empresa_envio']

    if 'numero_guia' in data:
        envio.numero_guia = data['numero_guia']

    if 'id_factura' in data:
        envio.id_factura = data['id_factura']

    if 'estado_envio' in data:
        envio.estado_envio = data['estado_envio']

    envio.update()

    return jsonify({
        'message': 'Envio actualizado exitosamente'
    }), 200