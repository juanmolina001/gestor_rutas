from flask import Flask 
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request 
import pymysql

paradas = Blueprint('paradas', __name__)


def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn


@paradas.route("/consulta_paradas")
def consulta_paradas():

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM paradas """)
        datos = cur.fetchall()
        data=[]

        for row in datos:
            dato={'id_paradas': row[0],'direccion': row[1]} 
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'parada': data, 'mensaje': 'gestor_rutas'})

    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

@paradas.route("/consulta_individual_paradas/<codigo>", methods=['get'])
def consulta_individual_paradas(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor() 
        cur.execute(""" SELECT * FROM paradas where id_paradas='{0}' """.format(codigo))

        datos=cur.fetchone()
        cur.close()
        conn.close()

        if datos!= None:
            dato={'id_paradas': datos[0],'direccion': datos[1]} 
            return jsonify({'paradas': dato, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:
         print(ex)
         return jsonify({'mensaje': 'Error'})

@paradas.route("/registro_paradas/",methods=['POST']) 
def registro_paradas():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        query = "insert into paradas (direccion) values \
            ('{0}', '{1}')""".format( request.json['direccion'])
        x=cur.execute(query)
        conn.commit()
        cur.close() 
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@paradas.route("/eliminar_paradas/<codigo>", methods=['delete'])
def eliminar_paradas (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        x=cur.execute(""" delete from paradas where id_paradas={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@paradas.route("/actualizar_paradas/<codigo>",methods=['PUT'])
def actualizar_paradas (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas') 
        cur = conn.cursor()
        query = query = "update paradas set direccion='{0}', where id_paradas={1}""".format(request.json['direccion'], codigo)
        x=cur.execute(query)

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
        
    except Exception as ex:

        print(ex)

        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    paradas.run(debug=True)