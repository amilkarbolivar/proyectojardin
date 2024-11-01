#app.py ---> Este archivo es el que va acontrolar toda la aplicación
#Autor: Sergio Capacho
#Fecha: Jueves 10/Oct/2024 - 09:00 Am



#01.- INICIO IMPORTACIÓN DE LIBRERIAS..........................
#......................................................................
#Importación de todos los paquete de la libreria OS 
#       la cual se usa para el Manejo del sistema operativo
import os 


#Importación desde la libreria flask  todos los paquetes/clases Flask  
from flask import Flask


#Importación desde la librería flask los paquetes/clases url_for
#       Esta clase se usa para trabajar rutas y archivos staticos 
from flask import url_for


#Importación desde la libreria flask el paquete render_template
#       la cual permite renderizar (Construir) la página
from flask import render_template 


#Importación desde la librería psycopg2 el paquete connect
#      que permite tiene los driver para establecer la conección con la Base de Datos PostGreSQL
from psycopg2 import connect


#Importación desde la libreria modelo_datos la función cadenaConexion
#       la cual permite establece la conexión con la Base de Datos
from models.modelo00_datos import cadenaConexion


#Importación desde la libreria flask  el paquete session
#       Se usa para crear y trabajar con las variables de session de Flask
#NOTA: Las variables de sessión se pierden al momento que se cierra el navegador
from flask import session


#Importación desde la libreria flask el paquete redirect
#       El cual le permite redireccionar y mostrar información
from flask import redirect


#Importación desde la librería flask el paquete request
#       La cual permite recibir o enviar datos desde una pagina web (Formularios)
from flask import request





#02.- INICIO IMPORTACIÓN DE PAQUETES Blueprints.........
#......................................................................
#02.01 ---> Importación el objeto tmcargos del del paquete bp01_tmcargos
#               que esta en la carpeta blueprints (Controlador)
from blueprints.bp01_tmcargos import obj_tmcargos
from blueprints.bp01_tmreportes import obj_tmreportes




#03.- INICIO DE LA CREACIÓN DE LA APLICACIÓN..................
#......................................................................
#Creación y asignación de la aplicación 
mi_app = Flask(__name__) 



#04.- CREACIÓN DE LA LLAVE SECRETA ..................
#......................................................................
#Creación de la llave secreta para el usos de la variables de session
mi_app.secret_key="practica"






#05.- INICIO DE LA CREACIÓN DE LAS RUTAS ..................
#......................................................................



#05.01.- RUTAS DEL MENÚ PRINCIPAL......
#........................................................
#RUTAS RAIZ ----> / 
@mi_app.route('/') 
def inicio(): 
    return render_template('sitio/index.html')


#RUTA PRODUCTOS ---> /productos
@mi_app.route('/productos')
def productos():
    return render_template('sitio/01productos.html')
    

    
#RUTA CURSOS ---> /cursos
@mi_app.route('/cursos') 
def cursos(): 
    return render_template('sitio/02cursos.html')



#RUTA GALERIA ---> /galeria
@mi_app.route('/galeria') 
def galeria(): 
    return render_template('sitio/03galeria.html')  






#05.02.- RUTAS DEL LOGIN ......
#........................................................

#RUTA LOGIN  ---> /login
@mi_app.route('/login') 
def login_formulario(): 
    xmensaje = " "
    return render_template('admin/p01_login00.html', mensaje = xmensaje) 



@mi_app.route('/login', methods = ['POST', 'GET'])
def login_validacion():
    _usuario = request.form['txt_usuario'].upper()    
    _clave = request.form['txt_clave']


    #Conversiones de texto
    #Var_texto.upper() ----------> Convertir a mayúsculas
    #Var_texto.lower() ----------> Convertir a minúsculas  
    #Var_Texto.capitalize() -----> Convertir solo la primera letra de un texto a mayúsculas


    #PASO 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()


    #PASO 2 ---> Se construye la consulta SQL
    sql = "SELECT * FROM tmusuarios WHERE (nom_u = %s)  AND (clave_u = %s) ;"
    datos = (_usuario, _clave)

    #PASO 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql, datos)
    resultado = cursor.fetchall()  #fetchone() ---> Retorna un solo registro
    codigo_conexion = conexion.commit()

    #PASO 4 ---> Se cierra la conexión con la base de datos 
    cursor.close()
    conexion.close()

 

    #print("Salida........................................")
    #print("Cantidad de registros recuperados ---> " + str(len(resultado) ))
    #print("¿La Lista esta llena? ---> " , bool(resultado))

    #NOTA: MUY IMPORTANTE TENER PRESENTE CUANDO SE EJECUTA UNA CONSULTA
    #1.- El resultado de la consulta el una TUPLA dentro de una LISTA
    #print("Resultado de la consulta --------------------> " , resultado)        # -------> [(4, 'SERGIO', 'CUATRO', '1234', 4)]     
    #print("El Tipo de dato de la Resultado -------------> " , type(resultado))  # Tipo --> <class 'list'>

    #2.- Para extraer el dato 
    #2.1.- primero se extrae el dato de la LISTA 
    #print("Elemento de la lista Resultado[0] ------------> " + str(resultado[0])) # ---> (4, 'SERGIO', 'CUATRO', '1234', 4)
    #print("Tipo de dato de la lista Resultado[0] -------> " , type(resultado[0])) # Tipo --> <class 'tuple'>

    #2.2.- y luego se extra eñ elemento de la TUPLA
    #print("Numero ------> " + str(resultado[0][0]))
    #print("Nombre ------> " + str(resultado[0][1]))
    #print("Usuario -----> " + str(resultado[0][2]))
    #print("Clave -------> " + str(resultado[0][3]))
    #print("Nivel -------> " + str(resultado[0][4]))

    if bool(resultado) :  #bool(resultado): Si la lista esta llena ---> True / Vacia ---> False
        #Asignación de valores a variables se sessión
        session["login"]=True
        session["xape"] = resultado[0][1]
        session["xusuario"]=resultado[0][2]
        session["xnivel"]=resultado[0][4]
        xmensaje = " "
        return render_template('admin/p02_login00.html')
    else:
        xmensaje = "¡¡¡ Acceso Denegado !!!"
        return render_template('admin/p01_login00.html', mensaje = xmensaje)



@mi_app.route('/login/cerrar')
def login_cerrar():
    #Cerrando y limpiar las variables de session
    session.clear()
    return render_template('sitio/index.html') 


@mi_app.route('/admin/menup')
def menu_principal():
    return render_template('admin/p03_menup00.html')





#05.03.- RUTAS PARA EL MÓDULO TMCARGOS ......
#........................................................
#   Registrando el Blueprints de TMCargos
mi_app.register_blueprint(obj_tmcargos, url_prefix='/tmcargos') 
mi_app.register_blueprint(obj_tmreportes, url_prefix='/reportes') 










#06.- PUESTA EN EJECUCIÓN DEL APLICATIVO ..................
#......................................................................
#   Validación del  programa principal
#   Creación del programa Debug (Depurador)
if __name__ == '__main__':
    mi_app.run(host="127.0.0.1", port = 5000, debug=True)



