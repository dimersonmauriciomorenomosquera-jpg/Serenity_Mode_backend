from flask import Blueprint, request, jsonify

from src.models.clientes import Cliente

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import create_access_token


Auth_bp = Blueprint("auth", __name__)


# =========================================
# REGISTRO DE USUARIO
# =========================================

@Auth_bp.route("/registro", methods=["POST"])
def registro():

    data = request.get_json()


    if not data:

        return jsonify({
            "message": "Debe enviar información."
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

                "message": f"El campo {campo} es obligatorio."

            }),400



    # Verificar si el correo ya existe

    usuario = Cliente.get_by_email(
        data["email_cliente"]
    )


    if usuario:

        return jsonify({

            "message": "El correo ya está registrado."

        }),400



    # Hashear contraseña

    password_hash = generate_password_hash(
        data["password"]
    )


    cliente = Cliente(

        nombre_cliente=data["nombre_cliente"],
        direccion_cliente=data["direccion_cliente"],
        nacimiento_cliente=data["nacimiento_cliente"],
        email_cliente=data["email_cliente"],
        numero_cliente=data["numero_cliente"],
        password=password_hash

    )


    cliente.save()


    return jsonify({

        "message": "Usuario registrado correctamente.",

        "usuario": cliente.to_dict()

    }),201



# =========================================
# LOGIN
# =========================================

@Auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()


    if not data:

        return jsonify({

            "message": "Debe enviar información."

        }),400



    email = data.get("email_cliente")

    password = data.get("password")



    cliente = Cliente.get_by_email(email)



    if cliente is None:

        return jsonify({

            "message": "Usuario no encontrado."

        }),404



    # Verificar contraseña

    if not check_password_hash(

        cliente.password,

        password

    ):

        return jsonify({

            "message": "Contraseña incorrecta."

        }),401



    # Crear token JWT

    token = create_access_token(

        identity=str(cliente.id_cliente)

    )


    return jsonify({

        "message": "Inicio de sesión exitoso.",

        "token": token,

        "usuario": {

            "id_cliente": cliente.id_cliente,

            "nombre": cliente.nombre_cliente,

            "email": cliente.email_cliente

        }

    }),200