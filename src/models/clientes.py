from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.models import Base, session

class Cliente(Base):
    __tablename__ = "cliente"
    
    id_cliente = Column(Integer, primary_key=True)
    nombre_cliente = Column(String(225), nullable=False)
    direccion_cliente = Column(String(225), nullable=False)
    nacimiento_cliente = Column(Date, nullable=False)
    email_cliente = Column(String(225), nullable=False, unique=True)
    numero_cliente = Column(String(20), nullable=False, unique=True)


    def __init__(self, nombre_cliente, dirrecion_cliente,email_cliente,numero_cliente,nacimiento_cliente):
        self.nombre_cliente = nombre_cliente
        self.direccion_cliente = direccion_cliente
        self.nacimiento_cliente = nacimiento_cliente
        self.email_cliente = email_cliente
        self.numero_cliente = numero_cliente
        

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
        cliente = session.query(Cliente).all()
        return cliente

    @staticmethod
    def get_by_id(id):
        return session.query(Cliente).filter_by(
            id_cliente=id
        ).first()


