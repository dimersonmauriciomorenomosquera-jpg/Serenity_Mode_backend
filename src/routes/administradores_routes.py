from flask import Blueprint, request, jsonify
from src.models.administrador import Administrador

from werkzeug.security import generate_password_hash,  check_password_hash

from flask_jwt_extended import jwt_required, get_jwt_identity

from src.utils.decorators import admin_required


Administradores_bp = Blueprint('Administrador', __name__)


# ==========================================================
# PERFIL DEL ADMINISTRADOR AUTENTICADO
# ==========================================================

@Administradores_bp.route("/perfil", methods=["GET"])
@admin_required
def perfil_administrador():

    id_administrador = get_jwt_identity()

    administrador = Administrador.get_by_id(id_administrador)

    if administrador is None:
        return jsonify({
            "message": "Administrador no encontrado."
        }), 404

    return jsonify({

        "id_administrador": administrador.id_administrador,
        "nombre_administrador": administrador.nombre_administrador,
        "telefono_administrador": administrador.telefono_administrador,
        "email_administrador": administrador.email_administrador,
        "rol_administrador": administrador.rol_administrador,
        "estado_administrador": administrador.estado_administrador

    }), 200


# ==========================================================
# OBTENER TODOS LOS ADMINISTRADORES
# ==========================================================

@Administradores_bp.route("/", methods=["GET"])
@admin_required
def get_administradores():

    administradores = Administrador.get()

    administradores_list = []

    for administrador in administradores:

        administradores_list.append({

            "id_administrador": administrador.id_administrador,
            "nombre_administrador": administrador.nombre_administrador,
            "rol_administrador": administrador.rol_administrador,
            "telefono_administrador": administrador.telefono_administrador,
            "estado_administrador": administrador.estado_administrador,
            "email_administrador": administrador.email_administrador

        })

    return jsonify(administradores_list), 200


# ==========================================================
# OBTENER ADMINISTRADOR POR ID
# ==========================================================

@Administradores_bp.route("/<int:id>", methods=["GET"])
@admin_required
def get_administrador(id):

    administrador = Administrador.get_by_id(id)

    if not administrador:

        return jsonify({
            "message": "Administrador no encontrado."
        }), 404

    administrador_data = {

        "id_administrador": administrador.id_administrador,
        "nombre_administrador": administrador.nombre_administrador,
        "rol_administrador": administrador.rol_administrador,
        "telefono_administrador": administrador.telefono_administrador,
        "estado_administrador": administrador.estado_administrador,
        "email_administrador": administrador.email_administrador

    }

    return jsonify(administrador_data), 200


# ==========================================================
# CREAR ADMINISTRADOR
# ==========================================================

@Administradores_bp.route("/", methods=["POST"])
@admin_required
def create_administrador():

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Debe enviar información."
        }), 400


    campos = [
        "nombre_administrador",
        "rol_administrador",
        "estado_administrador",
        "telefono_administrador",
        "email_administrador",
        "password_administrador"
    ]


    # ======================================================
    # VALIDAR CAMPOS
    # ======================================================

    for campo in campos:

        if campo not in data or not data[campo]:

            return jsonify({
                "message": f"El campo {campo} es obligatorio."
            }), 400


    # ======================================================
    # VALIDAR TELÉFONO
    # ======================================================

    try:

        int(data["telefono_administrador"])

    except (ValueError, TypeError):

        return jsonify({
            "message": "El teléfono debe ser numérico."
        }), 400


    # ======================================================
    # HASHEAR CONTRASEÑA
    # ======================================================

    password_hash = generate_password_hash(
        data["password_administrador"]
    )


    administrador = Administrador(

        nombre_administrador=data["nombre_administrador"],

        rol_administrador=data["rol_administrador"],

        estado_administrador=data["estado_administrador"],

        telefono_administrador=data["telefono_administrador"],

        email_administrador=data["email_administrador"],

        password_administrador=password_hash

    )


    # ======================================================
    # GUARDAR
    # ======================================================

    try:

        administrador.save()

    except Exception as e:

        return jsonify({
            "message": "Error al crear el administrador.",
            "error": str(e)
        }), 400


    return jsonify({

        "message": "Administrador creado exitosamente.",

        "administrador": {

            "id_administrador": administrador.id_administrador,

            "nombre_administrador":
                administrador.nombre_administrador,

            "rol_administrador":
                administrador.rol_administrador,

            "telefono_administrador":
                administrador.telefono_administrador,

            "estado_administrador":
                administrador.estado_administrador,

            "email_administrador":
                administrador.email_administrador

        }

    }), 201


# ==========================================================
# ELIMINAR ADMINISTRADOR
# ==========================================================

@Administradores_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete_administrador(id):

    administrador = Administrador.get_by_id(id)

    if not administrador:

        return jsonify({
            "message": "Administrador no encontrado."
        }), 404


    try:

        administrador.delete()

    except Exception as e:

        return jsonify({
            "message": "Error al eliminar el administrador.",
            "error": str(e)
        }), 400


    return jsonify({
        "message": "Administrador eliminado exitosamente."
    }), 200

# ==========================================================
# CAMBIAR CONTRASEÑA DEL ADMINISTRADOR AUTENTICADO
# ==========================================================

@Administradores_bp.route(
    "/cambiar-password",
    methods=["PUT"]
)
@admin_required
def cambiar_password():

    # ======================================================
    # OBTENER ADMINISTRADOR DESDE EL JWT
    # ======================================================

    id_administrador = get_jwt_identity()

    administrador = Administrador.get_by_id(
        id_administrador
    )

    if administrador is None:

        return jsonify({
            "message": "Administrador no encontrado."
        }), 404


    # ======================================================
    # OBTENER DATOS
    # ======================================================

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

    password_confirmar = data.get(
        "password_confirmar"
    )


    # ======================================================
    # VALIDAR CAMPOS
    # ======================================================

    if not password_actual:

        return jsonify({
            "message": "La contraseña actual es obligatoria."
        }), 400


    if not password_nueva:

        return jsonify({
            "message": "La nueva contraseña es obligatoria."
        }), 400


    if not password_confirmar:

        return jsonify({
            "message": "Debe confirmar la nueva contraseña."
        }), 400


    # ======================================================
    # COMPROBAR CONTRASEÑA ACTUAL
    # ======================================================

    if not check_password_hash(
        administrador.password_administrador,
        password_actual
    ):

        return jsonify({
            "message": "La contraseña actual es incorrecta."
        }), 401


    # ======================================================
    # COMPROBAR NUEVA CONTRASEÑA
    # ======================================================

    if password_nueva != password_confirmar:

        return jsonify({
            "message": "Las nuevas contraseñas no coinciden."
        }), 400


    # ======================================================
    # EVITAR MISMA CONTRASEÑA
    # ======================================================

    if check_password_hash(
        administrador.password_administrador,
        password_nueva
    ):

        return jsonify({
            "message": "La nueva contraseña debe ser diferente a la actual."
        }), 400


    # ======================================================
    # VALIDAR LONGITUD
    # ======================================================

    if len(password_nueva) < 8:

        return jsonify({
            "message": "La nueva contraseña debe tener mínimo 8 caracteres."
        }), 400


    # ======================================================
    # GENERAR NUEVO HASH
    # ======================================================

    nuevo_hash = generate_password_hash(
        password_nueva
    )


    administrador.password_administrador = \
        nuevo_hash


    # ======================================================
    # GUARDAR
    # ======================================================

    try:

        administrador.update()

    except Exception as e:

        return jsonify({
            "message": "Error al actualizar la contraseña.",
            "error": str(e)
        }), 500


    # ======================================================
    # RESPUESTA
    # ======================================================

    return jsonify({

        "message":
            "Contraseña actualizada correctamente."

    }), 200

# ==========================================================
# ACTUALIZAR ADMINISTRADOR
# ==========================================================

@Administradores_bp.route("/<int:id>", methods=["PUT"])
@admin_required
def update_administrador(id):

    administrador = Administrador.get_by_id(id)

    if not administrador:

        return jsonify({
            "message": "Administrador no encontrado."
        }), 404


    data = request.get_json()

    if not data:

        return jsonify({
            "message": "Debe enviar información."
        }), 400


    # ======================================================
    # ACTUALIZAR NOMBRE
    # ======================================================

    if "nombre_administrador" in data:

        if not data["nombre_administrador"]:

            return jsonify({
                "message": "El nombre es obligatorio."
            }), 400

        administrador.nombre_administrador = \
            data["nombre_administrador"]


    # ======================================================
    # ACTUALIZAR ROL
    # ======================================================

    if "rol_administrador" in data:

        if not data["rol_administrador"]:

            return jsonify({
                "message": "El rol es obligatorio."
            }), 400

        administrador.rol_administrador = \
            data["rol_administrador"]


    # ======================================================
    # ACTUALIZAR ESTADO
    # ======================================================

    if "estado_administrador" in data:

        if not data["estado_administrador"]:

            return jsonify({
                "message": "El estado es obligatorio."
            }), 400

        administrador.estado_administrador = \
            data["estado_administrador"]


    # ======================================================
    # ACTUALIZAR TELÉFONO
    # ======================================================

    if "telefono_administrador" in data:

        try:

            int(data["telefono_administrador"])

        except (ValueError, TypeError):

            return jsonify({
                "message": "El teléfono debe ser numérico."
            }), 400

        administrador.telefono_administrador = \
            data["telefono_administrador"]


    # ======================================================
    # ACTUALIZAR EMAIL
    # ======================================================

    if "email_administrador" in data:

        if not data["email_administrador"]:

            return jsonify({
                "message": "El email es obligatorio."
            }), 400

        administrador.email_administrador = \
            data["email_administrador"]


    # ======================================================
    # ACTUALIZAR CONTRASEÑA
    # ======================================================

    if "password_administrador" in data:

        if not data["password_administrador"]:

            return jsonify({
                "message": "La contraseña es obligatoria."
            }), 400

        # IMPORTANTE:
        # Nunca guardar la contraseña directamente.
        # Siempre volver a generar el hash.

        administrador.password_administrador = \
            generate_password_hash(
                data["password_administrador"]
            )


    # ======================================================
    # GUARDAR CAMBIOS
    # ======================================================

    try:

        administrador.update()

    except Exception as e:

        return jsonify({
            "message": "Error al actualizar el administrador.",
            "error": str(e)
        }), 400


    return jsonify({

        "message": "Administrador actualizado exitosamente.",

        "administrador": {

            "id_administrador":
                administrador.id_administrador,

            "nombre_administrador":
                administrador.nombre_administrador,

            "rol_administrador":
                administrador.rol_administrador,

            "telefono_administrador":
                administrador.telefono_administrador,

            "estado_administrador":
                administrador.estado_administrador,

            "email_administrador":
                administrador.email_administrador

        }

    }), 200