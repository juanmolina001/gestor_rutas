from flask import Flask 
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request 
import pymysql

driver_location = Blueprint('driver_location', __name__)



def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn


@driver_location.route("/consulta_driver_location")
def consulta_driver_location():

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM driver_location """)
        datos = cur.fetchall()
        data=[]

        for row in datos:
            dato={'conductor_id': row[0], 'latitude': row[1], 'longitude': row[2], 'timestamp' :row[3]} 
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'conductor_id': data, 'mensaje': 'gestor_rutas'})

    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

@driver_location.route("/consulta_individual_driver_location/<codigo>", methods=['get'])
def consulta_individual_driver_location(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor() 
        cur.execute(""" SELECT * FROM conductor_id where conductor_id='{0}' """.format(codigo))

        datos=cur.fetchone()
        cur.close()
        conn.close()

        if datos!= None:
            datos={'conductor_id': datos[0], 'latitude': datos[1], 'longitude': datos[2], 'timestamp' :datos[3], 'celular' :datos[4], 'correo' :datos[5], 'ficha' :datos[6], 'password' :datos[7]} 
            return jsonify({'conductor_id': datos, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:
         print(ex)
         return jsonify({'mensaje': 'Error'})

@driver_location.route("/registro_driver_location",methods=['POST']) 
def registro_driver_location():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        query = "insert into conductor_id (latitude, longitude, timestamp, celular, correo, ficha, password) values \
            ('{0}', '{1}', '{2}')""".format(request.json['latitude'], request.json['longitude'], request.json['timestamp'])
        x=cur.execute(query)
        conn.commit()
        cur.close() 
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@driver_location.route("/eliminar_driver_location/<codigo>", methods=['delete'])
def eliminar_driver_location (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        x=cur.execute(""" delete from driver_location where conductor_id={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@driver_location.route("/actualizar_driver_location/<codigo>",methods=['PUT'])
def actualizar_driver_location(codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas') 
        cur = conn.cursor()
        query = query = "update conductor_id set latitude='{1}', longitude='{2}', timestamp='{3}' where conductor_id={0}""".format(request.json['latitude'], request.json['longitude'], request.json['timestamp'], codigo)
        x=cur.execute(query)

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
        
    except Exception as ex:

        print(ex)

        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    driver_location.run(debug=True)