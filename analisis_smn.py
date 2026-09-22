import sys 
import zipfile

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
    "convierte texto a float, sacando las barras '/' y los espacios"
    texto= texto.strip().replace('/', '').strip()
    if texto == "" or texto == "-" or texto.lower()== "no se calcula":
        return None
    try:
        return float(texto)
    except ValueError:
        return None
    
def observaciones(ruta):
    """lee el archivo y devuelve un dict con las observaciones por ciudad"""
    observ = {}
    lineas= []
    try:
        if zipfile.is_zipfile(ruta):
            with zipfile.ZipFile(ruta, 'r') as file:
                n_archivo= file.namelist()[0]
                with file.open(n_archivo) as f:
                    lineas = [l.decode('latin-1', errors= 'ignore') for l in f]
        else:
            with open(ruta, 'r', encoding='latin-1', errors='ignore') as file:
                lineas = file.readlines()
        for x in lineas:
            linea= x.strip()
            if not linea:
                continue

            campos= linea.split(";")
            if len(campos) < 10:
                continue

            ciudad= campos[0].strip()
            if not ciudad:
                continue

            dire_v, veloc_v= viento(campos[8])

            observ[ciudad]= {
                "fecha": campos[1].strip(),
                "hora": campos[2].strip(),
                "condicion": campos[3].strip(),
                "visibilidad": campos[4].strip(),
                "temperatura": st_float(campos[5]),
                "sensacion_termica": st_float(campos[6]),
                "humedad": st_float(campos[7]),
                "direccion_del_viento": dire_v,
                "velocidad_del_viento": veloc_v,
                "presion": st_float(campos[9])
            }
    except  FileNotFoundError:
      print("error: no se encontro el dato en ", ruta)
    return observ   
   
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

def mostrar_resumen(observ):
    """Imprime por pantalla el resumen con todas las características calculada"""
    if not observ:
        print("no se encontraron datos para imprimir")
        return
    print("RESUMEN DE OBSERVACIONES SMN")
    print("total de ciudades leidas: ", cantidad_c(observ))
    print("ciudades con datos completos: ", cantidad_c_completas(observ))

    faltantes, e_campo= datos_faltantes(observ)
    print("datos faltantes por campo: ", faltantes)
    print("top 5 mas calidas: ", top_ciudades(observ, "temperatura", n=5, descendente=True))
    print("top 5 mas fria: ", top_ciudades(observ, "temperatura", n=5, descendente= False))
    print("top 5 con mas viento: ", top_ciudades(observ, "velocidad_del_viento", n=5, descendente= True))
    print("top 5 con menos viento: ", top_ciudades(observ, "velocidad_del_viento", n=5, descendente= False))
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta= sys.argv[1]
        datos= observaciones(ruta)
        mostrar_resumen(datos)
    else:
        print("falta indicar el archivo")
