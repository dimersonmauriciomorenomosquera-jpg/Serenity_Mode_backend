from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey
from src.models import Base, session


class Carrito(Base):

    __tablename__ = "carrito"

    id_carrito = Column(Integer, primary_key=True)
    fecha_creacion = Column(Date, nullable=False)
    total_carrito = Column(Numeric(10, 2), nullable=False)
    id_cliente = Column(
        Integer,
        ForeignKey("cliente.id_cliente"),
        nullable=False
    )

    def __init__(self, fecha_creacion, total_carrito, id_cliente):
        self.fecha_creacion = fecha_creacion
        self.total_carrito = total_carrito
        self.id_cliente = id_cliente

    # ==========================
    # GUARDAR
    # ==========================

    def save(self):
        session.add(self)
        session.commit()

    # ==========================
    # ELIMINAR
    # ==========================

    def delete(self):
        session.delete(self)
        session.commit()

    # ==========================
    # ACTUALIZAR
    # ==========================

    def update(self):
        session.commit()

    # ==========================
    # OBTENER TODOS
    # ==========================

    @staticmethod
    def get():
        return session.query(Carrito).all()

    # ==========================
    # OBTENER POR ID CARRITO
    # ==========================

    @staticmethod
    def get_by_id(id_carrito):
        return session.query(Carrito).filter_by(
            id_carrito=id_carrito
        ).first()

    # ==========================
    # OBTENER POR ID CLIENTE
    # ==========================

    @staticmethod
    def get_by_cliente(id_cliente):
        return session.query(Carrito).filter_by(
            id_cliente=id_cliente
        ).first()