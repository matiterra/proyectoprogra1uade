
import re
import random
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
    if len(palabra[:indice_coincidencia]) + 2 > len(palabra[indice_coincidencia + 1:]): #En el caso de que tenga más letras por encima o a la izquierda del punto de intersección, será de dirección "norte"
        flag_direccion = "norte" 
    elif len(palabra[:indice_coincidencia]) + 2 == len(palabra[indice_coincidencia + 1:]): #En el caso que queden la misma cantidad de letras de ambos lados desde el punto de intersección, se asignará al azar
        
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

    filas = 30
    columnas = 30
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

def LogicaConstruccion(lista_palabras,diccionario):
    '''Esta función delimitará la lógica de construcción partida a partida a partir del primer 
    llamado a la función anterior: "BuscarPrimerPalabra" que devolverá una palabra que minimamente tenga 7 caracteres o más. La palabras irán de a pares: Horizontales y Verticales'''
    

    #La primer palabra siempre se utilizará de manera horizontal y tendrá 7 o más caracteres
    palabras_partida = BuscarPrimerPalabra(lista_palabras)
    lista_direcciones = ["-"]
    lista_coincidencias = ["-"]
    
    flag_direccion = ""
    while len(palabras_partida) != 5:
        if len(palabras_partida) == 1: #Segunda palabra - Vertical
            indice_letra_a_buscar = random.randint(0,2) 
            letra_palabra = palabras_partida[0][indice_letra_a_buscar] 
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
            palabras_partida.append(siguiente_palabra)
            if len(indice_coincidencia) == 1:
                lista_coincidencias.append([palabras_partida[0].index(letra_palabra),indice_coincidencia[0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
            else:
                indice_random = random.randint(0,len(indice_coincidencia) - 1)
                
                lista_coincidencias.append([palabras_partida[0].index(letra_palabra),indice_coincidencia[indice_random]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[indice_random])
            lista_direcciones.append("vertical-"+flag_direccion)
            
        if len(palabras_partida) == 2: #Tercera palabra - Vertical - Depende de como se formó la primera y el flag de dirección de la segunda
            if lista_direcciones[1].count("norte") > 0: #Si la palabra N°2 tiene dirección "norte", a esta le asignare "sur" para evitar colisiones a futuro
                flag_direccion = "sur"
                indice_letra_a_buscar = random.choice([-1,-2])
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while (siguiente_palabra[0] != letra_palabra and siguiente_palabra[1] != letra_palabra) or siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))#Se buscará una palabra que en su indice 0 o 1 coincidan con la letra que se busca de la palabra (última o anteúltima de la primer palabra)
              
                lista_coincidencias.append([palabras_partida[0].rindex(letra_palabra),indice_coincidencia[0]])
                palabras_partida.append(siguiente_palabra)
                lista_direcciones.append("vertical-"+flag_direccion)
                
            else:
                flag_direccion = "norte" #Si la palabra N°2 tiene dirección "sur", a esta le asignaré "norte" para evitar colisiones
                lista_direcciones.append("vertical-"+flag_direccion)
                indice_letra_a_buscar = random.choice([-1,-2])
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while (siguiente_palabra[-1] != letra_palabra and  siguiente_palabra[-2] != letra_palabra ) or siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) #Se buscará una palabra que en su último o anteúltimo índice coíncida con la letra buscada (última o anteúltima de la primer palabra)
                if len(indice_coincidencia) == 1:
                   lista_coincidencias.append([palabras_partida[0].rindex(letra_palabra),indice_coincidencia[0]])#Uso de rindex para que busque el primer índice coincidente desde la derecha
                else:
                    lista_coincidencias.append([palabras_partida[0].rindex(letra_palabra),indice_coincidencia[-1]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)

                
                palabras_partida.append(siguiente_palabra)
                
                
        if len(palabras_partida) == 3:
            if lista_direcciones[1].count("norte") > 0: #Cuarta palabra - Horizontal - Depende de como se formó la segunda
                #En caso de que la palabra N°2 tenga dirección "Norte", buscaré palabras que coíncidan con las primeras letras de la palabra N°2
                if len(palabras_partida[1]) > 6: #En caso de que la palabra N°2 tenga una longitud de caracteres mayor a 6, habilitare la busqueda de letra entre sus índice 0 y 1
                    indice_letra_a_buscar = random.randint(0,1)
                else:
                    indice_letra_a_buscar = 0 #Caso contrario, solo buscare una letra coincidente en el índice 0
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) 
                while siguiente_palabra in palabras_partida: 
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) #Se buscará una palabra que no esté repetida
                
                lista_coincidencias.append([palabras_partida[1].index(letra_palabra),indice_coincidencia[0]])
                
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+ flag_direccion)
                
                palabras_partida.append(siguiente_palabra)
           
            else:
                #En caso de que la palabra N°2 tenga dirección "sur", buscaré palabras que coíncidan con las últimas letras de la palabra N°2
                if len(palabras_partida[1]) > 6:
                    indice_letra_a_buscar = random.randint(-2,-1) #En caso de que la palabra N°2 tenga una longitud de caracteres mayor a 6, habilitare la busqueda de letra entre su último y anteúltimo índices
                else:
                   indice_letra_a_buscar = -1 #Caso contrario, solo buscare una letra coincidente en el último índice
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))#Se buscará una palabra que no esté repetida
                while siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
               
                lista_coincidencias.append([palabras_partida[1].rindex(letra_palabra),indice_coincidencia[0]])
                
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)
                palabras_partida.append(siguiente_palabra)
        if len(palabras_partida) == 4: #Quinta palabra - Horizontal - Depende de como se formó la tercera palabra
            if lista_direcciones[2].count("norte") > 0: #En caso de que la palabra N°3 tenga dirección "Norte", buscaré palabras que coíncidan con las primeras letras de la palabra N°3
                if len(palabras_partida[2]) > 6: #En caso de que la palabra N°3 tenga una longitud de caracteres mayor a 6, habilitare la busqueda de letra entre sus índice 0 y 1
                    indice_letra_a_buscar = random.randint(0,1) 
                else:
                   indice_letra_a_buscar = 0 #Caso contrario, solo buscare una letra coincidente en el índice 0
                letra_palabra = palabras_partida[2][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) 
                while siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))  #Se buscará una palabra que no esté repetida
                lista_coincidencias.append([palabras_partida[2].index(letra_palabra),indice_coincidencia[0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal" + flag_direccion)
                palabras_partida.append(siguiente_palabra)
            else:
                #En caso de que la palabra N°2 tenga dirección "sur", buscaré palabras que coíncidan con las últimas letras de la palabra N°3
                if len(palabras_partida[2]) > 6:
                    indice_letra_a_buscar = random.randint(-2,-1) #En caso de que la palabra N°3 tenga una longitud de caracteres mayor a 6, habilitare la busqueda de letra entre su último y anteúltimo índices
                else:
                   indice_letra_a_buscar = -1 #Caso contrario, solo buscare una letra coincidente en el último índice
                letra_palabra = palabras_partida[2][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) #Se buscará una palabra que no esté repetida
                lista_coincidencias.append([palabras_partida[2].rindex(letra_palabra),indice_coincidencia[0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)
                palabras_partida.append(siguiente_palabra)
    return palabras_partida,lista_direcciones,lista_coincidencias

def ConstruirTablero(tablero,lista_palabras,lista_coincidencias,direcciones):
    '''Función que parte desde un índice de fila y columna inicial y que sucesivamente sumará nuevos caracteres en las listas que contiene la matriz'''
    indice_fila_inicial = 12
    indice_columna_inicial = 12
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
                


    return tablero, coordenadas


def AgregoIndice(palabras_partida):
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

    for fila in tablero_actualizado:
        print(" ".join(fila)) #Convierto el tablero_actualizado en una cadena de texto separada con " "

    return tablero_actualizado

def ImprimirTableroActualizado(tablero_actualizado, flag_palabra, palabras_con_indice, coordenadas, lista_direcciones, SeleccionaNumero):
    '''Función encargada de la impresión del tablero utilizado como parámetros de entrada: tablero_actualizado (tablero con números y guiones)
                                                                                           flag_palabra (True si es adivinada correctamente)
                                                                                           palabras_con_indice (Ejemplo: 1-casa)
                                                                                           coordenadas (Ejemplo: [5,5]) 
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
            coordenadas = [12, 12]
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

def IngresarPalabraNumero(numero_palabra_encontrada, palabras_para_jugar, palabras, definiciones1, definiciones2, definiciones3):
    '''Función encargada de controles e ingreso de datos del usuario. Se ingresa el número de la palabra que se quiere adivinar,
       si se quiere pedir una pista extra y la palabra a adivinar. Cada uno de estos ingresos tiene su validación correspondiente.
       Devuelve la palabra Ingresada, el número de la palabra a adivinar y si el usuario necesita una pista. '''

    bandera = True
    while bandera:
        try:
            SeleccionaNumero = int(input("Ingrese el número de la palabra que quiere adivinar ó de la que quiere consultar una Pista: ")) #se le pide ingresar el número al usuario.
            if 1 <= SeleccionaNumero <= 5 and SeleccionaNumero not in numero_palabra_encontrada: #se valida que el número sea de 0 a 5 y que no se haya adivinado previamente.
                
                LogicaPrimerPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones1)

                bandera = False
            else:
                print("El número ingresado debe corresponder a uno de los números que se muestran en el tablero.") 
        except ValueError:
            print("Por favor ingrese un número. Vuelva a intentarlo.") #si hay un error por ingresar un caracter, se muestra error.

    bandera2 = True
    while bandera2:
        PedirPista = input("¿Desea pedir una pista extra? S = Sí / N = No: ").strip().upper()
        if PedirPista == "S" or PedirPista == "N":

            LogicaSegundaPista(SeleccionaNumero, palabras_para_jugar, palabras,definiciones2, PedirPista)

            bandera2 = False
        else:
            print("Por favor, ingrese 'S' para Sí o 'N'  para No.") #si no ingresa s o n, no puede continuar.

    bandera3 = True
    while bandera3:
        IngresaPalabra = input("Ingrese la palabra que quiere adivinar: ") #tiene que ingresar si o si una palabra.
        if IngresaPalabra.isalpha():
            bandera3 = False
            return IngresaPalabra, SeleccionaNumero, PedirPista
        else: 
            print("Por favor ingrese una palabra. Vuelva a intentarlo.")


def ValidarPalabra(palabras_con_indice, IngresaPalabra, SeleccionaNumero):
    '''Función encargada de controles sobre la palabra ingresada. Sirve para verificar si la palabra es correcta. Utiliza: palabras_con_indice (1-casa, 2-techo)
                                                                                                                           IngresaPalabra (Palabra ingresada por el usuario)
                                                                                                                           SeleccionaNumero (Número que corresponde a la palabra)'''
    numero_palabra_encontrada = []
    numero_indice = SeleccionaNumero - 1
    flag_palabra = False
    palabra_con_numero= f"{SeleccionaNumero}-{IngresaPalabra}" #convierte en un string el número y la palabra ingresados por el usuario (1-casa)

    palabrita = "".join(palabras_con_indice[numero_indice]) #accede a la palabra con el número correspondiente y la formatea para que no tenga espacios y sea un string (1-casa)

    if palabra_con_numero == palabrita: #si son iguales la palabra es correcta.
        print("Correcto! La palabra adivinada es correcta")
        flag_palabra = True

        numero_palabra_encontrada.append(SeleccionaNumero) #se apendea en número de palabras encontradas.
    else: #si no son iguales la palabra es incorrecta.
        print("Incorrecto! La palabra adivinada no es correcta")
        
    return flag_palabra, numero_palabra_encontrada

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


def LogicaPrimerPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones1):

    indice_palabra = SeleccionaNumero - 1
    palabra_elegida = palabras_para_jugar[indice_palabra]
    indice_palabra_elegida = palabras.index(palabra_elegida)
    pista1 = definiciones1[indice_palabra_elegida]

    print(pista1)

def LogicaSegundaPista(SeleccionaNumero, palabras_para_jugar, palabras, definiciones2, PedirPista):

    indice_palabra = SeleccionaNumero - 1
    palabra_elegida = palabras_para_jugar[indice_palabra]
    indice_palabra_elegida = palabras.index(palabra_elegida)

    if PedirPista == "S":
        pista2 = definiciones2[indice_palabra_elegida]
        if pista2 == "-":
            print("No hay definiciones extras para esta palabra.")
        else:
            print(pista2)





def reiniciar_partida():
    print("\nReiniciando la partida...\n")
    main()
    
def main():


    diccionario_completo = {
  "abaco" : ["Instrumento de cálculo que utiliza cuentas que se deslizan a lo largo de una serie de barras de metal o madera fijadas a un marco para representar las unidades que sirve para efectuar operaciones aritméticas sencillas (sumas, restas y multiplicaciones)." , "Conocido como tablero de conteo y en desuso al tener mejores herramientas de cálculo"],
  "abandonar" : ["Acto de dejar solo a algo o alguien alejandose de ello o dejando de cuidarlo", "Dejar una actividad u ocupación o no seguir realizándola."],
  "abogado" : ["Persona que ejerce profesionalmente la defensa jurídica", "Profesión de 'Saul Goodman'"],
  "acuerdo" : ["Resolución premeditada de una sola persona o de varias.","Acción y efecto de acordar."],
  "acusar" : ["Señalar a alguien atribuyéndole la culpa de una falta, de un delito o de un hecho reprobable." , "Achacar, imputar, denunciar"],
  "admirar" : ["Ver, contemplar o considerar con estima o agrado especiales a alguien o algo que llaman la atención"],
  "agregar" : ["Incorporar algo a otra cosa.","Añadir algo a lo ya dicho o escrito.", "Unir o juntar unas personas o cosas a otras"],
  "ahora" : ["En este momento o en el tiempo actual.", "A esta hora, en este momento, en el tiempo actual"],
  "alegría" : ["Palabras, gestos o actos con que se expresa el júbilo o alegría.", "Una de las emociones protagonista de la película 'Intensamente'"],
  "alivio" : ["Consuelo, descanso o desahogo", "Acción y efecto de aliviar o aliviarse"],
  "alumno" : ["Persona que recibe enseñanza, respecto de un profesor o de la escuela, colegio o universidad donde estudia."],
  "amar" : ["Tener amor a alguien o algo."],
  "análisis" : ["Distinción y separación de las partes de algo para conocer su composición.", "Estudio detallado de algo, especialmente de una obra o de un escrito"],
  "anotar" : ["Poner notas en un escrito, una cuenta o un libro."],
  "ansiedad" : ["Preocupación y miedo intensos, excesivos y continuos ante situaciones cotidianas","Sentimiento de miedo, temor e inquietud", "Puede hacer que sude, se sienta inquieto y tenso, y tener palpitaciones."],
  "aprender" : ["Adquirir el conocimiento de algo por medio del estudio o de la experiencia"],
  "aroma" : ["Perfume, olor muy agradable."],
  "arte" : ["Cualquier actividad o producto realizado con una finalidad estética y también comunicativa, mediante la cual se expresan ideas, emociones y, en general, una visión del mundo, a través de diversos recursos, como los plásticos, lingüísticos, sonoros, corporales y mixtos.", "Conjunto de disciplinas y producciones realizadas por el ser humano con fines estéticos y simbólicos"],
  "asociar" : ["Juntar una cosa con otra para concurrir a un mismo fin.", "Unir una persona a otra que colabore en el desempeño de algún cargo, comisión o trabajo."],
  "bailar" : ["Ejecutar movimientos acompasados con el cuerpo, brazos y pies.", "Mover el cuerpo al compás de la música"],
  "banco" : ["Entidad de crédito o entidad de depósito, es una empresa financiera que acepta depósitos del público y crea depósitos a la vista, que comúnmente se llaman cuentas", "Palabra usada también para asiento, con respaldo o sin él, en que pueden sentarse dos o más personas."],
  "barco" : ["Embarcación de estructura cóncava y, generalmente, de grandes dimensiones.", "Titanic"],
  "belleza" : ["Persona o cosa notable por su hermosura"],
  "brillante" : ["Admirable o sobresaliente en su línea.", "Una persona, idea o actuación brillante es extremadamente inteligente o hábil", "Que brilla"],
  "brindar" : ["Manifestar, al ir a beber vino, licor u otra bebida alcohólica, el bien que se desea a alguien o la satisfacción por algo.", "Tradición en las festividades de compartir los tragos con alegría"],
  "cabeza" : ["Parte superior del cuerpo humano en la que se ubica el cerebro"],
  "cambiar" : ["Dejar una cosa o situación para tomar otra.", "Convertir o mudar algo en otra cosa"],
  "camino" : ["Vía rural destinada al uso de peatones, vehículos y animales.", "Vía que se construye para transitar."],
  "cantar" : ["Producir con la voz sonidos melodiosos, formando palabras o sin formarlas.", "Interpretar con la voz (una composición musical)."],
  "cargar" : ["Poner o echar peso sobre alguien o sobre una bestia.", "Acto de renovar la carga de batería"],
  "carta" : ["Papel escrito, y ordinariamente cerrado, que una persona envía a otra para comunicarse con ella.", "Medio de comunicación a través de un papel escrito y firmado por el emisor"],
  "celebrar" : ["Conmemorar, festejar una fecha, un acontecimiento."],
  "ciudad" : ["Conjunto de edificios y calles, regidos por un ayuntamiento, cuya población densa y numerosa ","Lo urbano"],
  "compañero" : ["Persona que se acompaña con otra para algún fin."],
  "conectar" : ["Unir o poner en comunicación dos cosas o dos personas", "Establecer comunicación entre dos lugares, o entre un lugar y otro."],
  "consentir" : ["Permitir algo o condescender en que se haga"],
  "correr" : ["Andar rápidamente y con tanto impulso que, entre un paso y el siguiente, los pies o las patas quedan por un momento en el aire.", "Ir deprisa."],
  "crear" : ["Producir algo de la nada."],
  "cultivar" : ["Dar a la tierra y a las plantas las labores necesarias para que fructifiquen", "Promover o mejorar el crecimiento de (una planta, cultivo, etc.) mediante trabajo y atención."],
  "curiosidad" : ["Emoción agradable que involucra la búsqueda de información, conocimientos y experiencias nuevas."],
  "dedicar" : ["Ofrecer a alguien algo, especialmente una obra literaria o artística, como obsequio o muestra de agradecimiento."],
  "defender" : ["Mantener, conservar, sostener algo contra el dictamen ajeno.","Amparar, librar, proteger"],
  "delicado" : ["Débil, flaco, delgado, enfermizo."],
  "demostrar" : ["Manifestar, declarar.", "Probar, sirviéndose de cualquier género de demostración."],
  "deporte" : ["Actividad física, ejercida como juego o competición, cuya práctica supone entrenamiento y sujeción a normas.", "Recreación, pasatiempo, placer, diversión o ejercicio físico, por lo común al aire libre."],
  "desafío" : ["Algo que hay que superar y es valorado como una situación o experiencia difícil y/o nueva"],
  "descubrir" : ["Hallar lo que estaba ignorado o escondido, principalmente tierras o mares desconocidos.","Enterarse, reconocer o darse cuenta por primera vez .hace 7 días"],
  "destino" : ["Concepto por el cual una persona cree que los eventos o las acciones están determinadas","Concepto por el cual una persona cree que los eventos o las acciones están determinadas"],
  "detener" : ["Impedir que algo o alguien sigan adelante.", "Interrumpir algo, como una acción o un movimiento"],
  "difundir" : ["Extender, esparcir, propagar físicamente"],
  "divertido" : ["Entretenido, ocurrente, ameno","Que divierte o hace pasar momentos agradables y de disfrute."],
  "dólar" : ["Nombre de la divisa oficial de USA"],
  "educar" : ["Desarrollar o perfeccionar las facultades intelectuales y morales del niño o del joven por medio de preceptos, ejercicios, ejemplos, etcétera."],
  "elefante" : ["Los mamíferos terrestres más grandes del mundo y tienen inmensos cuerpos, orejas grandes y trompas largas.","Usan sus trompas para recoger objetos, emitir sonidos de aviso"],
  "elegir" : ["Escoger o preferir a alguien","Significa quedarte con algo y dejar algo"],
  "emocionar" : ["Conmover el ánimo","Conmover el ánimo"],
  "empresa" : ["Unidad de organización dedicada a actividades industriales, mercantiles o de prestación de servicios con fines lucrativos.","Acción o tarea que entraña dificultad y cuya ejecución requiere decisión y esfuerzo."],
  "encontrar" : ["Dar con alguien o algo que se busca","Hallar algo o a alguien"]  ,
  "enviar" : ["Encomendar a alguien que vaya a alguna parte.","Hacer que algo se dirija o sea llevado a alguna parte."],
  "entender" : ["Tener idea clara de las cosas.","Comprender, ver, asimilar"],
  "escribir" : ["Componer libros, discursos, etcétera", "Representar las palabras o las ideas con letras u otros signos trazados en papel u otra superficie."],
  "esperanza" : ["Estado de ánimo que surge cuando se presenta como alcanzable lo que se desea.","Una motivación para perseverar hacia una meta o un estado final, incluso si somos escépticos sobre la probabilidad de un resultado positivo"],
  "estilo" : ["Modo, manera, forma de comportamiento.","Uso, práctica, costumbre, moda."],
  "eterno" : ["Que no tiene principio ni fin.","Que se repite con excesiva frecuencia."],
  "evidente" : ["Cierto, claro, patente y sin la menor duda.","Certeza clara y manifiesta de la que no se puede dudar."],
  "felicidad" : ["Estado de grata satisfacción espiritual y física.","Persona, situación, objeto o conjunto de ellos que contribuyen a hacer feliz."],
  "futuro" : ["Que está por venir y ha de suceder con el tiempo", "Que todavía no es pero va a ser."],
  "ganar" : ["Obtener (algo) como resultado de haber vencido en un combate, una disputa o una competición"],
  "gusto" : ["Sentido corporal con el que se perciben sustancias químicas disueltas, como las de los alimentos.","Sabor que tienen las cosas."],
  "hablar" : ["Emitir palabras.","Comunicar, expresar, decir","Enunciar, pronunciar, resollar, locutar"],
  "herencia" : ["Conjunto de bienes, derechos y obligaciones que, al morir alguien, son transmisibles a sus herederos o a sus legatarios.", "Derecho a heredar."],
  "historia" : ["Narración y exposición de los acontecimientos pasados y dignos de memoria, sean públicos o privados.","Disciplina que estudia y narra cronológicamente los acontecimientos pasados."],
  "honor" : ["Cualidad moral que lleva al cumplimiento de los propios deberes respecto del prójimo y de uno mismo.","Gloria o buena reputación que sigue a la virtud, al mérito o a las acciones heroicas"],
  "hospital" : ["Establecimiento destinado al diagnóstico y tratamiento de enfermos"],
  "idea" : ["Imagen o representación que del objeto percibido queda en la mente.","Conocimiento, noción, comprensión, concepción, pensamiento"],
  "iluminar" : ["Alumbrar, dar luz o bañar de resplandor","Adornar con muchas luces los templos, casas u otros sitios."],
  "imaginación" : ["Capacidad del ser humano de construir posibilidades creativas o inusuales","Facultad para representar en la mente las imágenes de las cosas reales o ideales"],
  "importante" : ["Que tiene importancia."],
  "inclusión" : ["Acción y efecto de incluir.","Pertenecer o ser parte de algo. "],
  "iniciar" : ["Comenzar","Dar principio a algo"],
  "innovar" : ["Mudar o alterar algo, introduciendo novedades.","Introducción de nuevas formas de diseñar, producir o vender bienes o servicios"],
  "intención" : ["Determinación de la voluntad en orden a un fin.", "Deseo que motiva una acción"],
  "intentar" : ["Tener ánimo de hacer algo.", "Propósito, intención, designio."],
  "interesante" : ["Que interesa o que es digno de interés.","Atrayente"],
  "inversión" : ["Acción y efecto de invertir."],
  "jardín" : ["Terreno donde se cultivan plantas"],
  "juego" : ["Acción y efecto de jugar por entretenimiento."],
  "juntar" : ["Unir unas cosas con otras.", "Reunir, congregar, poner en el mismo lugar."],
  "lápiz" : ["Utensilio para escribir o dibujar","Madera con una barra de grafito en su interior."],
  "lavar" : ["Limpiar algo con agua u otro líquido.","Purificar, quitar un defecto, mancha o descrédito"],
  "libertad" : ["Facultad natural que tiene el hombre de obrar de una manera o de otra", "Estado o condición de quien no es esclavo."],
  "libro" : ["Conjunto de muchas hojas de papel u otro material semejante que, encuadernadas, forman un volumen."],
  "luz" : ["Agente físico que hace visibles los objetos.", "Claridad que irradian los cuerpos en combustión, ignición o incandescencia."],
  "magia" : ["Creencia en el poder sobrenatural para producir efectos que van más allá de las leyes de la naturaleza", "Arte o ciencia oculta con que se pretende producir, valiéndose de ciertos actos o palabras, o con la intervención de seres imaginables, resultados contrarios a las leyes naturales."],
  "maravilla" : ["Suceso o cosa extraordinarios que causan admiración.", "Acción y efecto de maravillar o maravillarse."],
  "medida" : ["Acción y efecto de maravillar o maravillarse."],
  "mientras" : ["Durante el tiempo que transcurre hasta la realización de lo que se expresa.", "Durante el tiempo en que."],
  "misterio" : ["Aquello que no se puede explicar, comprender o descubrir", "Algo que no se entiende o que está más allá de la comprensión"],
  "modificar" : ["Transformar o cambiar algo mudando alguna de sus características"],
  "motivo" : ["Causa o razón que mueve para algo."],
  "música" : ["Arte de combinar los sonidos de la voz humana o de los instrumentos, o de unos y otros a la vez, de suerte que produzcan deleite, conmoviendo la sensibilidad"],
  "navegar" : ["Desplazarse por el agua en un buque o en otra embarcación"],
  "naturaleza" : ["Todo aquello que se ha formado de manera espontánea en el planeta Tierra","Reino general de los seres vivos y, en algunos casos, a los procesos asociados con objetos inanimados"],
  "ofrecer" : ["Comprometerse a dar, hacer o decir algo.","Presentar y dar voluntariamente algo."],
  "optimismo" : ["Propensión a ver y juzgar las cosas en su aspecto más favorable.","Ven el lado positivo de las cosas"],
  "organizar" : ["Establecer o reformar algo para lograr un fin, coordinando las personas y los medios adecuados.", "Poner algo en orden."],
  "paz" : ["Situación en la que no existe lucha armada en un país o entre países.", "Relación de armonía entre las personas, sin enfrentamientos ni conflictos."],
  "pedir" : ["Expresar a alguien la necesidad o el deseo de algo para que lo satisfaga."],
  "pensar" : ["Formar o combinar ideas o juicios en la mente.", "Examinar mentalmente algo con atención para formar un juicio."],
  "pequeño" : ["Que tiene poco tamaño o un tamaño inferior a otros de su misma clase."],
  "placer" : ["Goce o disfrute físico o espiritual producido por la realización o la percepción de algo que gusta o se considera bueno."],
  "poder" : ["Tener expedita la facultad o potencia de hacer algo.","Es un mando fáctico, es una fuerza que se impone aun contra la voluntad del otro y sin importar la razón de aquella."],
  "preguntar" : ["Exponer en forma de interrogación"],
  "probar" : ["Hacer examen y experimento de las cualidades de alguien o algo.", "Examinar si algo está arreglado a la medida, muestra o proporción de otra cosa a que se debe ajustar."],
  "promesa" : ["Expresión de la voluntad de dar a alguien o hacer por él algo.", "Persona o cosa que promete por sus especiales cualidades."],
  "propósito" : ["Ánimo o intención de hacer o de no hacer algo","Visión general para tu futuro basada en las cosas que son más significativas para ti"],
  "pueblo" : ["Todo grupo de personas que constituyen una comunidad u otro grupo en virtud de una cultura, religión o elemento similar comunes", "Población"],
  "recibir" : ["Hacerse cargo de lo que le dan o le envían.", "Tomar, obtener"],
  "reconocer" : ["Examinar algo o a alguien para conocer su identidad, naturaleza y circunstancias.", "Establecer la identidad de algo o de alguien."],
  "reflejar" : ["Dicho de una superficie lisa y brillante, como el agua o un espejo, que devuelve una imagen"],
  "regresar" : ["Devolver o restituir algo a su poseedor.", "Volver al lugar de donde se partió."],
  "relación" : ["Conexión, correspondencia de algo con otra cosa.", "Conexión, correspondencia, trato, comunicación de alguien con otra persona."],
  "reparar" : ["Arreglar algo que está roto o estropeado."],
  "requerir" : ["Necesitar, precisar, exigir."],
  "resolver" : ["Solucionar un problema, una duda, una dificultad o algo que los entraña"],
  "respeto" : ["Valor que permite al ser humano reconocer, aceptar, apreciar y valorar las cualidades del prójimo y sus derechos", "Sentimiento hacia una persona u objeto que lleva a actuar con cuidado de no ofender[la], dañar[la] o desobedecer[la]."],
  "resultado" : ["Efecto y consecuencia de un hecho, operación o deliberación.", "Efecto o consecuencia de una acción, proceso o situación"],
  "ramificación" : ["Acción y efecto de ramificar o ramificarse.", "Dividirse en ramas"],
  "sabiduría" : ["Grado más alto del conocimiento."],
  "salud" : ["Estado en que el ser orgánico ejerce normalmente todas sus funciones.", "Condición física y psíquica en que se encuentra un organismo en un momento determinado.", "Estado de completo bienestar físico, mental y social"],
  "satisfacción" : ["Acción y efecto de satisfacer o satisfacerse.", "El cumplimiento de un deseo o la resolución de una necesidad, de manera tal que se produce sosiego y tranquilidad."],
  "semilla" : ["Parte del fruto de las fanerógamas, que contiene el embrión de una futura planta", "Grano que en diversas formas producen las plantas y que al caer o ser sembrado produce, a su vez, nuevas plantas de la misma especie."],
  "sentido" : ["Capacidad para percibir estímulos externos o internos mediante determinados órganos"],
  "sueño" : ["Período de inconsciencia durante el cual el cerebro permanece sumamente activo", "Ganas de dormir."],
  "sorpresa" : ["Acción y efecto de sorprender."],
  "sostenible" : ["Que se puede sostener."],
   "sumar": ["Realizar la acción de añadir o agregar cantidades para obtener un total."],
  "superar": ["Vencer un obstáculo o dificultad.", "Sobrepasar un límite o nivel."],
  "sustento": ["Apoyo o base que proporciona lo necesario para vivir.", "Conjunto de elementos que sustentan una idea o proyecto."],
  "suerte": ["Accidente favorable o desgraciado que afecta a una persona.", "Fortuna que se tiene en las decisiones o eventos."],
  "tarea": ["Actividad o trabajo que debe realizarse.", "Deber que se asigna a alguien."],
  "tiempo": ["Duración en la que se desarrollan los acontecimientos.", "Condición atmosférica en un momento específico."],
  "trabajo": ["Actividad física o mental realizada a cambio de una remuneración.", "Esfuerzo destinado a lograr un objetivo."],
  "tranquilidad": ["Estado de calma y sosiego.", "Ausencia de preocupaciones o agitación."],
  "tratar": ["Intentar hacer algo o abordar un tema.", "Establecer una relación o comunicación con alguien."],
  "unir": ["Juntar o combinar cosas para formar un todo.", "Establecer una conexión entre elementos."],
  "valer": ["Tener un precio o un valor determinado.", "Ser útil o tener importancia."],
  "valor": ["Cualidad de lo que es útil, deseable o apreciado.", "Precio de una cosa en dinero."],
  "variar": ["Cambiar o modificar algo.", "Tener diferentes formas o manifestaciones."],
  "viajar": ["Desplazarse de un lugar a otro, generalmente por placer o trabajo.", "Conocer diferentes culturas y lugares."],
  "vida": ["Estado de los seres que tienen funciones biológicas.", "Conjunto de experiencias y eventos que se viven."],
  "vivir": ["Existir o tener vida.", "Experimentar la vida en sus diferentes facetas."],
  "volver": ["Regresar a un lugar o situación anterior.", "Repetir una acción."],
  "voto": ["Expresión de una opinión, especialmente en una elección.", "Decisión que se toma en una asamblea o reunión."],
  "yacer": ["Estar tendido o reclinado en un lugar.", "Estar en estado de reposo."],
  "zanahoria": ["Planta herbácea cuyas raíces son comestibles y de color anaranjado.", "Símbolo de recompensa o incentivo."],
  "zapato": ["Calzado que cubre el pie.", "Elemento de vestimenta utilizado para protección."],
  "zona": ["Área o región determinada por ciertas características.", "División geográfica."],
  "zénit": ["Punto más alto en el cielo o en la vida de alguien.", "Momento culminante o de mayor desarrollo."],
  }

#Funciones que se deben ejecutar al principio del programa:
    lista_cargada = LeerDict(diccionario_completo)
    
    palabras,definiciones_1,definiciones_2,definiciones_3 = cargarListas(lista_cargada)

    diccionario_coincidencias = Buscolista_coincidencias(palabras)
    tablero = ConstruccionTableroVacio()
    palabras_para_jugar,lista_direcciones,lista_coincidencias = LogicaConstruccion(palabras,diccionario_coincidencias)
    palabras_con_indice = AgregoIndice(palabras_para_jugar)
    producto_final, coordenadas = ConstruirTablero(tablero, palabras_con_indice, lista_coincidencias, lista_direcciones)
    tablero_actualizado = ImpresionTablero(tablero)

    numero_palabra_encontrada = []
    continuar_jugando = 'sí'
    primer_intento = True  # Variable para controlar el primer intento

    while continuar_jugando == 'sí' or len(numero_palabra_encontrada) < 5:
        palabra_ingresada, numero_ingresado, pista_pedido = IngresarPalabraNumero(numero_palabra_encontrada, palabras_para_jugar, palabras, definiciones_1, definiciones_2, definiciones_3)
        validation, param4 = ValidarPalabra(palabras_con_indice, palabra_ingresada, numero_ingresado)

        tablero_actualizado_final = ImprimirTableroActualizado(tablero_actualizado, validation, palabras_con_indice, coordenadas, lista_direcciones, numero_ingresado)

        if validation:
            numero_palabra_encontrada.append(palabra_ingresada)

        if len(numero_palabra_encontrada) >= 5:
            print("¡Has encontrado todas las palabras!")
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
