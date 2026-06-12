from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.mdels import Base, session

class Detalle_Factura(Base):
    __tablename__ = "detalle_factura"

    id_detalle_factura = Column(Integer, primary_key=True)
    id_factura = Column(Integer, ForeignKey(f"factura.id_factura"),nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"),nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10,2),nullable=False)
    subtotal = Column(Numeric(10,2), nullable=False)

    def __init__ (self,id_factura, id_producto, cantidad,precio_unitario,subtotal):
        self.id_factura = id_factura
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal

    
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
        detalle_factura = session.query(Detalle_Factura).all()
        return detalle_factura

    @staticmethod
    def get_by_id(id):
        return session.query(Detalle_Factura).filter_by(
            id_detalle_factura=id
        ).first()   