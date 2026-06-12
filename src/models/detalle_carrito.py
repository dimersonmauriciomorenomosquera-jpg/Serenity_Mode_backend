from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.mdels import Base, session

class Detalle_Carrito(Base):
    __tablename__ = "detalle_carrito"

    id_detalle_carrito = Column(Integer, primary_key=True)
    id_carrito = Column(Integer, ForeignKey("carrito.id_carrito"),nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario =Column(Numeric(10,2),nullable=False)

    def __init__(self, cantidad, id_carrito, id_producto):
        self.id_carrito = id_carrito
        self.id_producto = id_producto
        self.cantidad = cantidad
    
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
        detalle_Carrito = session.query(Detalle_Carrito).all()
        return detalle_Carrito

    @staticmethod
    def get_by_id(id):
        return session.query(Detalle_Carrito).filter_by(
            id_detalle_carrito=id
        ).first()




