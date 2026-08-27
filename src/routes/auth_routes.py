from flask import Blueprint, request, jsonify

from src.models.administrador import Administrador
from src.models.clientes import Cliente

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)


Auth_bp = Blueprint(
    "auth",
    __name__
)


# ==========================================================
# INFORMACIÓN DEL USUARIO
# ==========================================================

@Auth_bp.route(
    "/usuario",
    methods=["GET"]
)
@jwt_required()
def informacion_usuario():

    id_cliente = get_jwt_identity()

    cliente = Cliente.get_by_id(
        id_cliente
    )

    if cliente is None:

        return jsonify({

            "message":
                "Usuario no encontrado."

        }), 404


    return jsonify({

        "id_cliente":
            cliente.id_cliente,

        "nombre":
            cliente.nombre_cliente,

        "direccion":
            cliente.direccion_cliente,

        "nacimiento":
            cliente.nacimiento_cliente,

        "email":
            cliente.email_cliente,

        "numero":
            cliente.numero_cliente

    }), 200


# ==========================================================
# REGISTRO DE USUARIO
# ==========================================================

@Auth_bp.route(
    "/registro",
    methods=["POST"]
)
def registro():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Debe enviar información."

        }), 400


    campos = [

        "nombre_cliente",
        "direccion_cliente",
        "nacimiento_cliente",
        "email_cliente",
        "numero_cliente",
        "password"

    ]


    for campo in campos:

        if campo not in data:

            return jsonify({

                "message":
                    f"El campo {campo} es obligatorio."

            }), 400


    # ======================================================
    # VERIFICAR CORREO
    # ======================================================

    usuario = Cliente.get_by_email(
        data["email_cliente"]
    )


    if usuario:

        return jsonify({

            "message":
                "El correo ya está registrado."

        }), 400


    # ======================================================
    # HASHEAR CONTRASEÑA
    # ======================================================

    password_hash = generate_password_hash(
        data["password"]
    )


    # ======================================================
    # CREAR CLIENTE
    # ======================================================

    cliente = Cliente(

        nombre_cliente=
            data["nombre_cliente"],

        direccion_cliente=
            data["direccion_cliente"],

        nacimiento_cliente=
            data["nacimiento_cliente"],

        email_cliente=
            data["email_cliente"],

        numero_cliente=
            data["numero_cliente"],

        password=
            password_hash

    )


    cliente.save()


    return jsonify({

        "message":
            "Usuario registrado correctamente.",

        "usuario":
            cliente.to_dict()

    }), 201


# ==========================================================
# LOGIN
# CLIENTE + ADMINISTRADOR
# ==========================================================

@Auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Debe enviar información."

        }), 400


    # ======================================================
    # DATOS DEL LOGIN
    # ======================================================

    email = data.get(
        "email"
    )

    password = data.get(
        "password"
    )


    if not email:

        return jsonify({

            "message":
                "El correo es obligatorio."

        }), 400


    if not password:

        return jsonify({

            "message":
                "La contraseña es obligatoria."

        }), 400


    # ======================================================
    # PRIMERO BUSCAR ADMINISTRADOR
    # ======================================================

    administrador = Administrador.get_by_email(
        email
    )


    if administrador:

        # ==============================================
        # VERIFICAR ESTADO
        # ==============================================

        if administrador.estado_administrador != "Activo":

            return jsonify({

                "message":
                    "El administrador está inactivo."

            }), 403


        # ==============================================
        # VERIFICAR CONTRASEÑA
        # ==============================================

        if not check_password_hash(

            administrador.password_administrador,

            password

        ):

            return jsonify({

                "message":
                    "Contraseña incorrecta."

            }), 401


        # ==============================================
        # CREAR TOKEN ADMINISTRADOR
        # ==============================================

        token = create_access_token(

            identity=
                str(
                    administrador.id_administrador
                ),

            additional_claims={

                "tipo":
                    "administrador",

                "rol":
                    administrador.rol_administrador

            }

        )


        # ==============================================
        # RESPUESTA ADMINISTRADOR
        # ==============================================

        return jsonify({

            "message":
                "Inicio de sesión de administrador exitoso.",

            "token":
                token,

            "tipo":
                "administrador",

            "administrador": {

                "id_administrador":
                    administrador.id_administrador,

                "nombre":
                    administrador.nombre_administrador,

                "email":
                    administrador.email_administrador,

                "rol":
                    administrador.rol_administrador

            }

        }), 200


    # ======================================================
    # SI NO ES ADMINISTRADOR → BUSCAR CLIENTE
    # ======================================================

    cliente = Cliente.get_by_email(
        email
    )


    if cliente is None:

        return jsonify({

            "message":
                "Usuario no encontrado."

        }), 404


    # ======================================================
    # VERIFICAR CONTRASEÑA CLIENTE
    # ======================================================

    if not check_password_hash(

        cliente.password,

        password

    ):

        return jsonify({

            "message":
                "Contraseña incorrecta."

        }), 401


    # ======================================================
    # CREAR TOKEN CLIENTE
    # ======================================================

    token = create_access_token(

        identity=
            str(
                cliente.id_cliente
            ),

        additional_claims={

            "tipo":
                "cliente"

        }

    )


    # ======================================================
    # RESPUESTA CLIENTE
    # ======================================================

    return jsonify({

        "message":
            "Inicio de sesión exitoso.",

        "token":
            token,

        "tipo":
            "cliente",

        "usuario": {

            "id_cliente":
                cliente.id_cliente,

            "nombre":
                cliente.nombre_cliente,

            "email":
                cliente.email_cliente

        }

    }), 200


# ==========================================================
# LOGIN ADMINISTRADOR
# ==========================================================
# Se conserva esta ruta por compatibilidad.
# Si alguna parte de tu proyecto todavía la utiliza,
# seguirá funcionando.
# ==========================================================

@Auth_bp.route(
    "/admin/login",
    methods=["POST"]
)
def login_admin():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Debe enviar información."

        }), 400


    email = data.get(
        "email_administrador"
    )

    password = data.get(
        "password_administrador"
    )


    if not email:

        return jsonify({

            "message":
                "El correo es obligatorio."

        }), 400


    if not password:

        return jsonify({

            "message":
                "La contraseña es obligatoria."

        }), 400


    administrador = Administrador.get_by_email(
        email
    )


    if administrador is None:

        return jsonify({

            "message":
                "Administrador no encontrado."

        }), 404


    if administrador.estado_administrador != "Activo":

        return jsonify({

            "message":
                "El administrador está inactivo."

        }), 403


    if not check_password_hash(

        administrador.password_administrador,

        password

    ):

        return jsonify({

            "message":
                "Contraseña incorrecta."

        }), 401


    token = create_access_token(

        identity=
            str(
                administrador.id_administrador
            ),

        additional_claims={

            "tipo":
                "administrador",

            "rol":
                administrador.rol_administrador

        }

    )


    return jsonify({

        "message":
            "Inicio de sesión de administrador exitoso.",

        "token":
            token,

        "tipo":
            "administrador",

        "administrador": {

            "id_administrador":
                administrador.id_administrador,

            "nombre":
                administrador.nombre_administrador,

            "email":
                administrador.email_administrador,

            "rol":
                administrador.rol_administrador

        }

    }), 200


# ==========================================================
# VERIFICAR CORREO PARA RECUPERACIÓN
# ==========================================================

@Auth_bp.route(
    "/recuperar/verificar",
    methods=["POST"]
)
def verificar_correo_recuperacion():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Debe enviar información."

        }), 400


    email = data.get(
        "email_cliente"
    )


    if not email:

        return jsonify({

            "message":
                "El correo es obligatorio."

        }), 400


    cliente = Cliente.get_by_email(
        email
    )


    if cliente is None:

        return jsonify({

            "message":
                "No existe una cuenta asociada a este correo."

        }), 404


    return jsonify({

        "message":
            "Correo verificado correctamente.",

        "usuario": {

            "id_cliente":
                cliente.id_cliente,

            "nombre":
                cliente.nombre_cliente,

            "email":
                cliente.email_cliente

        }

    }), 200


# ==========================================================
# RESTABLECER CONTRASEÑA
# ==========================================================

@Auth_bp.route(
    "/recuperar/restablecer",
    methods=["PUT"]
)
def restablecer_password():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "Debe enviar información."

        }), 400


    email = data.get(
        "email_cliente"
    )

    nueva_password = data.get(
        "nueva_password"
    )


    if not email:

        return jsonify({

            "message":
                "El correo es obligatorio."

        }), 400


    if not nueva_password:

        return jsonify({

            "message":
                "La nueva contraseña es obligatoria."

        }), 400


    if len(nueva_password) < 8:

        return jsonify({

            "message":
                "La contraseña debe tener mínimo 8 caracteres."

        }), 400


    cliente = Cliente.get_by_email(
        email
    )


    if cliente is None:

        return jsonify({

            "message":
                "Usuario no encontrado."

        }), 404


    cliente.password = generate_password_hash(
        nueva_password
    )


    cliente.save()


    return jsonify({

        "message":
            "Contraseña actualizada correctamente."

    }), 200