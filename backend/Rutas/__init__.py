from flask import Flask
from flask_cors import CORS


from Rutas.paradas import paradas
from Rutas.aprendiz import aprendiz
from Rutas.ruta import ruta
from Rutas.programa import programa
from Rutas.conductor import conductor
from Rutas.driver_location import driver_location
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(paradas)
    app.register_blueprint(aprendiz)
    app.register_blueprint(ruta)
    app.register_blueprint(programa)
    app.register_blueprint(conductor)
    app.register_blueprint(driver_location)
    return app