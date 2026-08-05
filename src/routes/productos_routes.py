from flask import Blueprint, request, jsonify
from src.models.productos import Productos

Productos_bp = Blueprint('Productos', __name__)

@Productos_bp.route('/buscar', methods=['GET'])
def get_productos():

    buscar = request.args.get("buscar")
    categoria = request.args.get("categoria")
    ordenar = request.args.get("ordenar")

    pagina = int(request.args.get("pagina", 1))
    por_pagina = int(request.args.get("por_pagina", 12))

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
            "id_producto": producto.id_producto,
            "nombre_producto": producto.nombre_producto,
            "descripcion_producto": producto.descripcion_producto,
            "talla": producto.talla,
            "precio_producto": float(producto.precio_producto),
            "stock_producto": producto.stock_producto,
            "marca_producto": producto.marca_producto,
            "sku": producto.sku,
            "categoria": producto.categoria,
            "imagen": producto.imagen
        })

    return jsonify({

        "productos": productos,

        "pagina": resultado["pagina"],

        "por_pagina": resultado["por_pagina"],

        "total_productos": resultado["total_productos"],

        "total_paginas": resultado["total_paginas"]

    }), 200


@Productos_bp.route('/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        producto_data = {
            'id_producto': producto.id_producto,
            'nombre_producto': producto.nombre_producto,
            'descripcion_producto': producto.descripcion_producto,
            'talla': producto.talla,
            'precio_producto': producto.precio_producto,
            'stock_producto': producto.stock_producto,
            'marca_producto': producto.marca_producto,
            'sku': producto.sku,
            'categoria': producto.categoria,
            'imagen': producto.imagen
        }
        return jsonify(producto_data), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404


@Productos_bp.route('/', methods=['POST'])
def create_producto():
    data = request.get_json()
    producto = Productos(
        codigo_barras=data['codigo_barras'],
        nombre_producto=data['nombre_producto'],
        descripcion_producto=data['descripcion_producto'],
        talla=data['talla'],
        precio_producto=data['precio_producto'],
        stock_producto=data['stock_producto'],
        marca_producto=data['marca_producto'],
        sku=data['sku'],
        categoria=data['categoria'],
        imagen=data['imagen']
    )
    try:
        float(producto.precio_producto)
    except ValueError:
        return jsonify({'message': 'El precio debe ser un numero valido'}), 400

    if producto.nombre_producto == '':
        return jsonify({'message': 'el nombre del producto es obligatorio'}), 400
    
    if producto.descripcion_producto == '':
        return jsonify({'message':'la descripcion del producto es obligatoria'}), 400

    if producto.codigo_barras == '':
        return jsonify({'message':'el codigo debe ser unico para cada producto'}), 400

    if producto.precio_producto <= 0:
        return jsonify({'message':'el precio debe ser mayor a cero'}), 400

    if producto.stock_producto < 0:
        return jsonify({'message':'El estcok no puede ser negativo'}), 400

    if producto.marca_producto == '':
        return jsonify({'message':'La marca del prodcuto es obligatoria'}), 400

    if producto.categoria.lower() in ["ropa", "zapatos"]:

        if producto.talla.strip() == "":
            return jsonify({
                "message": "La talla es obligatoria para ropa y zapatos."
        }), 400

    elif producto.categoria.lower() == "accesorios":

        producto.talla = "N/A"
    if producto.sku =='':
        return jsonify({'message':'el identificador del producto debe ser unico'}), 400

    
    if producto.categoria == '':
        return jsonify({'message': 'La categoria es obligatoria'}), 400 

    if producto.imagen == '':
        return jsonify({'message': 'La url de la imagen es obligatoria'}), 400 
    
    


    producto.save()
    return jsonify({'message':'Producto creado exitosamenete', 'producto' :producto.to_dict()}), 201

@Productos_bp.route('/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        producto.delete()
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404

@Productos_bp.route('/<int:id>', methods=['PUT'])
def update_Productos(id):
    producto = Productos.get_by_id(id)
    if producto:
        data = request.get_json()
        producto.nombre_producto = data['nombre_producto']
        producto.codigo_barras=data['codigo_barras']
        producto.descripcion_producto=data['descripcion_producto']
        producto.talla=data['talla']
        producto.precio_producto=data['precio_producto']
        producto.stock_producto=data['stock_producto']
        producto.marca_producto=data['marca_producto']
        producto.sku=data['sku']
        producto.categoria=data['categoria']
        producto.imagen=data['imagen']
        producto.activo = True
        try:
            producto.precio_producto = float(producto.precio_producto)
        except ValueError:
            return jsonify({'message': 'El precio debe ser un numero valido'}), 400

        if producto.nombre_producto == '':
            return jsonify({'message': 'el nombre del producto es obligatorio'}), 400
    
        if producto.descripcion_producto == '':
            return jsonify({'message':'la descripcion del producto es obligatoria'}), 400

        if producto.codigo_barras == '':
            return jsonify({'message':'el codigo debe ser unico para cada producto'}), 400

        if producto.precio_producto <= 0:
            return jsonify({'message':'el precio debe ser mayor a cero'}), 400

        if producto.stock_producto < 0:
            return jsonify({'message':'El estcok no puede ser negativo'}), 400

        if producto.marca_producto == '':
            return jsonify({'message':'La marca del prodcuto es obligatoria'}), 400

        if producto.talla == '':
            return jsonify({'message':'las tallas disponibles son obligatorias' }), 400

        if producto.sku =='':
            return jsonify({'message':'el identificador del producto debe ser unico'}), 400

    
        if producto.categoria == '':
            return jsonify({'message': 'La categoria es obligatoria'}), 400
        
        if producto.imagen == '':
            return jsonify({'message': 'La url de la imagen es obligatoria'}), 400 
    
    
    


        producto.save()
        return jsonify({'message':'Producto fue Actulizado  exitosamenete', 'producto' :producto.to_dict()}), 201
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404
