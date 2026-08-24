from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.models import Base, session

class Envio(Base):
    __tablename__ = "envio"

    id_envio = Column(Integer, primary_key=True)
    fecha_factura = Column(Date)
    destino = Column(String(50), nullable=True)
    direccion_envio = Column(String(250), nullable=True)
    empresa_envio = Column(String(100), nullable=False)
    numero_guia = Column(String(25), nullable=False)
    id_factura = Column(Integer, ForeignKey("factura.id_factura"))
    estado_envio = Column(String(50), nullable=False)

    def __init__(self, fecha_factura,numero_guia, id_factura, estado_envio, destino, direccion_envio, empresa_envio):
        self.destino = destino
        self.direccion_envio = direccion_envio
        self.empresa_envio = empresa_envio
        self.numero_guia = numero_guia
        self.id_factura = id_factura
        self.fecha_factura = fecha_factura
        self.estado_envio = estado_envio



    def delete(self):
        session.delete(self)
        session.commit()

    def update(self):
        session.commit()

    @staticmethod
    def get(page=1, per_page=10):
        query = session.query(Envio)

        total = query.count()

        envios = (
            query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return envios, total

    @staticmethod
    def get_by_id(id):
        return session.query(Envio).filter_by(
            id_envio=id
        ).first()   
    
    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e