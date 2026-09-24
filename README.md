Trabajo Practico - Lectura y caracterizacion de observaciones meteorologicas del SMN

Este proyecto consiste en construir una herramienta de linea de comandos desde Python para leer, procesar y analizar datos meteorologicos del SMN. Se organizan los datos por ciudad/ estacion, identifica registros incompletos, columnas ausentes o filas mal formadas, y genera un resumen estadistico con metricas y rankigs de temperaturas y vientos

Para obtener los datos necesarios de debe de:
- ingresar a la pagina de descarga del SMN <https://www.smn.gob.ar/descarga-de-datos> 
- descargar el archivo comprimido ('.rar') correspondiente a  **observaciones actuales**
- descomprimir el archivo '.rar'
- guardar el archivo '.txt' resultante dentro de la carpeta 'datos' del proyecto.

como se ejecuta:
desde la terminal de debe de ejecutar: python analisis_smn.py datos/observaciones_smn.txt
ejemplo de resumen de observaciones:
RESUMEN DE OBSERVACIONES SMN
total de ciudades leidas:  105
ciudades con datos completos:  82
lineas descartadas/ mal formadas: 1

datos faltantes por campo:  {'sensacion_termica': 20, 'humedad': 3}
estaciones afectadas por campo:  {'sensacion_termica': ['Benito Juárez', 'Ezeiza'], 'humedad': ['Río Gallegos']}

Extremos:
temperatura max:  ('Tartagal', 32.5)
temperatura min:  ('Base Marambio', -12.4)
viento maximo:  ('Comodoro Rivadavia', 45.0)
viento minimo:  ('Calafate', 0.0)

Ranking (top 5):
top 5 temperaturas mas calidas:  [('Tartagal', 32.5), ('Ramon Lista', 31.0), ('Oran', 30.2), ('Resistencia', 29.8), ('Formosa', 29.5)]
top 5 tempertauras mas frias:  [('Base Marambio', -12.4), ('Ushuaia', -2.1), ('Río Grande', -1.0), ('Bariloche', 1.2), ('Esquel', 2.0)]
top 5 con mas viento:  [('Comodoro Rivadavia', 45.0), ('Río Gallegos', 38.0), ('Trelew', 32.0), ('Bahía Blanca', 28.0), ('Neuquén', 25.0)]
top 5 con menos viento:  [('Calafate', 0.0), ('San Luis', 0.0), ('La Rioja', 0.0), ('Catamarca', 2.0), ('Mendoza', 3.0)]