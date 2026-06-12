from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from src.mdels import Base, session

class Productos(Base):
    __tablename__ = 'productos'

    id_producto = Column(Integer, primary_key=True)
    nombre_producto = Column(String(225),nullable=False, unique=False)
    precio_producto = Column(Numeric(10,2), nullable=False)
    stock_producto = Column(Integer, nullable=False)
    marca_producto = Column(String(100), nullable=False)
    codigo_barras = Column(String(50), nullable=False, unique=False)
    sku = Column(String(50), unique=True, nullable=False)

    def __init__(self, nombre_producto, marca_producto, stock_producto, precio_producto, codigo_barras, sku):
        self.nombre_producto = nombre_producto
        self.marca_producto = marca_producto
        self.precio_producto = precio_producto
        self.stock_producto = stock_producto
        self.codigo_barras = codigo_barras
        self.sku = sku

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def get():
        productos = session.query(Productos).all()
        return productos

    @staticmethod
    def get_by_id(id):
        return session.query(Productos).filter_by(
            id_producto=id
        ).first()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self):
        session.commit()