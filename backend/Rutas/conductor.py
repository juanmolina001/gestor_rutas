from flask import Flask 
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request 
import pymysql

conductor = Blueprint('conductor', __name__)



def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn


@conductor.route("/consulta_conductor")
def consulta_conductor():

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM conductor """)
        datos = cur.fetchall()
        data=[]

        for row in datos:
            dato={'conductor_id': row[0], 'usuario': row[1], 'password' :row[2]} 
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'conductor': data, 'mensaje': 'gestor_rutas'})

    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

@conductor.route("/consulta_individual_conductor/<codigo>", methods=['get'])
def consulta_individual_conductor(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor() 
        cur.execute(""" SELECT * FROM conductor where conductor_id='{0}' """.format(codigo))

        datos=cur.fetchone()
        cur.close()
        conn.close()

        if datos!= None:
            datos={'conductor_id': datos[0], 'usuario': datos[1], 'password' :datos[2]} 
            return jsonify({'conductor': datos, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:
         print(ex)
         return jsonify({'mensaje': 'Error'})

@conductor.route("/registro_conductor",methods=['POST']) 
def registro_conductor():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        query = "insert into conductor (usuario, password) values \
            ('{0}', '{1}')""".format(request.json['usuario'], request.json['password'])
        x=cur.execute(query)
        conn.commit()
        cur.close() 
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@conductor.route("/eliminar_conductor/<codigo>", methods=['delete'])
def eliminar_conductor (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        x=cur.execute(""" delete from conductor where conductor_id={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@conductor.route("/actualizar_conductor/<codigo>",methods=['PUT'])
def actualizar_conductor(codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas') 
        cur = conn.cursor()
        query = query = "update conductor set usuario='{1}', password='{2}' where conductor_id={0}""".format(request.json['usuario'], request.json['password'], codigo)
        x=cur.execute(query)

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
        
    except Exception as ex:

        print(ex)

        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    conductor.run(debug=True)