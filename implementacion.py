import os
import re
import random
import json

# Función para registrar un nuevo usuario
def registrar_usuario(nombre_usuario, contrasenia, archivo_credenciales='credenciales.json'):
    """Función para registrar un usuario en el sistema."""
    if not re.match(r"^[A-Za-z]{5,}\d{2}$", nombre_usuario):
        print("El nombre de usuario debe tener al menos 5 letras seguidas de 2 números.")
        return False

    if not re.match(r"^[A-Za-z0-9]{6,}$", contrasenia):
        print("La contraseña debe tener al menos 6 caracteres alfanuméricos.")
        return False

    try:
        # Leer el archivo de credenciales o inicializar un diccionario vacío
        if os.path.exists(archivo_credenciales):
            with open(archivo_credenciales, 'r', encoding='utf-8') as archivo_json:
                credenciales = json.load(archivo_json)
        else:
            credenciales = {}

        if nombre_usuario in credenciales:
            print("Este usuario ya existe. Por favor, elija otro nombre de usuario.")
            return False

        # Calcular el nuevo ID y agregar el usuario
        ultimo_id = max((int(usuario.get("id", 0)) for usuario in credenciales.values()), default=0)
        nuevo_id = ultimo_id + 1
        credenciales[nombre_usuario] = {
            "id": nuevo_id,
            "nombre_usuario": nombre_usuario,
            "contraseña": contrasenia,
            "score": 0
        }

        # Guardar los datos actualizados en el archivo
        with open(archivo_credenciales, 'w', encoding='utf-8') as archivo_json:
            json.dump(credenciales, archivo_json, indent=4, ensure_ascii=False)
            
        print("--------------------------------")
        print(f"Usuario {nombre_usuario} registrado exitosamente!")
        return True

    except Exception as e:
        print(f"Error al registrar usuario: {str(e)}")
        return False


def iniciar_sesion(nombre_usuario, contrasenia, archivo_credenciales='credenciales.json'):
    """Función para iniciar sesión con un usuario registrado."""
    try:
        if not os.path.exists(archivo_credenciales):
            print("No se encontraron usuarios registrados.")
            return False

        with open(archivo_credenciales, 'r', encoding='utf-8') as archivo_json:
            credenciales = json.load(archivo_json)

        if nombre_usuario in credenciales:
            if credenciales[nombre_usuario]['contraseña'] == contrasenia:
                print("--------------------------------")
                print(f"Bienvenido, {nombre_usuario}!")
                return True
            else:
                print("Contraseña incorrecta.")
                return False
        else:
            print("El nombre de usuario no existe.")
            return False

    except json.JSONDecodeError:
        print("Error al leer el archivo de credenciales.")
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
                          de 9 o más letras)'''
    palabras_para_jugar = []
    while len(palabras_para_jugar) == 0:
        palabra = random.choice(lista)
        if len(palabra) >= 9:
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

def elegir_palabra_e_indice(diccionario, letra, palabras_partida, dependencia="si", primer_indice=0, segundo_indice=1):
    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))
    max_intentos = 100  # Número máximo de intentos
    intentos = 0
    
    

    if dependencia == "no":
        while siguiente_palabra in palabras_partida and intentos < max_intentos:
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))
            intentos += 1
    else:
        while (siguiente_palabra in palabras_partida or 
               len(siguiente_palabra) <= max(primer_indice, segundo_indice) or 
               (siguiente_palabra[primer_indice] != letra and siguiente_palabra[segundo_indice] != letra)) and intentos < max_intentos:
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra).items()))
            intentos += 1
    if intentos >= max_intentos:
        raise ValueError("No se pudo encontrar una palabra válida después de múltiples intentos")
    

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
        if len(palabras_partida[indice_palabra]) > 9:
            indice_letra_a_buscar = random.randint(0,1)
        else:
            indice_letra_a_buscar = 0

    else:
        if len(palabras_partida[indice_palabra]) > 9:
            indice_letra_a_buscar = random.choice([-1,-2])
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
    while len(siguiente_palabra) < 7 :
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
            while len(siguiente_palabra) < 7 :
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,
        "si",0,1)
            coincidencia = elegir_coincidencia(palabras_partida,indice_coincidencia,letra_palabra,0,"final-sur")
                
    else:
            flag_direccion = "norte"
            siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,
                                                                            "si", -1, -1)
            while len(siguiente_palabra) < 6:
                siguiente_palabra, indice_coincidencia = elegir_palabra_e_indice(diccionario,letra_palabra,palabras_partida,
        "si",0,1)
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
    devolucion_palabras = list(map(lambda x: f"{x[0]}-{x[1]}", enumerate(palabras_partida)))


    


    return devolucion_palabras 

    
def ImpresionTablero(tablero):
    '''Función encargada de la impresión del tablero utilizado como parámetros de entrada: tablero(matriz con todas las palabras puestas en su lugar)
       A partir del tablero con todas las palabras en su lugar, se crea un tablero nuevo que tenga solamente guiones y números, y cuando hay
       una letra, se appendea un guión bajo. Si no hay nada se deja el espacio en blanco. '''
 
    tablero_actualizado = []
    variable = False

    

    for fila in tablero: #Se recorre el tablero principal dónde están todas las palabras ya posicionadas
        nueva_fila = [] #Se crea una lista para almacenar los elementos de tablero
        for elemento in fila:
                


            if elemento[0].isdigit() or elemento[0] == "-": #Si es un número o un guión, se appendea.
                nueva_fila.append(elemento[0])


            elif  elemento[0].isalpha(): #Si es una letra, se appendea un _
                nueva_fila.append("_")
                
            elif   elemento[0] == " ":
                nueva_fila.append(" ") #Y si no hay nada se deja el espacio vacío.


        tablero_actualizado.append(nueva_fila) #Se appendean todas las filas al tablero_actualizado.
    

    return tablero_actualizado




def PrintPistasTablero(tablero_actualizado, definiciones_1, palabras_para_jugar, palabras):
    '''Función encargada de imprimir el tablero con las definiciones de las palabras
       Parámetros de entrada: tablero_actualizado (matriz actual del juego)
                             definiciones_1 (lista de definiciones principales)
                             palabras_para_jugar (lista de palabras en el crucigrama)
                             palabras (lista completa de palabras disponibles)
       Variables de salida: tablero_actualizado (matriz con las definiciones agregadas)'''
    
    definiciones_jugables = []
    coordenadas = [2,53]

    x, y = coordenadas
    for fila in tablero_actualizado:
        if x < 45:
            tablero_actualizado [x][y] = '|'
            x = x + 1

    for num in range(10):
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
    numero_indice = SeleccionaNumero 

    if flag_palabra == True:
        palabra = palabras_con_indice[numero_indice]
        coordenadas = coordenadas[numero_indice]
        direccion = lista_direcciones[numero_indice] #Busco datos de la palabra

        if direccion in ["vertical-norte", "vertical-sur"]:
            direccion = "flag-vertical"
        elif direccion in ["horizontal-norte", "horizontal-sur"]:
            direccion = "flag-horizontal" #Cambio flags

        if SeleccionaNumero == 0:
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


def IngresarPalabraNumero(numero_palabra_encontrada, palabras_para_jugar, palabras, definiciones2, definiciones3, lista_comodin):
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
            print("\nEn cualquier momento puedes escribir 'B' para volver al menú de retroceso")
            print("--------------------------------")

            IngresaOpcion = input("Ingrese una opción:\n 1) Ingresar número de palabra a adivinar\n 2) Pedir Pista Extra\n 3) Utilizar Comodín\n Opción: ").strip()
            print("--------------------------------")


            if IngresaOpcion.upper() == 'B':
                
                bandera1 = False
            else:
                IngresaOpcion = int(IngresaOpcion)

                if 1 <= IngresaOpcion <= 3:
                    bandera1 = False
                else:
                    print("El número ingresado debe corresponder a uno de los números que se muestran en las opciones.") 

                if IngresaOpcion == 1:
                    while bandera2:
                        try:
                            entrada_numero = input("Ingrese el número de la palabra que quiere adivinar (o 'B' para volver): ").strip()
                            if entrada_numero.upper() == 'B':
                                bandera1 = False
                                bandera2 = False
                            else:
                                SeleccionaNumero = int(entrada_numero)
                                if 0 <= SeleccionaNumero <= 9 and SeleccionaNumero not in numero_palabra_encontrada:
                                    entrada_palabra = input("Ingrese la palabra que quiere adivinar (o 'B' para volver): ").strip()
                                    if entrada_palabra.upper() == 'B':
                                        
                                        bandera1 = False    
                                        bandera2 = False
                                    elif entrada_palabra.isalpha():
                                        IngresaPalabra = entrada_palabra
                                        bandera2 = False
                                    else: 
                                        print("Por favor ingrese una palabra válida. Vuelva a intentarlo.")
                                else:
                                    print("El número ingresado debe corresponder a uno de los números que se muestran en el tablero y no corresponder a uno de los adivinados anteriormente.") 
                        except ValueError:
                            print("Por favor ingrese un número. Vuelva a intentarlo.")

                if IngresaOpcion == 2:
                    while bandera3:
                        PedirPista = "S"
                        try:
                            entrada_pista = input("Ingrese el número de la palabra que quiere consultar la Pista Extra (o 'B' para volver): ").strip()
                            if entrada_pista.upper() == 'B':
                                bandera1 = False    
                                bandera2 = False
                                bandera3 = False
                            else:
                                SeleccionaNumero = int(entrada_pista)
                                if 0 <= SeleccionaNumero <= 9 and SeleccionaNumero not in numero_palabra_encontrada:
                                    LogicaSegundaPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones2, PedirPista)
                                    bandera3 = False
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
        
        numero_indice = SeleccionaNumero 
        
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




def LogicaSegundaPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones2, PedirPista):
    '''Función encargada de manejar la lógica de mostrar la segunda pista
       Parámetros de entrada: SeleccionaNumero (entero con número de palabra)
                             palabras_para_jugar (lista de palabras en juego)
                             palabras (lista completa de palabras)
                             definiciones2 (lista de segundas definiciones)
                             PedirPista (string "S"/"N")
       Variables de salida: pista (string con la segunda pista si existe)'''

    indice_palabra = SeleccionaNumero 
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
            print("--------------------------------")
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
    
    #Obtener el directorio actual del script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    #Definir el nombre del archivo JSON según la temática
    if tematica == 1:
        nombre_archivo = "json_palabras_generales.json"
    elif tematica == 2:
        nombre_archivo = "json_palabras_futbol.json"
    elif tematica == 3:
        nombre_archivo = "json_palabras_sistemas.json"
    else:
        raise ValueError("Temática no válida")
    
    #Construir la ruta completa al archivo JSON
    ruta_json = os.path.join(directorio_actual, nombre_archivo)
    
    #Leer el archivo JSON
    lista_json = []
    with open(ruta_json, "r", encoding="utf-8") as file:
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
        a=0
        b=9
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
    while True:
        opcion = input("Seleccione una opción (1-Registrar, 2-Iniciar sesión): ")
        
        if opcion == '1':  # Registrar usuario
            volver_al_menu = False
            while not volver_al_menu:
                nombre_usuario = input("Ingrese un nombre de usuario (debe contener al menos 5 letras y luego 2 números) o 'B' para volver a elegir: ")
                if nombre_usuario.upper() == 'B':
                    volver_al_menu = True  # Cambiar bandera para salir al menú principal
                    continue
                
                contrasenia = input("Ingrese una contraseña (debe contener al menos 6 caracteres alfanuméricos) o 'B' para volver a elegir: ")
                if contrasenia.upper() == 'B':
                    volver_al_menu = True  # Cambiar bandera para salir al menú principal
                    continue
                
                if registrar_usuario(nombre_usuario, contrasenia):
                    print("Registro exitoso.")
                    return nombre_usuario  # Salir de la función si el registro fue exitoso
                else:
                    print("Error en el registro. Intente nuevamente.")

        elif opcion == '2':  # Iniciar sesión
            volver_al_menu = False
            while not volver_al_menu:
                nombre_usuario = input("Ingrese su nombre de usuario o 'B' para volver a elegir: ")
                if nombre_usuario.upper() == 'B':
                    volver_al_menu = True  # Cambiar bandera para salir al menú principal
                    continue
                
                contrasenia = input("Ingrese su contraseña o 'B' para volver a elegir: ")
                if contrasenia.upper() == 'B':
                    volver_al_menu = True  # Cambiar bandera para salir al menú principal
                    continue
                
                if iniciar_sesion(nombre_usuario, contrasenia):
                    print("Inicio de sesión exitoso.")
                    return nombre_usuario  # Salir de la función si el inicio de sesión fue exitoso
                else:
                    print("Error en el inicio de sesión. Intente nuevamente.")
        
        else:
            print("Opción no válida. Por favor, seleccione 1 o 2.")

        
    
    return nombre_usuario

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

def menu_retroceso():
    """Muestra el menú de retroceso y maneja las opciones"""
    while True:
        print("\nMenú de retroceso:")
        print("1. Continuar jugando")
        print("2. Volver al menú principal")
        print("3. Salir del juego")
        
        opcion = input("\nSelecciona una opción (1-3): ")
        
        if opcion == "1":
            LimpioPantalla()
            return False, True  # (volver_menu, continuar_jugando)
        elif opcion == "2":
            LimpioPantalla()
            return True, False  # (volver_menu, continuar_jugando)
        elif opcion == "3":
            print("\n¡Gracias por jugar! Hasta pronto.")
            exit()
        else:
            print("Opción no válida. Por favor, selecciona 1, 2 o 3.")

def actualizar_puntaje(nombre_usuario, puntaje_nuevo):
    """Función para actualizar el puntaje del usuario usando su ID"""
    try:
        with open('credenciales.json', 'r', encoding='utf-8') as archivo:
            credenciales = json.load(archivo)
            
        if nombre_usuario in credenciales:
            usuario_id = credenciales[nombre_usuario]['id']
            puntaje_actual = int(credenciales[nombre_usuario].get('score', 0))
            credenciales[nombre_usuario]['score'] = puntaje_actual + puntaje_nuevo
            
            with open('credenciales.json', 'w', encoding='utf-8') as archivo:
                json.dump(credenciales, archivo, indent=4, ensure_ascii=False)
            
            # Cargar y mostrar todos los puntajes
            puntajes = cargar_puntajes()
            print("\n=== TABLA DE PUNTAJES ===")
            for id_usuario, datos in sorted(puntajes.items(), key=lambda x: x[1]['score'], reverse=True):
                print(f"Usuario: {datos['nombre']} - Puntaje: {datos['score']}")
            print("=======================")
            return True
        else:
            print("Error: Usuario no encontrado")
            return False
            
    except FileNotFoundError:
        print("Error: No se encontró el archivo de credenciales")
        return False
    except json.JSONDecodeError:
        print("Error: Problema al leer el archivo de credenciales")
        return False

def cargar_puntajes():
    """Función para cargar todos los puntajes de los usuarios"""
    try:
        with open('credenciales.json', 'r', encoding='utf-8') as archivo:
            credenciales = json.load(archivo)
            puntajes = {}
            for usuario, datos in credenciales.items():
                if 'id' in datos and 'score' in datos:
                    puntajes[datos['id']] = {
                        'nombre': usuario,
                        'score': datos['score']
                    }
            return puntajes
    except FileNotFoundError:
        print("Error: No se encontró el archivo de credenciales")
        return {}
    except json.JSONDecodeError:
        print("Error: Problema al leer el archivo de credenciales")
        return {}
import os

def printear_texto_descripcion(texto, width=80):
    # Obtiene el ancho de la terminal
    terminal_width = os.get_terminal_size().columns

    lineas = texto.split('\n')
    lineas_enmarcadas = []

    # Calcula el ancho del texto más largo para centrar correctamente
    ancho_maximo_texto = max(len(linea) for linea in lineas)
    ancho_cuadro = max(width, ancho_maximo_texto + 4)

    # Construye la parte superior del marco
    lineas_enmarcadas.append('+' + '-' * (ancho_cuadro - 2) + '+')
    
    # Crea las líneas con el texto centrado dentro del recuadro
    for linea in lineas:
        linea_centrada = linea.center(ancho_maximo_texto)
        linea_ajustada = linea_centrada.center(ancho_cuadro - 2)
        lineas_enmarcadas.append(f'|{linea_ajustada}|')
    
    # Construye la parte inferior del marco
    lineas_enmarcadas.append('+' + '-' * (ancho_cuadro - 2) + '+')
    
    # Imprime cada línea centrada respecto al ancho de la terminal
    for linea_enmarcada in lineas_enmarcadas:
        print(linea_enmarcada.center(terminal_width))
def imprimir_centrado_ascii(ascii_art):
    # Obtiene el ancho de la terminal
    terminal_width = os.get_terminal_size().columns
    
    # Divide el arte ASCII en líneas y centra cada una
    for linea in ascii_art.strip().split('\n'):
        print(linea.center(terminal_width))
        
ascii_art = r"""
______ _                           _     _                       _____           __   ____   __              _      
| ___ (_)                         (_)   | |                     /  __ \          \ \ / /\ \ / /             | |     
| |_/ /_  ___ _ ____   _____ _ __  _  __| | ___  ___     __ _   | /  \/_ __ _   _ \ V /  \ V /   _  __ _  __| | ___ 
| ___ \ |/ _ \ '_ \ \ / / _ \ '_ \| |/ _` |/ _ \/ __|   / _` |  | |   | '__| | | |/   \   \ / | | |/ _` |/ _` |/ _ \
| |_/ / |  __/ | | \ V /  __/ | | | | (_| | (_) \__ \  | (_| |  | \__/\ |  | |_| / /^\ \  | | |_| | (_| | (_| |  __/
\____/|_|\___|_| |_|\_/ \___|_| |_|_|\__,_|\___/|___/   \__,_|   \____/_|   \__,_\/   \/  \_/\__,_|\__,_|\__,_|\___|
                                                                                                                    
                                                                                                                  """
texto = """Bienvenid@s a CruXYuade, un juego de crucigrama minimalista diseñado para desafiar tu vocabulario directamente desde la terminal.
¡Cada crucigrama es único, y la diversión no tiene límites!
Elige una opción, ingresa tus respuestas, y deja que el arte ASCII te motive en cada victoria."""

def main():
    imprimir_centrado_ascii(ascii_art)
    printear_texto_descripcion(texto)

    nombre_usuario = Login()
    continuar_programa = True
    
    while continuar_programa:
        tematica = ElegirTematicas()
        lista_cargada = LeerJSON(tematica)
        bandera_errores = True
        
        while bandera_errores:
            try: 
                palabras,definiciones_1,definiciones_2,definiciones_3 = cargarListas(lista_cargada)
                diccionario_coincidencias = Buscolista_coincidencias(palabras)
                tablero = ConstruccionTableroVacio()
                palabras_para_jugar,lista_direcciones,lista_coincidencias,dependencia_decima_palabra = LogicaConstruccion(palabras,diccionario_coincidencias)
            except (AttributeError, ValueError):
                print("No se encontró una combinación, reintentando...")
                continue
            else:
                bandera_errores = False

        palabras_con_indice = AgregoIndice(palabras_para_jugar)
        producto_final, coordenadas = ConstruirTablero(tablero, palabras_con_indice, lista_coincidencias, lista_direcciones,dependencia_decima_palabra)
        tablero_actualizado = ImpresionTablero(tablero)
        PrintPistasTablero(tablero_actualizado, definiciones_1, palabras_para_jugar, palabras)

        numero_palabra_encontrada = []
        puntaje_total = 0
        continuar_jugando = True
        primer_intento = True
        lista_comodin = []
        palabra_ingresada = " "
        pista2 = ""
        pista3 = ""
        
        while continuar_jugando and len(numero_palabra_encontrada) < 10:
            # print("\nPresiona 'B' en cualquier momento para acceder al menú de retroceso")
            print("--------------------------------")
            accion = input("\nPresiona Enter para continuar o 'B' para el menú de retroceso: ").strip().upper()
            print("--------------------------------")

            if accion == 'B':
                print(f"\nGuardando puntaje final: {puntaje_total}")
                actualizar_puntaje(nombre_usuario, puntaje_total)
                volver_menu, continuar_jugando = menu_retroceso()
                if volver_menu:
                    LimpioPantalla()
                    continue  # Salta el resto del bucle actual
                
            if continuar_jugando:  # Solo ejecuta el código del juego si continuar_jugando es True
                LimpioPantalla()
                PrintPistasTablero(tablero_actualizado, definiciones_1, palabras_para_jugar, palabras)
                
                palabra_ingresada, numero_seleccionado, comodin = IngresarPalabraNumero(
                    numero_palabra_encontrada, 
                    palabras_para_jugar, 
                    palabras, 
                    definiciones_2, 
                    definiciones_3, 
                    lista_comodin
                )
                
                flag_palabra = ValidarPalabra(palabras_con_indice, palabra_ingresada, numero_seleccionado)
                
                if flag_palabra or comodin:
                    if comodin:
                        tablero_actualizado = Comodin(
                            numero_seleccionado,
                            palabras_con_indice,
                            comodin,
                            tablero_actualizado,
                            coordenadas,
                            lista_direcciones,
                            flag_palabra,
                            numero_palabra_encontrada
                        )
                    else:
                        ImprimirTableroActualizado(
                            tablero_actualizado,
                            flag_palabra,
                            palabras_con_indice,
                            coordenadas,
                            lista_direcciones,
                            numero_seleccionado
                        )
                    
                    if numero_seleccionado not in numero_palabra_encontrada:
                        numero_palabra_encontrada.append(numero_seleccionado)
                        puntaje_total += Score(palabras_para_jugar, flag_palabra, numero_seleccionado)

        if len(numero_palabra_encontrada) >= 10:
            print("¡Felicitaciones! Has completado el crucigrama.")
            print(f"Puntaje final: {puntaje_total}")
            actualizar_puntaje(nombre_usuario, puntaje_total)



# Llamada inicial al programa
if __name__ == "__main__":
    main()
