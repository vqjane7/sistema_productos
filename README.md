instalar las siguientes dependencias necesarias

pip install flask flask-mysqldb mysqlclient # dependencia para mysql

pip install flask pymysql 


¿Qué hace?

Este comando instala Flask y dos bibliotecas relacionadas con MySQL para conectarse a bases de datos:

flask:

Framework web en Python.

Permite crear aplicaciones web, APIs, etc.

flask-mysqldb:

Extensión para Flask que facilita la conexión a MySQL usando el conector mysqlclient.

Usa el conector nativo en C (más rápido) que se instala con mysqlclient.

mysqlclient:

Es una biblioteca de bajo nivel que implementa el conector MySQL para Python.

Es rápida, pero requiere compilación y dependencias del sistema, como libmysqlclient o compiladores.