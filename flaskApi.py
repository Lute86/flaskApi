import sqlite3
from flask import Flask, jsonify, request, g
from flask_cors import CORS

DATABASE = 'inventarios.db'

app = Flask(__name__)
CORS(app)

def get_db_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def create_table():
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicios (
                codigo INTEGER PRIMARY KEY,
                aplicacion TEXT NOT NULL,
                servicio TEXT NOT NULL,
                precio REAL NOT NULL
            ) ''')
        conn.commit()
        cursor.close()

def create_database():
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

create_database()

class Servicio:
    def __init__(self, codigo, aplicacion, servicio, precio):
        self.codigo = codigo
        self.aplicacion = aplicacion
        self.servicio = servicio
        self.precio = precio

    def modificar(self, nueva_aplicacion, nuevo_servicio, nuevo_precio):
        self.aplicacion = nueva_aplicacion
        self.servicio = nuevo_servicio
        self.precio = nuevo_precio

@app.route('/servicios', methods=['POST'])
def agregar_servicio():
    data = request.get_json()
    codigo = data.get('codigo')
    aplicacion = data.get('aplicacion')
    servicio = data.get('servicio')
    precio = data.get('precio')

    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM servicios WHERE codigo = ?', (codigo,))
        row = cursor.fetchone()
        if row:
            cursor.close()
            return jsonify({'message': 'Ya existe un servicio con ese código.'}), 400

        nuevo_servicio = Servicio(codigo, aplicacion, servicio, precio)

        cursor.execute('INSERT INTO servicios VALUES (?, ?, ?, ?)', (codigo, aplicacion, servicio, precio))
        conn.commit()
        cursor.close()

    return jsonify({'message': 'Servicio agregado correctamente.'}), 200

@app.route('/servicios', methods=['GET'])
def listar_servicios():
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM servicios')
        rows = cursor.fetchall()
        cursor.close()

        servicios = []
        for row in rows:
            codigo, aplicacion, servicio, precio = row
            servicio = {'codigo': codigo, 'aplicacion': aplicacion, 'servicio': servicio, 'precio': precio}
            servicios.append(servicio)

    return jsonify(servicios), 200

@app.route('/servicios/<int:codigo>', methods=['GET'])
def obtener_servicio(codigo):
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM servicios WHERE codigo = ?', (codigo,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            codigo, aplicacion, servicio, precio = row
            servicio = {'codigo': codigo, 'aplicacion': aplicacion, 'servicio': servicio, 'precio': precio}
            return jsonify(servicio), 200

    return jsonify({'message': 'Servicio no encontrado.'}), 404

@app.route('/servicios/<int:codigo>', methods=['PUT'])
def modificar_servicio(codigo):
    data = request.get_json()
    nueva_aplicacion = data.get('aplicacion')
    nuevo_servicio = data.get('servicio')
    nuevo_precio = data.get('precio')

    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM servicios WHERE codigo = ?', (codigo,))
        row = cursor.fetchone()

        if row:
            servicio = Servicio(*row)
            servicio.modificar(nueva_aplicacion, nuevo_servicio, nuevo_precio)

            cursor.execute('UPDATE servicios SET aplicacion = ?, servicio = ?, precio = ? WHERE codigo = ?',
                           (nueva_aplicacion, nuevo_servicio, nuevo_precio, codigo))
            conn.commit()
            cursor.close()

            return jsonify({'message': 'Servicio modificado correctamente.'}), 200

    return jsonify({'message': 'Servicio no encontrado.'}), 404

@app.route('/servicios/<int:codigo>', methods=['DELETE'])
def eliminar_servicio(codigo):
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM servicios WHERE codigo = ?', (codigo,))
        row = cursor.fetchone()

        if row:
            cursor.execute('DELETE FROM servicios WHERE codigo = ?', (codigo,))
            conn.commit()
            cursor.close()

            return jsonify({'message': 'Servicio eliminado correctamente.'}), 200

    return jsonify({'message': 'Servicio no encontrado.'}), 404

if __name__ == '__main__':
    app.run()
