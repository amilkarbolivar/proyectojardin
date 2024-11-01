#bp01_tmcargos.py: Programa controlador para TMCargos

#1.- IMPORTACIÓN DE LAS LIBRERIAS DE TRABAJO.....
from flask import  Blueprint, render_template, flash, redirect, url_for, request,  Flask
from psycopg2 import connect


#2.- IMPORTACIÓN DEL MODELO
#2.1.- Importación Base de Datos)
from models.modelo00_datos import cadenaConexion


#2.2.- Importación del archivo para majenar las operaciones SQL de tmcargos
#		get_alumno_by_dni, get_alumno_by_id, get_all_alumnos, delete_alumno, add_alumno, update_alumno
from models.modelo01_tmcargos import get_all_vtmcargos, add_tmcargo, set_delete_tmcargo, get_cargo_by_codcar
from models.modelo01_tmcargos import set_modificar_tmcargo
from models.modelo01_tmcargos import get_all_status



#3.- Creacion del objeto tmcargos 
obj_tmcargos = Blueprint('tmcargos', __name__)


#4.- Operaciones SQL

#4.1.- Menú TMCargos
@obj_tmcargos.route('/menu')
def menu():
    return render_template('/tmcargos/tmcargos00_menu.html')


#4.2.- Reporte TMCargos
@obj_tmcargos.route('/reporte')
def reporte():
    xmensaje = " "
    datos = get_all_vtmcargos()
    return render_template('/tmcargos/tmcargos05_reporte.html', listadocargos = datos, mensaje = xmensaje)



#4.3.- Agregar un TMCargo
@obj_tmcargos.route('/agregar')
def agregar01():
    return render_template('/tmcargos/tmcargos02_agregar.html')


@obj_tmcargos.route('/agregar', methods=['GET', 'POST'])
def agregar02():
    xmensaje = " "
    if request.method == 'POST':
        dcargo = request.form['txt_descipcion'].upper()
        sueldo = request.form['txt_sueldo']
        add_tmcargo(dcargo , sueldo)
        xmensaje = "¡¡¡ " + dcargo + " fue Registrado con Éxito !!!"
    
   
    datos = get_all_vtmcargos()
    return render_template('/tmcargos/tmcargos05_reporte.html', listadocargos = datos, mensaje = xmensaje)


#4.4.- Eliminación lógica del un TMCargo
@obj_tmcargos.route('/eliminar/<int:xcodcar>')
def eliminar(xcodcar=None):
    xresp = set_delete_tmcargo(xcodcar)

    print("Respuesta en el controlador ---> " + str(xresp))
    if (xresp):
        xmensaje = "¡¡¡ Error al eliminar " + str(xcodcar) + " !!!"
    else:
        xmensaje = "¡¡¡ El código " + str(xcodcar) + " fue eliminado con Éxito !!!"

    print (" " + xmensaje)

    return redirect("/tmcargos/reporte")



#4.5.- Consultar un TMCargo
@obj_tmcargos.route('/consultar')
def consultar01():
    return render_template('/tmcargos/tmcargos03_consultar.html')


@obj_tmcargos.route('/consultar', methods=['GET', 'POST'])
def consultar02():
    if request.method == 'POST':
        xmen = " "
        xcodcar = request.form['txt_codcar'] 
        print("Código del Cargo en Controlador TMCargos ---> " + str(xcodcar))
        xcargo = get_cargo_by_codcar(xcodcar) 
        datos = get_all_status()
        if xcargo:
            xmen = "!!! Código " + str(xcodcar) + " Encontrado ¡¡¡"
        else:
            xmen = "!!! El Código " + str(xcodcar) + " No Existe ¡¡¡"


    return render_template('/tmcargos/tmcargos03_consultar.html', cargo = xcargo, mensaje = xmen, tmstatus = datos)


#4.6.- Modificar TMCargos
@obj_tmcargos.route('/modificar', methods=['GET', 'POST'])
def modificar():
    if request.method == 'POST':
        xmen = " "
        xcodcar = request.form['txt_codcar']
        xdcargo = request.form['txt_descipcion'].upper()
        xsueldo = request.form['txt_sueldo']
        xfkcods = request.form['txt_fkcods']
        
        #Enviando datos para la modificación
        xresp = set_modificar_tmcargo(xcodcar, xdcargo, xsueldo, xfkcods)

    return redirect("/tmcargos/reporte")