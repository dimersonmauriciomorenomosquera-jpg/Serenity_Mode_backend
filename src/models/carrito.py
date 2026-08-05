from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.models import Base, session

class Carrito(Base):
    __tablename__ = "carrito"

    id_carrito = Column(Integer, primary_key=True)
    fecha_creacion = Column(Date, nullable=False)
    total_carrito = Column(Numeric(10,2), nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente") )

    def __init__ (self, fecha_creacion, total_carrito, id_cliente):
        self.fecha_creacion = fecha_creacion
        self.total_carrito = total_carrito
        self.id_cliente = id_cliente

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self):
        session.commit()

    @staticmethod
    def get():
        carrito = session.query(Carrito).all()
        return carrito

    @staticmethod
    def get_by_id(id):
        return session.query(Carrito).filter_by(
            id_carrito=id
        ).first()

    @staticmethod
    def get_by_cliente(id_cliente):
        return session.query(Carrito).filter_by(
            id_cliente=id_cliente
    ).first()


