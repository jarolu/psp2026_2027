# ejemplo de uso: python measure_command.py ping as.com
# salida esperada
#Ejecutando: ping as.com
#Salida del proceso:

# Haciendo ping a as.com [2.20.253.82] con 32 bytes de datos:
# Respuesta desde 2.20.253.82: bytes=32 tiempo=13ms TTL=55
# Respuesta desde 2.20.253.82: bytes=32 tiempo=13ms TTL=55
# Respuesta desde 2.20.253.82: bytes=32 tiempo=12ms TTL=55
# Respuesta desde 2.20.253.82: bytes=32 tiempo=12ms TTL=55

# Estadísticas de ping para 2.20.253.82:
#     Paquetes: enviados = 4, recibidos = 4, perdidos = 0
#     (0% perdidos),
# Tiempos aproximados de ida y vuelta en milisegundos:
#     Mínimo = 12ms, Máximo = 13ms, Media = 12ms


#Tarea terminada

#Tiempo de ejecución: 2.01 segundos
#Código de salida: 0

import subprocess
import sys
import time

argumentos = sys.argv[1:]
print(f"""
Ejecutando: {" ".join(argumentos)}
Salida del proceso:""")
inicio = time.perf_counter()
resultado = subprocess.run(argumentos, shell=True)
fin = time.perf_counter()
print(f"""
Tarea terminada

Tiempo de ejecución: {(fin-inicio):2.2f} segundos
Código de salida: {resultado.returncode}
""")

