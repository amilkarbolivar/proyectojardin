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

def get_cedula_vtmreportes(cedula):
    # Paso 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # Paso 2 ---> Se construye la consulta SQL
    sql = """
SELECT 
    e.cedemple AS cedula,
    e.nomemple AS nombre,
    c.dcargo AS cargo
FROM 
    tmempleados e
JOIN 
    tdretardos r ON e.cedemple = r.fkcedemple
JOIN 
    tmcargos c ON e.fkcodcar = c.codcar
WHERE 
    r.fkcedemple = %s
GROUP BY 
    e.cedemple, e.nomemple, c.dcargo;
"""



    # Paso 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql, (cedula,))  # Usa una tupla para pasar parámetros
    resultado = cursor.fetchall()  # fetchall() para obtener todos los registros que coincidan

    # Paso 4 ---> Se cierra la conexión con la base de datos
    cursor.close()
    conexion.close()

    # Paso 5 ---> Retornar resultado
    return resultado

def get_excusas():
    # Paso 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # Paso 2 ---> Se construye la consulta SQL
    sql = """
    SELECT 
        codexcu AS codigo,
        dexcusa AS excusa
    FROM 
        tmexcusas;
    """

    # Paso 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql)  # No hay parámetros en esta consulta
    resultadoexcu = cursor.fetchall()  # fetchall() para obtener todos los registros que coincidan

    # Paso 4 ---> Se cierra la conexión con la base de datos
    cursor.close()
    conexion.close()

    # Paso 5 ---> Retornar resultado
    return resultadoexcu

def agregar_retardo(cedula,excusa, fecha,hora):
    # Paso 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # Paso 2 ---> Se construye la consulta SQL
    sql = """
    INSERT INTO tdretardos (fkcedemple, fkcodexcu, fecha, hora) 
    VALUES (%s, %s, %s, %s);
    """
    datos = (cedula,excusa,hora,fecha)

    # Paso 3 ---> Se ejecuta la consulta SQL
    try:
        cursor.execute(sql, datos)
        conexion.commit()  # Confirmar los cambios
        mensaje='agregado'
    except Exception as e:
        mensaje=(f"Error al agregar el retardo: {e}")
        conexion.rollback()  # Revertir los cambios en caso de error

    # Paso 4 ---> Se cierra la conexión con la base de datos
    cursor.close()
    conexion.close()

    # Paso 5 ---> Retornar resultado (opcional)
    return mensaje # Puedes cambiar esto según lo que necesites

def consulta_reportes(cedula):
    # Paso 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # Paso 2 ---> Se construye la consulta SQL
    sql = """
    SELECT 
        r.nr AS numero_reporte,
        r.fkcedemple AS cedula,
        e.nomemple AS nombre,
        ex.dexcusa AS excusa,   -- Selecciona la descripción de la excusa en lugar del código
        c.dcargo AS cargo,      -- Selecciona el nombre del cargo desde la tabla tmcargos
        r.fecha AS fecha_reporte,
        r.hora AS hora_reporte,
        s.dstatus AS estado
    FROM 
        tdretardos r
    JOIN 
        tmempleados e ON r.fkcedemple = e.cedemple
    JOIN 
        tmexcusas ex ON r.fkcodexcu = ex.codexcu
    JOIN 
        tmstatus s ON r.fkcods = s.cods
    JOIN 
        tmcargos c ON e.fkcodcar = c.codcar
    WHERE 
        r.fkcedemple = %s
    ORDER BY 
        r.fecha DESC, r.hora DESC;
    """

    # Paso 3 ---> Se ejecuta la consulta SQL
    cursor.execute(sql, (cedula,))  # Usa una tupla para pasar parámetros
    reportes = cursor.fetchall()  # fetchall() para obtener todos los registros que coincidan

    # Paso 4 ---> Se cierra la conexión con la base de datos
    cursor.close()
    conexion.close()

    # Paso 5 ---> Retornar resultado
    return reportes


def reportes_por_fecha(cedula, fecha, fecha2):
    # Paso 1 ---> Se establece la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # Paso 2 ---> Se construye la consulta SQL
    sql = """
    SELECT 
        r.nr AS numero_reporte,
        r.fkcedemple AS cedula,
        e.nomemple AS nombre,
        ex.dexcusa AS excusa,   -- Selecciona la descripción de la excusa
        c.dcargo AS cargo,      -- Selecciona el nombre del cargo desde la tabla tmcargos
        r.fecha AS fecha_reporte,
        r.hora AS hora_reporte,
        s.dstatus AS estado
    FROM 
        tdretardos r
    JOIN 
        tmempleados e ON r.fkcedemple = e.cedemple
    JOIN 
        tmexcusas ex ON r.fkcodexcu = ex.codexcu
    JOIN 
        tmstatus s ON r.fkcods = s.cods
    JOIN 
        tmcargos c ON e.fkcodcar = c.codcar
    WHERE 
         r.fkcedemple = %s AND 
         r.fecha BETWEEN %s AND %s
    ORDER BY 
        r.fecha DESC, r.hora DESC;
    """

    try:
        # Paso 3 ---> Se ejecuta la consulta SQL
        cursor.execute(sql, (cedula, fecha, fecha2))  # Usa una tupla para pasar parámetros
        reportes = cursor.fetchall()  # fetchall() para obtener todos los registros que coincidan
        
    except Exception as e:
        print(f"Error al consultar los reportes: {e}")
        reportes = []  # Retornar una lista vacía en caso de error

    finally:
        # Paso 4 ---> Se cierra la conexión con la base de datos
        cursor.close()
        conexion.close()

    # Paso 5 ---> Retornar resultado
    return reportes

