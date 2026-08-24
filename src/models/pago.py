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
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))

    def __init__(self, fecha_pago, monto, metodo_pago, estado_pago, id_cliente, id_factura):
        self.fecha_pago = fecha_pago
        self.estado_pago = estado_pago
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.id_cliente = id_cliente
        self.id_factura = id_factura

    def to_dict(self):
        return {
            "id_pago": self.id_pago,
            "fecha_pago": self.fecha_pago,
            "estado_pago": self.estado_pago,
            "monto": self.monto,
            "estado_pago": self.estado_pago,
            "id_cliente": self.id_cliente,
            "id_factura": self.id_factura
        }

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get(page=1, per_page=10):
        query = session.query(Pago)

        total = query.count()

        pagos = (
            query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return pagos, total

    @staticmethod
    def get_by_id(id):
        return session.query(Pago).filter_by(
            id_pago=id
        ).first()

    def update(self):
        session.commit()





