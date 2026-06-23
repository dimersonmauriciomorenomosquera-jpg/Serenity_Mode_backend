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
from src.routes.clientes_routes import Clientes_bp
from src.routes.administradores_routes import Administradores_bp
from src.routes.carrito_routes import Carrito_bp
from src.routes.pago_routes import Pago_bp
from src.routes.factura_routes import Factura_bp


app = Flask(__name__)
Base.metadata.create_all(engine)

app.register_blueprint(Productos_bp, url_prefix='/productos')
app.register_blueprint(Clientes_bp, url_prefix='/clientes')
app.register_blueprint(Administradores_bp, url_prefix='/administrador')
app.register_blueprint(Carrito_bp, url_prefix='/carrito')
app.register_blueprint(Pago_bp, url_prefix='/pago')
app.register_blueprint(Factura_bp, url_prefix='/factura')

if __name__ == '__main__':
    app.run(debug=True)