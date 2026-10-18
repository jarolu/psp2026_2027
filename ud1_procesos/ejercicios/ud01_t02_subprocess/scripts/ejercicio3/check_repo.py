# Utilidad para chequear el estado de un repositorio de Git

# Al ejecutar check_repo.py en un directorio que sea un repositorio de Git, la utilidad comprueba el estado del mismo generando una salida similar a esta:

# ========================================
# COMPROBACIÓN DEL REPOSITORIO
# ========================================

# Estado del repositorio:
# Repositorio limpio.

# Último commit:
# 8f31a2c Añadido ejercicio de subprocess

# Actualización del repositorio remoto:
# Fetch realizado correctamente.

# ========================================
# RESUMEN
# ========================================

# El repositorio no tiene cambios pendientes.
# La información del repositorio remoto se ha actualizado.


import subprocess
import sys


#Comandos de Git para comprobar el estado básico
git_status = ['git','status', '--porcelain']
git_log = ['git','log', '-1', '--oneline']
git_fetch = ['git', 'fetch']


#Comando de Git para comprobar la relacion entre el repo local y el repo remoto

git_log_completo = ['git', 'log', '--oneline', '--decorate']


estado_del_repo = "Repositorio limpio."
ultimo_commit = ""
estado_fecth = "Fetch realizado correctamente."
cambios_en_remoto = "El repositorio no tiene cambios pendientes."

dicc_claves_porcelain = {
    'M': "Modificado:",
    'A': "Añadido:",
    'R': "Renombrado:",
    'D': "Eliminado:",
    '??': "Sin seguimiento. Nuevo fichero en el área de trabajo:"
}

resultado_git_status = subprocess.run(git_status,capture_output=True, text=True, encoding="utf-8")

if resultado_git_status.returncode != 0: 
    print("No estás en un repositorio Git")
    sys.exit()

if resultado_git_status.stdout != "":
    estado_del_repo = ""
    for l in resultado_git_status.stdout.split("\n"):
        l= l.strip()
        if len(l)>0: 
            codigo = l.split()[0]
            if codigo in dicc_claves_porcelain:
                estado_del_repo+=dicc_claves_porcelain[codigo]+l[len(codigo):]+"\n"
            else:
                estado_del_repo+=l

resultado_git_log= subprocess.run(git_log,capture_output=True, text=True, encoding="utf-8")

if resultado_git_log.returncode != 0: 
    print("No estás en un repositorio Git")
    sys.exit()

ultimo_commit = resultado_git_log.stdout.split()
ultimo_commit = ultimo_commit[0]+" "+" ".join(ultimo_commit[2:])

resultado_git_fetch= subprocess.run(git_fetch,capture_output=True, text=True, encoding="utf-8")

if resultado_git_fetch.returncode != 0: 
    print("No se pudo recuperar información del repositorio remoto")
    print(resultado_git_fetch.stdout)
    sys.exit()

if resultado_git_fetch.stdout != "":
    cambios_en_remoto = resultado_git_fetch.stdout

### Ampliación comparación entre el último commit actual y el ultimo remoto
### Objetivo: recorrer las lienas del git log y ver que apuntadores aparecen antes, o si apuntan al mismo commit

### Se asume que la utilidad solo tarbaja con la rama main
str_puntero_area_de_trabajo = "HEAD"
str_puntero_repo_local = "main"
str_puntero_repo_remoto = "origin/main"

puntero_area_de_trabajo = -1
puntero_repo_local = -1
puntero_repo_remoto = -1


resultado_git_log_completo = subprocess.run(git_log_completo, capture_output=True, text=True, encoding="utf-8")
lineas = resultado_git_log_completo.stdout.splitlines()

for l, index in zip(lineas, range(len(lineas))):
    partes = l.split()
    linea_commit_sin_id = " ".join(partes[1:])
    if linea_commit_sin_id.startswith("(") : 
        bloque_punteros = linea_commit_sin_id[1:linea_commit_sin_id.find(")")]
        punteros = list(map(lambda cad: cad.strip(), bloque_punteros.replace("->",",").split(",")))

        if str_puntero_repo_local in punteros:
            puntero_repo_local = index
        if str_puntero_area_de_trabajo in punteros:
            puntero_area_de_trabajo = index
        if str_puntero_repo_remoto in punteros:
            puntero_repo_remoto = index

### Posibles estados

### No aparece el puntero main => HEAD apunta a un commit antiguo en el histórico => Mensaje para el usuario: "No estás en el último commit de tu repo local, ubícate en el antes de empezar a trabajar"  => No analizar los otros punteros

### HEAD == main y (HEAD -> main) < origin/main => "Tu repositorio local se encuentra por delante del repositorio remoto. Recuerda enviar los cambios al repositorio remoto"

### HEAD == main y (HEAD -> main) > origin/main => "Tu repositorio local está por detrás del repositorio remoto. Incorpora los cambios del repositorio remoto a tu rama local antes de empezar a trabajar"

if puntero_repo_local == -1 or puntero_repo_local != puntero_area_de_trabajo:
    cambios_en_remoto = "No estás en el último commit de tu repo local, ubícate en el antes de empezar a trabajar"
    print(f"indx repo local{puntero_repo_local} indx area de trabajo {puntero_area_de_trabajo}")
elif puntero_repo_local == puntero_area_de_trabajo:

    if puntero_repo_local < puntero_repo_remoto:
        cambios_en_remoto = "Tu repositorio local se encuentra por delante del repositorio remoto. Recuerda enviar los cambios al repositorio remoto"
    elif puntero_repo_local > puntero_repo_remoto:
        cambios_en_remoto = "Tu repositorio local está por detrás del repositorio remoto. Incorpora los cambios del repositorio remoto a tu rama local antes de empezar a trabajar"
    else:
        cambios_en_remoto+="\nEl repositorio remoto y local están sincronizados."


print(f"""========================================
COMPROBACIÓN DEL REPOSITORIO
========================================

Estado del repositorio:
{estado_del_repo}

Último commit:
{ultimo_commit}

Actualización del repositorio remoto:
{estado_fecth}

========================================
RESUMEN
========================================

{cambios_en_remoto}
La información del repositorio remoto se ha actualizado.""")