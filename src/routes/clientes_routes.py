from flask import Blueprint, request, jsonify
from src.models.clientes import Cliente

Clientes_bp = Blueprint('Clientes', __name__)

@Clientes_bp.route('/', methods=['GET'])
def get_clientes():
    clientes = Cliente.get()
    Clientes_list = []
    for cliente in clientes:
        Clientes_list.append({
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'nacimiento_cliente': cliente.nacimiento_cliente,
            'numero_cliente': cliente.numero_cliente,
            'direccion_cliente': cliente.direccion_cliente,
            'email_cliente': cliente.email_cliente
        })
    return jsonify(Clientes_list), 200

@Clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente =  Clientes.get_by_id(id)
    if cliente:
        cliente_data = {
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'nacimiento_cliente': cliente.nacimiento_cliente,
            'numero_cliente': cliente.numero_cliente,
            'direccion_cliente': cliente.direccion_cliente,
            'email_cliente': cliente.email_cliente
        }
        return jsonify(Clientes_data), 200
    else:
        return jsonify({'message': 'cliente no encontrado'}), 404


@Clientes_bp.route('/', methods=['POST'])
def create_clientes():
    data = request.get_json()
    cliente = Cliente(
        nombre_cliente=data['nombre_cliente'],
        nacimiento_cliente=data['nacimiento_cliente'],
        numero_cliente=data['numero_cliente'],
        direccion_cliente=data['direccion_cliente'],
        email_cliente=data['email_cliente'],
    )
    try:
        float(data['numero_cliente'])
    except ValueError:
        return jsonify({'message': 'El número debe ser numérico'}), 400
    if cliente.nombre_cliente == '':
        return jsonify({'message': 'el nombre del producto es obligatorio'}), 400
    
    if cliente.nacimiento_cliente == '':
        return jsonify({'message':'la fecha es obligatoria'}), 400

    if cliente.direccion_cliente  == '':
        return jsonify({'message':'el codigo debe ser unico para cada producto'}), 400

    if cliente.numero_cliente == '':
        return jsonify({'message':'el numero de cliente debe ser mayor a cero'}), 400

    if cliente.email_cliente =='':
        return jsonify({'message':'el email es obligatorio'}), 400

    cliente.save()
    return jsonify({'message':'Cliente creado exitosamenete', 'cliente' :cliente.to_dict()}), 201

@Clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.get_by_id(id)
    if cliente:
        cliente.delete()
        return jsonify({'message': 'cliente eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'cliente no encontrado'}), 404

@Clientes_bp.route('/<int:id>', methods=['PUT'])
def update_Clientes(id):
    cliente = Cliente.get_by_id(id)
    if cliente:
        data = request.get_json()
        cliente.nombre_cliente = data['nombre_cliente']
        cliente.nacimiento_cliente=data['nacimiento_cliente']
        cliente.direccion_cliente=data['direccion_cliente']
        cliente.numero_cliente=data['numero_cliente']
        cliente.email_cliente=data['email_cliente']
        cliente.activo = True
        try:
            float(data['numero_cliente'])
        except ValueError:
            return jsonify({'message': 'El número debe ser numérico'}), 400
        if cliente.nombre_cliente == '':
            return jsonify({'message': 'el nombre del producto es obligatorio'}), 400
    
        if cliente.nacimiento_cliente == '':
            return jsonify({'message':'la fecha es obligatoria'}), 400

        if cliente.direccion_cliente  == '':
            return jsonify({'message':'el codigo debe ser unico para cada producto'}), 400

        if cliente.numero_cliente == '':
            return jsonify({'message':'el numero de cliente debe ser mayor a cero'}), 400

        if cliente.email_cliente =='':
            return jsonify({'message':'el email es obligatorio'}), 400

        cliente.save()
        return jsonify({'message':'Cliente actulizado exitosamenete', 'cliente' :cliente.to_dict()}), 201

    else:
        return jsonify({'message': 'Producto no encontrado'}), 404
