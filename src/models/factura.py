from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey,Time
from src.models import Base, session



class Factura(Base):
    __tablename__ = "factura"

    id_factura = Column(Integer, primary_key=True)
    fecha_factura = Column(Date, nullable=False)
    hora_factura = Column(Time, nullable=False)

    subtotal_productos = Column(
        Numeric(10, 2),
        nullable=False
    )

    costo_envio = Column(
        Numeric(10, 2),
        nullable=False
    )

    total_pagar = Column(
        Numeric(10, 2),
        nullable=False
    )

    estado_pago = Column(String(50), nullable=False)

    id_cliente = Column(
        Integer,
        ForeignKey("cliente.id_cliente")
    )

    id_carrito = Column(
        Integer,
        ForeignKey("carrito.id_carrito")
    )

    def __init__(
        self,
        fecha_factura,
        subtotal_productos,
        costo_envio,
        total_pagar,
        estado_pago,
        id_cliente,
        id_carrito,
        hora_factura
    ):
        self.fecha_factura = fecha_factura
        self.subtotal_productos = subtotal_productos
        self.costo_envio = costo_envio
        self.total_pagar = total_pagar
        self.estado_pago = estado_pago
        self.id_cliente = id_cliente
        self.id_carrito = id_carrito
        self.hora_factura = hora_factura

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self):
        session.commit()

    @staticmethod
    def get(page=1, per_page=10):
        query = session.query(Factura)

        total = query.count()

        facturas = (
            query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return facturas, total

    @staticmethod
    def get_by_id(id):
        return session.query(Factura).filter_by(
            id_factura=id
        ).first()

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e