from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from src.models import Base, session


class Detalle_Carrito(Base):
    __tablename__ = "detalle_carrito"

    id_detalle_carrito = Column(Integer, primary_key=True)

    id_carrito = Column(
        Integer,
        ForeignKey("carrito.id_carrito"),
        nullable=False
    )

    id_producto = Column(
        Integer,
        ForeignKey("productos.id_producto"),
        nullable=False
    )

    cantidad = Column(
        Integer,
        nullable=False
    )

    precio_unitario = Column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    talla = Column(
        String(20),
        nullable=True
    )


    def __init__(
        self,
        id_carrito,
        id_producto,
        cantidad,
        precio_unitario,
        talla
    ):
        self.id_carrito = id_carrito
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = precio_unitario * cantidad
        self.talla = talla


    def to_dict(self):
        return {
            "id_detalle_carrito": self.id_detalle_carrito,
            "id_carrito": self.id_carrito,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio_unitario": float(self.precio_unitario),
            "subtotal": float(self.subtotal),
            "talla": self.talla
        }


    def save(self):
        session.add(self)
        session.commit()


    def delete(self):
        session.delete(self)
        session.commit()


    def update(self):
        self.subtotal = self.precio_unitario * self.cantidad
        session.commit()


    @staticmethod
    def get():
        return session.query(Detalle_Carrito).all()


    @staticmethod
    def get_by_id(id):
        return session.query(Detalle_Carrito).filter_by(
            id_detalle_carrito=id
        ).first()


    @staticmethod
    def get_by_carrito(id_carrito):
        return session.query(Detalle_Carrito).filter_by(
            id_carrito=id_carrito
        ).all()