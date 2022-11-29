# Importo las librerias necesarias para llevar a cabo el programa
import json
from git import Repo
import signal, sys, re

# Defino la función que va a gestionar el control c
def handler_signal(signal, frame): 
    print("\n\n [!] Out ........... \n") 
    # Imprimo por pantalla que el programa se cerrará
    sys.exit(1)  # Salgo del programa indicado que hubo algún problema

# gestiono el ctrl C
signal.signal(signal.SIGINT,handler_signal) 
# Defino la variable que indica el directorio en el que está el repositorio
DIRECTORIO_REPO = "./skale/skale-manager"
# Defino la variable que indica las palabras que pueden indicar una contraseña o un nombre de usuaio 
PALABRAS_IMPORTANTES = ['username', 'password', 'key', 'credentials', 'acess code', 'identification', 'countersign', 'signature']

def extract(DIRECTORIO_REPO): # Defino la función que va a extraer los datos que queremos del repositorio
    repositorio = Repo(DIRECTORIO_REPO) # Creo el repositorio como objeto de python
    ramas = repositorio.branches # Compruebo que ramas existen en el repositorio
    nombre_ramas = [rama.name for rama in ramas] # Para cada objeto rama del repositorio, guardo el nombre en una lista
    print(nombre_ramas) # Imprimo los nombres de las ramas
    mensajes = list(repositorio.iter_commits(nombre_ramas[0])) # Creo una lista con los commits de la rama que queremos analizar
    return mensajes # Devuelvo una lista con todos los commits cargados

def transform(mensajes): # Defino la función que transforma y filtra los datos
    informacion_relevante = {} # Creo un diccionario en el que vamos a almacenar los commits relevantes y la clave que cifra la información relevante
    for mensaje in mensajes: # Para cada commit buscamos si encontramos alguna de las palabras importantes definitas previamente
        for palabra in PALABRAS_IMPORTANTES: 
            if re.search(palabra, mensaje.message, flags = re.IGNORECASE): 
                # Si en el commit encuentro alguna de las palabras (sin tener en cuenta mayúsculas y minúsculas), entonces lo añado en el diccionario
                informacion_relevante[mensaje.hexsha] = mensaje.message 
                # El atributo hexsa indica la clave con la que se accede a los datos
                # El atributo message indica el mensaje del commit
    return informacion_relevante # Devuelvo la información importante

def load(informacion_relevante): # Defino al función que carga los datos en un json
    with open('git_leaks.json', 'w') as archivo: # Creo un archivo json en modo de escritura
        # Escribo en el json abierto el diccionario con los commits y las claves correspondientes a la informacion
        json.dump(informacion_relevante, archivo, indent= 3) 

if __name__ == "__main__":
    # Como estamos utilizando una estructura ETL defino las tres funciones
    mensajes = extract(DIRECTORIO_REPO) # Llamo a la función que extrae los datos 
    informacion_relevante = transform(mensajes) # Llamo a la función que transforma los datos
    load(informacion_relevante) # Llamo a la función que carga los datos en un json

