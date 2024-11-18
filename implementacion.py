import os
import re
import random
import json
# Función para registrar un nuevo usuario
def registrar_usuario(nombre_usuario, contrasenia):
    '''Función encargada del registro de nuevos usuarios en el sistema
       Parámetros de entrada: nombre_usuario (string con el nombre de usuario a registrar)
                             contrasenia (string con la contraseña del usuario)
       Variables de salida: No retorna valores. Almacena en credenciales.json el usuario con su id, nombre, 
                          contraseña y score inicial'''
    import json
    try:
        with open('credenciales.json', 'r', encoding='utf-8') as archivo_json:
            contenido = archivo_json.read()
            credenciales = json.loads(contenido) if contenido else {}
    except FileNotFoundError:
        credenciales = {}

    ultimo_id = max((int(usuario.get("id", 0)) for usuario in credenciales.values()), default=0)
    nuevo_id = ultimo_id + 1

    while nombre_usuario in credenciales:
        nombre_usuario = input("Ingrese un nombre de usuario único: ")

    credenciales[nombre_usuario] = {
        "id": nuevo_id,
        "nombre_usuario": nombre_usuario,
        "contraseña": contrasenia,
        "score": 0  # Inicializamos el puntaje en 0 al crear el usuario
    }
# Función para iniciar sesión
def iniciar_sesion(nombre_usuario, contrasenia):
    '''Función encargada de la validación de credenciales de usuarios existentes
       Parámetros de entrada: nombre_usuario (string con el nombre de usuario)
                             contrasenia (string con la contraseña)
       Variables de salida: flag_login (boolean True si las credenciales son correctas, False si son incorrectas)'''
    try:
        # Cargar el archivo JSON que contiene las credenciales
        with open('credenciales.json', 'r', encoding='utf-8') as archivo_json:
            credenciales = json.load(archivo_json)
    except FileNotFoundError:
        print("No se encontraron usuarios registrados.")
        return False
    except json.JSONDecodeError:
        print("Error al leer el archivo de credenciales.")
        return False

    # Verificar si el nombre de usuario existe y la contraseña es correcta
    if nombre_usuario in credenciales:
        if credenciales[nombre_usuario]['contraseña'] == contrasenia:
            print(f"Bienvenido, {nombre_usuario}!")
            return True
        else:
            print("Contraseña incorrecta.")
            return False
    else:
        print("El nombre de usuario no existe.")
        return False

        
def Buscolista_coincidencias(palabras):
    '''Función encargada de encontrar todas las coincidencias de letras entre las palabras
       Parámetros de entrada: palabras (lista de strings con las palabras disponibles para el juego)
       Variables de salida: resultado (diccionario con estructura {letra: {palabra: [indices]}} donde cada letra 
                          mapea a las palabras donde aparece y sus posiciones)'''

    lista_coincidencias = {}

    # Recorre cada palabra buscando lista_coincidencias de letras
    for palabra in palabras:
        palabra_str = ''.join(palabra)  # Convierte la lista de letras en una cadena de texto
        index = 0  # Índice manual

        while index < len(palabra):  # Itera por la palabra usando el índice manual
            letra = palabra[index]
            if letra not in lista_coincidencias:
                lista_coincidencias[letra] = []  # Crea la entrada para la letra si no existe
            lista_coincidencias[letra].append({
                'palabra': palabra_str,
                'indice': index  # Guarda el índice de la letra
            })
            index += 1  # Incrementa el índice manualmente

    # Filtrar letras que tienen más de una coincidencia ENTRE DISTINTAS PALABRAS
    letras_comunes = {}
    for letra, datos in lista_coincidencias.items():
        palabras_vistas = []
        for dato in datos:
            if dato['palabra'] not in palabras_vistas:
                palabras_vistas.append(dato['palabra'])
        
        # Si la letra aparece en más de una palabra diferente
        if len(palabras_vistas) > 1:
            letras_comunes[letra] = datos

    # Construir la salida mostrando lista_coincidencias agrupadas en diccionarios
    resultado = {}
    for letra, datos in letras_comunes.items():
        lista_coincidencias_letra = {}
        for dato in datos:
            palabra = dato['palabra']
            indice = dato['indice']
            if palabra not in lista_coincidencias_letra:
                lista_coincidencias_letra[palabra] = []
            lista_coincidencias_letra[palabra].append(indice)
        
        resultado[letra] = lista_coincidencias_letra

    # Retornar el resultado
    return resultado

def BuscarPrimerPalabra(lista):
    '''Función encargada de seleccionar la primera palabra del crucigrama
       Parámetros de entrada: lista (lista de strings con todas las palabras disponibles)
       Variables de salida: palabras_para_jugar (lista con un único string, palabra seleccionada aleatoriamente 
                          de 7 o más letras)'''
    palabras_para_jugar = []
    while len(palabras_para_jugar) == 0:
        palabra = random.choice(lista)
        if len(palabra) >= 7:
            palabras_para_jugar.append(palabra)
    return palabras_para_jugar

def definir_direccion(palabra,indice_coincidencia): 
    '''Función encargada de determinar la dirección de una palabra en el tablero
       Parámetros de entrada: palabra (string con la palabra a posicionar)
                             indice_coincidencia (entero con la posición de intersección)
       Variables de salida: flag_direccion (string "norte" o "sur" según la dirección calculada)'''
    flag_direccion = ""
    if len(palabra[:indice_coincidencia])  > len(palabra[indice_coincidencia + 1:]): #En el caso de que tenga más letras por encima o a la izquierda del punto de intersección, será de dirección "norte"
        flag_direccion = "norte" 
    elif len(palabra[:indice_coincidencia])  == len(palabra[indice_coincidencia + 1 :]): #En el caso que queden la misma cantidad de letras de ambos lados desde el punto de intersección, se asignará al azar
        
        random_flag = random.randint(1,2)
        if random_flag == 1:
            flag_direccion = "norte"
        else:
            flag_direccion = "sur"
            
    else: flag_direccion = "sur" #En el caso de tener más letras por debajo o a la derecha del punto de intersección, se asignará la dirección "sur"
    return flag_direccion
            
def calcularFila(fila_anterior,indice,direccion):
    '''Función encargada de calcular la fila para ubicar la siguiente palabra
       Parámetros de entrada: fila_anterior (entero con el número de fila actual)
                             indice (entero con la posición de coincidencia)
                             direccion (string con la orientación de la palabra)
       Variables de salida: fila_siguiente (entero con el número de fila calculado para la nueva palabra)'''

    #En todos los casos, se suma o resta 2 para compensar y evitar tener en cuenta que cada palabra comienza con: "Número", "-"
     
    #En caso de ser horizontal, se hará el calculo de filas a partir de la fila de inicio  y se suma el indice que ocupa en la primer palabra la letra que coincide 
    if direccion in ["horizontal-sur" ,"horizontal-norte"]:
        fila_siguiente = fila_anterior + indice + 2
    
    #En caso de ser vertical, se hará el calculo de filas a partir de la resta de la fila de inicio y el indice que ocupa la letra en la segunda palabra
    else: 
        fila_siguiente = fila_anterior - indice  - 2
    
   
    return fila_siguiente


def ConstruccionTableroVacio():
    '''Función encargada de crear la matriz inicial del tablero
       Parámetros de entrada: No recibe parámetros
       Variables de salida: tablero_vacio (matriz de 100x100 inicializada con espacios en blanco)'''

    filas = 100
    columnas = 100
    tablero_vacio = [[list(" ") for i in range(columnas)] for i in range(filas)]

    return tablero_vacio

def calcularColumna(columna_anterior,indice,direccion):
    '''Función encargada de calcular la columna para ubicar la siguiente palabra
       Parámetros de entrada: columna_anterior (entero con el número de columna actual)
                             indice (entero con la posición de coincidencia)
                             direccion (string con la orientación de la palabra)
       Variables de salida: columna_siguiente (entero con el número de columna calculado para la nueva palabra)'''
    #En todos los casos, se suma o resta 2 para compensar y evitar tener en cuenta que cada palabra comienza con: "Número", "-"


    #En caso de ser vertical, el calculo se hace a partir de la columna donde inicia la primer palabra y el indice donde se encuentra la letra coincidente en ella
    if direccion in ["vertical-norte","vertical-sur"]:
        columna_siguiente = columna_anterior + indice + 2
    #En caso de ser horizontal, el calculo se hace a partir de la resta de la columna anterior y el índice donde se encuentra la letra en la segunda palabra
    else:
        columna_siguiente = columna_anterior - indice - 2


   
    return columna_siguiente

def elegir_palabra_e_indice (diccionario,letra,palabras_partida,dependencia = "si",primer_indice = 0, segundo_indice = 1):
    '''Función encargada de seleccionar una palabra y su índice de coincidencia
       Parámetros de entrada: diccionario (dict con palabras y sus coincidencias)
                             letra (char con la letra coincidente a buscar)
                             palabras_partida (lista de palabras ya utilizadas)
                             dependencia (string "si"/"no" para verificar dependencias)
                             primer_indice (entero con posición inicial a verificar)
                             segundo_indice (entero con posición final a verificar)
       Variables de salida: siguiente_palabra (string con la palabra seleccionada)
                          indice_coincidencia (lista con los índices de coincidencia)'''
    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))

    if dependencia == "no":
        while siguiente_palabra in palabras_partida:
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))
    else:

        while (siguiente_palabra[primer_indice] != letra and siguiente_palabra[segundo_indice] != letra) or     siguiente_palabra in palabras_partida:
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))

    return siguiente_palabra, indice_coincidencia

def elegir_coincidencia (palabras_partida,indice_coincidencia,letra_palabra,indice_palabra,seleccion_posicion = "principio"):
    '''Función encargada de determinar los índices de coincidencia entre palabras
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             indice_coincidencia (lista de índices posibles)
                             letra_palabra (char con la letra coincidente)
                             indice_palabra (entero con la posición de la palabra)
                             seleccion_posicion (string con el criterio de selección)
       Variables de salida: coincidencias (lista [indice1, indice2] con las posiciones de coincidencia)'''

    
    if seleccion_posicion == "principio":
        if len(indice_coincidencia) == 1:
            coincidencias= [palabras_partida[indice_palabra].index(letra_palabra),indice_coincidencia[0]]
        else:
            indice_random = random.randint(0,len(indice_coincidencia) - 1)
            
            coincidencias=[palabras_partida[indice_palabra].index(letra_palabra),indice_coincidencia[indice_random]]
    
    elif seleccion_posicion == "final":
        if len(indice_coincidencia) == 1:
            coincidencias= [palabras_partida[indice_palabra].rindex(letra_palabra),indice_coincidencia[0]]
        else:
            indice_random = random.randint(0, len(indice_coincidencia) - 1)
            
            coincidencias=[palabras_partida[indice_palabra].rindex(letra_palabra),indice_coincidencia[indice_random]]
    
    
    elif seleccion_posicion == "principio-norte":
        if len(indice_coincidencia) == 1:
            coincidencias = [palabras_partida[indice_palabra].index(letra_palabra), indice_coincidencia[0]]
        else:
            coincidencias = [palabras_partida[indice_palabra].index(letra_palabra), indice_coincidencia[-1]]
    elif seleccion_posicion == "final-norte":
        if len(indice_coincidencia) == 1:
            coincidencias = [palabras_partida[indice_palabra].rindex(letra_palabra), indice_coincidencia[0]]
        else:
            coincidencias = [palabras_partida[indice_palabra].rindex(letra_palabra), indice_coincidencia[-1]]
    elif seleccion_posicion == "principio-sur":
        coincidencias = [palabras_partida[indice_palabra].index(letra_palabra), indice_coincidencia[0]]
    else:
        coincidencias = [palabras_partida[indice_palabra].rindex(letra_palabra), indice_coincidencia[0]]

    return coincidencias






def elegir_indice_y_letra(palabras_partida,indice_palabra,direccion = "norte"):
    '''Función encargada de seleccionar un índice y letra de una palabra según su dirección
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             indice_palabra (entero con la posición de la palabra)
                             direccion (string con la orientación deseada)
       Variables de salida: letra_palabra (char con la letra seleccionada de la palabra)'''
    if direccion == "norte":
        if len(palabras_partida[indice_palabra]) > 8:
            indice_letra_a_buscar = random.randint(0,2)
        else:
            indice_letra_a_buscar = 0

    else:
        if len(palabras_partida[indice_palabra]) > 8:
            indice_letra_a_buscar = random.choice([-1,-2,-3])
        else:
            indice_letra_a_buscar = -1
    
    letra_palabra = palabras_partida[indice_palabra][indice_letra_a_buscar]

    return letra_palabra

def logica_construccion_segunda_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias):
    '''Función encargada de implementar la lógica para la segunda palabra del crucigrama
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             diccionario (dict con coincidencias entre palabras)
                             lista_direcciones (lista de orientaciones actuales)
                             lista_coincidencias (lista de intersecciones actuales)
       Variables de salida: palabras_partida (lista actualizada con la nueva palabra)
                          lista_coincidencias (lista actualizada con nuevas coincidencias)
                          lista_direcciones (lista actualizada con nueva dirección)'''
    
    letra_palabra = elegir_indice_y_letra(palabras_partida,0)
    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,
    "no")
    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,0,"principio")

    flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
    lista_coincidencias.append(coincidencia)
    lista_direcciones.append("vertical-" + flag_direccion)
    palabras_partida.append(siguiente_palabra)
        
    return palabras_partida,lista_coincidencias,lista_direcciones
    
def logica_construccion_tercer_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias):
    '''Función encargada de implementar la lógica para la tercera palabra del crucigrama
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             diccionario (dict con coincidencias entre palabras)
                             lista_direcciones (lista de orientaciones actuales)
                             lista_coincidencias (lista de intersecciones actuales)
       Variables de salida: palabras_partida (lista actualizada con la nueva palabra)
                          lista_coincidencias (lista actualizada con nuevas coincidencias)
                          lista_direcciones (lista actualizada con nueva dirección)'''
    letra_palabra = elegir_indice_y_letra(palabras_partida,0,"sur")
    if lista_direcciones[1].count("norte"):
            flag_direccion = "sur"
            siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,
        "si",0,1)
            coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,0,"final-sur")
                
    else:
            flag_direccion = "norte"
            siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,
                                                                             "si", -1, -1)
            coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,0,"final-norte")
            
    lista_coincidencias.append(coincidencia)
    lista_direcciones.append("vertical-" + flag_direccion)
    palabras_partida.append(siguiente_palabra)
        
    return palabras_partida,lista_coincidencias,lista_direcciones
    
def logica_construccion_cuarta_y_quinta_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,indice_palabra_dependencia):
    '''Función encargada de implementar la lógica para la cuarta y quinta palabra
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             diccionario (dict con coincidencias entre palabras)
                             lista_direcciones (lista de orientaciones actuales)
                             lista_coincidencias (lista de intersecciones actuales)
                             indice_palabra_dependencia (entero con índice de palabra base)
       Variables de salida: palabras_partida (lista actualizada con la nueva palabra)
                          lista_coincidencias (lista actualizada con nuevas coincidencias)
                          lista_direcciones (lista actualizada con nueva dirección)'''
    if lista_direcciones[indice_palabra_dependencia].count("norte"):
                letra_palabra = elegir_indice_y_letra(palabras_partida,indice_palabra_dependencia,"norte")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_palabra_dependencia,"principio")
                
    else:
                letra_palabra = elegir_indice_y_letra(palabras_partida,indice_palabra_dependencia,"sur")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_palabra_dependencia,"final")
    flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
    lista_coincidencias.append(coincidencia)
    lista_direcciones.append("horizontal-" + flag_direccion)
    palabras_partida.append(siguiente_palabra)
    return palabras_partida,lista_coincidencias,lista_direcciones
        
def logica_construccion_sexta_y_septima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,indice_primera_palabra_dependencia,indice_segunda_palabra_dependencia):
    '''Función encargada de implementar la lógica para la sexta y séptima palabra
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             diccionario (dict con coincidencias entre palabras)
                             lista_direcciones (lista de orientaciones actuales)
                             lista_coincidencias (lista de intersecciones actuales)
                             indice_primera_palabra_dependencia (entero con primer índice base)
                             indice_segunda_palabra_dependencia (entero con segundo índice base)
       Variables de salida: palabras_partida (lista actualizada con la nueva palabra)
                          lista_coincidencias (lista actualizada con nuevas coincidencias)
                          lista_direcciones (lista actualizada con nueva dirección)'''
    if lista_direcciones[indice_primera_palabra_dependencia].count("norte"):
            if lista_direcciones[indice_segunda_palabra_dependencia].count("norte"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,indice_segunda_palabra_dependencia,"norte")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",-1,-2)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_segunda_palabra_dependencia,"principio-norte")
                
            
            elif lista_direcciones[indice_segunda_palabra_dependencia].count("sur"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,indice_segunda_palabra_dependencia,"sur")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",-1,-2)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_segunda_palabra_dependencia,"final-norte")
                
            lista_coincidencias.append(coincidencia)
            lista_direcciones.append("vertical-norte")
            palabras_partida.append(siguiente_palabra)

    elif lista_direcciones[indice_primera_palabra_dependencia].count("sur"):
            if lista_direcciones[indice_segunda_palabra_dependencia].count("norte"):
                   letra_palabra = elegir_indice_y_letra(palabras_partida,indice_segunda_palabra_dependencia,"norte")
                   siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",0,1)
                   coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_segunda_palabra_dependencia,"principio-sur")
                
            elif lista_direcciones[indice_segunda_palabra_dependencia].count("sur"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,indice_segunda_palabra_dependencia,"sur")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",0,1)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_segunda_palabra_dependencia,"final-sur")
                
            lista_coincidencias.append(coincidencia)
            lista_direcciones.append("vertical-sur")
            palabras_partida.append(siguiente_palabra)
    
    return palabras_partida,lista_coincidencias,lista_direcciones
    
def logica_construccion_octava_y_novena_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,indice_palabra_dependencia):
    '''Función encargada de implementar la lógica para la octava y novena palabra
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             diccionario (dict con coincidencias entre palabras)
                             lista_direcciones (lista de orientaciones actuales)
                             lista_coincidencias (lista de intersecciones actuales)
                             indice_palabra_dependencia (entero con índice de palabra base)
       Variables de salida: palabras_partida (lista actualizada con la nueva palabra)
                          lista_coincidencias (lista actualizada con nuevas coincidencias)
                          lista_direcciones (lista actualizada con nueva dirección)'''
    if lista_direcciones[indice_palabra_dependencia].count("norte"):
                letra_palabra = elegir_indice_y_letra(palabras_partida,indice_palabra_dependencia,"norte")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_palabra_dependencia,"principio")
                
    else:
                letra_palabra = elegir_indice_y_letra(palabras_partida,indice_palabra_dependencia,"sur")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,indice_palabra_dependencia,"final")
    flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
    lista_coincidencias.append(coincidencia)
    lista_direcciones.append("horizontal-" + flag_direccion)
    palabras_partida.append(siguiente_palabra)
    
    return palabras_partida,lista_coincidencias,lista_direcciones


def logica_construccion_decima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,indice_palabra_dependencia):
    '''Función encargada de implementar la lógica para la décima palabra
       Parámetros de entrada: palabras_partida (lista de palabras en el juego)
                             diccionario (dict con coincidencias entre palabras)
                             lista_direcciones (lista de orientaciones actuales)
                             lista_coincidencias (lista de intersecciones actuales)
                             indice_palabra_dependencia (entero con índice de palabra base)
       Variables de salida: palabras_partida (lista actualizada con la nueva palabra)
                          lista_coincidencias (lista actualizada con nuevas coincidencias)
                          lista_direcciones (lista actualizada con nueva dirección)'''
    if indice_palabra_dependencia == 7:
        palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_sexta_y_septima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,5,7)
    else:
        palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_sexta_y_septima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,6,8)
        
    return palabras_partida,lista_coincidencias,lista_direcciones
    

def LogicaConstruccion(lista_palabras, diccionario):
    '''Función encargada de implementar la lógica principal de construcción del crucigrama
       Parámetros de entrada: lista_palabras (lista de palabras disponibles)
                             diccionario (dict con coincidencias entre palabras)
       Variables de salida: palabras_partida (lista de palabras seleccionadas)
                          lista_direcciones (lista de orientaciones de cada palabra)
                          lista_coincidencias (lista de puntos de intersección)
                          dependencia_decima_palabra (entero con índice de dependencia)'''
    palabras_partida = BuscarPrimerPalabra(lista_palabras)
    lista_direcciones = ["-"]
    lista_coincidencias = ["-"]
    flag_direccion = ""

    for i in range(1,10):
        if i == 1:
           palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_segunda_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias)
       

        elif i == 2: #Tercer palabra - vertical

            palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_tercer_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias)
              
        elif i == 3: #Cuarta palabra
            palabras_partida,lista_coincidencias,lista_direcciones =  logica_construccion_cuarta_y_quinta_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,1)
           
        elif i == 4: #Quinta palabra
             palabras_partida,lista_coincidencias,lista_direcciones =  logica_construccion_cuarta_y_quinta_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,2)
        
        elif i == 5: #Sexta palabra
             palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_sexta_y_septima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,1,3)
            
        elif i == 6: #Séptima palabra
            palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_sexta_y_septima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,2,4)
            
        elif i == 7: #Octava palabra
            
            palabras_partida,lista_coincidencias,lista_direcciones =  logica_construccion_octava_y_novena_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,5)
           
        elif i == 8: #Novena palabra
            palabras_partida,lista_coincidencias,lista_direcciones =  logica_construccion_octava_y_novena_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,6)



        elif i == 9:
            if len(lista_palabras[7]) > len(lista_palabras[8]):
                palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_sexta_y_septima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,5,7)
                dependencia_decima_palabra = 7
            else:
                palabras_partida,lista_coincidencias,lista_direcciones = logica_construccion_sexta_y_septima_palabra(palabras_partida,diccionario,lista_direcciones,lista_coincidencias,6,8)
                dependencia_decima_palabra = 8

        
        



    return palabras_partida,lista_direcciones,lista_coincidencias,dependencia_decima_palabra

def Construccion_palabras_verticales(coordenada_dependencia, lista_coordenadas, tablero, direcciones, i, j, lista_palabras, lista_coincidencias):
    '''Función encargada de construir las palabras en dirección vertical en el tablero
       Parámetros de entrada: coordenada_dependencia (entero con índice de coordenada base)
                             lista_coordenadas (lista de posiciones actuales)
                             tablero (matriz del juego)
                             direcciones (lista de orientaciones)
                             i (entero con índice de palabra actual)
                             j (entero con posición dentro de la palabra)
                             lista_palabras (lista de palabras a colocar)
                             lista_coincidencias (lista de intersecciones)
       Variables de salida: tablero (matriz actualizada con palabras verticales)
                          lista_coordenadas (lista actualizada con nuevas posiciones)'''
    proxima_fila = calcularFila(lista_coordenadas[coordenada_dependencia][0],lista_coincidencias[i][1],direcciones[i])
    proxima_columna = calcularColumna(lista_coordenadas[coordenada_dependencia][1],lista_coincidencias[i][0],direcciones[i])
    if len(lista_coordenadas) == i: #Guardo las coordenadas
        lista_coordenadas.append([proxima_fila,proxima_columna])
    tablero[proxima_fila + j][proxima_columna][0] = lista_palabras[i][j]
    
    return tablero,lista_coordenadas

def Construccion_palabras_horizontales(coordenada_dependencia, lista_coordenadas, tablero, direcciones, i, j, lista_palabras, lista_coincidencias):
    '''Función encargada de construir las palabras en dirección horizontal en el tablero
       Parámetros de entrada: coordenada_dependencia (entero con índice de coordenada base)
                             lista_coordenadas (lista de posiciones actuales)
                             tablero (matriz del juego)
                             direcciones (lista de orientaciones)
                             i (entero con índice de palabra actual)
                             j (entero con posición dentro de la palabra)
                             lista_palabras (lista de palabras a colocar)
                             lista_coincidencias (lista de intersecciones)
       Variables de salida: tablero (matriz actualizada con palabras horizontales)
                          lista_coordenadas (lista actualizada con nuevas posiciones)'''
    proxima_fila = calcularFila(lista_coordenadas[coordenada_dependencia][0],lista_coincidencias[i][0],direcciones[i])
    proxima_columna = calcularColumna(lista_coordenadas[coordenada_dependencia][1],lista_coincidencias[i][1],direcciones[i])
    if len(lista_coordenadas) == i: #Guardo las coordenadas
        lista_coordenadas.append([proxima_fila,proxima_columna])
    tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]
    
    return tablero,lista_coordenadas    

def ConstruirTablero(tablero, lista_palabras, lista_coincidencias, direcciones, dependencia_decima_palabra):
    '''Función encargada de construir el tablero final del crucigrama
       Parámetros de entrada: tablero (matriz inicial vacía)
                             lista_palabras (lista de palabras a colocar)
                             lista_coincidencias (lista de puntos de intersección)
                             direcciones (lista de orientaciones de palabras)
                             dependencia_decima_palabra (entero con dependencia final)
       Variables de salida: tablero (matriz con el crucigrama completo)
                          lista_coordenadas (lista de posiciones de cada palabra)'''
    indice_fila_inicial = 25
    indice_columna_inicial = 25
    fila_anterior = indice_fila_inicial
    columna_anterior = indice_columna_inicial
    coordenadas = []
    for i in range(len(lista_palabras)):
        
        for j in range(len(lista_palabras[i])):

            if i == 0: #Primer Palabra - Horizontal
                fila_anterior = indice_fila_inicial 
                columna_anterior =indice_columna_inicial 
                if len(coordenadas) == 0: #Guardo las coordenadas
                    coordenadas.append([fila_anterior,columna_anterior])
                
                tablero[fila_anterior][columna_anterior + j][0] = lista_palabras[i][j]

            elif i in [1,2]: #Segunda Palabra - Vertical - Depende de la Palabra N°1 /// #Tercera Palabra - Vertical - Depende de la Palabra N°1
                tablero,coordenadas = Construccion_palabras_verticales(0,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)
                

            elif i == 3: #Cuarta Palabra - Horizontal - Depende de la Palabra N° 2
                tablero,coordenadas = Construccion_palabras_horizontales(1,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)
                
            elif i == 4: #Quinta Palabra - Horizontal - Depende de la plabra N 3
                tablero,coordenadas = Construccion_palabras_horizontales(2,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)

            elif i == 5: #Sexta palabra
                tablero,coordenadas = Construccion_palabras_verticales(3,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)
                
            elif i == 6: #Séptima palabra
                tablero,coordenadas = Construccion_palabras_verticales(4,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)

            elif i == 7: #Octava palabra
                tablero,coordenadas = Construccion_palabras_horizontales(5,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)

            elif i == 8: #Novena palabra
                tablero,coordenadas = Construccion_palabras_horizontales(6,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)
            elif i == 9:
                tablero,coordenadas = tablero,coordenadas = Construccion_palabras_verticales(dependencia_decima_palabra,coordenadas,tablero,direcciones,i,j,lista_palabras,lista_coincidencias)

    return tablero, coordenadas
def AgregoIndice(palabras_partida):
    '''Función encargada de agregar índices numéricos a las palabras
       Parámetros de entrada: palabras_partida (lista de palabras sin índice)
       Variables de salida: palabras_con_indice (lista de palabras con formato "número-palabra")'''
    devolucion_palabras = []

    for i, palabra in enumerate(palabras_partida): #recorre palabras_partida y devuelve el indice y la palabra en la posición i
       
        devolucion_palabras.append(list(f"{i+1}"+ "-" + palabra)) #appendea a la lista las palabras de la siguiente forma: (0+1)-casa, (1+1)-gato, (2+1)-plaza
    return devolucion_palabras 

    
def ImpresionTablero(tablero):
    '''Función encargada de generar la versión del tablero para mostrar al jugador
       Parámetros de entrada: tablero (matriz con el crucigrama completo)
       Variables de salida: tablero_actualizado (matriz con guiones en lugar de letras y números visibles)'''
    
    tablero_actualizado = []

    for fila_idx, fila in enumerate(tablero):  #recorrer filas en el tablero
        nueva_fila = []  #nueva fila tendrá mismos elementos
        col_idx = 0  

        while col_idx < len(fila):  #recorrer columnas

            #caso número 10
            if fila[col_idx][0] == "1" and fila_idx + 1 < len(tablero) and tablero[fila_idx + 1][col_idx][0] == "0":
                
                nueva_fila.append(" ")  
                tablero[fila_idx + 1][col_idx] = ["1"]  # El "1" se coloca en la fila siguiente
                if col_idx + 1 < len(tablero[fila_idx + 1]):  # Validación para evitar fuera de rango
                    tablero[fila_idx + 1][col_idx + 1] = ["0"]  #El "0" también se coloca en la fila siguiente
                col_idx += 1  #saltamos la columna ya manejada

            elif fila[col_idx][0].isdigit() or fila[col_idx][0] == "-":  #Si es un número o un guion se deja como está
                nueva_fila.append(fila[col_idx][0])

            elif fila[col_idx][0].isalpha():  #Si es una letra, appendeo un guion bajo
                nueva_fila.append("_")

            else:  #Espacios vacíos se dejan igual
                nueva_fila.append(" ")

            col_idx += 1  #Pasamos a la siguiente columna

        tablero_actualizado.append(nueva_fila)  #Añadimos la fila actualizada al tablero actualizado

    return tablero_actualizado


def PrintPistasTablero(tablero_actualizado, definiciones_1, palabras_para_jugar, palabras):
    '''Función encargada de imprimir el tablero con las definiciones de las palabras
       Parámetros de entrada: tablero_actualizado (matriz actual del juego)
                             definiciones_1 (lista de definiciones principales)
                             palabras_para_jugar (lista de palabras en el crucigrama)
                             palabras (lista completa de palabras disponibles)
       Variables de salida: tablero_actualizado (matriz con las definiciones agregadas)'''
    definiciones_jugables = []
    coordenadas = [2, 53]

    x, y = coordenadas
    for fila in tablero_actualizado:
        if x < 45:
            tablero_actualizado[x][y] = '|'
            x += 1

    for num in range(10):
        indice_palabra = num
        palabra_elegida = palabras_para_jugar[indice_palabra]
        indice_palabra_elegida = palabras.index(palabra_elegida)
        definiciones_jugables.append(definiciones_1[indice_palabra_elegida])
        lista_definiciones = list(AgregoIndice(definiciones_jugables))

        fila_inicio = 2
        columna_inicio = 56

    fila = fila_inicio
    col = columna_inicio

    for definicion in lista_definiciones:
        i = 0
        while i < len(definicion):
            letra = definicion[i]
        
            #verificar para el número 10
            if letra.isdigit() and i + 1 < len(definicion) and definicion[i:i+2] == '10':

                tablero_actualizado[fila][col] = '1'
                col += 1
                tablero_actualizado[fila][col] = '0'
                col += 1
                i += 2  #espacio entre definiciones
            elif letra.isdigit():
                fila += 2
                col = columna_inicio
                i += 1  #avanzar al siguiente caracter
            else:
                if col < 90:
                    tablero_actualizado[fila][col] = letra
                    col += 1
                else:
                    fila += 1
                    col = columna_inicio
                    if fila < 50:
                        tablero_actualizado[fila][col] = letra
                        col += 1
                i += 1  #avanzar al siguiente caracter

    for fila in tablero_actualizado:
        print(" ".join(fila))




def IngresarPalabraNumero(numero_palabra_encontrada, palabras_para_jugar, palabras, definiciones2, definiciones3, lista_comodin):
    '''Función encargada de manejar el ingreso de palabras y pistas por parte del usuario
       Parámetros de entrada: numero_palabra_encontrada (lista de números ya adivinados)
                             palabras_para_jugar (lista de palabras en juego)
                             palabras (lista completa de palabras)
                             definiciones2 (lista de segundas definiciones)
                             definiciones3 (lista de terceras definiciones)
                             lista_comodin (lista de comodines usados)
       Variables de salida: palabra_ingresada (string con la palabra del usuario)
                          numero_seleccionado (entero con el número elegido)
                          comodin_usado (boolean indicando uso de comodín)'''
    
    SeleccionaNumero = -1
    PedirPista = "S"
    IngresaPalabra = ""
    flag_palabra = True
    comodin = False
    bandera1 = True
    bandera2 = True
    bandera3 = True

    while bandera1:
            
            try:
                IngresaOpcion = int(input("Ingrese una opción:\n 1) Ingresar número de palabra a adivinar\n 2) Pedir Pista Extra\n 3) Utilizar Comodín\n Opción: "))

                if 1 <= IngresaOpcion <= 3:
                    bandera1 = False
                else:
                    print("El número ingresado debe corresponder a uno de los números que se muestran en las opciones.") 

                if IngresaOpcion == 1:
                    while bandera2:
                        try:
                            SeleccionaNumero = int(input("Ingrese el número de la palabra que quiere adivinar: ")) #se le pide ingresar el número al usuario.
                            if 1 <= SeleccionaNumero <= 10 and SeleccionaNumero not in numero_palabra_encontrada: #se valida que el número sea de 0 a 5 y que no se haya adivinado previamente.
                                IngresaPalabra = input("Ingrese la palabra que quiere adivinar: ")
                                if IngresaPalabra.isalpha():
                                    bandera2 = False
                                else: 
                                    print("Por favor ingrese una palabra. Vuelva a intentarlo.")
                            else:
                                print("El número ingresado debe corresponder a uno de los números que se muestran en el tablero y no corresponder a uno de los adivinados anteriormente.") 
                        except ValueError:
                            print("Por favor ingrese un número. Vuelva a intentarlo.") #si hay un error por ingresar un caracter, se muestra error.

                if IngresaOpcion == 2:
                    while bandera3:
                        PedirPista = "S"
                        try:
                            SeleccionaNumero = int(input("Ingrese el número de la palabra que quiere consultar la Pista Extra: "))
                            if 1 <= SeleccionaNumero <= 5 and SeleccionaNumero not in numero_palabra_encontrada:

                                LogicaSegundaPista(SeleccionaNumero, palabras_para_jugar, palabras,definiciones2, PedirPista)


    
                                PedirPista = input("¿Desea pedir una pista extra? S = Sí / N = No: ").strip().upper()

                                if PedirPista == "S" or PedirPista == "N":
                                    LogicaTercerPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones3, PedirPista)
                                    bandera3 = False
                                else:
                                    print("Por favor, ingrese 'S' para Sí o 'N'  para No.")
                            else:
                                print("El número ingresado debe corresponder a uno de los números que se muestran en el tablero y no corresponder a uno de los adivinados anteriormente.")
                        except ValueError:
                            print("Por favor ingrese un número. Vuelva a intentarlo.")


                if IngresaOpcion == 3:
                    if len(lista_comodin) < 1:
                        comodin = True
                        lista_comodin.append("-")
                    else:
                        print("Ya se utilizaron todos los comodines disponibles para esta partida")
            except ValueError:
                print("Por favor ingrese un número. Vuelva a intentarlo.")

    return IngresaPalabra, SeleccionaNumero, comodin

def ValidarPalabra(palabras_con_indice, IngresaPalabra, SeleccionaNumero):
    '''Función encargada de verificar si la palabra ingresada es correcta
       Parámetros de entrada: palabras_con_indice (lista de palabras numeradas)
                             IngresaPalabra (string con la palabra del usuario)
                             SeleccionaNumero (entero con el número elegido)
       Variables de salida: flag_palabra (boolean indicando si la palabra es correcta)'''

    flag_palabra = False
    if SeleccionaNumero != -1:
        
        numero_indice = SeleccionaNumero - 1
        
        palabra_con_numero= f"{SeleccionaNumero}-{IngresaPalabra}" #convierte en un string el número y la palabra ingresados por el usuario (1-casa)

        palabrita = "".join(palabras_con_indice[numero_indice]) #accede a la palabra con el número correspondiente y la formatea para que no tenga espacios y sea un string (1-casa)

        if palabra_con_numero == palabrita: #si son iguales la palabra es correcta.
            print("Correcto! La palabra adivinada es correcta")
            flag_palabra = True

        elif palabra_con_numero != palabrita and IngresaPalabra != "": #si no son iguales la palabra es incorrecta.
            print("Incorrecto! La palabra adivinada no es correcta")
        
    return flag_palabra

def LeerDict(diccionario):
    '''Función encargada de convertir un diccionario en una lista de pares clave-valor
       Parámetros de entrada: diccionario (dict a convertir)
       Variables de salida: lista_dict (lista de listas [clave, valor])'''
    lista_extraida = []
    for clave,valor in diccionario.items():
        lista_extraida.append([clave,valor])
    return lista_extraida
def cargarListas(lista):
    '''Función encargada de separar una lista de palabras y definiciones en listas individuales
       Parámetros de entrada: lista (lista de listas con palabras y sus definiciones)
       Variables de salida: palabras (lista de palabras)
                          definiciones_1 (lista de definiciones principales)
                          definiciones_2 (lista de segundas definiciones)
                          definiciones_3 (lista de terceras definiciones)'''
    palabras = []
    definiciones_1 = []
    definiciones_2 = []
    definiciones_3 = []
    
    for i in range(len(lista)):
        palabras.append(lista[i][0])
        cantidad_definiciones = len(lista[i][1])
        if cantidad_definiciones > 2:
            definiciones_1.append(lista[i][1][0])
            definiciones_2.append(lista[i][1][1])
            definiciones_3.append(lista[i][1][2])
        elif cantidad_definiciones > 1:
            definiciones_1.append(lista[i][1][0])
            definiciones_2.append(lista[i][1][1])
            definiciones_3.append("-")
        else:
            definiciones_1.append(lista[i][1][0])
            definiciones_2.append("-")
            definiciones_3.append("-")
    
            
            
        
    return palabras,definiciones_1,definiciones_2,definiciones_3


def LogicaTercerPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones3, PedirPista):
    '''Función encargada de manejar la lógica de mostrar la tercera pista
       Parámetros de entrada: SeleccionaNumero (entero con número de palabra)
                             palabras_para_jugar (lista de palabras en juego)
                             palabras (lista completa de palabras)
                             definiciones3 (lista de terceras definiciones)
                             PedirPista (string "S"/"N")
       Variables de salida: No retorna valores. Imprime la pista si existe'''

    indice_palabra = SeleccionaNumero - 1
    palabra_elegida = palabras_para_jugar[indice_palabra]
    indice_palabra_elegida = palabras.index(palabra_elegida)

    if PedirPista == "S":
        pista3 = definiciones3[indice_palabra_elegida]
        if pista3 == "-":
            print("No hay definiciones extras para esta palabra.")
        else:
            print("La pista extra es: ", pista3)


def LogicaSegundaPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones2, PedirPista):
    '''Función encargada de manejar la lógica de mostrar la segunda pista
       Parámetros de entrada: SeleccionaNumero (entero con número de palabra)
                             palabras_para_jugar (lista de palabras en juego)
                             palabras (lista completa de palabras)
                             definiciones2 (lista de segundas definiciones)
                             PedirPista (string "S"/"N")
       Variables de salida: pista (string con la segunda pista si existe)'''

    indice_palabra = SeleccionaNumero - 1
    palabra_elegida = palabras_para_jugar[indice_palabra]
    indice_palabra_elegida = palabras.index(palabra_elegida)

    if PedirPista == "S":
        pista2 = definiciones2[indice_palabra_elegida]
        if pista2 == "-":
            print("No hay definiciones extras para esta palabra.")
        else:
            print("La pista extra es: ", pista2)


    return pista2

def ElegirTematicas():
    '''Función encargada de permitir al usuario seleccionar la temática del juego
       Parámetros de entrada: No recibe parámetros
       Variables de salida: tematica (entero 1, 2 o 3 con la temática seleccionada)'''
    bandera1=True

    while bandera1 == True:
        try:
            tematica=int(input("Ingrese una opción para elegir la tematica:\n 1) Palabras generales\n 2) Palabras con relación al fútbol\n 3) Palabras con relación a Sistemas \n Opción: "))
            if tematica < 1 or tematica > 3:
                print("Por favor elija un número dentro de las opciones")
            else:
                bandera1 = False

        except ValueError:
            print("Por favor ingrese un número")

    return tematica


def LeerJSON(tematica):
    '''Función encargada de leer el archivo JSON correspondiente a la temática elegida
       Parámetros de entrada: tematica (entero con la opción elegida)
       Variables de salida: lista_palabras_definiciones (lista de listas con palabras y definiciones del JSON)'''
    lista_json = []
    if tematica == 1:
        jsonabrir = "json_palabras_generales.json"

    if tematica == 2:
        jsonabrir = "json_palabras_futbol.json"

    if tematica == 3:
        jsonabrir = "json_palabras_sistemas.json"        

    with open(jsonabrir, "r", encoding="utf-8") as file:
        data = json.load(file)
        for clave in data.items():
            lista_json.append(list(clave))
 
    return lista_json




def Comodin(SeleccionaNumero, palabras_con_indice, comodin, tablero_actualizado, coordenadas, lista_direcciones, flag_palabra, numero_palabra_encontrada):
    '''Función encargada de implementar la lógica del comodín para revelar una palabra
       Parámetros de entrada: SeleccionaNumero (entero con número de palabra)
                             palabras_con_indice (lista de palabras numeradas)
                             comodin (boolean indicando si se usa comodín)
                             tablero_actualizado (matriz actual del juego)
                             coordenadas (lista de posiciones)
                             lista_direcciones (lista de orientaciones)
                             flag_palabra (boolean de palabra correcta)
                             numero_palabra_encontrada (lista de números adivinados)
       Variables de salida: tablero_actualizado (matriz con la palabra revelada)'''
    if comodin == True:
        a=1
        b=5
        numero_random = random.randint(a,b)
        SeleccionaNumero = numero_random - 1
        while SeleccionaNumero in numero_palabra_encontrada:
            numero_random = random.randint(a,b)
            SeleccionaNumero = numero_random - 1
        print("Se utilizó el Comodin y ahora una palabra fue descubierta")
        flag_palabra = True
        ImprimirTableroActualizado(tablero_actualizado, flag_palabra, palabras_con_indice, coordenadas, lista_direcciones, SeleccionaNumero)

    return tablero_actualizado

def LimpioPantalla():
    '''Función encargada de limpiar la pantalla de la consola
       Parámetros de entrada: No recibe parámetros
       Variables de salida: No retorna valores'''
    os.system('cls' if os.name == 'nt' else 'clear')


def reiniciar_partida():
    '''Función encargada de reiniciar el juego desde el principio
       Parámetros de entrada: No recibe parámetros
       Variables de salida: No retorna valores. Llama a main()'''
    print("\nReiniciando la partida...\n")
    main()

def Login():
    '''Función encargada de manejar el registro e inicio de sesión de usuarios
       Parámetros de entrada: No recibe parámetros
       Variables de salida: No retorna valores'''
    bandera = True
    opcion_valida = False  # Variable para controlar la selección de opción válida

    # Bucle para asegurar que el usuario elige una opción válida
    while not opcion_valida:
        # Opción de registro o inicio de sesión
        opcion = input("Seleccione una opción (1-Registrar, 2-Iniciar sesión): ")
        
        if opcion == '1':
            # Registro de usuario
            nombre_usuario = input("Ingrese un nombre de usuario: ")
            contrasenia = input("Ingrese una contraseña: ")
            registrar_usuario(nombre_usuario, contrasenia)
            opcion_valida = True  # Marca la opción como válida para salir del bucle
        elif opcion == '2':
            # Intento de inicio de sesión con bucle para reintentar si falla
            while bandera:
                nombre_usuario = input("Ingrese su nombre de usuario: ")
                contrasenia = input("Ingrese su contraseña: ")
                if iniciar_sesion(nombre_usuario, contrasenia):
                    print("Inicio de sesión exitoso.")
                    bandera = False  # Termina el bucle de intento de inicio de sesión
                    opcion_valida = True  # Marca la opción como válida para salir del bucle principal
                else:
                    print("Error en el inicio de sesión. Intente nuevamente.")
        else:
            print("Opción no válida. Por favor, seleccione 1 o 2.")



def Score(palabras_para_jugar, flag_palabra, SeleccionaNumero):
    '''Función encargada de calcular el puntaje por palabra adivinada
       Parámetros de entrada: palabras_para_jugar (lista de palabras en juego)
                             flag_palabra (boolean de palabra correcta)
                             SeleccionaNumero (entero con número de palabra)
       Variables de salida: puntaje (entero con el puntaje calculado)'''
    puntaje = 0
    if flag_palabra == True:
        indice = SeleccionaNumero - 1
        palabra = palabras_para_jugar[indice]

        lista_palabra = list(palabra)

        for letra in lista_palabra:
            puntaje = puntaje + 1

    return puntaje



def main():
    '''Función principal encargada de controlar el flujo del juego
       Parámetros de entrada: No recibe parámetros
       Variables de salida: No retorna valores'''

#Funciones que se deben ejecutar al principio del programa:
    bandera_errores = True
    Login()
    tematica = ElegirTematicas()
    lista_cargada = LeerJSON(tematica)
    
    palabras,definiciones_1,definiciones_2,definiciones_3 = cargarListas(lista_cargada)


    diccionario_coincidencias = Buscolista_coincidencias(palabras)
    tablero = ConstruccionTableroVacio()
    #manejo errores por si no cuentra palabras
    while bandera_errores:

        try: 
            palabras_para_jugar,lista_direcciones,lista_coincidencias,dependencia_decima_palabra = LogicaConstruccion(palabras,diccionario_coincidencias)
            bandera_errores = False

        except AttributeError:
            print("No se encontró una combinación, reintentando...")

    palabras_con_indice = AgregoIndice(palabras_para_jugar)
    producto_final, coordenadas = ConstruirTablero(tablero, palabras_con_indice, lista_coincidencias, lista_direcciones,dependencia_decima_palabra)
    tablero_actualizado = ImpresionTablero(tablero)
    PrintPistasTablero(tablero_actualizado, definiciones_1, palabras_para_jugar, palabras)

    numero_palabra_encontrada = []
    puntaje_total = 0
    continuar_jugando = 'sí'
    primer_intento = True  # Variable para controlar el primer intento
    lista_comodin = []
    palabra_ingresada = " "
    while continuar_jugando == 'sí' or len(numero_palabra_encontrada) < 10:

        palabra_ingresada, numero_ingresado, comodin = IngresarPalabraNumero(numero_palabra_encontrada, palabras_para_jugar, palabras, definiciones_2, definiciones_3, lista_comodin)

    
        validation = ValidarPalabra(palabras_con_indice, palabra_ingresada, numero_ingresado)

        puntaje = Score(palabras_para_jugar, validation, numero_ingresado)

        puntaje_total = puntaje + puntaje_total

        print ("Su puntaje en esta partida es: ", puntaje_total)

        ImprimirTableroActualizado(tablero_actualizado, validation, palabras_con_indice, coordenadas, lista_direcciones, numero_ingresado)
        
        if validation == True:
            numero_palabra_encontrada.append(numero_ingresado)


        if comodin == True:
            Comodin(numero_ingresado, palabras_con_indice, comodin, tablero_actualizado, coordenadas, lista_direcciones, validation, numero_palabra_encontrada)

        if len(numero_palabra_encontrada) >= 10:
            print("¡Has encontrado todas las palabras!")
            print("Su puntaje en esta partida fue: ", puntaje_total)

            continuar_jugando = 'no'  # Cambia la variable para salir del bucle

        #Preguntar si quiere continuar, reiniciar o salir después del primer intento
        if not primer_intento:
            bandera = True
            while bandera == True:

                opcion = input("¿Deseas continuar jugando o reiniciar la partida? (C/R): ").strip().lower()


                if opcion not in ['c', 'r']:
                    print("Ingrese una opción correcta.")

                else:
                
                    if opcion == 'r':
                        reiniciar_partida() #Llama a la función para reiniciar  
                     
                    elif opcion == 'c':
                        print("Continua el juego.")
                        bandera = False
        else:
            primer_intento = False  #Cambiar a False después del primer intento

    if continuar_jugando == 'no':
        print("Gracias por jugar. ¡Hasta la próxima!")

# Inicia el juego
main()