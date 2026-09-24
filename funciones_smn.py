from datetime import datetime

meses= {
    "enero": 1, "febrero":2, "marzo":3, "abril": 4, "mayo": 5, "junio":6, "julio":7, "agosto":8,
    "septiembre":9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
def fecha_hora(fecha_str: str, hora_str: str) -> datetime:
    fechas= fecha_str.strip().split('-')
    dia= int(fechas[0])
    mes= meses[fechas[1].lower()]
    year= int(fechas[2])
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

def observaciones(ruta):
    """lee el archivo y devuelve un dict con las observaciones por ciudad y el total de lineas 
    mal formadas"""
    observ = {}
    lineas_i= 0
    try:
        with open(ruta, 'r') as file:
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
            validos.append((ciudad, datos[campo]))
    validos.sort(key=lambda x: x[1], reverse=descendente)
    return validos[:n]

def horarios(observ):
    horario= set()
    for datos in observ.values():
        dt= datos.get("fecha_y_hora")
        if isinstance(dt, datetime):
            horario.add(dt.strftime("%H:%M"))
    return sorted(list(horario))