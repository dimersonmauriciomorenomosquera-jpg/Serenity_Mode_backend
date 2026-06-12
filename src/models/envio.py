from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.mdels import Base, session

class Envio(Base):
    __tablename__ = "envio"

    id_envio = Column(Integer, primary_key=True)
    destino = Column(String(50), nullable=True)
    dirrecion_envio = Column(String(250), nullable=True)
    empresa_envio = Column(String(100), nullable=False)
    numero_guia = Column(String(25), nullable=False)
    id_factura = Column(Integer, ForeignKey("factura.id_factura"))
    estado_envio = Column(String(50), nullable=False)

    def __init__(self, fecha_factura, total_pagar, estado_pago, id_cliente, id_carrito, estado_envio):
        self.destino = destino
        self.dirrecion_envio = dirrecion_envio
        self.empresa_envio = empresa_envio
        self.numero_guia = numero_guia
        self.id_factura = id_factura
        self.fecha_factura = fecha_factura
        self.estado_envio = estado_envio

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
        envio = session.query(Envio).all()
        return envio

    @staticmethod
    def get_by_id(id):
        return session.query(Envio).filter_by(
            id_envio=id
        ).first()   