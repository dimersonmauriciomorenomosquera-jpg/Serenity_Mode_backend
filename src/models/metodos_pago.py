from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.models import Base, session


class MetodoPago(Base):
    __tablename__ = "metodos_pago"

    id_metodo = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)

    tipo_metodo = Column(String(50), nullable=False)
    titular = Column(String(100), nullable=False)
    numero_tarjeta = Column(String(20), nullable=True)
    fecha_vencimiento = Column(String(5), nullable=True)

    predeterminado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)

    fecha_registro = Column(DateTime, server_default=func.now())

    def __init__(
        self,
        id_cliente,
        tipo_metodo,
        titular,
        numero_tarjeta,
        fecha_vencimiento,
        predeterminado=False,
        activo=True
    ):
        self.id_cliente = id_cliente
        self.tipo_metodo = tipo_metodo
        self.titular = titular
        self.numero_tarjeta = numero_tarjeta
        self.fecha_vencimiento = fecha_vencimiento
        self.predeterminado = predeterminado
        self.activo = activo

    def to_dict(self):
        return {
            "id_metodo": self.id_metodo,
            "id_cliente": self.id_cliente,
            "tipo_metodo": self.tipo_metodo,
            "titular": self.titular,
            "numero_tarjeta": self.numero_tarjeta,
            "fecha_vencimiento": self.fecha_vencimiento,
            "predeterminado": self.predeterminado,
            "activo": self.activo,
            "fecha_registro": self.fecha_registro
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

    def update(self):
        session.commit()

    @staticmethod
    def get():
        return session.query(MetodoPago).all()

    @staticmethod
    def get_by_id(id):
        return session.query(MetodoPago).filter_by(
            id_metodo=id
        ).first()

    @staticmethod
    def get_by_cliente(id_cliente):
        return session.query(MetodoPago).filter_by(
            id_cliente=id_cliente
        ).all()