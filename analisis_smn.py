import sys
from funciones_smn import (observaciones, cantidad_c, cantidad_c_completas, datos_faltantes, top_ciudades, horarios)

def mostrar_resumen(observ, lineas_i):
    """Imprime por pantalla el resumen con todas las características calculada"""
    if not observ:
        print("no se encontraron datos para imprimir")
        return
    print("RESUMEN DE OBSERVACIONES SMN")
    print("total de ciudades leidas: ", cantidad_c(observ))
    print("ciudades con datos completos: ", cantidad_c_completas(observ))
    print("lineas descartadas/ mal formadas", lineas_i)
    print("horarios obtenidos: ", horarios(observ))

    faltantes, afectados= datos_faltantes(observ)
    print("datos faltantes por campo: ", faltantes)
    print("estaciones afectadas por campo: ", afectados)

    print("Extremos:")
    print("temperatura max: ",top_ciudades(observ, "temperatura", n=1, descendente=True)[0])
    print("temperatura min: ", top_ciudades(observ, "temperatura", n=1, descendente=False)[0])
    print("viento maximo: ", top_ciudades(observ, "velocidad_viento", n=1, descendente= True)[0])
    print("viento minimo: ", top_ciudades(observ, "velocidad_viento", n=1, descendente=False)[0])

    print("Ranking (top 5):")
    print("top 5 temperaturas mas calidas: ", top_ciudades(observ, "temperatura", n=5, descendente=True))
    print("top 5 tempertauras mas frias: ", top_ciudades(observ, "temperatura", n=5, descendente= False))
    print("top 5 con mas viento: ", top_ciudades(observ, "velocidad_viento", n=5, descendente= True))
    print("top 5 con menos viento: ", top_ciudades(observ, "velocidad_viento", n=5, descendente= False))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta= sys.argv[1]
        dato, invalido= observaciones(ruta)
        mostrar_resumen(dato, invalido)
    else:
        print("falta indicar el archivo")
