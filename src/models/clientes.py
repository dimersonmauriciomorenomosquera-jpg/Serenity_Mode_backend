from sqlalchemy import Column, Integer, String, Date
from src.models import Base, session


class Cliente(Base):

    __tablename__ = "cliente"

    # ==========================================================
    # COLUMNAS
    # ==========================================================

    id_cliente = Column(
        Integer,
        primary_key=True
    )

    nombre_cliente = Column(
        String(225),
        nullable=False
    )

    direccion_cliente = Column(
        String(225),
        nullable=False
    )

    nacimiento_cliente = Column(
        Date,
        nullable=False
    )

    email_cliente = Column(
        String(225),
        nullable=False,
        unique=True
    )

    numero_cliente = Column(
        String(20),
        nullable=False,
        unique=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    estado_cliente = Column(
        String(20),
        nullable=False,
        default="Activo"
    )

    # ==========================================================
    # CONSTRUCTOR
    # ==========================================================

    def __init__(
        self,
        nombre_cliente,
        direccion_cliente,
        email_cliente,
        numero_cliente,
        nacimiento_cliente,
        password,
        estado_cliente="Activo"
    ):

        self.nombre_cliente = nombre_cliente
        self.direccion_cliente = direccion_cliente
        self.nacimiento_cliente = nacimiento_cliente
        self.email_cliente = email_cliente
        self.numero_cliente = numero_cliente
        self.password = password
        self.estado_cliente = estado_cliente

    # ==========================================================
    # CONVERTIR A DICCIONARIO
    # ==========================================================

    def to_dict(self):

        return {
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "nacimiento_cliente": self.nacimiento_cliente,
            "email_cliente": self.email_cliente,
            "numero_cliente": self.numero_cliente,
            "direccion_cliente": self.direccion_cliente,
            "estado_cliente": self.estado_cliente
        }

    # ==========================================================
    # GUARDAR
    # ==========================================================

    def save(self):

        try:

            session.add(self)
            session.commit()

        except Exception as e:

            session.rollback()
            raise e

    # ==========================================================
    # ELIMINAR
    # ==========================================================

    def delete(self):

        session.delete(self)
        session.commit()

    # ==========================================================
    # ACTUALIZAR
    # ==========================================================

    def update(self):

        session.commit()

    # ==========================================================
    # OBTENER CLIENTES
    # ==========================================================

    @staticmethod
    def get(page=1, per_page=10):

        query = session.query(Cliente)

        total = query.count()

        clientes = (
            query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return clientes, total

    # ==========================================================
    # OBTENER CLIENTE POR ID
    # ==========================================================

    @staticmethod
    def get_by_id(id):

        return session.query(Cliente).filter_by(
            id_cliente=id
        ).first()

    # ==========================================================
    # OBTENER CLIENTE POR EMAIL
    # ==========================================================

    @staticmethod
    def get_by_email(email):

        return session.query(Cliente).filter_by(
            email_cliente=email
        ).first()