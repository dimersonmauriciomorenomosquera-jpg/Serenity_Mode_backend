from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.mdels import Base, session

class Factura(Base):
    __tablename__ = "factura"

    id_factura = Column(Integer, primary_key=True)
    fecha_factura = Column(Date, nullable=False)
    total_pagar = Column(Numeric(10,2), nullable=False)
    estado_pago = Column(string(50), nullable=False)
    id_cliente = column(Integer, ForeignKey("clientes.id_cliente"))
    id_carrito = Column(Integer, ForeignKey("carrito.id_carrito"))

    def __init__(self, fecha_factura, total_pagar, estado_pago, id_cliente, id_carrito):
        self.fecha_factura = fecha_factura
        self.total_pagar = total_pagar
        self.estado_pago = estado_pago
        self.id_cliente = id_cliente
        self.id_carrito = id_carrito

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
        factura = session.query(Factura).all()
        return factura

    @staticmethod
    def get_by_id(id):
        return session.query(Factura).filter_by(
            id_factura=id
        ).first()   
