from flask import Blueprint, request, jsonify
from src.models.administrador import Administrador

Administradores_bp = Blueprint('Administrador', __name__)

@Administradores_bp.route('/', methods=['GET'])
def get_Administradores():
    administradores = Administrador.get()
    Administradores_list = []
    for administrador in administradores:
        Administradores_list.append({
            'id_administrador': administrador.id_administrador,
            'nombre_administrador': administrador.nombre_administrador,
            'rol_administrador': administrador.rol_administrador,
            'telefono_administrador': administrador.telefono_administrador,
            'estado_administrador': administrador.estado_administrador,
            'email_administrador': administrador.email_administrador,
            'password_administrador': administrador.password_administrador
        })
    return jsonify(Administradores_list), 200

@Administradores_bp.route('/<int:id>', methods=['GET'])
def get_Administrador(id):
    administrador =  Administrador.get_by_id(id)
    if administrador:
        administrador_data = {
            'id_administrador': administrador.id_administrador,
            'nombre_administrador': administrador.nombre_administrador,
            'rol_administrador': administrador.rol_administrador,
            'telefono_administrador': administrador.telefono_administrador,
            'estado_administrador': administrador.estado_administrador,
            'email_administrador': administrador.email_administrador,
            'password_administrador': administrador.password_administrador
        }
        return jsonify(administrador_data), 200
    else:
        return jsonify({'message': 'Administrador  no encontrado'}), 404


@Administradores_bp.route('/', methods=['POST'])
def create_Administrador():
    data = request.get_json()
    administrador = Administrador(
        nombre_administrador=data['nombre_administrador'],
        rol_administrador=data['rol_administrador'],
        estado_administrador=data['estado_administrador'],
        email_administrador=data['email_administrador'],
        password_administrador=data['password_administrador'],
        telefono_administrador=data['telefono_administrador']
    )   
    try:
        ['telefono_administrador']
    except ValueError:
        return jsonify({'message': 'El número debe ser numérico'}), 400
    if administrador.nombre_administrador == '':
        return jsonify({'message': 'el nombre del administrador es obligatorio'}), 400
    
    if administrador.rol_administrador == '':
        return jsonify({'message':'el rol es obligatoria'}), 400

    if administrador.estado_administrador  == '':
        return jsonify({'message':'el estado del administrador es obligatorio'}), 400

    if administrador.telefono_administrador == '':
        return jsonify({'message':'el numero del administrador debe cumplir con las caracteristica de un numero '}), 400

    if administrador.email_administrador =='':
        return jsonify({'message':'el email es obligatorio'}), 400

    if administrador.password_administrador =='':
        return jsonify({'message':'la contraseña es obligatoria '}), 400

    administrador.save()
    return jsonify({'message':'adminisrador creado exitosamenete', 'administrador' :administrador.to_dict()}), 201

@Administradores_bp.route('/<int:id>', methods=['DELETE'])
def delete_administrador(id):
    administrador = Administrador.get_by_id(id)
    if administrador:
        administrador.delete()
        return jsonify({'message': 'administrador eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'administrador no encontrado'}), 404

@Administradores_bp.route('/<int:id>', methods=['PUT'])
def update_Administrador(id):
    administrador = Administrador.get_by_id(id)
    if administrador:
        data = request.get_json()
        id_administrador=data['id_administrador'],
        nombre_administrador=data['nombre_administrador'],
        rol_administrador=data['rol_administrador'],
        estado_administrador=data['estado_administrador'],
        email_administrador=data['email_administrador'],
        password_administrador=data['password_administrador']
        try:
            ['telefono_administrador']
        except ValueError:
            return jsonify({'message': 'El número debe ser numérico'}), 400
        if administrador.nombre_administrador == '':
            return jsonify({'message': 'el nombre del administrador es obligatorio'}), 400
    
        if administrador.rol_administrador == '':
            return jsonify({'message':'el rol es obligatoria'}), 400

        if administrador.estado_administrador  == '':
            return jsonify({'message':'el estado del administrador es obligatorio'}), 400

        if administrador.telefono_administrador == '':
            return jsonify({'message':'el numero del administrador debe cumplir con las caracteristica de un numero '}), 400

        if administrador.email_administrador =='':
            return jsonify({'message':'el email es obligatorio'}), 400

        if administrador.password_administrador =='':
            return jsonify({'message':'la contraseña es obligatoria '}), 400

        administrador.save()
        return jsonify({'message':'adminisrador actulizado exitosamenete', 'administrador' :administrador.to_dict()}), 201

    else:
        return jsonify({'message': 'administrador no encontrado'}), 404
