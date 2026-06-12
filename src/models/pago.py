from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.models import Base, session

class Pago(Base):
    __tablename__ = "pago"

    id_pago = Column(Integer, primary_key=True)
    fecha_pago = Column(Date, nullable=False)
    monto = Column(Numeric(10,2), nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    estado_pago = Column(String(50), nullable=False)
    id_factura = Column(Integer, ForeignKey("factura.id_factura"))

    def __init__(self, fecha_pago, monto, metodo_pago, estado_pago, id_cliente, id_factura):
        self.fecha_pago = fecha_pago
        self.estado_pago = estado_pago
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.id_cliente = id_cliente
        self.id_factura = id_factura

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        pago = session.query(Pago).all()
        return pago

    @staticmethod
    def get_by_id(id):
        return session.query(Pago).filter_by(
            id_pago=id
        ).first()

    def update(self):
        session.commit()





