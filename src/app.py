from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
from src.models import Base, engine
from src.models.clientes import Cliente
from src.models.productos import Productos
from src.models.envio import Envio
from src.models.factura import Factura
from src.models.pago import Pago
from src.models.detalle_factura import Detalle_Factura
from src.models.carrito import Carrito
from src.models.administrador import Administrador
from src.models.metodos_pago import MetodoPago
from src.routes.detalle_carrito_routes import DetalleCarrito_bp

from src.routes.envio_routes import Envio_bp
from src.routes.productos_routes import Productos_bp
from src.routes.clientes_routes import Clientes_bp
from src.routes.administradores_routes import Administradores_bp
from src.routes.carrito_routes import Carrito_bp
from src.routes.pago_routes import Pago_bp
from src.routes.factura_routes import Factura_bp
from src.routes.metodos_pago import metodos_pago_bp
from src.routes.auth_routes import Auth_bp




app = Flask(__name__)
Base.metadata.create_all(engine)


app.register_blueprint(Envio_bp, url_prefix='/envio')
app.register_blueprint(Productos_bp, url_prefix='/productos')
app.register_blueprint(Clientes_bp, url_prefix='/clientes')
app.register_blueprint(Administradores_bp, url_prefix='/administrador')
app.register_blueprint(Carrito_bp, url_prefix='/carrito')
app.register_blueprint(Pago_bp, url_prefix='/pago')
app.register_blueprint(Factura_bp, url_prefix='/factura')
app.register_blueprint(metodos_pago_bp)
app.register_blueprint(Auth_bp, url_prefix="/auth")


app.register_blueprint(
    DetalleCarrito_bp,
    url_prefix="/detalle_carrito"
)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://127.0.0.1:5001",
            "http://localhost:5001",

            "http://localhost:8100",
            "http://127.0.0.1:8100"
        ]
    }
})

app.config["JWT_SECRET_KEY"] = "serenity_mode_secret"
app.config["SECRET_KEY"] = "serenity_mode_session_secret"


jwt = JWTManager(app) 

if __name__ == '__main__':
    app.run(debug=True)