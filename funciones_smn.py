from datetime import datetime
import json
import os
import glob

meses= {
    "enero": 1, "febrero":2, "marzo":3, "abril": 4, "mayo": 5, "junio":6, "julio":7, "agosto":8,
    "septiembre":9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
def fecha_hora(fecha_str, hora_str):
    fechas= fecha_str.strip().split('-')
    m= fechas[0].strip()
    m1=fechas[1].strip().lower()
    m2=fechas[2].strip()
    if len(m) == 4:
        year= int(m)
        mes= int(m1) if m1.isdigit() else meses[m1]
        dia= int(m2)
    else:
        dia = int(m)
        mes= int(m1) if m1.isdigit() else meses[m1]
        year= int(m2)

    horas= hora_str.strip().split(':')
    hora= int(horas[0])
    minutos= int(horas[1])
    return datetime(year, mes, dia, hora, minutos)


def viento(campo_viento):
    """ 
    convierte el dato 'Norte 3' en ('Norte', 3.0).
    en caso de que sea 'Calma', se le asignara un valor de 0.0
    """
    campo_viento = campo_viento.strip()

    if campo_viento.lower() == 'calma':
        return("Calma", 0.0)
    partes= campo_viento.split()

    if len(partes) >= 2:
        v_texto = partes[-1]
        dire= " ".join(partes[:-1])
        try:
            velo= float(v_texto)
            return(dire, velo)
        except ValueError:
            return(campo_viento, None)
        
    return(campo_viento, None)

def st_float(texto):
    "convierte texto a float, sacando las barras '/', guiones y 'nose calcula'"
    texto= texto.strip().replace('/', '').strip()
    if texto == "" or texto == "-" or texto.lower()== "no se calcula":
        return None
    try:
        return float(texto)
    except ValueError:
        return None

def dectectar_codificaciones(ruta):
    """detecta si el archivo esta en utf-8 o latin-1"""
    for enc in ('utf-8', 'latin-1'):
        try:
            with open(ruta, 'r', encoding=enc) as f:
                f.read()
            return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'

def observaciones(ruta):
    """lee el archivo y devuelve un dict con las observaciones por ciudad y el total de lineas 
    mal formadas"""
    observ = {}
    lineas_i= 0
    enc = dectectar_codificaciones(ruta)

    try:
        with open(ruta, 'r', encoding=enc) as file:
            for x in file:
                linea= x.strip()
                if not linea:
                    continue

                campos= linea.split(";")
                if len(campos) != 10:
                    lineas_i += 1
                    continue

                ciudad= campos[0].strip()
                if not ciudad:
                    lineas_i += 1
                    continue

                dire_v, veloc_v= viento(campos[8])

                observ[ciudad]= {
                    "fecha_y_hora": fecha_hora(campos[1], campos[2]),
                    "condicion": campos[3].strip(),
                    "visibilidad": campos[4].strip(),
                    "temperatura": st_float(campos[5]),
                    "sensacion_termica": st_float(campos[6]),
                    "humedad": st_float(campos[7]),
                    "direccion_viento": dire_v,
                    "velocidad_viento": veloc_v,
                    "presion": st_float(campos[9])
                }
    except  FileNotFoundError:
      print("error: no se encontro el dato en ", ruta)
    return observ, lineas_i
   
def cantidad_c(observ):
    """ devuelve el total de ciudades leidas"""
    return len(observ)

def cantidad_c_completas(observ):
    """ devuelve la cantidad de ciudades sin ningun dato faltante"""
    completas = 0
    for datos in observ.values():
        if None not in datos.values():
            completas += 1
    return completas

def datos_faltantes(observ):
    """calcula la cantidad de datos faltantes por cada campo"""
    faltantes= {}
    e_campo= {}
    for ciudad, datos in observ.items():
        for campo, valor in datos.items():
            if valor is None:
                faltantes[campo]= faltantes.get(campo, 0) +1
                if campo not in e_campo:
                    e_campo[campo]= []
                e_campo[campo].append(ciudad)
    return faltantes, e_campo

def top_ciudades(observ, campo, n=5, descendente= True):
    """ devuelve las n ciudades ordenadas segun 'campo' de mayor a menor """
    validos= []
    for ciudad, datos in observ.items():
        if datos.get(campo) is not None:
            validos.append((datos[campo], ciudad))
    validos.sort(reverse=descendente)
    resultado= []
    for valor, ciudad in validos[:n]:
        resultado.append((ciudad, valor))
    return resultado

def horarios(observ):
    horario= set()
    for datos in observ.values():
        dt= datos.get("fecha_y_hora")
        if isinstance(dt,datetime):
            horario.add(dt.strftime("%H:%M"))
    return sorted(list(horario))

parsear_fecha_hora = fecha_hora
separar_viento = viento

def leer_observaciones(ruta):
    return observaciones(ruta)[0]

def leer_observaciones_json(ruta):
    "lee un archivo .json guardado antes en obs_json"
    with open(ruta, 'r', encoding='utf-8') as f:
        observ = json.load(f)
    print("archivo leido")
    return observ

def convertir_a_json(observ):
    "convierte las fechas datetime a formato ISO 8601 sin segundos"
    observ_j= {}
    for ciudad, datos in observ.items():
        datoss= datos.copy()
        if isinstance(datoss.get('fecha_y_hora'), datetime):
            datoss["fecha_y_hora"] = datoss["fecha_y_hora"].isoformat(timespec= 'minutes')
        observ_j[ciudad] = datoss
    return observ_j

def guardar_c_json(ruta_txt, observ):
    """guarda el diccionario de observaciones en formato json en obs_j"""
    print("archivo SMN, convirtiendose a Json")

    d_destino= "obs_json"
    if not os.path.exists(d_destino):
        print(f"el diccionario {d_destino} no existe, procesando...")
        os.mkdir(d_destino)
        print("diccionario creado!")
    else:
        print(f"el diccionario {d_destino} ya existe")

    nomb_archivo = ruta_txt.replace("datos/", "").replace("datos\\", "")
    ruta_j= os.path.join(d_destino, nomb_archivo)
    observ_s= convertir_a_json(observ)

    try:
        with open(ruta_j, "w", encoding='utf-8') as f:
            json.dump(observ_s, f)
        print("archivo guardado correctactamente en", ruta_j)
    except Exception as e:
        print("error al guardad el archivo json: ", e)

def contar_archivo():
    """"""
    cant_txt = 0
    if os.path.exists("datos") and os.path.isdir("datos"):
        cant_txt = len([f for f in os.listdir("obs_json") if f[-4:] == ".txt"])
    cant_json= 0
    if os.path.exists("obs_json") and os.path.isdir("obs_json"):
        cant_json = len([f for f in os.path.isdir("obs_json") if f[-5:] == ".json"])
    return cant_txt, cant_json