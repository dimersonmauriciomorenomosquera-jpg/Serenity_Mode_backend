from flask import Flask
from src.models import Base, engine
from src.models.clientes import Cliente
from src.models.productos import Productos
from src.models.envio import Envio
from src.models.factura import Factura
from src.models.pago import Pago
from src.models.detalle_factura import Detalle_Factura
from src.models.detalle_carrito import Detalle_Carrito
from src.models.carrito import Carrito
from src.models.administrador import Administrador
from src.routes.productos_routes import Productos_bp

app = Flask(__name__)
Base.metadata.create_all(engine)

app.register_blueprint(Productos_bp, url_prefix='/productos')

if __name__ == '__main__':
    app.run(debug=True)