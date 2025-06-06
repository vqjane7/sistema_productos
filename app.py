from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Facil123*'
app.config['MYSQL_DB'] = 'sistema_productos'
app.config['MYSQL_PORT'] = '3308'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# ----- CRUD PRODUCTOS -----
@app.route('/productos')
def productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT codigo_producto, nombre_producto FROM producto")
    productos = cur.fetchall()
    return jsonify(productos)

@app.route('/producto', methods=['POST'])
def add_producto():
    data = request.json
    nombre = data.get('nombre_producto')
    if not nombre:
        return jsonify({'status': 'error', 'msg': 'Nombre requerido'}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO producto (nombre_producto) VALUES (%s)", [nombre])
    mysql.connection.commit()
    return jsonify({'status': 'ok'})

@app.route('/producto/<int:codigo_producto>', methods=['PUT'])
def edit_producto(codigo_producto):
    data = request.json
    nombre = data.get('nombre_producto')
    if not nombre:
        return jsonify({'status': 'error', 'msg': 'Nombre requerido'}), 400
    cur = mysql.connection.cursor()
    cur.execute("UPDATE producto SET nombre_producto=%s WHERE codigo_producto=%s", (nombre, codigo_producto))
    mysql.connection.commit()
    return jsonify({'status': 'ok'})

@app.route('/producto/<int:codigo_producto>', methods=['DELETE'])
def delete_producto(codigo_producto):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM producto WHERE codigo_producto=%s", [codigo_producto])
    mysql.connection.commit()
    return jsonify({'status': 'ok'})


# ----- CRUD PROVEEDORES -----
@app.route('/proveedores/<int:codigo_producto>')
def proveedores(codigo_producto):
    cur = mysql.connection.cursor()
    if codigo_producto == 0:
        cur.execute("""SELECT proveedor.codigo_proveedor, proveedor.nombre_proveedor, producto.nombre_producto, proveedor.codigo_producto
                       FROM proveedor JOIN producto ON proveedor.codigo_producto = producto.codigo_producto""")
    else:
        cur.execute("""SELECT proveedor.codigo_proveedor, proveedor.nombre_proveedor, producto.nombre_producto, proveedor.codigo_producto
                       FROM proveedor JOIN producto ON proveedor.codigo_producto = producto.codigo_producto
                       WHERE proveedor.codigo_producto=%s""", (codigo_producto,))
    proveedores = cur.fetchall()
    return jsonify(proveedores)

@app.route('/proveedor', methods=['POST'])
def add_proveedor():
    data = request.json
    nombre = data.get('nombre_proveedor')
    codigo_producto = data.get('codigo_producto')
    if not nombre or not codigo_producto:
        return jsonify({'status': 'error', 'msg': 'Datos requeridos'}), 400
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO proveedor (nombre_proveedor, codigo_producto) VALUES (%s, %s)", (nombre, codigo_producto))
    mysql.connection.commit()
    return jsonify({'status': 'ok'})

@app.route('/proveedor/<int:codigo_proveedor>', methods=['PUT'])
def edit_proveedor(codigo_proveedor):
    data = request.json
    nombre = data.get('nombre_proveedor')
    codigo_producto = data.get('codigo_producto')
    if not nombre or not codigo_producto:
        return jsonify({'status': 'error', 'msg': 'Datos requeridos'}), 400
    cur = mysql.connection.cursor()
    cur.execute("UPDATE proveedor SET nombre_proveedor=%s, codigo_producto=%s WHERE codigo_proveedor=%s", (nombre, codigo_producto, codigo_proveedor))
    mysql.connection.commit()
    return jsonify({'status': 'ok'})

@app.route('/proveedor/<int:codigo_proveedor>', methods=['DELETE'])
def delete_proveedor(codigo_proveedor):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM proveedor WHERE codigo_proveedor=%s", [codigo_proveedor])
    mysql.connection.commit()
    return jsonify({'status': 'ok'})


# ----- CRUD ÓRDENES -----
@app.route('/orden', methods=['POST'])
def crear_orden():
    data = request.json
    codigo_producto = data.get('codigo_producto')
    codigo_proveedor = data.get('codigo_proveedor')
    errors = {}
    if not codigo_producto:
        errors['producto'] = "Selecciona un producto."
    if not codigo_proveedor:
        errors['proveedor'] = "Selecciona un proveedor."
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1 FROM proveedor WHERE codigo_proveedor=%s AND codigo_producto=%s", (codigo_proveedor, codigo_producto))
        if not cur.fetchone():
            errors['relacion'] = "El proveedor no pertenece al producto seleccionado."
    if errors:
        return jsonify({'status': 'error', 'errors': errors}), 400

    fecha_orden = datetime.date.today()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orden (fecha_orden, codigo_producto, codigo_proveedor) VALUES (%s, %s, %s)",
                (fecha_orden, codigo_producto, codigo_proveedor))
    mysql.connection.commit()
    return jsonify({'status': 'ok'})

@app.route('/ordenes')
def ordenes():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT o.codigo_orden, o.fecha_orden, 
               p.nombre_producto, pr.nombre_proveedor
        FROM orden o
        JOIN producto p ON o.codigo_producto = p.codigo_producto
        JOIN proveedor pr ON o.codigo_proveedor = pr.codigo_proveedor
        ORDER BY o.codigo_orden DESC
    """)
    ordenes = cur.fetchall()
    return jsonify(ordenes)

@app.route('/orden/<int:codigo_orden>', methods=['PUT'])
def edit_orden(codigo_orden):
    data = request.json
    codigo_producto = data.get('codigo_producto')
    codigo_proveedor = data.get('codigo_proveedor')
    fecha_orden = data.get('fecha_orden')
    if not codigo_producto or not codigo_proveedor or not fecha_orden:
        return jsonify({'status': 'error', 'msg': 'Datos requeridos'}), 400
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orden SET codigo_producto=%s, codigo_proveedor=%s, fecha_orden=%s WHERE codigo_orden=%s",
                (codigo_producto, codigo_proveedor, fecha_orden, codigo_orden))
    mysql.connection.commit()
    return jsonify({'status': 'ok'})

@app.route('/orden/<int:codigo_orden>', methods=['DELETE'])
def delete_orden(codigo_orden):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orden WHERE codigo_orden=%s", [codigo_orden])
    mysql.connection.commit()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)