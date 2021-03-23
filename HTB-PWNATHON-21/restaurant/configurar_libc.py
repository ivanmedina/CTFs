#! /usr/bin/python3
from pwn import *
import requests
import sys

'''
Procesamiento de argumentos.
argv[1] = ruta del binario
argv[2] = ruta del libc
'''
if(len(sys.argv) != 3):
    print("Uso : %s <ruta-binario> <ruta-libc>" % sys.argv[0])
    exit()

ruta_libc = sys.argv[2]
ruta_binario = sys.argv[1]
log.info("Leyendo libc")
context.binary = ruta_libc

DIR_DESCARGAS = "archivos_libc"

'''
Muestra mensaje de advertencia sobre los archivos a sobreescribir
'''
def advertencia(version_corta):
    log.warning("Se va a sobreescribir los archivos : ")
    log.warning("./libc.so.6")
    log.warning("./ld-" + version_corta + ".so")
    log.warning("./libc-" + version_corta + ".so.debug")
    log.warning("./ld-" + version_corta + ".so.debug")
    log.warning("Y se parchara el binario : " + ruta_binario)
    progreso = log.progress("CTRL-C si desea cancelar")
    TIEMPO_ESPERA = 3
    for i in range(TIEMPO_ESPERA):
        progreso.status("%ds restantes" % (TIEMPO_ESPERA - i))
        import time; time.sleep(1)
    progreso.success("CONTINUANDO")

'''
Obtener la cadena que representa la version de libc. Por ejemplo
2.23-0ubuntu11.2
Buscaremos primero la palabra 'ubuntu' y despues ir obteniendo la
cadena completa.
'''
def obtener_libc_version():
    try:
        pos_ubuntu = next(context.binary.search(b"ubuntu"))
    except:
        log.error("No se pudo encontrar la version de libc")

    ini_cad = pos_ubuntu
    while(context.binary.read(ini_cad, 1) != b' '):
        ini_cad -= 1
    ini_cad += 1

    tam_cad = 1
    while(context.binary.read(ini_cad + tam_cad, 1) != b')'):
        tam_cad += 1
    return bytes.decode(context.binary.read(ini_cad, tam_cad))

'''
Verificar que la pagina dada por el URL existe.
'''
def existe_pagina(url):
    r = requests.get(url)
    rc = r.status_code
    r.close()
    return rc == 200

'''
Obtener URL del libc a partir de una cadena de version
Por ejemplo:
2.23-0ubuntu5 -> https://launchpad.net/ubuntu/xenial/amd64/libc6-dbg/2.23-0ubuntu5 
'''
def obtener_url(libc_version):
    distros = ["precise", "trusty", "xenial", "bionic", "focal", "eoan", "groovy"]
    progreso = log.progress("Buscando URL del libc")
    for distro in distros:
        url = "https://launchpad.net/ubuntu/" + distro + "/" + context.arch + "/libc6/" + libc_version
        if(existe_pagina(url)):
            progreso.success("Listo")
            return url
    progreso.failure("Distro no encontrada")
    log.error("No se pudo encontrar el url del libc")

'''
Descarga el .deb del libc dado el URL del libc.
Busca en la pagina (html) el nombre del deb y desde ahi
avanza hacia atras para encontrar el url completo.
Regresa el nombre del archivo descargado.
'''
def descarga_libc(url, libc_version, version_debug=False):
    nombre_deb = "libc6_" + libc_version + "_" + context.arch + ".deb"
    if(version_debug):
        url = url.replace("/libc6/", "/libc6-dbg/")
        nombre_deb = nombre_deb.replace("libc6_", "libc6-dbg_")

    r = requests.get(url)
    ini_cad = r.text.find(nombre_deb)
    fin_cad = ini_cad + len(nombre_deb)
    # Avanzando hacia atras hasta tener el http
    while(r.text[ini_cad:fin_cad][:4] != "http"):
        ini_cad -= 1

    url_descarga = r.text[ini_cad:fin_cad]
    r.close()

    progreso = log.progress("Descargando " + nombre_deb)
    r = requests.get(url_descarga)
    if(r.status_code != 200):
        progreso.failure("Error")
        log.error("No se pudo obtener el URL de descarga del .deb")

    progreso.status("Descarga completa. Escribiendo archivo")
    with open("./" + DIR_DESCARGAS + "/" + nombre_deb, "wb") as f:
        f.write(r.content)
    r.close()
    progreso.success("Listo")
    return nombre_deb

'''
Muestra y ejecuta el comando
'''
def ejecuta_comando(comando):
    log.info(comando)
    if(os.system(comando) != 0):
        log.error("Error al ejecutar el comando : " + comando)

'''
Extrae del .deb los archivos libc y ld.
'''
def extrae_libc(nombre_deb, version_corta, version_debug=False):
    ruta_desc = "./" + DIR_DESCARGAS + "/"
    ruta = ruta_desc + nombre_deb
    log.info("Extrayendo .deb")
    ejecuta_comando("dpkg-deb -x " + ruta + " " + ruta_desc)

    ruta_libs = ruta_desc + "lib/x86_64-linux-gnu/"
    if(version_debug): ruta_libs = ruta_desc + "usr/lib/debug/lib/x86_64-linux-gnu/"

    nombre_libc = "libc-" + version_corta + ".so"
    nombre_ld = "ld-" + version_corta + ".so"
    if(version_debug):
        ejecuta_comando("mv " + ruta_libs + nombre_libc + " ./" + nombre_libc + ".debug")
        ejecuta_comando("mv " + ruta_libs + nombre_ld + " ./" + nombre_ld + ".debug")
    else:
        ejecuta_comando("mv " + ruta_libs + nombre_libc + " ./libc.so.6")
        ejecuta_comando("mv " + ruta_libs + nombre_ld + " ./" + nombre_ld)

    log.info("Limpiando")
    ejecuta_comando("rm -r ./" + DIR_DESCARGAS)

'''
Modifica el .dbg_link de libc y ld
'''
def enlaza_libcs(version_corta):
    nombre_libc = "libc-" + version_corta + ".so"
    nombre_ld = "ld-" + version_corta + ".so"
    ejecuta_comando("objcopy --remove-section .gnu_debuglink ./libc.so.6")
    ejecuta_comando("objcopy --add-gnu-debuglink=./" + nombre_libc + ".debug ./libc.so.6")
    ejecuta_comando("objcopy --remove-section .gnu_debuglink ./" + nombre_ld)
    ejecuta_comando("objcopy --add-gnu-debuglink=./" + nombre_ld + ".debug ./" + nombre_ld)

'''
Modifica el interprete y el rpath del binario para utilizar
los descargados.
'''
def parcha_binario(version_corta):
    ejecuta_comando("patchelf --set-interpreter ./ld-" + version_corta + ".so " + ruta_binario)
    ejecuta_comando("patchelf --set-rpath . " + ruta_binario)

if __name__ == "__main__":
    version = obtener_libc_version()
    version_corta = version.split("-")[0]
    advertencia(version_corta)

    log.info("Version de libc : " + version)

    url = obtener_url(version)
    log.info("URL de libc : " + url)

    log.info("Obteniendo archivos de libc")
    ejecuta_comando("mkdir " + DIR_DESCARGAS)
    nombre_deb = descarga_libc(url, version)
    extrae_libc(nombre_deb, version_corta)

    log.info("Obtienen archivo de libc-dbg")
    ejecuta_comando("mkdir " + DIR_DESCARGAS)
    nombre_deb = descarga_libc(url, version, True)
    extrae_libc(nombre_deb, version_corta, True)

    log.info("Enlazando archivos de libc")
    enlaza_libcs(version_corta)

    log.info("Parchando binario")
    parcha_binario(version_corta)
