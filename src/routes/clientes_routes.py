from flask import Blueprint, request, jsonify
from src.models.clientes import Cliente

from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from src.utils.decorators import admin_required


Clientes_bp = Blueprint(
    'Clientes',
    __name__
)


# ==========================================================
# OBTENER TODOS LOS CLIENTES
# ==========================================================

@Clientes_bp.route('/', methods=['GET'])
@admin_required
def get_clientes():

    page = request.args.get(
        'page',
        1,
        type=int
    )

    per_page = request.args.get(
        'per_page',
        10,
        type=int
    )

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

    total_pages = (
        total + per_page - 1
    ) // per_page

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


# ==========================================================
# OBTENER CLIENTE POR ID
# ==========================================================

@Clientes_bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_cliente(id):

    cliente = Cliente.get_by_id(id)

    if cliente:

        return jsonify(
            cliente.to_dict()
        ), 200

    return jsonify({
        'message': 'Cliente no encontrado'
    }), 404


# ==========================================================
# CREAR CLIENTE
# ==========================================================

@Clientes_bp.route('/', methods=['POST'])
def create_clientes():

    data = request.get_json()

    if not data:

        return jsonify({
            'message': 'Debe enviar información'
        }), 400

    # ======================================================
    # OBTENER DATOS
    # ======================================================

    nombre = data.get('nombre_cliente')
    nacimiento = data.get('nacimiento_cliente')
    numero = data.get('numero_cliente')
    direccion = data.get('direccion_cliente')
    email = data.get('email_cliente')
    password = data.get('password')

    # ======================================================
    # VALIDACIONES
    # ======================================================

    if not nombre:

        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if not nacimiento:

        return jsonify({
            'message': 'La fecha de nacimiento es obligatoria'
        }), 400

    if not direccion:

        return jsonify({
            'message': 'La dirección es obligatoria'
        }), 400

    if not numero:

        return jsonify({
            'message': 'El número de cliente es obligatorio'
        }), 400

    if not email:

        return jsonify({
            'message': 'El email es obligatorio'
        }), 400

    if not password:

        return jsonify({
            'message': 'La contraseña es obligatoria'
        }), 400

    # ======================================================
    # VALIDAR NÚMERO
    # ======================================================

    try:

        float(numero)

    except (ValueError, TypeError):

        return jsonify({
            'message': 'El número debe ser numérico'
        }), 400

    # ======================================================
    # VALIDAR EMAIL EXISTENTE
    # ======================================================

    cliente_existente = Cliente.get_by_email(email)

    if cliente_existente:

        return jsonify({
            'message': 'El email ya está registrado'
        }), 409

    # ======================================================
    # CREAR CLIENTE
    # ======================================================

    cliente = Cliente(

        nombre_cliente=nombre,

        nacimiento_cliente=nacimiento,

        numero_cliente=numero,

        direccion_cliente=direccion,

        email_cliente=email,

        password=generate_password_hash(password)

    )

    # ======================================================
    # ESTADO
    # ======================================================

    cliente.estado_cliente = "Activo"

    try:

        cliente.save()

    except Exception as e:

        return jsonify({
            'message': 'No se pudo crear el cliente',
            'error': str(e)
        }), 500

    return jsonify({

        'message': 'Cliente creado exitosamente',

        'cliente': cliente.to_dict()

    }), 201


@Clientes_bp.route('/<int:id>/estado', methods=['PUT'])
@admin_required
def cambiar_estado_cliente(id):

    cliente = Cliente.get_by_id(id)

    if not cliente:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Debe enviar información'
        }), 400

    estado = data.get('estado_cliente')

    if not estado:
        return jsonify({
            'message': 'El estado_cliente es obligatorio'
        }), 400

    if estado not in ['Activo', 'Inactivo']:
        return jsonify({
            'message': 'El estado debe ser Activo o Inactivo'
        }), 400

    cliente.estado_cliente = estado

    try:

        cliente.save()

    except Exception as e:

        return jsonify({
            'message': 'No se pudo actualizar el estado del cliente',
            'error': str(e)
        }), 500

    return jsonify({

        'message': f'Cliente {estado.lower()} correctamente',

        'cliente': cliente.to_dict()

    }), 200

# ==========================================================
# ACTUALIZAR CLIENTE - ADMINISTRADOR
# ==========================================================

@Clientes_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_Clientes(id):

    cliente = Cliente.get_by_id(id)

    if not cliente:

        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            'message': 'Debe enviar información'
        }), 400

    # ======================================================
    # DATOS
    # ======================================================

    nombre = data.get(
        'nombre_cliente',
        cliente.nombre_cliente
    )

    nacimiento = data.get(
        'nacimiento_cliente',
        cliente.nacimiento_cliente
    )

    direccion = data.get(
        'direccion_cliente',
        cliente.direccion_cliente
    )

    numero = data.get(
        'numero_cliente',
        cliente.numero_cliente
    )

    email = data.get(
        'email_cliente',
        cliente.email_cliente
    )

    # ======================================================
    # VALIDACIONES
    # ======================================================

    if not nombre:

        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if not nacimiento:

        return jsonify({
            'message': 'La fecha es obligatoria'
        }), 400

    if not direccion:

        return jsonify({
            'message': 'La dirección es obligatoria'
        }), 400

    if not numero:

        return jsonify({
            'message': 'El número de cliente es obligatorio'
        }), 400

    if not email:

        return jsonify({
            'message': 'El email es obligatorio'
        }), 400

    # ======================================================
    # VALIDAR NÚMERO
    # ======================================================

    try:

        float(numero)

    except (ValueError, TypeError):

        return jsonify({
            'message': 'El número debe ser numérico'
        }), 400

    # ======================================================
    # VALIDAR EMAIL
    # ======================================================

    if email != cliente.email_cliente:

        cliente_existente = Cliente.get_by_email(email)

        if cliente_existente:

            return jsonify({
                'message': 'El email ya está registrado'
            }), 409

    # ======================================================
    # ACTUALIZAR DATOS
    # ======================================================

    cliente.nombre_cliente = nombre

    cliente.nacimiento_cliente = nacimiento

    cliente.direccion_cliente = direccion

    cliente.numero_cliente = numero

    cliente.email_cliente = email

    # ======================================================
    # ESTADO DEL CLIENTE
    # ======================================================

    if 'estado_cliente' in data:

        estado = data['estado_cliente']

        if estado not in ['Activo', 'Inactivo']:

            return jsonify({
                'message': 'El estado debe ser Activo o Inactivo'
            }), 400

        cliente.estado_cliente = estado

    # ======================================================
    # CONTRASEÑA OPCIONAL
    # ======================================================

    if 'password' in data and data['password']:

        cliente.password = generate_password_hash(
            data['password']
        )

    # ======================================================
    # GUARDAR
    # ======================================================

    try:

        cliente.save()

    except Exception as e:

        return jsonify({
            'message': 'No se pudo actualizar el cliente',
            'error': str(e)
        }), 500

    return jsonify({

        'message': 'Cliente actualizado exitosamente',

        'cliente': cliente.to_dict()

    }), 200


# ==========================================================
# OBTENER MI PERFIL
# ==========================================================

@Clientes_bp.route(
    "/perfil",
    methods=["GET"]
)
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

    cliente = Cliente.get_by_id(
        id_cliente
    )

    if cliente is None:

        return jsonify({
            "message": "Cliente no encontrado."
        }), 404

    return jsonify(
        cliente.to_dict()
    ), 200


# ==========================================================
# ACTUALIZAR MI PERFIL
# ==========================================================

@Clientes_bp.route(
    "/perfil",
    methods=["PUT"]
)
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

    cliente = Cliente.get_by_id(
        id_cliente
    )

    if cliente is None:

        return jsonify({
            "message": "Cliente no encontrado."
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Debe enviar información."
        }), 400

    # ======================================================
    # ACTUALIZAR CAMPOS PERMITIDOS
    # ======================================================

    if "nombre" in data:

        cliente.nombre_cliente = data["nombre"]

    if "email" in data:

        nuevo_email = data["email"]

        if nuevo_email != cliente.email_cliente:

            cliente_existente = Cliente.get_by_email(
                nuevo_email
            )

            if cliente_existente:

                return jsonify({
                    "message": "El email ya está registrado."
                }), 409

        cliente.email_cliente = nuevo_email

    if "telefono" in data:

        cliente.numero_cliente = data["telefono"]

    if "direccion" in data:

        cliente.direccion_cliente = data["direccion"]

    # ======================================================
    # VALIDACIONES
    # ======================================================

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

    # ======================================================
    # GUARDAR
    # ======================================================

    try:

        cliente.save()

    except Exception as e:

        return jsonify({
            "message": "No se pudo actualizar el perfil.",
            "error": str(e)
        }), 500

    return jsonify({

        "message": "Perfil actualizado correctamente.",

        "cliente": cliente.to_dict()

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

    cliente = Cliente.get_by_id(
        id_cliente
    )

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

        print(
            "CONTRASEÑA ACTUAL INCORRECTA"
        )

        return jsonify({
            "message":
                "La contraseña actual es incorrecta."
        }), 401

    cliente.password = generate_password_hash(
        password_nueva
    )

    try:

        cliente.save()

    except Exception as e:

        return jsonify({
            "message":
                "No se pudo actualizar la contraseña.",
            "error": str(e)
        }), 500

    print(
        "CONTRASEÑA ACTUALIZADA CORRECTAMENTE"
    )

    return jsonify({

        "message":
            "Contraseña actualizada correctamente."

    }), 200