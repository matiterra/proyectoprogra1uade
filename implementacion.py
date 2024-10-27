import os
import re
import random
import json
# Función para registrar un nuevo usuario
def registrar_usuario(nombre_usuario, contrasenia):
    # Intentar cargar las credenciales existentes
    try:
        with open('credenciales.json', 'r', encoding='utf-8') as archivo_json:
            contenido = archivo_json.read()
            if contenido:  # Verifica si el archivo no está vacío
                credenciales = json.loads(contenido)
                print("Archivo cargado correctamente.")
            else:
                print("Archivo vacío, creando nuevo diccionario.")
                credenciales = {}
    except FileNotFoundError:
        # Si el archivo no existe, crear un diccionario vacío
        print("Archivo no encontrado, creando nuevo diccionario.")
        credenciales = {}

    # Verificar si el nombre de usuario ya existe
    while nombre_usuario in credenciales:
        print(f"Error: El usuario '{nombre_usuario}' ya está registrado. Intente con otro nombre.")
        nombre_usuario = input("Ingrese un nombre de usuario único: ")

    # Agregar las nuevas credenciales al diccionario
    credenciales[nombre_usuario] = {
        "nombre_usuario": nombre_usuario,
        "contraseña": contrasenia
    }
    print(f"Nuevas credenciales agregadas: {credenciales}")

    # Sobrescribir el archivo JSON con todas las credenciales (viejas + nuevas)
    with open('credenciales.json', 'w', encoding='utf-8') as archivo_json:
        json.dump(credenciales, archivo_json, indent=4, ensure_ascii=False)
    print("Archivo actualizado correctamente.")


# Función para iniciar sesión
def iniciar_sesion(nombre_usuario, contrasenia):
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
    '''Esta función eligirá la primera letra de maner aleatoría siempre que tenga 7 o más letras y la retornará como la primer posición de la lista para iniciar la construcción del crucigrama por cada partida'''
    palabras_para_jugar = []
    while len(palabras_para_jugar) == 0:
        palabra = random.choice(lista)
        if len(palabra) >= 7:
            palabras_para_jugar.append(palabra)
    return palabras_para_jugar

def definir_direccion(palabra,indice_coincidencia): 
    '''Función para definir la dirección de la palabra evaluando la cantidad de letra correspondientes antes y despues de la letra coincidente'''
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
    '''Función que permite calcular las filas desde donde ubicarse a partir de las coordenadas de la palabra anterior'''

    #En todos los casos, se suma o resta 2 para compensar y evitar tener en cuenta que cada palabra comienza con: "Número", "-"
     
    #En caso de ser horizontal, se hará el calculo de filas a partir de la fila de inicio  y se suma el indice que ocupa en la primer palabra la letra que coincide 
    if direccion in ["horizontal-sur" ,"horizontal-norte"]:
        fila_siguiente = fila_anterior + indice + 2
    
    #En caso de ser vertical, se hará el calculo de filas a partir de la resta de la fila de inicio y el indice que ocupa la letra en la segunda palabra
    else: 
        fila_siguiente = fila_anterior - indice  - 2
    
   
    return fila_siguiente


def ConstruccionTableroVacio():
    '''Función encargada de generar un tablero vacio con el centro marcado con un *'''

    filas = 100
    columnas = 100
    tablero_vacio = [[list(" ") for i in range(columnas)] for i in range(filas)]

    return tablero_vacio

def calcularColumna(columna_anterior,indice,direccion):
    '''Función que permite calcular las columnas desde donde ubicarse a partir de las coordenadas de la palabra anterior'''
    #En todos los casos, se suma o resta 2 para compensar y evitar tener en cuenta que cada palabra comienza con: "Número", "-"


    #En caso de ser vertical, el calculo se hace a partir de la columna donde inicia la primer palabra y el indice donde se encuentra la letra coincidente en ella
    if direccion in ["vertical-norte","vertical-sur"]:
        columna_siguiente = columna_anterior + indice + 2
    #En caso de ser horizontal, el calculo se hace a partir de la resta de la columna anterior y el índice donde se encuentra la letra en la segunda palabra
    else:
        columna_siguiente = columna_anterior - indice - 2


   
    return columna_siguiente

def elegir_palabra_e_indice (diccionario,letra,palabras_partida,dependencia = "si",primer_indice = 0, segundo_indice = 1):
    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))

    if dependencia == "no":
        while siguiente_palabra in palabras_partida:
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))
    else:

        while (siguiente_palabra[primer_indice] != letra and siguiente_palabra[segundo_indice] != letra) or     siguiente_palabra in palabras_partida:
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))

    return siguiente_palabra, indice_coincidencia

def elegir_coincidencia (palabras_partida,indice_coincidencia,letra_palabra,indice_palabra,seleccion_posicion = "principio"):

    
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

def LogicaConstruccion(lista_palabras,diccionario):
    '''Esta función delimitará la lógica de construcción partida a partida a partir del primer 
    llamado a la función anterior: "BuscarPrimerPalabra" que devolverá una palabra que minimamente tenga 7 caracteres o más. La palabras irán de a pares: Horizontales y Verticales'''
    palabras_partida = BuscarPrimerPalabra(lista_palabras)
    lista_direcciones = ["-"]
    lista_coincidencias = ["-"]
    flag_direccion = ""

    while len(palabras_partida) != 9:
        if len(palabras_partida) == 1: #Segunda palabra - Vertical
            letra_palabra = elegir_indice_y_letra(palabras_partida,0)
            siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,
            "no")
            coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,0,"principio")
            print(coincidencia)
            flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
            lista_coincidencias.append(coincidencia)
            lista_direcciones.append("vertical-" + flag_direccion)
            palabras_partida.append(siguiente_palabra)
        
        ######################################

        elif len(palabras_partida) == 2: #Tercer palabra - vertical
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
        ######################################        
        elif len(palabras_partida) == 3: #Cuarta palabra
            if lista_direcciones[1].count("norte"):
                letra_palabra = elegir_indice_y_letra(palabras_partida,1,"norte")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,1,"principio")
                
            else:
                letra_palabra = elegir_indice_y_letra(palabras_partida,1,"sur")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,1,"final")
            flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
            lista_coincidencias.append(coincidencia)
            lista_direcciones.append("horizontal-" + flag_direccion)
            palabras_partida.append(siguiente_palabra)
        ######################################
        elif len(palabras_partida) == 4: #Quinta palabra
            if lista_direcciones[2].count("norte"):
                letra_palabra = elegir_indice_y_letra(palabras_partida,2,"norte")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,2,"principio")
                
            else:
                letra_palabra = elegir_indice_y_letra(palabras_partida,2,"sur")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,2,"final")
            flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
            lista_coincidencias.append(coincidencia)
            lista_direcciones.append("horizontal-" + flag_direccion)
            palabras_partida.append(siguiente_palabra)
        ######################################
        elif len(palabras_partida) == 5: #Sexta palabra
            if lista_direcciones[1].count("norte"):
                if lista_direcciones[3].count("norte"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,3,"norte")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",-1,-2)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,3,"principio-norte")
                
            
                elif lista_direcciones[3].count("sur"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,3,"sur")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",-1,-2)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,3,"final-norte")
                
                lista_coincidencias.append(coincidencia)
                lista_direcciones.append("vertical-norte")
                palabras_partida.append(siguiente_palabra)

            elif lista_direcciones[1].count("sur"):
                if lista_direcciones[3].count("norte"):
                   letra_palabra = elegir_indice_y_letra(palabras_partida,3,"norte")
                   siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",0,1)
                   coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,3,"principio-sur")
                
                elif lista_direcciones[3].count("sur"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,3,"sur")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",0,1)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,3,"final-sur")
                
                lista_coincidencias.append(coincidencia)
                lista_direcciones.append("vertical-sur")
                palabras_partida.append(siguiente_palabra)
        ######################################
        elif len(palabras_partida) == 6: #Séptima palabra
            if lista_direcciones[2].count("norte"):
                if lista_direcciones[4].count("norte"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,4,"norte")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",-2,-1)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,4,"principio-norte")
                
            
                elif lista_direcciones[4].count("sur"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,4,"sur")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",-1,-2)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,4,"final-norte")
                
                lista_coincidencias.append(coincidencia)
                lista_direcciones.append("vertical-norte")
                palabras_partida.append(siguiente_palabra)

            elif lista_direcciones[2].count("sur"):
                if lista_direcciones[4].count("norte"):
                    letra_palabra = elegir_indice_y_letra(palabras_partida,4,"norte")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",0,1)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,4,"principio-sur")
                
                elif lista_direcciones[4].count("sur"):    
                    letra_palabra = elegir_indice_y_letra(palabras_partida,4,"sur")
                    siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"si",0,1)
                    coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,4,"final-sur")
                
                lista_coincidencias.append(coincidencia)
                lista_direcciones.append("vertical-sur")
                palabras_partida.append(siguiente_palabra)
        ######################################
        elif len(palabras_partida) == 7: #Octava palabra
            if lista_direcciones[5].count("norte"):
                letra_palabra = elegir_indice_y_letra(palabras_partida,5,"norte")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,5,"principio")
                
            else:
                letra_palabra = elegir_indice_y_letra(palabras_partida,5,"sur")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,5,"final")
            flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
            lista_coincidencias.append(coincidencia)
            lista_direcciones.append("horizontal-" + flag_direccion)
            palabras_partida.append(siguiente_palabra)
        ######################################
        elif len(palabras_partida) == 8: #Novena palabra
            if lista_direcciones[6].count("norte"):
                letra_palabra = elegir_indice_y_letra(palabras_partida,6,"norte")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,6,"principio")
                
            else:
                letra_palabra = elegir_indice_y_letra(palabras_partida,6,"sur")
                
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,"no")
                coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,6,"final")
            flag_direccion = definir_direccion(siguiente_palabra,coincidencia[1])
            lista_coincidencias.append(coincidencia)
            lista_direcciones.append("horizontal-" + flag_direccion)
            palabras_partida.append(siguiente_palabra)
        
        



    return palabras_partida,lista_direcciones,lista_coincidencias

def ConstruirTablero(tablero,lista_palabras,lista_coincidencias,direcciones):
    '''Función que parte desde un índice de fila y columna inicial y que sucesivamente sumará nuevos caracteres en las listas que contiene la matriz'''
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
                proxima_fila = calcularFila(coordenadas[0][0],lista_coincidencias[i][1],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[0][1],lista_coincidencias[i][0],direcciones[i])
                if len(coordenadas) == i: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                tablero[proxima_fila + j][proxima_columna][0] = lista_palabras[i][j]
                

            elif i == 3: #Cuarta Palabra - Horizontal - Depende de la Palabra N° 2
                proxima_fila = calcularFila(coordenadas[1][0],lista_coincidencias[i][0],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[1][1],lista_coincidencias[i][1],direcciones[i])
                if len(coordenadas) == i: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]
                
            elif i == 4: #Quinta Palabra - Horizontal - Depende de la plabra N 3
                proxima_fila = calcularFila(coordenadas[2][0],lista_coincidencias[i][0],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[2][1],lista_coincidencias[i][1],direcciones[i])
                if len(coordenadas) == i: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]

            elif i == 5: #Sexta palabra
                proxima_fila = calcularFila(coordenadas[3][0],lista_coincidencias[i][1],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[3][1],lista_coincidencias[i][0],direcciones[i])
                if len(coordenadas) == i: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                tablero[proxima_fila + j][proxima_columna][0] = lista_palabras[i][j]
                
            elif i == 6: #Séptima palabra
                proxima_fila = calcularFila(coordenadas[4][0],lista_coincidencias[i][1],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[4][1],lista_coincidencias[i][0],direcciones[i])
                if len(coordenadas) == i: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                tablero[proxima_fila + j][proxima_columna][0] = lista_palabras[i][j]

            elif i == 7: #Octava palabra
                proxima_fila = calcularFila(coordenadas[5][0],lista_coincidencias[i][0],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[5][1],lista_coincidencias[i][1],direcciones[i])
                if len(coordenadas) == i: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]

            elif i == 8: #Novena palabra
                proxima_fila = calcularFila(coordenadas[6][0],lista_coincidencias[i][0],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[6][1],lista_coincidencias[i][1],direcciones[i])
                if len(coordenadas) == i: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]

    return tablero, coordenadas

def AgregoIndice(palabras_partida):
    print(palabras_partida)
    '''Función encargada de colocar el prefijo utilizando una palabra a analizar. (1-casa)
       Utiliza como valor de entrada palabras_partida(palabras sin prefijo, ejemplo: casa)'''

    devolucion_palabras = []

    for i, palabra in enumerate(palabras_partida): #recorre palabras_partida y devuelve el indice y la palabra en la posición i
       
        devolucion_palabras.append(list(f"{i+1}"+ "-" + palabra)) #appendea a la lista las palabras de la siguiente forma: (0+1)-casa, (1+1)-gato, (2+1)-plaza
    return devolucion_palabras 

def ImpresionTablero(tablero):
    '''Función encargada de la impresión del tablero utilizado como parámetros de entrada: tablero(matriz con todas las palabras puestas en su lugar)
       A partir del tablero con todas las palabras en su lugar, se crea un tablero nuevo que tenga solamente guiones y números, y cuando hay
       una letra, se appendea un guión bajo. Si no hay nada se deja el espacio en blanco. '''
    
    tablero_actualizado = []

    for fila in tablero: #Se recorre el tablero principal dónde están todas las palabras ya posicionadas
        nueva_fila = [] #Se crea una lista para almacenar los elementos de tablero
        for elemento in fila:
            if elemento[0].isdigit() or elemento[0] == "-": #Si es un número o un guión, se appendea.
                nueva_fila.append(elemento[0]) 

            elif elemento[0].isalpha(): #Si es una letra, se appendea un _
                nueva_fila.append("_")
            else:
                nueva_fila.append(" ") #Y si no hay nada se deja el espacio vacío.

        tablero_actualizado.append(nueva_fila) #Se appendean todas las filas al tablero_actualizado.


    return tablero_actualizado

def ImprimirTableroActualizado(tablero_actualizado, flag_palabra, palabras_con_indice, coordenadas, lista_direcciones, SeleccionaNumero):
    '''Función encargada de la impresión del tablero utilizado como parámetros de entrada: tablero_actualizado (tablero con números y guiones)
                                                                                           flag_palabra (True si es adivinada correctamente)
                                                                                           palabras_con_indice (Ejemplo: 1-casa)
                                                                                           coordenadas (Ejemplo: [5,5])    ([F,C]) 
                                                                                           lista_direcciones (Ejemplo: "horizontal-norte")
                                                                                           SeleccionaNumero (Ejemplo: 3)
       A partir de estos valores, se seleccionan los datos de la palabra con el número ingresado por el usuario.
       se setean las coordenadas, y si la palabra es horizontal, se suma 1 por cada letra al eje y, lo mismo con el eje x
       luego lo printeo como si fuese un string para lograr una mejor visualización.'''
    numero_indice = SeleccionaNumero - 1

    if flag_palabra == True:
        palabra = palabras_con_indice[numero_indice]
        coordenadas = coordenadas[numero_indice]
        direccion = lista_direcciones[numero_indice] #Busco datos de la palabra

        if direccion in ["vertical-norte", "vertical-sur"]:
            direccion = "flag-vertical"
        elif direccion in ["horizontal-norte", "horizontal-sur"]:
            direccion = "flag-horizontal" #Cambio flags

        if SeleccionaNumero == 1:
            coordenadas = [25, 25]
            direccion = "flag-horizontal" #Coordenadas de primer palabra.

        x, y = coordenadas
        
        for letra in palabra:
            tablero_actualizado [x][y] = str(letra)

            if direccion == "flag-horizontal": #Suma eje y
                y = y + 1

            elif direccion == "flag-vertical": #Suma eje x
                x = x + 1
                
        for fila in tablero_actualizado: #Recorro filas en tablero_actualizado
            nueva_fila = [celda for celda in fila] #Se toma cada elemento de la fila y se incluye en nueva_fila
            print(" ".join(nueva_fila)) #Convierto nueva_fila en una cadena de texto separado con " "

        return tablero_actualizado
    

def PrintPistasTablero(tablero_actualizado, definiciones_1, palabras_para_jugar, palabras):
    definiciones_jugables = []
    coordenadas = [2,53]

    x, y = coordenadas
    for fila in tablero_actualizado:
        if x < 45:
            tablero_actualizado [x][y] = '|'
            x = x + 1

    for num in range(9):
        indice_palabra = num
        palabra_elegida = palabras_para_jugar[indice_palabra]
        indice_palabra_elegida = palabras.index(palabra_elegida)
        definiciones_jugables.append((definiciones_1[indice_palabra_elegida]))
        lista_definiciones = list(AgregoIndice(definiciones_jugables))

        fila_inicio = 2
        columna_inicio = 56


        fila = fila_inicio
        col = columna_inicio
        for definicion in lista_definiciones:
            for letra in definicion:
                
                if letra.isdigit():
                    fila += 2
                    col = columna_inicio

                if col < 90:
                    tablero_actualizado[fila][col] = letra
                    col += 1
                else:
                    fila += 1
                    col = columna_inicio
                    if fila < 50:  
                        tablero_actualizado[fila][col] = letra
                        col += 1

    for fila in tablero_actualizado:
            print(" ".join(fila))

    return tablero_actualizado

def IngresarPalabraNumero(numero_palabra_encontrada, palabras_para_jugar, palabras, definiciones2, definiciones3, lista_comodin):
    '''Función encargada de controles e ingreso de datos del usuario. Se ingresa el número de la palabra que se quiere adivinar,
       si se quiere pedir una pista extra y la palabra a adivinar. Cada uno de estos ingresos tiene su validación correspondiente.
       Devuelve la palabra Ingresada, el número de la palabra a adivinar y si el usuario necesita una pista. '''
    
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
                            if 1 <= SeleccionaNumero <= 9 and SeleccionaNumero not in numero_palabra_encontrada: #se valida que el número sea de 0 a 5 y que no se haya adivinado previamente.
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
            except ValueError:
                print("Por favor ingrese un número. Vuelva a intentarlo.")

                if IngresaOpcion == 3:
                    if len(lista_comodin) < 1:
                        comodin = True
                        lista_comodin.append("-")
                    else:
                        print("Ya se utilizaron todos los comodines disponibles para esta partida")

    return IngresaPalabra, SeleccionaNumero, comodin

def ValidarPalabra(palabras_con_indice, IngresaPalabra, SeleccionaNumero):
    '''Función encargada de controles sobre la palabra ingresada. Sirve para verificar si la palabra es correcta. Utiliza: palabras_con_indice (1-casa, 2-techo)
                                                                                                                           IngresaPalabra (Palabra ingresada por el usuario)
                                                                                                                           SeleccionaNumero (Número que corresponde a la palabra)'''

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
    '''Función para traducir los datos en formato clave-valor del diccionario en una lista de listas'''
    lista_extraida = []
    for clave,valor in diccionario.items():
        lista_extraida.append([clave,valor])
    return lista_extraida
def cargarListas(lista):
    '''Función que recibirá una lista de listas de palabras y definiciones la cual retornara listas individuales de distintas categorías pero que comparten los índices de los elementos entre ellas: Palabras - Definiciones1 - Definiciones2- Definiciones3. En caso de que la palabra no contenga una definición, se imprimirá un "-"'''
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
    os.system('cls' if os.name == 'nt' else 'clear')


def reiniciar_partida():
    print("\nReiniciando la partida...\n")
    main()

def Login():
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
    puntaje = 0
    if flag_palabra == True:
        indice = SeleccionaNumero - 1
        palabra = palabras_para_jugar[indice]

        lista_palabra = list(palabra)

        for letra in lista_palabra:
            puntaje = puntaje + 1

    return puntaje



def main():

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
            palabras_para_jugar,lista_direcciones,lista_coincidencias = LogicaConstruccion(palabras,diccionario_coincidencias)
            bandera_errores = False

        except AttributeError:
            print("No se encontró una combinación, reintentando...")

    palabras_con_indice = AgregoIndice(palabras_para_jugar)
    producto_final, coordenadas = ConstruirTablero(tablero, palabras_con_indice, lista_coincidencias, lista_direcciones)
    tablero_actualizado = ImpresionTablero(tablero)
    PrintPistasTablero(tablero_actualizado, definiciones_1, palabras_para_jugar, palabras)

    numero_palabra_encontrada = []
    puntaje_total = 0
    continuar_jugando = 'sí'
    primer_intento = True  # Variable para controlar el primer intento
    lista_comodin = []
    palabra_ingresada = " "
    while continuar_jugando == 'sí' or len(numero_palabra_encontrada) < 9:

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

        if len(numero_palabra_encontrada) >= 9:
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
