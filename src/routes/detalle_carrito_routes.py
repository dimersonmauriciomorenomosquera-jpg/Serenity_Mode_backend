from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.detalle_carrito import Detalle_Carrito
from src.models.carrito import Carrito
from src.models.productos import Productos


# ==========================================================
# BLUEPRINT
# ==========================================================

DetalleCarrito_bp = Blueprint(
    "detalle_carrito",
    __name__
)


# ==========================================================
# OBTENER TODOS LOS DETALLES DEL CARRITO
# ==========================================================

@DetalleCarrito_bp.route("/", methods=["GET"])
@jwt_required()
def get_detalles():

    print("========== OBTENER DETALLES CARRITO ==========")

    id_cliente = get_jwt_identity()

    print("ID CLIENTE:", id_cliente)

    # ======================================================
    # BUSCAR CARRITO DEL CLIENTE
    # ======================================================

    carrito = Carrito.get_by_cliente(id_cliente)

    if carrito is None:

        return jsonify({
            "message": "El carrito del usuario no existe."
        }), 404

    # ======================================================
    # BUSCAR DETALLES
    # ======================================================

    detalles = Detalle_Carrito.get_by_carrito(
        carrito.id_carrito
    )

    respuesta = []

    # ======================================================
    # CONSTRUIR RESPUESTA
    # ======================================================

    for detalle in detalles:

        producto = Productos.get_by_id(
            detalle.id_producto
        )

        if producto is None:
            continue

        respuesta.append({

            "id_detalle_carrito":
                detalle.id_detalle_carrito,

            "id_carrito":
                detalle.id_carrito,

            "id_producto":
                detalle.id_producto,

            "nombre":
                producto.nombre_producto,

            "imagen":
                producto.imagen,

            "descripcion":
                producto.descripcion_producto,

            "cantidad":
                detalle.cantidad,

            "precio_unitario":
                float(detalle.precio_unitario),

            "subtotal":
                float(detalle.subtotal),

            "talla":
                detalle.talla

        })

    return jsonify(respuesta), 200


# ==========================================================
# OBTENER UN DETALLE
# ==========================================================

@DetalleCarrito_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_detalle(id):

    print("========== OBTENER DETALLE ==========")

    id_cliente = get_jwt_identity()

    # ======================================================
    # BUSCAR CARRITO
    # ======================================================

    carrito = Carrito.get_by_cliente(id_cliente)

    if carrito is None:

        return jsonify({
            "message": "El carrito del usuario no existe."
        }), 404

    # ======================================================
    # BUSCAR DETALLE
    # ======================================================

    detalle = Detalle_Carrito.get_by_id(id)

    if detalle is None:

        return jsonify({
            "message": "Detalle del carrito no encontrado."
        }), 404

    # ======================================================
    # VALIDAR PROPIETARIO
    # ======================================================

    if detalle.id_carrito != carrito.id_carrito:

        return jsonify({
            "message": "No tiene permisos para ver este detalle."
        }), 403

    return jsonify(
        detalle.to_dict()
    ), 200


# ==========================================================
# CREAR / AGREGAR PRODUCTO AL CARRITO
# ==========================================================

@DetalleCarrito_bp.route("/", methods=["POST"])
@jwt_required()
def create_detalle():

    print("========== AGREGAR PRODUCTO AL CARRITO ==========")

    data = request.get_json()

    id_cliente = get_jwt_identity()

    print("ID CLIENTE:", id_cliente)
    print("DATA:", data)

    # ======================================================
    # VALIDAR DATA
    # ======================================================

    if not data:

        return jsonify({
            "message":
                "Debe enviar información en formato JSON."
        }), 400

    # ======================================================
    # CAMPOS OBLIGATORIOS
    # ======================================================

    campos = [
        "id_producto",
        "cantidad"
    ]

    for campo in campos:

        if campo not in data:

            return jsonify({
                "message":
                    f"El campo '{campo}' es obligatorio."
            }), 400

    # ======================================================
    # BUSCAR O CREAR CARRITO
    # ======================================================

    carrito = Carrito.get_by_cliente(
        id_cliente
    )

    if carrito is None:

        carrito = Carrito(

            fecha_creacion=None,

            total_carrito=0,

            id_cliente=id_cliente

        )

        # Usamos la fecha actual directamente
        from datetime import date

        carrito.fecha_creacion = date.today()

        carrito.save()

        print(
            "CARRITO CREADO:",
            carrito.id_carrito
        )

    # ======================================================
    # BUSCAR PRODUCTO
    # ======================================================

    producto = Productos.get_by_id(
        data["id_producto"]
    )

    if producto is None:

        return jsonify({
            "message":
                "El producto no existe."
        }), 404

    # ======================================================
    # VALIDAR CANTIDAD
    # ======================================================

    try:

        cantidad = int(
            data["cantidad"]
        )

    except (
        ValueError,
        TypeError
    ):

        return jsonify({
            "message":
                "La cantidad debe ser un número entero."
        }), 400

    if cantidad <= 0:

        return jsonify({
            "message":
                "La cantidad debe ser mayor que cero."
        }), 400

    # ======================================================
    # VALIDAR STOCK
    # ======================================================

    if cantidad > producto.stock_producto:

        return jsonify({
            "message":
                "No hay suficiente stock."
        }), 400

    # ======================================================
    # VALIDAR TALLA
    # ======================================================

    categoria = (
        producto.categoria or ""
    ).lower().strip()

    if categoria in ["ropa", "zapatos"]:

        talla = str(
            data.get("talla", "")
        ).strip()

        if talla == "":

            return jsonify({
                "message":
                    "Debe seleccionar una talla."
            }), 400

    else:

        talla = None

    # ======================================================
    # BUSCAR PRODUCTO YA EXISTENTE
    # ======================================================

    detalles_existentes = (
        Detalle_Carrito.get_by_carrito(
            carrito.id_carrito
        )
    )

    detalle_existente = None

    for detalle in detalles_existentes:

        if detalle.id_producto != producto.id_producto:
            continue

        if categoria in ["ropa", "zapatos"]:

            if detalle.talla == talla:

                detalle_existente = detalle
                break

        else:

            if detalle.talla is None:

                detalle_existente = detalle
                break

    # ======================================================
    # SI YA EXISTE → SUMAR CANTIDAD
    # ======================================================

    if detalle_existente is not None:

        nueva_cantidad = (
            detalle_existente.cantidad
            + cantidad
        )

        print(
            "DETALLE EXISTENTE:",
            detalle_existente.id_detalle_carrito
        )

        print(
            "CANTIDAD ACTUAL:",
            detalle_existente.cantidad
        )

        print(
            "NUEVA CANTIDAD:",
            nueva_cantidad
        )

        # ==================================================
        # VALIDAR STOCK TOTAL
        # ==================================================

        if nueva_cantidad > producto.stock_producto:

            return jsonify({
                "message":
                    "No hay suficiente stock para agregar esa cantidad."
            }), 400

        # ==================================================
        # ACTUALIZAR CANTIDAD
        # ==================================================

        detalle_existente.cantidad = nueva_cantidad

        detalle_existente.update()

        # ==================================================
        # RECALCULAR TOTAL DEL CARRITO
        # ==================================================

        carrito.recalcular_total()

        print(
            "CANTIDAD SUMADA CORRECTAMENTE"
        )

        return jsonify({

            "message":
                "La cantidad del producto fue actualizada.",

            "detalle":
                detalle_existente.to_dict(),

            "total_carrito":
                float(carrito.total_carrito)

        }), 200

    # ======================================================
    # SI NO EXISTE → CREAR DETALLE
    # ======================================================

    precio = producto.precio_producto

    detalle = Detalle_Carrito(

        id_carrito=
            carrito.id_carrito,

        id_producto=
            producto.id_producto,

        cantidad=
            cantidad,

        precio_unitario=
            precio,

        talla=
            talla

    )

    detalle.save()

    # ======================================================
    # RECALCULAR TOTAL DEL CARRITO
    # ======================================================

    carrito.recalcular_total()

    print(
        "NUEVO DETALLE CREADO:",
        detalle.id_detalle_carrito
    )

    return jsonify({

        "message":
            "Producto agregado al carrito correctamente.",

        "detalle":
            detalle.to_dict(),

        "total_carrito":
            float(carrito.total_carrito)

    }), 201


# ==========================================================
# ACTUALIZAR DETALLE
# ==========================================================

@DetalleCarrito_bp.route(
    "/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def update_detalle(id):

    print("========== ACTUALIZAR DETALLE ==========")

    # ======================================================
    # DATA
    # ======================================================

    data = request.get_json()

    if not data:

        return jsonify({
            "message":
                "Debe enviar información en formato JSON."
        }), 400

    # ======================================================
    # CLIENTE
    # ======================================================

    id_cliente = get_jwt_identity()

    # ======================================================
    # BUSCAR CARRITO
    # ======================================================

    carrito = Carrito.get_by_cliente(
        id_cliente
    )

    if carrito is None:

        return jsonify({
            "message":
                "El carrito del usuario no existe."
        }), 404

    # ======================================================
    # BUSCAR DETALLE
    # ======================================================

    detalle = Detalle_Carrito.get_by_id(id)

    if detalle is None:

        return jsonify({
            "message":
                "Detalle del carrito no encontrado."
        }), 404

    # ======================================================
    # VALIDAR PROPIETARIO
    # ======================================================

    if detalle.id_carrito != carrito.id_carrito:

        return jsonify({
            "message":
                "No autorizado."
        }), 403

    # ======================================================
    # BUSCAR PRODUCTO
    # ======================================================

    producto = Productos.get_by_id(
        detalle.id_producto
    )

    if producto is None:

        return jsonify({
            "message":
                "El producto ya no existe."
        }), 404

    # ======================================================
    # ACTUALIZAR CANTIDAD
    # ======================================================

    if "cantidad" in data:

        try:

            cantidad = int(
                data["cantidad"]
            )

        except (
            ValueError,
            TypeError
        ):

            return jsonify({
                "message":
                    "Cantidad inválida."
            }), 400

        if cantidad <= 0:

            return jsonify({
                "message":
                    "La cantidad debe ser mayor que cero."
            }), 400

        if cantidad > producto.stock_producto:

            return jsonify({
                "message":
                    "Stock insuficiente."
            }), 400

        detalle.cantidad = cantidad

    # ======================================================
    # ACTUALIZAR TALLA
    # ======================================================

    categoria = (
        producto.categoria or ""
    ).lower().strip()

    if categoria in ["ropa", "zapatos"]:

        if "talla" in data:

            talla = str(
                data["talla"]
            ).strip()

            if talla == "":

                return jsonify({
                    "message":
                        "La talla es obligatoria."
                }), 400

            detalle.talla = talla

    # ======================================================
    # GUARDAR
    # ======================================================

    detalle.update()

    # ======================================================
    # RECALCULAR TOTAL DEL CARRITO
    # ======================================================

    carrito.recalcular_total()

    return jsonify({

        "message":
            "Detalle actualizado correctamente.",

        "detalle":
            detalle.to_dict(),

        "total_carrito":
            float(carrito.total_carrito)

    }), 200


# ==========================================================
# ELIMINAR DETALLE
# ==========================================================

@DetalleCarrito_bp.route(
    "/<int:id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_detalle(id):

    print("========== ELIMINAR DETALLE ==========")

    # ======================================================
    # CLIENTE
    # ======================================================

    id_cliente = get_jwt_identity()

    # ======================================================
    # BUSCAR CARRITO
    # ======================================================

    carrito = Carrito.get_by_cliente(
        id_cliente
    )

    if carrito is None:

        return jsonify({
            "message":
                "El carrito del usuario no existe."
        }), 404

    # ======================================================
    # BUSCAR DETALLE
    # ======================================================

    detalle = Detalle_Carrito.get_by_id(id)

    if detalle is None:

        return jsonify({
            "message":
                "Detalle del carrito no encontrado."
        }), 404

    # ======================================================
    # VALIDAR PROPIETARIO
    # ======================================================

    if detalle.id_carrito != carrito.id_carrito:

        return jsonify({
            "message":
                "No autorizado."
        }), 403

    # ======================================================
    # ELIMINAR
    # ======================================================

    detalle.delete()

    # ======================================================
    # RECALCULAR TOTAL
    # ======================================================

    carrito.recalcular_total()

    return jsonify({

        "message":
            "Producto eliminado del carrito correctamente.",

        "total_carrito":
            float(carrito.total_carrito)

    }), 200