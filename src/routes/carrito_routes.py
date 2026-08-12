from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.carrito import Carrito
from datetime import datetime


Carrito_bp = Blueprint("Carrito", __name__)


# =========================================================
# OBTENER MI CARRITO
# GET /carrito/
# =========================================================

@Carrito_bp.route("/", methods=["GET"])
@jwt_required()
def get_carrito():

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_cliente(id_cliente)

    if not carrito:

        return jsonify({
            "message": "El cliente no tiene carrito"
        }), 404

    return jsonify({
        "id_carrito": carrito.id_carrito,
        "fecha_creacion": str(carrito.fecha_creacion),
        "total_carrito": float(carrito.total_carrito),
        "id_cliente": carrito.id_cliente
    }), 200




# =========================================================
# OBTENER CARRITO POR ID
# GET /carrito/<id>
# =========================================================

@Carrito_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_carrito_by_id(id):

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_id(id)

    if not carrito:

        return jsonify({
            "message": "Carrito no encontrado"
        }), 404

    # El carrito debe pertenecer al usuario autenticado
    if carrito.id_cliente != int(id_cliente):

        return jsonify({
            "message": "No tienes permiso para acceder a este carrito"
        }), 403

    return jsonify({
        "id_carrito": carrito.id_carrito,
        "fecha_creacion": str(carrito.fecha_creacion),
        "total_carrito": float(carrito.total_carrito),
        "id_cliente": carrito.id_cliente
    }), 200


# =========================================================
# OBTENER CARRITO POR CLIENTE
# GET /carrito/cliente/<id_cliente>
# =========================================================

@Carrito_bp.route("/cliente/<int:id_cliente>", methods=["GET"])
@jwt_required()
def get_carrito_cliente(id_cliente):

    id_usuario = get_jwt_identity()

    # Evitamos que un usuario consulte
    # el carrito de otro cliente
    if int(id_usuario) != id_cliente:

        return jsonify({
            "message": "No tienes permiso para acceder a este carrito"
        }), 403

    carrito = Carrito.get_by_cliente(id_cliente)

    if not carrito:

        return jsonify({
            "message": "El cliente no tiene carrito"
        }), 404

    return jsonify({
        "id_carrito": carrito.id_carrito,
        "fecha_creacion": str(carrito.fecha_creacion),
        "total_carrito": float(carrito.total_carrito),
        "id_cliente": carrito.id_cliente
    }), 200


# =========================================================
# CREAR CARRITO
# POST /carrito/
# =========================================================

@Carrito_bp.route("/", methods=["POST"])
@jwt_required()
def create_carrito():

    id_cliente = get_jwt_identity()

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "No se recibieron datos"
        }), 400

    # =====================================================
    # FECHA
    # =====================================================

    fecha_creacion = data.get("fecha_creacion")

    if fecha_creacion:

        try:

            fecha = datetime.strptime(
                fecha_creacion,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                "message": "Formato de fecha inválido (YYYY-MM-DD)"
            }), 400

    else:

        fecha = datetime.now().date()

    # =====================================================
    # TOTAL
    # =====================================================

    total_carrito = data.get("total_carrito", 0)

    try:

        total = float(total_carrito)

        if total < 0:

            return jsonify({
                "message": "El total no puede ser negativo"
            }), 400

    except (ValueError, TypeError):

        return jsonify({
            "message": "El total debe ser numérico"
        }), 400

    # =====================================================
    # VERIFICAR SI YA EXISTE
    # =====================================================

    carrito_existente = Carrito.get_by_cliente(id_cliente)

    if carrito_existente:

        return jsonify({
            "message": "El cliente ya tiene un carrito",
            "carrito": {
                "id_carrito": carrito_existente.id_carrito,
                "fecha_creacion": str(
                    carrito_existente.fecha_creacion
                ),
                "total_carrito": float(
                    carrito_existente.total_carrito
                ),
                "id_cliente": carrito_existente.id_cliente
            }
        }), 409

    # =====================================================
    # CREAR
    # =====================================================

    carrito = Carrito(
        fecha_creacion=fecha,
        total_carrito=total,
        id_cliente=id_cliente
    )

    carrito.save()

    return jsonify({
        "message": "Carrito creado exitosamente",
        "carrito": {
            "id_carrito": carrito.id_carrito,
            "fecha_creacion": str(
                carrito.fecha_creacion
            ),
            "total_carrito": float(
                carrito.total_carrito
            ),
            "id_cliente": carrito.id_cliente
        }
    }), 201


# =========================================================
# ACTUALIZAR CARRITO
# PUT /carrito/<id>
# =========================================================

@Carrito_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_carrito(id):

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_id(id)

    if not carrito:

        return jsonify({
            "message": "Carrito no encontrado"
        }), 404

    # =====================================================
    # VERIFICAR PROPIETARIO
    # =====================================================

    if carrito.id_cliente != int(id_cliente):

        return jsonify({
            "message": "No tienes permiso para modificar este carrito"
        }), 403

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "No se recibieron datos"
        }), 400

    # =====================================================
    # FECHA
    # =====================================================

    if "fecha_creacion" in data:

        try:

            carrito.fecha_creacion = datetime.strptime(
                data["fecha_creacion"],
                "%Y-%m-%d"
            ).date()

        except (ValueError, TypeError):

            return jsonify({
                "message": "Fecha inválida. Usa YYYY-MM-DD"
            }), 400

    # =====================================================
    # TOTAL
    # =====================================================

    if "total_carrito" in data:

        try:

            total = float(data["total_carrito"])

            if total < 0:

                return jsonify({
                    "message": "El total no puede ser negativo"
                }), 400

            carrito.total_carrito = total

        except (ValueError, TypeError):

            return jsonify({
                "message": "Total inválido"
            }), 400

    # =====================================================
    # GUARDAR
    # =====================================================

    carrito.save()

    return jsonify({
        "message": "Carrito actualizado exitosamente",
        "carrito": {
            "id_carrito": carrito.id_carrito,
            "fecha_creacion": str(
                carrito.fecha_creacion
            ),
            "total_carrito": float(
                carrito.total_carrito
            ),
            "id_cliente": carrito.id_cliente
        }
    }), 200


# =========================================================
# ELIMINAR CARRITO
# DELETE /carrito/<id>
# =========================================================

@Carrito_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_carrito(id):

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_id(id)

    if not carrito:

        return jsonify({
            "message": "Carrito no encontrado"
        }), 404

    # =====================================================
    # VERIFICAR PROPIETARIO
    # =====================================================

    if carrito.id_cliente != int(id_cliente):

        return jsonify({
            "message": "No tienes permiso para eliminar este carrito"
        }), 403

    carrito.delete()

    return jsonify({
        "message": "Carrito eliminado exitosamente"
    }), 200