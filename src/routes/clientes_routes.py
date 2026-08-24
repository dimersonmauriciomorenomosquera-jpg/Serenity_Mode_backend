from flask import Blueprint, request, jsonify
from src.models.clientes import Cliente

from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from src.utils.decorators import admin_required

Clientes_bp = Blueprint('Clientes', __name__)


@Clientes_bp.route('/', methods=['GET'])
@admin_required
def get_clientes():

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

    clientes, total = Cliente.get(
        page=page,
        per_page=per_page
    )

    total_pages = (total + per_page - 1) // per_page

    clientes_list = [
        cliente.to_dict()
        for cliente in clientes
    ]

    return jsonify({
        'data': clientes_list,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': total_pages
        }
    }), 200


@Clientes_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_cliente(id):

    cliente = Cliente.get_by_id(id)

    if cliente:

        cliente_data = {
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'nacimiento_cliente': cliente.nacimiento_cliente,
            'numero_cliente': cliente.numero_cliente,
            'direccion_cliente': cliente.direccion_cliente,
            'email_cliente': cliente.email_cliente
        }

        return jsonify(cliente_data), 200

    return jsonify({
        'message': 'Cliente no encontrado'
    }), 404


@Clientes_bp.route('/', methods=['POST'])
def create_clientes():

    data = request.get_json()

    cliente = Cliente(
        nombre_cliente=data['nombre_cliente'],
        nacimiento_cliente=data['nacimiento_cliente'],
        numero_cliente=data['numero_cliente'],
        direccion_cliente=data['direccion_cliente'],
        email_cliente=data['email_cliente'],
        password=data["password"]
    )

    try:
        float(data['numero_cliente'])

    except ValueError:

        return jsonify({
            'message': 'El número debe ser numérico'
        }), 400

    if cliente.nombre_cliente == '':

        return jsonify({
            'message': 'el nombre del producto es obligatorio'
        }), 400

    if cliente.nacimiento_cliente == '':

        return jsonify({
            'message':'la fecha es obligatoria'
        }), 400

    if cliente.direccion_cliente == '':

        return jsonify({
            'message':'el codigo debe ser unico para cada producto'
        }), 400

    if cliente.numero_cliente == '':

        return jsonify({
            'message':'el numero de cliente debe ser mayor a cero'
        }), 400

    if cliente.email_cliente == '':

        return jsonify({
            'message':'el email es obligatorio'
        }), 400

    cliente.save()

    return jsonify({
        'message':'Cliente creado exitosamenete',
        'cliente': cliente.to_dict()
    }), 201


@Clientes_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_cliente(id):

    cliente = Cliente.get_by_id(id)

    if cliente:

        cliente.delete()

        return jsonify({
            'message': 'cliente eliminado exitosamente'
        }), 200

    else:

        return jsonify({
            'message': 'cliente no encontrado'
        }), 404


@Clientes_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_Clientes(id):

    cliente = Cliente.get_by_id(id)

    if cliente:

        data = request.get_json()

        cliente.nombre_cliente = data['nombre_cliente']
        cliente.nacimiento_cliente = data['nacimiento_cliente']
        cliente.direccion_cliente = data['direccion_cliente']
        cliente.numero_cliente = data['numero_cliente']
        cliente.email_cliente = data['email_cliente']
        cliente.password = data["password"]
        cliente.activo = True

        try:

            float(data['numero_cliente'])

        except ValueError:

            return jsonify({
                'message': 'El número debe ser numérico'
            }), 400

        if cliente.nombre_cliente == '':

            return jsonify({
                'message': 'el nombre del producto es obligatorio'
            }), 400

        if cliente.nacimiento_cliente == '':

            return jsonify({
                'message':'la fecha es obligatoria'
            }), 400

        if cliente.direccion_cliente == '':

            return jsonify({
                'message':'el codigo debe ser unico para cada producto'
            }), 400

        if cliente.numero_cliente == '':

            return jsonify({
                'message':'el numero de cliente debe ser mayor a cero'
            }), 400

        if cliente.email_cliente == '':

            return jsonify({
                'message':'el email es obligatorio'
            }), 400

        cliente.save()

        return jsonify({
            'message':'Cliente actulizado exitosamenete',
            'cliente': cliente.to_dict()
        }), 201

    else:

        return jsonify({
            'message': 'Producto no encontrado'
        }), 404


# ==========================================================
# OBTENER MI PERFIL
# ==========================================================

@Clientes_bp.route("/perfil", methods=["GET"])
@jwt_required()
def get_perfil():

    print("======================================")
    print("OBTENER PERFIL")
    print("======================================")

    id_cliente = get_jwt_identity()

    print(
        "ID CLIENTE DESDE JWT:",
        id_cliente
    )

    cliente = Cliente.get_by_id(id_cliente)

    if cliente is None:

        return jsonify({
            "message": "Cliente no encontrado."
        }), 404

    return jsonify({

        "id_cliente": cliente.id_cliente,

        "nombre_cliente": cliente.nombre_cliente,

        "nacimiento_cliente": cliente.nacimiento_cliente,

        "numero_cliente": cliente.numero_cliente,

        "direccion_cliente": cliente.direccion_cliente,

        "email_cliente": cliente.email_cliente

    }), 200


# ==========================================================
# ACTUALIZAR MI PERFIL
# ==========================================================

@Clientes_bp.route("/perfil", methods=["PUT"])
@jwt_required()
def actualizar_perfil():

    print("======================================")
    print("ACTUALIZAR PERFIL")
    print("======================================")

    id_cliente = get_jwt_identity()

    print(
        "ID CLIENTE DESDE JWT:",
        id_cliente
    )

    cliente = Cliente.get_by_id(id_cliente)

    if cliente is None:

        return jsonify({
            "message": "Cliente no encontrado."
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Debe enviar información."
        }), 400

    if "nombre" in data:

        cliente.nombre_cliente = data["nombre"]

    if "email" in data:

        cliente.email_cliente = data["email"]

    if "telefono" in data:

        cliente.numero_cliente = data["telefono"]

    if "direccion" in data:

        cliente.direccion_cliente = data["direccion"]

    if not cliente.nombre_cliente:

        return jsonify({
            "message": "El nombre es obligatorio."
        }), 400

    if not cliente.email_cliente:

        return jsonify({
            "message": "El email es obligatorio."
        }), 400

    if not cliente.numero_cliente:

        return jsonify({
            "message": "El número de teléfono es obligatorio."
        }), 400

    if not cliente.direccion_cliente:

        return jsonify({
            "message": "La dirección es obligatoria."
        }), 400

    cliente.save()

    return jsonify({

        "message": "Perfil actualizado correctamente.",

        "cliente": {

            "id_cliente": cliente.id_cliente,

            "nombre_cliente": cliente.nombre_cliente,

            "nacimiento_cliente": cliente.nacimiento_cliente,

            "numero_cliente": cliente.numero_cliente,

            "direccion_cliente": cliente.direccion_cliente,

            "email_cliente": cliente.email_cliente

        }

    }), 200


# ==========================================================
# CAMBIAR CONTRASEÑA
# ==========================================================

@Clientes_bp.route(
    "/cambiar-password",
    methods=["PUT"]
)
@jwt_required()
def cambiar_password():

    print("======================================")
    print("CAMBIAR CONTRASEÑA")
    print("======================================")

    id_cliente = get_jwt_identity()

    print(
        "ID CLIENTE DESDE JWT:",
        id_cliente
    )

    cliente = Cliente.get_by_id(id_cliente)

    if cliente is None:

        return jsonify({
            "message": "Cliente no encontrado."
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Debe enviar información."
        }), 400

    password_actual = data.get(
        "password_actual"
    )

    password_nueva = data.get(
        "password_nueva"
    )

    if not password_actual:

        return jsonify({
            "message":
                "Debes ingresar tu contraseña actual."
        }), 400

    if not password_nueva:

        return jsonify({
            "message":
                "Debes ingresar la nueva contraseña."
        }), 400

    if not check_password_hash(
        cliente.password,
        password_actual
    ):

        print("CONTRASEÑA ACTUAL INCORRECTA")

        return jsonify({
            "message":
                "La contraseña actual es incorrecta."
        }), 401

    cliente.password = generate_password_hash(
        password_nueva
    )

    cliente.save()

    print("CONTRASEÑA ACTUALIZADA CORRECTAMENTE")

    return jsonify({

        "message":
            "Contraseña actualizada correctamente."

    }), 200