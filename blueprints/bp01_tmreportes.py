#bp01_tmcargos.py: Programa controlador para TMCargos

#1.- IMPORTACIÓN DE LAS LIBRERIAS DE TRABAJO.....
from flask import  Blueprint, render_template, flash, redirect, url_for, request,  Flask
from psycopg2 import connect


#2.- IMPORTACIÓN DEL MODELO
#2.1.- Importación Base de Datos)
from models.modelo00_datos import cadenaConexion


#2.2.- Importación del archivo para majenar las operaciones SQL de tmcargos
from models.modelo_reportes import get_cedula_vtmreportes
from models.modelo_reportes import get_excusas
from models.modelo_reportes import agregar_retardo
from models.modelo_reportes import consulta_reportes
from models.modelo_reportes import reportes_por_fecha
#3.- Creacion del objeto tmcargos 
obj_tmreportes = Blueprint('reportes', __name__)


#4.- Operaciones SQL

#4.1.- Menú TMCargos
@obj_tmreportes.route('/menu')
def menu():
    return render_template('/reportes/reportes01.html')





@obj_tmreportes.route('/agregar')
def agregar01():
    return render_template('/reportes/reportes03.html')


@obj_tmreportes.route('/agregar_cedula', methods=['POST'])
def agregar_cedula():
    # Paso 1: Obtener la cédula del formulario
    cedula = request.form.get('cedula')

    # Paso 2: Llamar a la función del modelo para obtener información por cédula
    info = get_cedula_vtmreportes(cedula)
    return render_template('/reportes/reportes05.html', informacion = info)


#4.5.- Consultar un TMCargo
@obj_tmreportes.route('/consultar')
def consultar01():
    return render_template('/reportes/reportes06.html')

@obj_tmreportes.route('/reporte_fecha')
def fecha1():
    return render_template('/reportes/reportes08.html')

@obj_tmreportes.route('/agregar_reporte', methods=['GET', 'POST'])
def reporte():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        # Aquí puedes procesar la cédula como necesites
        print(f"Cédula recibida: {cedula}")  # Por ejemplo, imprimir en la consola
        # Redireccionar o hacer algo más después de recibir la cédula
        excusas =get_excusas()
        return render_template('/reportes/reportes04.html' ,ced=cedula, excusa=excusas)


@obj_tmreportes.route('/fecha', methods=['GET', 'POST'])
def reporte_fecha():
    if request.method == 'POST':
   
        fecha= request.form.get('fecha')
        fecha2= request.form.get('fecha2')
        reporte=reportes_por_fecha(fecha,fecha2)


        return render_template('/reportes/reportes09.html', reportes=reporte)

@obj_tmreportes.route('/agregar_reporte2', methods=['GET', 'POST'])
def reporte2():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        excusa = request.form.get('excusa')
        hora = request.form.get('hora')
        hora+=':00'
        fecha= request.form.get('fecha')
       
        succed=agregar_retardo(cedula,excusa,hora,fecha)
 
        return render_template('/reportes/reportes01.html',succed=succed)


@obj_tmreportes.route('/consultar_re', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        ced=request.form.get('cedula1')
        datos_retardos=consulta_reportes(ced)
        mensaje='no existe esta cedula'

        if datos_retardos:
            return render_template('/reportes/reportes07.html', datos=datos_retardos)
        else:
            return render_template('/reportes/reportes06.html',mensj=mensaje)