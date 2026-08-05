from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.detalle_carrito import Detalle_Carrito
from src.models.carrito import Carrito
from src.models.productos import Productos

DetalleCarrito_bp = Blueprint("detalle_carrito", __name__)


# =========================================
# OBTENER TODOS LOS DETALLES DEL CARRITO
# =========================================

@DetalleCarrito_bp.route("/", methods=["GET"])
@jwt_required()
def get_detalles():

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_cliente(id_cliente)

    if carrito is None:

        return jsonify({
            "message": "El carrito del usuario no existe."
        }), 404

    detalles = Detalle_Carrito.get_by_carrito(carrito.id_carrito)

    respuesta = []

    for detalle in detalles:

        producto = Productos.get_by_id(detalle.id_producto)

        if producto is None:
            continue

        respuesta.append({

            "id_detalle_carrito": detalle.id_detalle_carrito,
            "id_carrito": detalle.id_carrito,
            "id_producto": detalle.id_producto,
            "nombre": producto.nombre_producto,
            "imagen": producto.imagen,
            "descripcion": producto.descripcion_producto,
            "cantidad": detalle.cantidad,
            "precio_unitario": float(detalle.precio_unitario),
            "subtotal": float(detalle.precio_unitario) * detalle.cantidad,
            "talla": detalle.talla

        })

    return jsonify(respuesta), 200


# =========================================
# OBTENER UN DETALLE
# =========================================

@DetalleCarrito_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_detalle(id):

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_cliente(id_cliente)

    if carrito is None:

        return jsonify({
            "message": "El carrito del usuario no existe."
        }), 404

    detalle = Detalle_Carrito.get_by_id(id)

    if detalle is None:

        return jsonify({
            "message": "Detalle del carrito no encontrado."
        }), 404

    if detalle.id_carrito != carrito.id_carrito:

        return jsonify({
            "message": "No autorizado."
        }), 403

    return jsonify(detalle.to_dict()), 200


# =========================================
# CREAR DETALLE
# =========================================

@DetalleCarrito_bp.route("/", methods=["POST"])
@jwt_required()
def create_detalle():

    data = request.get_json()

    id_cliente = get_jwt_identity()

    if not data:

        return jsonify({
            "message": "Debe enviar información."
        }), 400

    for campo in ["id_producto", "cantidad"]:

        if campo not in data:

            return jsonify({
                "message": f"El campo '{campo}' es obligatorio."
            }), 400


    # ======================================
    # BUSCAR O CREAR EL CARRITO DEL USUARIO
    # ======================================

    carrito = Carrito.get_by_cliente(id_cliente)

    if carrito is None:

        carrito = Carrito(
            fecha_creacion=date.today(),
            total_carrito=0,
            id_cliente=id_cliente
        )

        carrito.save()


    # ======================================
    # VALIDAR PRODUCTO
    # ======================================

    producto = Productos.get_by_id(data["id_producto"])

    if producto is None:

        return jsonify({
            "message": "El producto no existe."
        }), 404


    # ======================================
    # VALIDAR CANTIDAD
    # ======================================

    try:

        cantidad = int(data["cantidad"])

    except ValueError:

        return jsonify({
            "message": "La cantidad debe ser un número entero."
        }), 400


    if cantidad <= 0:

        return jsonify({
            "message": "La cantidad debe ser mayor que cero."
        }), 400


    if cantidad > producto.stock_producto:

        return jsonify({
            "message": "No hay suficiente stock."
        }), 400


    # ======================================
    # VALIDAR TALLA
    # ======================================

    talla = None

    if producto.categoria.lower() in ["ropa", "zapatos"]:

        talla = str(data.get("talla", "")).strip()

        if talla == "":

            return jsonify({
                "message": "Debe seleccionar una talla."
            }), 400


    # ======================================
    # CREAR DETALLE
    # ======================================

    detalle = Detalle_Carrito(

        id_carrito=carrito.id_carrito,

        id_producto=producto.id_producto,

        cantidad=cantidad,

        precio_unitario=producto.precio_producto,

        talla=talla

    )

    detalle.save()

    return jsonify({

        "message": "Producto agregado al carrito correctamente.",

        "detalle": detalle.to_dict()

    }), 201

    # =========================================
# ACTUALIZAR DETALLE
# =========================================

@DetalleCarrito_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_detalle(id):

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_cliente(id_cliente)

    if carrito is None:

        return jsonify({
            "message": "El carrito del usuario no existe."
        }), 404

    detalle = Detalle_Carrito.get_by_id(id)

    if detalle is None:

        return jsonify({
            "message": "Detalle del carrito no encontrado."
        }), 404

    if detalle.id_carrito != carrito.id_carrito:

        return jsonify({
            "message": "No autorizado."
        }), 403

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Debe enviar información."
        }), 400

    producto = Productos.get_by_id(detalle.id_producto)

    if producto is None:

        return jsonify({
            "message": "El producto ya no existe."
        }), 404

    # ==========================
    # ACTUALIZAR CANTIDAD
    # ==========================

    if "cantidad" in data:

        try:

            cantidad = int(data["cantidad"])

        except ValueError:

            return jsonify({
                "message": "Cantidad inválida."
            }), 400

        if cantidad <= 0:

            return jsonify({
                "message": "La cantidad debe ser mayor que cero."
            }), 400

        if cantidad > producto.stock_producto:

            return jsonify({
                "message": "Stock insuficiente."
            }), 400

        detalle.cantidad = cantidad

    # ==========================
    # ACTUALIZAR TALLA
    # ==========================

    if producto.categoria.lower() in ["ropa", "zapatos"]:

        if "talla" in data:

            talla = str(data["talla"]).strip()

            if talla == "":

                return jsonify({
                    "message": "La talla es obligatoria."
                }), 400

            detalle.talla = talla

    detalle.update()

    return jsonify({

        "message": "Detalle actualizado correctamente.",

        "detalle": detalle.to_dict()

    }), 200


# =========================================
# ELIMINAR DETALLE
# =========================================

@DetalleCarrito_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_detalle(id):

    id_cliente = get_jwt_identity()

    carrito = Carrito.get_by_cliente(id_cliente)

    if carrito is None:

        return jsonify({
            "message": "El carrito del usuario no existe."
        }), 404

    detalle = Detalle_Carrito.get_by_id(id)

    if detalle is None:

        return jsonify({
            "message": "Detalle del carrito no encontrado."
        }), 404

    if detalle.id_carrito != carrito.id_carrito:

        return jsonify({
            "message": "No autorizado."
        }), 403

    detalle.delete()

    return jsonify({
        "message": "Producto eliminado del carrito correctamente."
    }), 200