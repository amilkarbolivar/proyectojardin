#model01_tmcargos.py: Archivo para manejar las operaciones con TMCargos;
#       Es decir el modelo de la TMCargos

#1.- IMPORTACIÓN DE LIBRERIAS
from flask import  Blueprint, render_template, flash, redirect, url_for, request, Flask
from psycopg2 import connect


#2.- IMPORTACIÓN DEL MODELO
#2.1.- Importación Base de Datos)
from models.modelo00_datos import cadenaConexion


#Importación desde la librería flask el paquete request
#       La cual permite recibir o enviar datos desde una pagina web (Formularios)
from flask import request



# Obtener todos los registros de la Vista TMCargos
def get_all_vtmcargos():
    #PASO 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()


    #PASO 2 ---> Se construye la consulta SQL
    #sql = "SELECT * FROM tmcargos WHERE fkcods = 1;"
    sql ="select * from tmcargos;"

    #PASO 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql,  )
    resultado = cursor.fetchall()  #fetchone() ---> Retorna un solo registro
    codigo_conexion = conexion.commit()

    #PASO 4 ---> Se cierra la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 5 ---> Retornar resultado
    return resultado


# Obtener todos los registros de TMStatus
def get_all_status():
    #PASO 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()


    #PASO 2 ---> Se construye la consulta SQL
    sql = "SELECT * FROM tmstatus;"
   

    #PASO 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql,  )
    resultado = cursor.fetchall()  #fetchone() ---> Retorna un solo registro
    codigo_conexion = conexion.commit()

    #PASO 4 ---> Se cierra la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 5 ---> Retornar resultado
    return resultado


#Agregar un cargo Nuevo
def add_tmcargo(xdcargo , xsueldo):
    #PASO 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()


    #PASO 2 ---> Se construye la consulta SQL
    sql = "INSERT INTO tmcargos(dcargo, sueldo) VALUES (%s, %s);"
    datos = (xdcargo, xsueldo)


    #PASO 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql, datos)
    codigo_conexion = conexion.commit()

    #PASO 4 ---> Se cierra la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 5 ---> Retornar resultado
    return codigo_conexion


#Eliminación lógica de un cargo
def set_delete_tmcargo(xcodcar):
    #PASO 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()


    #PASO 2 ---> Se construye la consulta SQL
    sql = "UPDATE tmcargos SET fkcods =  %s  WHERE codcar = %s ;"
    datos = ("0",xcodcar)


    #PASO 3 ---> Se ejecuta la consulta SQL
    respuesta = cursor.execute(sql, datos)
    codigo_conexion = conexion.commit()

    #PASO 4 ---> Se cierra la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 5 ---> Retornar resultado
    return respuesta


#Buscar los datos del cargo por medio del código del cargo
def get_cargo_by_codcar(xcodcar):
    print("Código del Cargo en Modelo TMCargos ---> " + str(xcodcar))
    #PASO 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()


    #PASO 2 ---> Se construye la consulta SQL
    sql = "SELECT * FROM tmcargos  WHERE codcar = %s "
    datos = (xcodcar, )


    #PASO 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql, datos)
    resultado = cursor.fetchone()  #fetchone() ---> Retorna un solo registro / fetchall() ---> Retorna un solo registro
    codigo_conexion = conexion.commit()

    #PASO 4 ---> Se cierra la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 5 ---> Retornar resultado
    return resultado



#Modificar los datos de un cargo
def set_modificar_tmcargo(xcodcar, xdcargo, xsueldo, xfkcods):
    #PASO 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()


    #PASO 2 ---> Se construye la consulta SQL
    sql = "UPDATE tmcargos SET  dcargo = %s, sueldo = %s, fkcods =  %s  WHERE codcar = %s ;"
    datos = (xdcargo, xsueldo, xfkcods, xcodcar )


    #PASO 3 ---> Se ejecuta la consulta SQL
    respuesta = cursor.execute(sql, datos)
    codigo_conexion = conexion.commit()

    #PASO 4 ---> Se cierra la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 5 ---> Retornar resultado
    return respuesta