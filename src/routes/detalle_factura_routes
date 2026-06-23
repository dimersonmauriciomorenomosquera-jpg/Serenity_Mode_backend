from flask import Blueprint, request, jsonify
from src.models.detalle_factura import DetalleFactura
from src.models import session

DetalleFactura_bp = Blueprint("detalle_factura", __name__)

# GET - Obtener todos los detalles
@DetalleFactura_bp.route("/", methods=["GET"])
def get_detalles_factura():
    detalles = session.query(DetalleFactura).all()

    return jsonify([
        {
            "id_detalle_factura": detalle.id_detalle_factura,
            "id_factura": detalle.id_factura,
            "id_producto": detalle.id_producto,
            "cantidad": detalle.cantidad,
            "precio_unitario": str(detalle.precio_unitario),
            "subtotal": str(detalle.subtotal)
        }
        for detalle in detalles
    ])


# POST - Crear detalle de factura
@DetalleFactura_bp.route("/", methods=["POST"])
def create_detalle_factura():
    data = request.get_json()

    nuevo_detalle = DetalleFactura(
        id_factura=data["id_factura"],
        id_producto=data["id_producto"],
        cantidad=data["cantidad"],
        precio_unitario=data["precio_unitario"],
        subtotal=data["subtotal"]
    )

    session.add(nuevo_detalle)
    session.commit()

    return jsonify({"mensaje": "Detalle de factura creado correctamente"}), 201


# PUT - Actualizar detalle
@DetalleFactura_bp.route("/<int:id>", methods=["PUT"])
def update_detalle_factura(id):
    detalle = session.query(DetalleFactura).filter_by(
        id_detalle_factura=id
    ).first()

    if not detalle:
        return jsonify({"error": "Detalle no encontrado"}), 404

    data = request.get_json()

    detalle.id_factura = data.get("id_factura", detalle.id_factura)
    detalle.id_producto = data.get("id_producto", detalle.id_producto)
    detalle.cantidad = data.get("cantidad", detalle.cantidad)
    detalle.precio_unitario = data.get("precio_unitario", detalle.precio_unitario)
    detalle.subtotal = data.get("subtotal", detalle.subtotal)

    session.commit()

    return jsonify({"mensaje": "Detalle actualizado correctamente"})


# DELETE - Eliminar detalle
@DetalleFactura_bp.route("/<int:id>", methods=["DELETE"])
def delete_detalle_factura(id):
    detalle = session.query(DetalleFactura).filter_by(
        id_detalle_factura=id
    ).first()

    if not detalle:
        return jsonify({"error": "Detalle no encontrado"}), 404

    session.delete(detalle)
    session.commit()

    return jsonify({"mensaje": "Detalle eliminado correctamente"})