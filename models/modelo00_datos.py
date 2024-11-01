#modelo00_datos.py ----> Declaración del Modelo Base de Datos (BDRetardados)
#Importación desde la librería psycopg2 el paquete connect
#      que permite tiene los driver para establecer la conección con la Base de Datos PostGreSQL
from psycopg2 import connect


def cadenaConexion():
    conexion = connect(host = "localhost", # localhost o http://127.0.0.1
                port = 5432, 
                dbname = "bdretardados3",             
                user = "postgres",
                password = "123456")
    return conexion

