from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from config import config

app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/publicaciones/*": {"origins": "http://localhost"}})

CORS(app, resources={r"/usuario/*": {"origins": "http://localhost"}})

conexion = MySQL(app)


# @cross_origin
# Obtener usuario login
@app.route('/usuario', methods=['GET'])
def obtener_usuario():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario where"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {
                'id': fila[0]
            }
            usuarios.append(usuario)
        return jsonify({'usuario': usuario, 'mensaje': "usuario obtenido.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# Agregar una nueva fdsfmdskjjdfjgdfhigdjgidfjgfdigjdfiogjdfoigjdfogfdjugfssdhfidsjfhdskjfhdsfkjdsfhdskj 
@app.route('/usuario', methods=['POST'])
def registrar_usuario():
    # print(request.json)
    
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO usuario (nombre, email, contrasena, foto) 
        VALUES ('{0}', '{1}', '{2}', '{3}')""".format(request.json['nombre'],
                                                request.json['email'], 
                                                request.json['contrasena'], 
                                                request.json['foto'],
                                                
                                                )
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de inserción.
        return jsonify({'mensaje': "usuario registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    

# Obtener todas las publicaciones
@app.route('/publicaciones', methods=['GET'])
def listar_publicaciones():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM publicaciones where"
        cursor.execute(sql)
        datos = cursor.fetchall()
        publicaciones = []
        for fila in datos:
            publicacion = {
                'id': fila[0],
                'titulo': fila[1],
                'descripcion': fila[2],
                'prioridad': fila[3],
                'estado': fila[4],
                'tiempo': fila[5],
                'usuario': fila[6],
                'fecha_creada': fila[7],
                'fecha_actualizada': fila[8]
            }
            publicaciones.append(publicacion)
        return jsonify({'publicaciones': publicaciones, 'mensaje': "publicaciones listadas.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})



# Agregar una nueva publicacion 
@app.route('/publicaciones', methods=['POST'])
def registrar_publicacion():
    # print(request.json)
    
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO publicaciones (titulo, descripcion, estado, tiempo, usuario, fecha_creada, fecha_actualizada) 
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')""".format(request.json['titulo'],
                                                request.json['descripcion'], 
                                                request.json['prioridad'], 
                                                request.json['estado'],
                                                request.json['tiempo'],
                                                request.json['usuario'],
                                                request.json['fecha_creada'],
                                                request.json['fecha_actualizada']
                                                )
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de inserción.
        return jsonify({'mensaje': "publicacion registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    

# Actualizar una publicacion
@app.route('/publicaciones/<id>', methods=['PUT'])
def actualizar_publicacion(id):
    try:
            cursor = conexion.connection.cursor()
            sql = """UPDATE publicaciones SET 
            titulo = '{0}', 
            descripcion = '{1}'
            prioridad = '{2}'
            estado = '{3}'
            tiempo = '{4}'
            usuario = '{5}'
            fecha_creada = '{6}'
            fecha_actualizada = '{7}'
            WHERE id = '{8}'""".format(request.json['titulo'],
                                                request.json['descripcion'], 
                                                request.json['prioridad'], 
                                                request.json['estado'],
                                                request.json['tiempo'],
                                                request.json['usuario'],
                                                request.json['fecha_creada'],
                                                request.json['fecha_actualizada'],
                                                 id)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de actualización.
            return jsonify({'mensaje': "publicacion actualizado.", 'exito': True})
        
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


#Borrar una publicacion
@app.route('/publicaciones/<id>', methods=['DELETE'])
def eliminar_publicacion(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM publicaciones WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la acción de eliminación.
        return jsonify({'mensaje': "Publicación eliminada.", 'exito': True})
      
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run() 
