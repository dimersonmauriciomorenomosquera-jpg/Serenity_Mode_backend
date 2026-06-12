from sqlalchemy import Column, Integer, String, Numeric,Date, ForeignKey
from src.models import Base, session

class Administrador(Base):
    __tablename__ = "administrador"

    id_administrador = Column(Integer, primary_key=True)
    nombre_administrador = Column(String(100), nullable=False )
    telefono_administrador = Column(String(28), nullable=False, unique=True)
    email_administrador = Column(String(120),nullable=False, unique=True)
    rol_administrador = Column(String(50), nullable=False)
    estado_administrador = Column(String(50), nullable=False)
    password_administrador = Column(String(25), nullable=False)

    def __init__ (self, rol_administrador, nombre_administrador, telefono_administrador, email_administrador, estado_administrador, contraseña_administrador):
        self.nombre_administrador = nombre_administrador
        self.telefono_administrador = telefono_administrador
        self.email_administrador = email_administrador
        self.rol_administrador = rol_administrador
        self.estado_administrador = estado_administrador
        self.contraseña_administrador = contraseña_administrador

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
        administrador = session.query(Administrador).all()
        return administrador

    @staticmethod
    def get_by_id(id):
        return session.query(Administrador).filter_by(
        id_administrador=id
        ).first()