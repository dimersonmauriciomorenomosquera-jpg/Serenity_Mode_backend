from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.metodos_pago import MetodoPago


metodos_pago_bp = Blueprint("metodos_pago", __name__)


# ==========================================================
# OBTENER TODOS LOS MÉTODOS DE PAGO DEL USUARIO
# ==========================================================

@metodos_pago_bp.route("/metodos_pago", methods=["GET"])
@jwt_required()
def get_metodos_pago():

    id_cliente = get_jwt_identity()

    metodos = MetodoPago.get_by_cliente(id_cliente)

    return jsonify([
        metodo.to_dict()
        for metodo in metodos
    ]), 200


# ==========================================================
# OBTENER UN MÉTODO DE PAGO
# ==========================================================

@metodos_pago_bp.route("/metodos_pago/<int:id>", methods=["GET"])
@jwt_required()
def get_metodo_pago(id):

    id_cliente = get_jwt_identity()

    metodo = MetodoPago.get_by_id(id)

    if metodo is None:

        return jsonify({
            "mensaje": "Método de pago no encontrado"
        }), 404

    # Verificar propietario

    if metodo.id_cliente != int(id_cliente):

        return jsonify({
            "mensaje": "No tienes permiso para acceder a este método de pago"
        }), 403

    return jsonify(
        metodo.to_dict()
    ), 200


# ==========================================================
# OBTENER MÉTODOS DE PAGO DE UN CLIENTE
# ==========================================================

@metodos_pago_bp.route(
    "/clientes/<int:id_cliente>/metodos_pago",
    methods=["GET"]
)
@jwt_required()
def get_metodos_cliente(id_cliente):

    id_usuario = get_jwt_identity()

    # El usuario solamente puede consultar
    # sus propios métodos de pago.

    if int(id_usuario) != id_cliente:

        return jsonify({
            "mensaje": "No tienes permiso para acceder a estos métodos de pago"
        }), 403

    metodos = MetodoPago.get_by_cliente(
        id_cliente
    )

    return jsonify([
        metodo.to_dict()
        for metodo in metodos
    ]), 200


# ==========================================================
# CREAR MÉTODO DE PAGO
# ==========================================================

@metodos_pago_bp.route(
    "/metodos_pago",
    methods=["POST"]
)
@jwt_required()
def create_metodo_pago():

    id_cliente = get_jwt_identity()

    data = request.get_json()

    metodo = MetodoPago(

        # NO viene del JSON.
        # Sale directamente del JWT.

        id_cliente=id_cliente,

        tipo_metodo=data["tipo_metodo"],
        titular=data["titular"],
        numero_tarjeta=data.get("numero_tarjeta"),
        fecha_vencimiento=data.get("fecha_vencimiento"),
        predeterminado=data.get("predeterminado", False),
        activo=data.get("activo", True)
    )

    metodo.save()

    return jsonify({

        "mensaje":
            "Método de pago creado correctamente",

        "metodo_pago":
            metodo.to_dict()

    }), 201


# ==========================================================
# ACTUALIZAR MÉTODO DE PAGO
# ==========================================================

@metodos_pago_bp.route(
    "/metodos_pago/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def update_metodo_pago(id):

    id_cliente = get_jwt_identity()

    metodo = MetodoPago.get_by_id(id)

    if metodo is None:

        return jsonify({
            "mensaje": "Método de pago no encontrado"
        }), 404

    # Verificar propietario

    if metodo.id_cliente != int(id_cliente):

        return jsonify({
            "mensaje": "No tienes permiso para modificar este método de pago"
        }), 403

    data = request.get_json()

    metodo.tipo_metodo = data.get(
        "tipo_metodo",
        metodo.tipo_metodo
    )

    metodo.titular = data.get(
        "titular",
        metodo.titular
    )

    metodo.numero_tarjeta = data.get(
        "numero_tarjeta",
        metodo.numero_tarjeta
    )

    metodo.fecha_vencimiento = data.get(
        "fecha_vencimiento",
        metodo.fecha_vencimiento
    )

    metodo.predeterminado = data.get(
        "predeterminado",
        metodo.predeterminado
    )

    metodo.activo = data.get(
        "activo",
        metodo.activo
    )

    metodo.update()

    return jsonify({

        "mensaje":
            "Método de pago actualizado correctamente",

        "metodo_pago":
            metodo.to_dict()

    }), 200


# ==========================================================
# ELIMINAR MÉTODO DE PAGO
# ==========================================================

@metodos_pago_bp.route(
    "/metodos_pago/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_metodo_pago(id):

    id_cliente = get_jwt_identity()

    metodo = MetodoPago.get_by_id(id)

    if metodo is None:

        return jsonify({
            "mensaje": "Método de pago no encontrado"
        }), 404

    # Verificar propietario

    if metodo.id_cliente != int(id_cliente):

        return jsonify({
            "mensaje": "No tienes permiso para eliminar este método de pago"
        }), 403

    metodo.delete()

    return jsonify({

        "mensaje":
            "Método de pago eliminado correctamente"

    }), 200