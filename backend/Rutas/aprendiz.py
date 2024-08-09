from flask import Flask 
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request 
import pymysql

aprendiz = Blueprint('aprendiz', __name__)



def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn


@aprendiz.route("/consulta_aprendiz")
def consulta_aprendiz():

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM aprendiz """)
        datos = cur.fetchall()
        data=[]

        for row in datos:
            dato={'id_aprendiz': row[0], 'nombre_completo': row[1], 'T_documento': row[2], 'N_documento' :row[3], 'celular' :row[4], 'correo' :row[5], 'ficha' :row[6], 'password' :row[7]} 
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'aprendiz': data, 'mensaje': 'gestor_rutas'})

    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

@aprendiz.route("/consulta_individual_aprendiz/<codigo>", methods=['get'])
def consulta_individual_aprendiz(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor() 
        cur.execute(""" SELECT * FROM aprendiz where id_aprendiz='{0}' """.format(codigo))

        datos=cur.fetchone()
        cur.close()
        conn.close()

        if datos!= None:
            datos={'id_aprendiz': datos[0], 'nombre_completo': datos[1], 'T_documento': datos[2], 'N_documento' :datos[3], 'celular' :datos[4], 'correo' :datos[5], 'ficha' :datos[6], 'password' :datos[7]} 
            return jsonify({'aprendiz': datos, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:
         print(ex)
         return jsonify({'mensaje': 'Error'})

@aprendiz.route("/registro_aprendiz",methods=['POST']) 
def registro_aprendiz():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        query = "insert into aprendiz (nombre_completo, T_documento, N_documento, celular, correo, ficha, password) values \
            ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(request.json['nombre_completo'], request.json['T_documento'], request.json['N_documento'], request.json['celular'], request.json['correo'], request.json['ficha'], request.json['password'])
        x=cur.execute(query)
        conn.commit()
        cur.close() 
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@aprendiz.route("/eliminar_aprendiz/<codigo>", methods=['delete'])
def eliminar_aprendiz (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        x=cur.execute(""" delete from aprendiz where id_aprendiz={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@aprendiz.route("/actualizar_aprendiz/<codigo>",methods=['PUT'])
def actualizar_aprendiz(codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas') 
        cur = conn.cursor()
        query = query = "update aprendiz set nombre_completo='{1}', T_documento='{2}', N_documento='{3}', celular='{4}', correo='{5}', ficha='{6}', password='{7}' where id_aprendiz={0}""".format(request.json['nombre_completo'], request.json['T_documento'], request.json['N_documento'], request.json['celular'], request.json['correo'], request.json['ficha'] ,request.json['password'], codigo)
        x=cur.execute(query)

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
        
    except Exception as ex:

        print(ex)

        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    aprendiz.run(debug=True)