from flask import Blueprint, request, jsonify

from src.models.productos import Productos
from src.utils.decorators import admin_required


Productos_bp = Blueprint(
    'Productos',
    __name__
)


# ==========================================================
# OBTENER TODOS LOS PRODUCTOS
# GET /productos/
# PÚBLICO
# ==========================================================

@Productos_bp.route(
    '/',
    methods=['GET']
)
def get_productos():

    try:

        buscar = request.args.get(
            "buscar",
            ""
        ).strip()

        categoria = request.args.get(
            "categoria",
            ""
        ).strip()

        ordenar = request.args.get(
            "ordenar",
            ""
        ).strip()

        pagina = request.args.get(
            "pagina",
            1,
            type=int
        )

        por_pagina = request.args.get(
            "por_pagina",
            1000,
            type=int
        )


        if pagina < 1:
            pagina = 1

        if por_pagina < 1:
            por_pagina = 1000


        resultado = Productos.get(

            buscar=buscar,

            categoria=categoria,

            ordenar=ordenar,

            pagina=pagina,

            por_pagina=por_pagina

        )


        productos = []


        for producto in resultado["productos"]:

            productos.append({

                "id_producto":
                    producto.id_producto,

                "nombre_producto":
                    producto.nombre_producto,

                "descripcion_producto":
                    producto.descripcion_producto,

                "talla":
                    producto.talla,

                "precio_producto":
                    float(
                        producto.precio_producto
                    ),

                "stock_producto":
                    producto.stock_producto,

                "marca_producto":
                    producto.marca_producto,

                "sku":
                    producto.sku,

                "categoria":
                    producto.categoria,

                "imagen":
                    producto.imagen

            })


        return jsonify({

            "productos":
                productos,

            "pagina":
                resultado["pagina"],

            "por_pagina":
                resultado["por_pagina"],

            "total_productos":
                resultado["total_productos"],

            "total_paginas":
                resultado["total_paginas"]

        }), 200


    except Exception as e:

        print(
            "ERROR OBTENIENDO PRODUCTOS:",
            e
        )

        return jsonify({

            "message":
                "Error obteniendo productos.",

            "error":
                str(e)

        }), 500


# ==========================================================
# BUSCAR / FILTRAR / ORDENAR / PAGINAR
# GET /productos/buscar
# PÚBLICO
# ==========================================================

@Productos_bp.route(
    '/buscar',
    methods=['GET']
)
def buscar_productos():

    try:

        buscar = request.args.get(
            "buscar",
            ""
        ).strip()

        categoria = request.args.get(
            "categoria",
            ""
        ).strip()

        ordenar = request.args.get(
            "ordenar",
            ""
        ).strip()

        pagina = request.args.get(
            "pagina",
            1,
            type=int
        )

        por_pagina = request.args.get(
            "por_pagina",
            12,
            type=int
        )


        if pagina < 1:
            pagina = 1

        if por_pagina < 1:
            por_pagina = 12


        resultado = Productos.get(

            buscar=buscar,

            categoria=categoria,

            ordenar=ordenar,

            pagina=pagina,

            por_pagina=por_pagina

        )


        productos = []


        for producto in resultado["productos"]:

            productos.append({

                "id_producto":
                    producto.id_producto,

                "nombre_producto":
                    producto.nombre_producto,

                "descripcion_producto":
                    producto.descripcion_producto,

                "talla":
                    producto.talla,

                "precio_producto":
                    float(
                        producto.precio_producto
                    ),

                "stock_producto":
                    producto.stock_producto,

                "marca_producto":
                    producto.marca_producto,

                "sku":
                    producto.sku,

                "categoria":
                    producto.categoria,

                "imagen":
                    producto.imagen

            })


        return jsonify({

            "productos":
                productos,

            "pagina":
                resultado["pagina"],

            "por_pagina":
                resultado["por_pagina"],

            "total_productos":
                resultado["total_productos"],

            "total_paginas":
                resultado["total_paginas"]

        }), 200


    except Exception as e:

        print(
            "ERROR BUSCANDO PRODUCTOS:",
            e
        )

        return jsonify({

            "message":
                "Error buscando productos.",

            "error":
                str(e)

        }), 500


# ==========================================================
# OBTENER PRODUCTO POR ID
# GET /productos/<id>
# PÚBLICO
# ==========================================================

@Productos_bp.route(
    '/<int:id>',
    methods=['GET']
)
def get_producto(id):

    producto = Productos.get_by_id(
        id
    )


    if not producto:

        return jsonify({

            "message":
                "Producto no encontrado"

        }), 404


    producto_data = {

        "id_producto":
            producto.id_producto,

        "nombre_producto":
            producto.nombre_producto,

        "descripcion_producto":
            producto.descripcion_producto,

        "talla":
            producto.talla,

        "precio_producto":
            float(
                producto.precio_producto
            ),

        "stock_producto":
            producto.stock_producto,

        "marca_producto":
            producto.marca_producto,

        "sku":
            producto.sku,

        "categoria":
            producto.categoria,

        "imagen":
            producto.imagen

    }


    return jsonify(
        producto_data
    ), 200


# ==========================================================
# CREAR PRODUCTO
# POST /productos/
# SOLO ADMINISTRADORES
# ==========================================================

@Productos_bp.route(
    '/',
    methods=['POST']
)
@admin_required
def create_producto():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Debe enviar los datos del producto."

        }), 400


    try:

        precio = float(
            data["precio_producto"]
        )

    except (
        ValueError,
        TypeError,
        KeyError
    ):

        return jsonify({

            "message":
                "El precio debe ser un numero valido."

        }), 400


    if precio <= 0:

        return jsonify({

            "message":
                "El precio debe ser mayor a cero."

        }), 400


    try:

        stock = int(
            data["stock_producto"]
        )

    except (
        ValueError,
        TypeError,
        KeyError
    ):

        return jsonify({

            "message":
                "El stock debe ser un numero valido."

        }), 400


    if stock < 0:

        return jsonify({

            "message":
                "El stock no puede ser negativo."

        }), 400


    nombre = data.get(
        "nombre_producto",
        ""
    ).strip()

    descripcion = data.get(
        "descripcion_producto",
        ""
    ).strip()

    codigo = data.get(
        "codigo_barras",
        ""
    ).strip()

    marca = data.get(
        "marca_producto",
        ""
    ).strip()

    sku = data.get(
        "sku",
        ""
    ).strip()

    categoria = data.get(
        "categoria",
        ""
    ).strip()

    talla = data.get(
        "talla",
        ""
    ).strip()

    imagen = data.get(
        "imagen",
        ""
    ).strip()


    if nombre == "":

        return jsonify({

            "message":
                "El nombre del producto es obligatorio."

        }), 400


    if descripcion == "":

        return jsonify({

            "message":
                "La descripcion del producto es obligatoria."

        }), 400


    if codigo == "":

        return jsonify({

            "message":
                "El codigo de barras es obligatorio."

        }), 400


    if marca == "":

        return jsonify({

            "message":
                "La marca del producto es obligatoria."

        }), 400


    if sku == "":

        return jsonify({

            "message":
                "El SKU es obligatorio."

        }), 400


    if categoria == "":

        return jsonify({

            "message":
                "La categoria es obligatoria."

        }), 400


    if categoria.lower() in [
        "ropa",
        "zapatos"
    ]:

        if talla == "":

            return jsonify({

                "message":
                    "La talla es obligatoria para ropa y zapatos."

            }), 400


    elif categoria.lower() == "accesorios":

        talla = "N/A"


    if imagen == "":

        return jsonify({

            "message":
                "La URL de la imagen es obligatoria."

        }), 400


    producto = Productos(

        codigo_barras=codigo,

        nombre_producto=nombre,

        descripcion_producto=descripcion,

        talla=talla,

        precio_producto=precio,

        stock_producto=stock,

        marca_producto=marca,

        sku=sku,

        categoria=categoria,

        imagen=imagen

    )


    producto.save()


    return jsonify({

        "message":
            "Producto creado exitosamente.",

        "producto":
            producto.to_dict()

    }), 201


# ==========================================================
# ACTUALIZAR PRODUCTO
# PUT /productos/<id>
# SOLO ADMINISTRADORES
# ==========================================================

@Productos_bp.route(
    '/<int:id>',
    methods=['PUT']
)
@admin_required
def update_producto(id):

    producto = Productos.get_by_id(
        id
    )


    if not producto:

        return jsonify({

            "message":
                "Producto no encontrado."

        }), 404


    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Debe enviar los datos del producto."

        }), 400


    try:

        precio = float(
            data["precio_producto"]
        )

    except (
        ValueError,
        TypeError,
        KeyError
    ):

        return jsonify({

            "message":
                "El precio debe ser un numero valido."

        }), 400


    if precio <= 0:

        return jsonify({

            "message":
                "El precio debe ser mayor a cero."

        }), 400


    try:

        stock = int(
            data["stock_producto"]
        )

    except (
        ValueError,
        TypeError,
        KeyError
    ):

        return jsonify({

            "message":
                "El stock debe ser un numero valido."

        }), 400


    if stock < 0:

        return jsonify({

            "message":
                "El stock no puede ser negativo."

        }), 400


    producto.nombre_producto = data.get(
        "nombre_producto",
        ""
    ).strip()

    producto.codigo_barras = data.get(
        "codigo_barras",
        ""
    ).strip()

    producto.descripcion_producto = data.get(
        "descripcion_producto",
        ""
    ).strip()

    producto.talla = data.get(
        "talla",
        ""
    ).strip()

    producto.precio_producto = precio

    producto.stock_producto = stock

    producto.marca_producto = data.get(
        "marca_producto",
        ""
    ).strip()

    producto.sku = data.get(
        "sku",
        ""
    ).strip()

    producto.categoria = data.get(
        "categoria",
        ""
    ).strip()

    producto.imagen = data.get(
        "imagen",
        ""
    ).strip()

    producto.activo = True


    if producto.nombre_producto == "":

        return jsonify({

            "message":
                "El nombre del producto es obligatorio."

        }), 400


    if producto.descripcion_producto == "":

        return jsonify({

            "message":
                "La descripcion del producto es obligatoria."

        }), 400


    if producto.codigo_barras == "":

        return jsonify({

            "message":
                "El codigo de barras es obligatorio."

        }), 400


    if producto.marca_producto == "":

        return jsonify({

            "message":
                "La marca del producto es obligatoria."

        }), 400


    if producto.sku == "":

        return jsonify({

            "message":
                "El SKU es obligatorio."

        }), 400


    if producto.categoria == "":

        return jsonify({

            "message":
                "La categoria es obligatoria."

        }), 400


    if producto.categoria.lower() in [
        "ropa",
        "zapatos"
    ]:

        if producto.talla == "":

            return jsonify({

                "message":
                    "La talla es obligatoria para ropa y zapatos."

            }), 400


    elif producto.categoria.lower() == "accesorios":

        producto.talla = "N/A"


    if producto.imagen == "":

        return jsonify({

            "message":
                "La URL de la imagen es obligatoria."

        }), 400


    producto.save()


    return jsonify({

        "message":
            "Producto actualizado exitosamente.",

        "producto":
            producto.to_dict()

    }), 200


# ==========================================================
# ELIMINAR PRODUCTO
# DELETE /productos/<id>
# SOLO ADMINISTRADORES
# ==========================================================

@Productos_bp.route(
    '/<int:id>',
    methods=['DELETE']
)
@admin_required
def delete_producto(id):

    producto = Productos.get_by_id(
        id
    )


    if not producto:

        return jsonify({

            "message":
                "Producto no encontrado."

        }), 404


    producto.delete()


    return jsonify({

        "message":
            "Producto eliminado exitosamente."

    }), 200