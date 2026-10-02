
import uuid

from flask import Blueprint, request, jsonify, current_app

from datetime import datetime
from decimal import Decimal, InvalidOperation

from mercadopago.config import RequestOptions

from flask_jwt_extended import jwt_required

from src.models import session

from src.models.pago import Pago
from src.models.carrito import Carrito
from src.models.detalle_carrito import Detalle_Carrito
from src.models.factura import Factura
from src.models.detalle_factura import Detalle_Factura
from src.models.productos import Productos

from src.utils.decorators import admin_required


Pago_bp = Blueprint('Pago', __name__)


# ==========================================================
# COSTOS DE ENVÍO
# ==========================================================

COSTOS_ENVIO = {
    "gratis": Decimal("0.00"),
    "estandar": Decimal("9900.00"),
    "express": Decimal("16900.00")
}


def obtener_costo_envio(tipo_envio):

    if not tipo_envio:
        return None

    tipo_envio = str(tipo_envio).strip().lower()

    return COSTOS_ENVIO.get(tipo_envio)


# ==========================================================
# OBTENER TODOS LOS PAGOS
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_pagos():

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

    pagos, total = Pago.get(
        page=page,
        per_page=per_page
    )

    total_pages = (total + per_page - 1) // per_page

    lista = []

    for pago in pagos:

        lista.append({

            'id_pago':
                pago.id_pago,

            'fecha_pago':
                str(pago.fecha_pago),

            'hora_pago':
                str(pago.hora_pago),

            'monto':
                float(pago.monto),

            'metodo_pago':
                pago.metodo_pago,

            'estado_pago':
                pago.estado_pago,

            'id_factura':
                pago.id_factura,

            'id_cliente':
                pago.id_cliente,

            'id_mercadopago':
                pago.id_mercadopago,

            'id_order_mercadopago':
                pago.id_order_mercadopago

        })

    return jsonify({

        'data':
            lista,

        'pagination': {

            'page':
                page,

            'per_page':
                per_page,

            'total':
                total,

            'pages':
                total_pages

        }

    }), 200


# ==========================================================
# OBTENER UN PAGO POR ID
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@admin_required
def get_pago(id):

    pago = Pago.get_by_id(id)

    if not pago:
        return jsonify({
            'message': 'Pago no encontrado'
        }), 404

    return jsonify({

        'id_pago':
            pago.id_pago,

        'fecha_pago':
            str(pago.fecha_pago),

        'hora_pago':
            str(pago.hora_pago),

        'monto':
            float(pago.monto),

        'metodo_pago':
            str(pago.metodo_pago),

        'estado_pago':
            str(pago.estado_pago),

        'id_factura':
            pago.id_factura,

        'id_cliente':
            pago.id_cliente,

        'id_mercadopago':
            pago.id_mercadopago,

        'id_order_mercadopago':
            pago.id_order_mercadopago

    }), 200


# ==========================================================
# CREAR ORDER DE MERCADO PAGO
#
# PRUEBA TEMPORAL SIN JWT
#
# AQUÍ NO SE CREA FACTURA NI PAGO.
# SOLO SE CREA LA ORDER.
# ==========================================================

@Pago_bp.route('/crear-order', methods=['POST'])
def crear_order():

    data = request.get_json()

    if not data or not data.get("id_carrito"):
        return jsonify({
            "message": "id_carrito es obligatorio"
        }), 400

    # ======================================================
    # OBTENER TIPO DE ENVÍO
    # ======================================================

    tipo_envio = data.get("tipo_envio")

    if not tipo_envio:
        return jsonify({
            "message": "tipo_envio es obligatorio",
            "tipos_validos": list(COSTOS_ENVIO.keys())
        }), 400

    tipo_envio = str(tipo_envio).strip().lower()

    costo_envio = obtener_costo_envio(tipo_envio)

    if costo_envio is None:
        return jsonify({
            "message": "Tipo de envío no válido",
            "tipo_envio": tipo_envio,
            "tipos_validos": list(COSTOS_ENVIO.keys())
        }), 400

    # ======================================================
    # OBTENER CARRITO
    # ======================================================

    id_carrito = data["id_carrito"]

    carrito = Carrito.get_by_id(id_carrito)

    if not carrito:
        return jsonify({
            "message": "Carrito no encontrado"
        }), 404

    detalles = Detalle_Carrito.get_by_carrito(id_carrito)

    if not detalles:
        return jsonify({
            "message": "El carrito está vacío"
        }), 400

    # ======================================================
    # CALCULAR SUBTOTAL DE PRODUCTOS
    # ======================================================

    items = []

    subtotal_productos = Decimal("0.00")

    try:

        for detalle in detalles:

            precio_unitario = Decimal(
                str(detalle.precio_unitario)
            )

            cantidad = int(
                detalle.cantidad
            )

            if cantidad <= 0:
                return jsonify({
                    "message":
                        f"La cantidad del producto "
                        f"{detalle.id_producto} debe ser mayor que 0"
                }), 400

            if precio_unitario < 0:
                return jsonify({
                    "message":
                        f"El precio del producto "
                        f"{detalle.id_producto} no puede ser negativo"
                }), 400

            subtotal = (
                precio_unitario * cantidad
            )

            subtotal_productos += subtotal

            precio_mp = int(
                precio_unitario
            )

            items.append({

                "title":
                    f"Producto {detalle.id_producto}",

                "quantity":
                    cantidad,

                "unit_price":
                    str(precio_mp)

            })

    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):

        return jsonify({
            "message":
                "Uno de los precios o cantidades del carrito es inválido"
        }), 400

    # ======================================================
    # VALIDAR SUBTOTAL
    # ======================================================

    if subtotal_productos <= 0:

        return jsonify({
            "message":
                "El subtotal de los productos debe ser mayor que 0"
        }), 400

    # ======================================================
    # AGREGAR COSTO DE ENVÍO COMO ITEM
    #
    # Mercado Pago exige que la suma de los items
    # coincida con total_amount.
    #
    # Si el envío es gratis, no agregamos un item
    # de valor 0.
    # ======================================================

    if costo_envio > 0:

        items.append({

            "title":
                f"Envío {tipo_envio}",

            "quantity":
                1,

            "unit_price":
                str(
                    int(costo_envio)
                )

        })

    # ======================================================
    # CALCULAR TOTAL FINAL
    # ======================================================

    total_final = (
        subtotal_productos +
        costo_envio
    )

    total_mp = int(
        total_final
    )

    if total_mp <= 0:

        return jsonify({
            "message":
                "El total de la compra debe ser mayor que 0"
        }), 400

    # ======================================================
    # VALIDAR QUE LOS ITEMS COINCIDAN CON EL TOTAL
    # ======================================================

    total_items = Decimal("0.00")

    try:

        for item in items:

            cantidad = Decimal(
                str(item["quantity"])
            )

            precio = Decimal(
                str(item["unit_price"])
            )

            total_items += (
                cantidad * precio
            )

    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):

        return jsonify({
            "message":
                "No fue posible calcular el total de los items"
        }), 400

    if total_items != Decimal(
        str(total_mp)
    ):

        return jsonify({

            "message":
                "La suma de los items no coincide con el total de la Order",

            "total_items":
                float(total_items),

            "total_final":
                float(total_final)

        }), 400

    # ======================================================
    # EXTERNAL REFERENCE
    #
    # Formato:
    #
    # 9_express
    #
    # Permite recuperar:
    #
    # id_carrito
    # tipo_envio
    # ======================================================

    external_reference = (
        f"{id_carrito}_{tipo_envio}"
    )

    # ======================================================
    # SDK MERCADO PAGO
    # ======================================================

    sdk = current_app.config["MP_SDK"]

    order_data = {

        "type":
            "online",

        "processing_mode":
            "manual",

        "total_amount":
            str(total_mp),

        "external_reference":
            external_reference,

        "items":
            items

    }

    print("====================================")
    print("DATOS ENVIADOS A MERCADO PAGO:")
    print(order_data)
    print("SUBTOTAL PRODUCTOS:", subtotal_productos)
    print("TIPO ENVÍO:", tipo_envio)
    print("COSTO ENVÍO:", costo_envio)
    print("TOTAL ITEMS:", total_items)
    print("TOTAL FINAL:", total_final)
    print("EXTERNAL REFERENCE:", external_reference)
    print("====================================")

    # ======================================================
    # CREAR ORDER
    # ======================================================

    try:

        order = sdk.order()

        request_options = RequestOptions(
            custom_headers={
                "x-idempotency-key":
                    str(uuid.uuid4())
            }
        )

        response = order.create(
            order_data,
            request_options
        )

        print("====================================")
        print("RESPUESTA MERCADO PAGO:")
        print(response)
        print("====================================")

        status_mp = response.get(
            "status",
            500
        )

        if status_mp not in [200, 201]:

            return jsonify({

                "message":
                    "Mercado Pago rechazó la Order",

                "order":
                    response

            }), status_mp

        return jsonify({

            "message":
                "Order creada correctamente",

            "subtotal_productos":
                float(subtotal_productos),

            "tipo_envio":
                tipo_envio,

            "costo_envio":
                float(costo_envio),

            "total_final":
                float(total_final),

            "external_reference":
                external_reference,

            "order":
                response

        }), 201

    except Exception as e:

        print("====================================")
        print("ERROR MERCADO PAGO:")
        print(e)
        print("====================================")

        return jsonify({

            "message":
                "Error al crear la Order",

            "error":
                str(e)

        }), 500


# ==========================================================
# VERIFICAR PAGO DE MERCADO PAGO
#
# PRUEBA TEMPORAL SIN JWT
# ==========================================================

@Pago_bp.route(
    '/verificar-pago/<int:payment_id>',
    methods=['GET']
)
def verificar_pago(payment_id):

    # ======================================================
    # OBTENER SDK
    # ======================================================

    sdk = current_app.config["MP_SDK"]

    # ======================================================
    # CONSULTAR PAGO
    # ======================================================

    try:

        payment = sdk.payment().get(
            payment_id
        )

        print("====================================")
        print("RESPUESTA DEL PAGO:")
        print(payment)
        print("====================================")

    except Exception as e:

        print("====================================")
        print("ERROR CONSULTANDO PAGO:")
        print(e)
        print("====================================")

        return jsonify({

            "message":
                "No fue posible consultar el pago en Mercado Pago",

            "error":
                str(e)

        }), 500

    # ======================================================
    # OBTENER RESPUESTA
    # ======================================================

    payment_data = payment.get(
        "response",
        payment
    )

    if not payment_data:

        return jsonify({

            "message":
                "Mercado Pago no devolvió información del pago"

        }), 404

    # ======================================================
    # ESTADO
    # ======================================================

    status = payment_data.get(
        "status"
    )

    status_detail = payment_data.get(
        "status_detail"
    )

    if status != "approved":

        return jsonify({

            "message":
                "El pago todavía no está aprobado",

            "payment_id":
                payment_id,

            "status":
                status,

            "status_detail":
                status_detail

        }), 400

    # ======================================================
    # VALIDAR ACREDITACIÓN
    # ======================================================

    if status_detail != "accredited":

        return jsonify({

            "message":
                "El pago no está acreditado",

            "payment_id":
                payment_id,

            "status":
                status,

            "status_detail":
                status_detail

        }), 400

    # ======================================================
    # VALIDAR MONEDA
    # ======================================================

    currency_id = payment_data.get(
        "currency_id"
    )

    if currency_id != "COP":

        return jsonify({

            "message":
                "La moneda del pago no es válida",

            "currency_id":
                currency_id

        }), 400

    # ======================================================
    # OBTENER MONTO PAGADO
    # ======================================================

    try:

        monto_pagado = Decimal(
            str(
                payment_data.get(
                    "transaction_amount",
                    0
                )
            )
        )

    except (
        InvalidOperation,
        TypeError,
        ValueError
    ):

        return jsonify({

            "message":
                "Mercado Pago devolvió un monto inválido"

        }), 400

    if monto_pagado <= 0:

        return jsonify({

            "message":
                "El monto pagado debe ser mayor que 0"

        }), 400

    # ======================================================
    # VALIDAR ORDER
    # ======================================================

    order_data = payment_data.get(
        "order"
    )

    if not order_data:

        return jsonify({

            "message":
                "El pago no contiene información de la Order"

        }), 400

    order_id = order_data.get(
        "id"
    )

    if not order_id:

        return jsonify({

            "message":
                "No fue posible obtener el ID de la Order"

        }), 400

    # ======================================================
    # EXTERNAL REFERENCE
    # ======================================================

    external_reference = payment_data.get(
        "external_reference"
    )

    if not external_reference:

        return jsonify({

            "message":
                "El pago no contiene external_reference"

        }), 400

    # ======================================================
    # SEPARAR CARRITO Y TIPO DE ENVÍO
    #
    # Formato:
    #
    # 9_express
    # ======================================================

    try:

        partes_reference = str(
            external_reference
        ).split("_", 1)

        if len(partes_reference) != 2:

            raise ValueError(
                "Formato de external_reference inválido"
            )

        id_carrito = int(
            partes_reference[0]
        )

        tipo_envio = (
            partes_reference[1]
            .strip()
            .lower()
        )

    except (
        ValueError,
        TypeError
    ):

        return jsonify({

            "message":
                "La external_reference del pago no contiene un carrito y tipo de envío válidos"

        }), 400

    # ======================================================
    # OBTENER COSTO DE ENVÍO
    # ======================================================

    costo_envio = obtener_costo_envio(
        tipo_envio
    )

    if costo_envio is None:

        return jsonify({

            "message":
                "El tipo de envío asociado al pago no es válido",

            "tipo_envio":
                tipo_envio,

            "tipos_validos":
                list(COSTOS_ENVIO.keys())

        }), 400

    # ======================================================
    # BUSCAR CARRITO
    # ======================================================

    carrito = Carrito.get_by_id(
        id_carrito
    )

    if not carrito:

        return jsonify({

            "message":
                "El carrito asociado al pago no existe",

            "id_carrito":
                id_carrito

        }), 404

    # ======================================================
    # VALIDAR CLIENTE
    # ======================================================

    if not carrito.id_cliente:

        return jsonify({

            "message":
                "El carrito no tiene un cliente asociado"

        }), 400

    # ======================================================
    # OBTENER DETALLES DEL CARRITO
    # ======================================================

    detalles = Detalle_Carrito.get_by_carrito(
        id_carrito
    )

    if not detalles:

        return jsonify({

            "message":
                "El carrito no contiene productos"

        }), 400

    # ======================================================
    # CALCULAR SUBTOTAL REAL
    # ======================================================

    subtotal_productos = Decimal("0.00")

    try:

        for detalle in detalles:

            precio_unitario = Decimal(
                str(
                    detalle.precio_unitario
                )
            )

            cantidad = int(
                detalle.cantidad
            )

            if cantidad <= 0:

                return jsonify({

                    "message":
                        f"La cantidad del producto "
                        f"{detalle.id_producto} debe ser mayor que 0"

                }), 400

            if precio_unitario < 0:

                return jsonify({

                    "message":
                        f"El precio del producto "
                        f"{detalle.id_producto} no puede ser negativo"

                }), 400

            subtotal = (
                precio_unitario *
                cantidad
            )

            subtotal_productos += subtotal

    except (
        InvalidOperation,
        ValueError,
        TypeError
    ):

        return jsonify({

            "message":
                "Uno de los productos del carrito tiene precio o cantidad inválida"

        }), 400

    # ======================================================
    # VALIDAR SUBTOTAL
    # ======================================================

    if subtotal_productos <= 0:

        return jsonify({

            "message":
                "El subtotal calculado de los productos debe ser mayor que 0",

            "subtotal_productos":
                float(subtotal_productos)

        }), 400

    # ======================================================
    # CALCULAR TOTAL FINAL
    # ======================================================

    total_final = (
        subtotal_productos +
        costo_envio
    )

    if total_final <= 0:

        return jsonify({

            "message":
                "El total final de la compra debe ser mayor que 0",

            "subtotal_productos":
                float(subtotal_productos),

            "costo_envio":
                float(costo_envio),

            "total_final":
                float(total_final)

        }), 400

    # ======================================================
    # COMPARAR MONTO PAGADO
    # ======================================================

    if monto_pagado != total_final:

        return jsonify({

            "message":
                "El monto pagado no coincide con el total de la compra",

            "monto_pagado":
                float(monto_pagado),

            "subtotal_productos":
                float(subtotal_productos),

            "costo_envio":
                float(costo_envio),

            "total_final":
                float(total_final)

        }), 400

    # ======================================================
    # EVITAR PAGO DUPLICADO
    # ======================================================

    pago_existente = (
        session
        .query(Pago)
        .filter_by(
            id_mercadopago=
                str(payment_id)
        )
        .first()
    )

    if pago_existente:

        return jsonify({

            "message":
                "Este pago ya fue procesado",

            "id_pago":
                pago_existente.id_pago,

            "id_mercadopago":
                pago_existente.id_mercadopago,

            "id_factura":
                pago_existente.id_factura,

            "fecha_pago":
                str(pago_existente.fecha_pago),

            "hora_pago":
                str(pago_existente.hora_pago)

        }), 200

    # ======================================================
    # VERIFICAR STOCK
    # ======================================================

    productos_stock = []

    for detalle in detalles:

        producto = Productos.get_by_id(
            detalle.id_producto
        )

        if not producto:

            return jsonify({

                "message":
                    "Uno de los productos del carrito ya no existe",

                "id_producto":
                    detalle.id_producto

            }), 404

        if producto.stock_producto < detalle.cantidad:

            return jsonify({

                "message":
                    "No hay suficiente stock para completar la compra",

                "id_producto":
                    producto.id_producto,

                "producto":
                    producto.nombre_producto,

                "stock_disponible":
                    producto.stock_producto,

                "cantidad_solicitada":
                    detalle.cantidad

            }), 409

        productos_stock.append(
            (
                producto,
                detalle.cantidad
            )
        )

    # ======================================================
    # REGISTRAR VENTA COMPLETA
    # ======================================================

    try:

        # ==================================================
        # FECHA Y HORA DE LA OPERACIÓN
        # ==================================================

        ahora = datetime.now()

        # ==================================================
        # CREAR FACTURA
        # ==================================================

        factura = Factura(

            fecha_factura=
                ahora.date(),

            hora_factura=
                ahora.time(),

            subtotal_productos=
                subtotal_productos,

            costo_envio=
                costo_envio,

            total_pagar=
                total_final,

            estado_pago=
                "pagado",

            id_cliente=
                carrito.id_cliente,

            id_carrito=
                carrito.id_carrito

        )

        session.add(
            factura
        )

        # ==================================================
        # FLUSH
        # ==================================================

        session.flush()

        # ==================================================
        # CREAR DETALLES DE FACTURA
        # ==================================================

        for detalle in detalles:

            precio_unitario = Decimal(
                str(
                    detalle.precio_unitario
                )
            )

            cantidad = int(
                detalle.cantidad
            )

            subtotal = (
                precio_unitario *
                cantidad
            )

            detalle_factura = Detalle_Factura(

                id_factura=
                    factura.id_factura,

                id_producto=
                    detalle.id_producto,

                cantidad=
                    cantidad,

                precio_unitario=
                    precio_unitario,

                subtotal=
                    subtotal

            )

            session.add(
                detalle_factura
            )

        # ==================================================
        # DESCONTAR STOCK
        # ==================================================

        for producto, cantidad in productos_stock:

            producto.stock_producto -= cantidad

        # ==================================================
        # OBTENER MÉTODO DE PAGO
        # ==================================================

        metodo_pago = payment_data.get(
            "payment_method_id"
        )

        if not metodo_pago:

            metodo_pago = payment_data.get(
                "payment_type_id",
                "mercado_pago"
            )

        # ==================================================
        # CREAR PAGO
        # ==================================================

        pago = Pago(

            fecha_pago=
                ahora.date(),

            hora_pago=
                ahora.time(),

            monto=
                monto_pagado,

            metodo_pago=
                metodo_pago,

            estado_pago=
                "pagado",

            id_cliente=
                carrito.id_cliente,

            id_factura=
                factura.id_factura,

            id_mercadopago=
                str(payment_id),

            id_order_mercadopago=
                str(order_id)

        )

        session.add(
            pago
        )

        # ==================================================
        # LIMPIAR CARRITO
        # ==================================================

        for detalle in detalles:

            session.delete(
                detalle
            )

        # ==================================================
        # REINICIAR TOTAL DEL CARRITO
        # ==================================================

        carrito.total_carrito = Decimal(
            "0.00"
        )

        # ==================================================
        # COMMIT FINAL
        # ==================================================

        session.commit()

    except Exception as e:

        session.rollback()

        print("====================================")
        print("ERROR REGISTRANDO VENTA:")
        print(e)
        print("====================================")

        return jsonify({

            "message":
                "El pago fue aprobado, pero ocurrió un error al registrar la venta",

            "error":
                str(e)

        }), 500

    # ======================================================
    # RESPUESTA FINAL
    # ======================================================

    return jsonify({

        "message":
            "Pago verificado y venta registrada correctamente",

        "payment": {

            "id_pago":
                pago.id_pago,

            "id_mercadopago":
                str(payment_id),

            "id_order_mercadopago":
                str(order_id),

            "fecha_pago":
                str(pago.fecha_pago),

            "hora_pago":
                str(pago.hora_pago),

            "status":
                status,

            "status_detail":
                status_detail,

            "monto":
                float(monto_pagado)

        },

        "venta": {

            "id_carrito":
                carrito.id_carrito,

            "id_factura":
                factura.id_factura,

            "id_cliente":
                carrito.id_cliente,

            "fecha_factura":
                str(factura.fecha_factura),

            "hora_factura":
                str(factura.hora_factura),

            "subtotal_productos":
                float(subtotal_productos),

            "tipo_envio":
                tipo_envio,

            "costo_envio":
                float(costo_envio),

            "total":
                float(total_final)

        }

    }), 201


# ==========================================================
# ELIMINAR PAGO
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_pago(id):

    pago = Pago.get_by_id(id)

    if not pago:

        return jsonify({
            'message': 'Pago no encontrado'
        }), 404

    pago.delete()

    return jsonify({

        'message':
            'Pago eliminado exitosamente'

    }), 200


# ==========================================================
# ACTUALIZAR PAGO
# SOLO ADMINISTRADORES
# ==========================================================

@Pago_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_pago(id):

    pago = Pago.get_by_id(id)

    if not pago:

        return jsonify({
            'message': 'Pago no encontrado'
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            'message': 'No se recibieron datos'
        }), 400

    # ======================================================
    # FECHA
    # ======================================================

    if 'fecha_pago' in data:

        try:

            pago.fecha_pago = datetime.strptime(
                data['fecha_pago'],
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                'message': 'Fecha inválida'
            }), 400

    # ======================================================
    # HORA
    # ======================================================

    if 'hora_pago' in data:

        try:

            pago.hora_pago = datetime.strptime(
                data['hora_pago'],
                "%H:%M:%S"
            ).time()

        except ValueError:

            return jsonify({
                'message': 'Hora inválida. Use el formato HH:MM:SS'
            }), 400

    # ======================================================
    # MONTO
    # ======================================================

    if 'monto' in data:

        try:

            monto = Decimal(
                str(data['monto'])
            )

            if monto < 0:

                return jsonify({
                    'message':
                        'El monto no puede ser negativo'
                }), 400

            pago.monto = monto

        except (
            ValueError,
            TypeError,
            InvalidOperation
        ):

            return jsonify({
                'message':
                    'Monto inválido'
            }), 400

    # ======================================================
    # MÉTODO DE PAGO
    # ======================================================

    if 'metodo_pago' in data:

        pago.metodo_pago = data[
            'metodo_pago'
        ]

    # ======================================================
    # ESTADO DEL PAGO
    # ======================================================

    if 'estado_pago' in data:

        pago.estado_pago = data[
            'estado_pago'
        ]

    # ======================================================
    # ID FACTURA
    # ======================================================

    if 'id_factura' in data:

        pago.id_factura = data[
            'id_factura'
        ]

    # ======================================================
    # ID CLIENTE
    # ======================================================

    if 'id_cliente' in data:

        pago.id_cliente = data[
            'id_cliente'
        ]

    # ======================================================
    # ID MERCADO PAGO
    # ======================================================

    if 'id_mercadopago' in data:

        pago.id_mercadopago = data[
            'id_mercadopago'
        ]

    # ======================================================
    # ID ORDER MERCADO PAGO
    # ======================================================

    if 'id_order_mercadopago' in data:

        pago.id_order_mercadopago = data[
            'id_order_mercadopago'
        ]

    # ======================================================
    # GUARDAR CAMBIOS
    # ======================================================

    try:

        pago.save()

    except Exception as e:

        return jsonify({

            'message':
                'Error al actualizar el pago',

            'error':
                str(e)

        }), 500

    return jsonify({

        'message':
            'Pago actualizado exitosamente',

        'pago':
            pago.to_dict()

    }), 200
