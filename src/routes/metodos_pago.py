from flask import Blueprint, jsonify, request
from src.models.metodos_pago import MetodoPago

metodos_pago_bp = Blueprint("metodos_pago", __name__)


# Obtener todos los métodos de pago
@metodos_pago_bp.route("/metodos_pago", methods=["GET"])
def get_metodos_pago():
    metodos = MetodoPago.get()
    return jsonify([metodo.to_dict() for metodo in metodos]), 200


# Obtener un método de pago por ID
@metodos_pago_bp.route("/metodos_pago/<int:id>", methods=["GET"])
def get_metodo_pago(id):
    metodo = MetodoPago.get_by_id(id)

    if metodo is None:
        return jsonify({"mensaje": "Método de pago no encontrado"}), 404

    return jsonify(metodo.to_dict()), 200


# Obtener los métodos de pago de un cliente
@metodos_pago_bp.route("/clientes/<int:id_cliente>/metodos_pago", methods=["GET"])
def get_metodos_cliente(id_cliente):
    metodos = MetodoPago.get_by_cliente(id_cliente)
    return jsonify([metodo.to_dict() for metodo in metodos]), 200


# Crear un método de pago
@metodos_pago_bp.route("/metodos_pago", methods=["POST"])
def create_metodo_pago():
    data = request.get_json()

    metodo = MetodoPago(
        id_cliente=data["id_cliente"],
        tipo_metodo=data["tipo_metodo"],
        titular=data["titular"],
        numero_tarjeta=data.get("numero_tarjeta"),
        fecha_vencimiento=data.get("fecha_vencimiento"),
        predeterminado=data.get("predeterminado", False),
        activo=data.get("activo", True)
    )

    metodo.save()

    return jsonify({
        "mensaje": "Método de pago creado correctamente",
        "metodo_pago": metodo.to_dict()
    }), 201


# Actualizar un método de pago
@metodos_pago_bp.route("/metodos_pago/<int:id>", methods=["PUT"])
def update_metodo_pago(id):
    metodo = MetodoPago.get_by_id(id)

    if metodo is None:
        return jsonify({"mensaje": "Método de pago no encontrado"}), 404

    data = request.get_json()

    metodo.tipo_metodo = data.get("tipo_metodo", metodo.tipo_metodo)
    metodo.titular = data.get("titular", metodo.titular)
    metodo.numero_tarjeta = data.get("numero_tarjeta", metodo.numero_tarjeta)
    metodo.fecha_vencimiento = data.get("fecha_vencimiento", metodo.fecha_vencimiento)
    metodo.predeterminado = data.get("predeterminado", metodo.predeterminado)
    metodo.activo = data.get("activo", metodo.activo)

    metodo.update()

    return jsonify({
        "mensaje": "Método de pago actualizado correctamente",
        "metodo_pago": metodo.to_dict()
    }), 200


# Eliminar un método de pago
@metodos_pago_bp.route("/metodos_pago/<int:id>", methods=["DELETE"])
def delete_metodo_pago(id):
    metodo = MetodoPago.get_by_id(id)

    if metodo is None:
        return jsonify({"mensaje": "Método de pago no encontrado"}), 404

    metodo.delete()

    return jsonify({
        "mensaje": "Método de pago eliminado correctamente"
    }), 200