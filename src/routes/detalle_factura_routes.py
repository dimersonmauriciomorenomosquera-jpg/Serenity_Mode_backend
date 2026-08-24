from flask import Blueprint, request, jsonify
from src.models.detalle_factura import DetalleFactura
from src.models import session
from src.utils.decorators import admin_required

DetalleFactura_bp = Blueprint("detalle_factura", __name__)


# ==========================================================
# GET - Obtener todos los detalles
# SOLO ADMINISTRADORES
# ==========================================================

@DetalleFactura_bp.route("/", methods=["GET"])
@admin_required
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


# ==========================================================
# POST - Crear detalle de factura
# SOLO ADMINISTRADORES
# ==========================================================

@DetalleFactura_bp.route("/", methods=["POST"])
@admin_required
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

    return jsonify({
        "mensaje": "Detalle de factura creado correctamente"
    }), 201


