
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
    '''Esta función eligirá la primera letra de maner aleatoría y la retornará como la primer posición de la lista para iniciar la construcción del crucigrama por cada partida'''
    palabras_para_jugar = []
    while len(palabras_para_jugar) == 0:
        palabra = random.choice(lista)
        if len(palabra) >= 7:
            palabras_para_jugar.append(palabra)
    return palabras_para_jugar

def definir_direccion(palabra,indice_coincidencia): 
    '''Función para definir la dirección de la palabra evaluando la cantidad de letra correspondientes antes y despues de la letra coincidente'''
    flag_direccion = ""
    if len(palabra[:indice_coincidencia]) + 2 > len(palabra[indice_coincidencia + 1:]): 
        flag_direccion = "norte" 
    elif len(palabra[:indice_coincidencia]) + 2 == len(palabra[indice_coincidencia + 1:]): 
        
        random_flag = random.randint(1,2)
        if random_flag == 1:
            flag_direccion = "norte"
        else:
            flag_direccion = "sur"
            
    else: flag_direccion = "sur"
    return flag_direccion
            
def calcularFila(fila_anterior,indice,direccion):
    

    if direccion in ["horizontal-sur" ,"horizontal-norte"]:
        fila_siguiente = fila_anterior + indice + 2
    
    else: 
        fila_siguiente = fila_anterior - indice  - 2
    
   
    return fila_siguiente


def ConstruccionTableroVacio():
    '''Función encargada de generar un tablero vacio con el centro marcado con un *'''

    filas = 30
    columnas = 30
    tablero_vacio = [[list(" ") for i in range(columnas)] for i in range(filas)]

    # tablero_vacio[39][39] = list("*")

    # for fila in tablero_vacio:
    #     print(fila)

    return tablero_vacio

def calcularColumna(columna_anterior,indice,direccion):
    if direccion in ["vertical-norte","vertical-sur"]:
        columna_siguiente = columna_anterior + indice + 2

    else:
        columna_siguiente = columna_anterior - indice - 2


   
    return columna_siguiente

def LogicaConstruccion(lista_palabras,diccionario):
    '''Esta función delimitará la lógica de construcción partida a partida a partir del primer 
    llamado a la función anterior: "BuscarPrimerPalabra" que devolverá una palabra que minimamente tenga 7 caracteres o más. La palabras irán de a pares: Horizontales y Verticales'''
    
    #La primer palabra siempre se utilizará de manera horizontal
    palabras_partida = BuscarPrimerPalabra(lista_palabras)
    lista_direcciones = ["-"]
    lista_coincidencias = ["-"]
    
    flag_direccion = ""
    while len(palabras_partida) != 5:
        if len(palabras_partida) == 1: #segunda palabra
            indice_letra_a_buscar = random.randint(0,2) 
            letra_palabra = palabras_partida[0][indice_letra_a_buscar] #
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
            
        if len(palabras_partida) == 2: #tercera palabra - depende de como se formó la primera
            if lista_direcciones[1].count("norte") > 0:
                flag_direccion = "sur"
                indice_letra_a_buscar = random.choice([-1,-2])
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while (siguiente_palabra[0] != letra_palabra and siguiente_palabra[1] != letra_palabra) or siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))#esto tendría que ser una palabra que empiece con la última letra de la primer palabra horizontal
                 #índice que tiene la letra de la palabra que voy a traer del diccionario de lista_coincidencias
                lista_coincidencias.append([palabras_partida[0].rindex(letra_palabra),indice_coincidencia[0]])
                palabras_partida.append(siguiente_palabra)
                lista_direcciones.append("vertical-"+flag_direccion)
                
            else:
                flag_direccion = "norte"
                lista_direcciones.append("vertical-"+flag_direccion)
                indice_letra_a_buscar = random.choice([-1,-2])
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while (siguiente_palabra[-1] != letra_palabra and  siguiente_palabra[-2] != letra_palabra ) or siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) #esto tendría que ser una palabra que termine con la última letra de la primer palabra horizontal
                if len(indice_coincidencia) == 1:
                   lista_coincidencias.append([palabras_partida[0].rindex(letra_palabra),indice_coincidencia[0]])
                else:
                    lista_coincidencias.append([palabras_partida[0].rindex(letra_palabra),indice_coincidencia[-1]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)

                
                palabras_partida.append(siguiente_palabra)
                
                
        if len(palabras_partida) == 3:
            if lista_direcciones[1].count("norte") > 0: #cuarta palabra, depende de como se formó la segunda
                if len(palabras_partida[1]) > 6:
                    indice_letra_a_buscar = random.randint(0,1)
                else:
                    indice_letra_a_buscar = 0
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) #se buscará un coincidencia con la primer letra de la palabra N° 2
                while siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                # if len(indice_coincidencia) == 1:
                lista_coincidencias.append([palabras_partida[1].index(letra_palabra),indice_coincidencia[0]])
                # else:
                #     lista_coincidencias.append([indice_letra_a_buscar,indice_coincidencia[0][0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+ flag_direccion)
                
                palabras_partida.append(siguiente_palabra)
           
            else:
                if len(palabras_partida[1]) > 6:
                    indice_letra_a_buscar = random.randint(-2,-1)
                else:
                   indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))#Se buscará una coincidencia con la última letra de la palabra N°2
                while siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                # if len(indice_coincidencia) == 1:
                lista_coincidencias.append([palabras_partida[1].rindex(letra_palabra),indice_coincidencia[0]])
                # else:
                #     lista_coincidencias.append([indice_letra_a_buscar,indice_coincidencia[0][0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)
                palabras_partida.append(siguiente_palabra)
        if len(palabras_partida) == 4: #Quinta palabra, depende de la palabra 3
            if lista_direcciones[2].count("norte") > 0:
                if len(palabras_partida[2]) > 6:
                    indice_letra_a_buscar = random.randint(0,1)
                else:
                   indice_letra_a_buscar = 0
                letra_palabra = palabras_partida[2][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) 
                while siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) 
                lista_coincidencias.append([palabras_partida[2].index(letra_palabra),indice_coincidencia[0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal" + flag_direccion)
                palabras_partida.append(siguiente_palabra)
            else:
                if len(palabras_partida[2]) > 6:
                    indice_letra_a_buscar = random.randint(-2,-1)
                else:
                   indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[2][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while siguiente_palabra in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                lista_coincidencias.append([palabras_partida[2].rindex(letra_palabra),indice_coincidencia[0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)
                palabras_partida.append(siguiente_palabra)
    return palabras_partida,lista_direcciones,lista_coincidencias

def ConstruirTablero(tablero,lista_palabras,lista_coincidencias,direcciones):
    indice_fila_inicial = 12
    indice_columna_inicial = 12
    fila_anterior = indice_fila_inicial
    columna_anterior = indice_columna_inicial
    coordenadas = []
    for i in range(len(lista_palabras)):
        
        for j in range(len(lista_palabras[i])):
        
            print(coordenadas)

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
                print(coordenadas)
            # elif i == 5: #Sexta Palabra - Vertical - Depende de la plabra N 4
            #     proxima_fila = calcularFila(coordenadas[3][0],lista_coincidencias[i][0],direcciones[i])
            #     proxima_columna = calcularColumna(coordenadas[3][1],lista_coincidencias[i][1],direcciones[i])
            #     if len(coordenadas) == 5: #Guardo las coordenadas
            #         coordenadas.append([proxima_fila,proxima_columna])
            #     tablero[proxima_fila + j][proxima_columna ][0] = lista_palabras[i][j]
            # elif i == 6: #Séptima Palabra - Vertical - Depende de la plabra N 5
            #     proxima_fila = calcularFila(coordenadas[4][0],lista_coincidencias[i][1],direcciones[i])
            #     proxima_columna = calcularColumna(coordenadas[4][1],lista_coincidencias[i][0],direcciones[i])
            #     print(proxima_fila,proxima_columna)
            #     if len(coordenadas) == 6: #Guardo las coordenadas
            #         coordenadas.append([proxima_fila,proxima_columna])
            #     tablero[proxima_fila + j][proxima_columna ][0] = lista_palabras[i][j]
            #     print(coordenadas)

    return tablero, coordenadas

IniciaConNumero = lambda palabra_a_analizar: palabra_a_analizar[0].isdigit()

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

def IngresarPalabraNumero(numero_palabra_encontrada):
    '''Función encargada de controles e ingreso de datos del usuario. Se ingresa el número de la palabra que se quiere adivinar,
       si se quiere pedir una pista extra y la palabra a adivinar. Cada uno de estos ingresos tiene su validación correspondiente.
       Devuelve la palabra Ingresada, el número de la palabra a adivinar y si el usuario necesita una pista. '''
    

    bandera = True
    while bandera:
        try:
            SeleccionaNumero = int(input("Ingrese el número de la palabra que quiere adivinar ó de la que quiere consultar una Pista: ")) #se le pide ingresar el número al usuario.
            if 1 <= SeleccionaNumero <= 5 and SeleccionaNumero not in numero_palabra_encontrada: #se valida que el número sea de 0 a 5 y que no se haya adivinado previamente.
                bandera = False
            else:
                print("El número ingresado debe corresponder a uno de los números que se muestran en el tablero.") 
        except ValueError:
            print("Por favor ingrese un número. Vuelva a intentarlo.") #si hay un error por ingresar un caracter, se muestra error.

    bandera2 = True
    while bandera2:
        PedirPista = input("¿Desea pedir una pista extra? S = Sí / N = No: ").strip().upper()
        if PedirPista == "S" or PedirPista == "N":
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
    lista_extraida = []
    for clave,valor in diccionario.items():
        lista_extraida.append([clave,valor])
    return lista_extraida
def cargarListas(lista):
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


def reiniciar_partida():
    print("\nReiniciando la partida...\n")
    main()
    
def main():
    # lista =[
    #     "abaco", "abandonar", "abogado", "acuerdo", "acusar",
    #     "admirar", "agregar", "ahora", "alegría", "alivio",
    #     "alumno", "amar", "análisis", "anotar", "ansiedad", "aprender",
    #     "aroma", "arte", "asociar",
    #     "bailar", "banco", "barco", "belleza", "brillante", "brindar",
    #     "cabeza", "cambiar", "camino", "cantar", "cargar", "carta", "celebrar", "ciudad", "compañero",
    #     "conectar", "consentir", "correr", "crear", "cultivar",
    #     "curiosidad", "dedicar", "defender", "delicado", "demostrar", "deporte",
    #     "desafío", "descubrir", "destino", "detener", "difundir", 
    #     "divertido", "dólar", "educar", "elefante", "elegir", "emocionar",
    #     "empresa", "encontrar", "enviar", "entender", "escribir", "esperanza",
    #     "estilo", "eterno", "evidente", "felicidad", "futuro",
    #     "ganar", "gusto", "hablar", "herencia", "historia",
    #     "honor", "hospital", "idea", "iluminar", "imaginación", "importante",
    #     "inclusión", "iniciar", "innovar", "intención", "intentar", "interesante", "inversión",
    #     "jardín", "juego", "juntar", "lápiz", "lavar", "libertad", "libro", "luz", "magia",
    #     "maravilla", "medida", "mientras", "misterio", "modificar", "motivo", "música",
    #     "navegar", "naturaleza", "ofrecer","optimismo", "organizar",
    #     "paz", "pedir", "pensar", "pequeño", "placer", "pluma", "poder", "preguntar",
    #     "probar", "promesa", "propósito", "pueblo", "recibir", "reconocer", "reflejar",
    #     "regresar", "relación", "reparar", "requerir", "resolver", "respeto", "resultar", "reunir",
    #     "saber", "salud", "salir", "satisfacción", "seguir", "semilla", "sentido", "sueño",
    #     "sorpresa", "sostenible", "sumar", "superar", "sustento", "suerte", "tarea", "tiempo",
    #     "trabajo", "tranquilidad", "tratar", "unir", "valer", "valor", "variar", "viajar",
    #     "vida", "vivir", "volver", "voto", "yacer", "zanahoria", "zapato", "zona",
    #     "acertar", "alegrar", "apasionar", "cautivar", "claro", "compromiso", "construir",
    #     "dar", "destacar", "educación", "entusiasmo", "equilibrio", "esfuerzo", "experiencia",
    #     "fuerza", "generosidad", "gesto", "honestidad", "imaginación", "inspirar", "inteligencia",
    #     "liberación", "magnífico", "metas", "optimista", "pasión", "perseverancia", "recuerdo",
    #     "reflejo", "renacer", "sincero", "sorpresa", "temprano", "tranquilidad", "transformar",
    #     "valentía", "vigor", "visión", "vital", "zénit"
    # ]

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
  "sostenible" : ["Que se puede sostener."]
  "sumar": ["Realizar la acción de añadir o agregar cantidades para obtener un total."],    
  "ramificación": ["Acción y efecto de ramificar o ramificarse.", "Dividirse en ramas"],
  "resultado": ["Efecto y consecuencia de un hecho, operación o deliberación.", "Efecto o consecuencia de una acción, proceso o situación"],
  "respeto": ["Valor que permite al ser humano reconocer, aceptar, apreciar y valorar las cualidades del prójimo y sus derechos", "Sentimiento hacia una persona u objeto que lleva a actuar con cuidado de no ofender[la], dañar[la] o desobedecer[la]."],
  "resolver": ["Solucionar un problema, una duda, una dificultad o algo que los entraña"],
  "requerir": ["Necesitar, precisar, exigir."],
  "reparar": ["Arreglar algo que está roto o estropeado."],
  "relación": ["Conexión, correspondencia de algo con otra cosa.", "Conexión, correspondencia, trato, comunicación de alguien con otra persona."],
  "regresar": ["Devolver o restituir algo a su poseedor.", "Volver al lugar de donde se partió."],
  "reflejar": ["Dicho de una superficie lisa y brillante, como el agua o un espejo, que devuelve una imagen"],
  "reconocer": ["Examinar algo o a alguien para conocer su identidad, naturaleza y circunstancias.", "Establecer la identidad de algo o de alguien."],
  "recibir": ["Hacerse cargo de lo que le dan o le envían.", "Tomar, obtener"],
  "valentía": ["Cualidad de enfrentar el miedo o el peligro con coraje."],
  "vigor": ["Energía, fuerza y vitalidad para realizar una actividad."],
  "visión": ["Capacidad de ver.","Forma de comprender el mundo o prever el futuro."],
  "vital": ["Que es fundamental o necesario para la vida.","Que posee mucha energía o importancia."],
  "zénit": ["Punto más alto en el cielo directamente sobre la cabeza de un observador.","Momento culminante o de máximo esplendor de algo."]


  
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

    for fila in producto_final:
        print(fila)

    numero_palabra_encontrada = []
    continuar_jugando = 'sí'
    primer_intento = True  # Variable para controlar el primer intento

    while continuar_jugando == 'sí' and len(numero_palabra_encontrada) < 5:
        param1, param2, param3 = IngresarPalabraNumero(numero_palabra_encontrada)
        validation, param4 = ValidarPalabra(palabras_con_indice, param1, param2)

        tablero_actualizado_final = ImprimirTableroActualizado(tablero_actualizado, validation, palabras_con_indice, coordenadas, lista_direcciones, param2)

        if validation:
            numero_palabra_encontrada.append(param1)

        if len(numero_palabra_encontrada) >= 5:
            print("¡Has encontrado todas las palabras!")
            continuar_jugando = 'no'  # Cambia la variable para salir del bucle

        # Preguntar si quiere continuar, reiniciar o salir después del primer intento
        if not primer_intento:
            opcion = input("¿Deseas continuar jugando, reiniciar la partida o salir? (continuar/reiniciar/salir): ").strip().lower()
            if opcion == 'reiniciar':
                reiniciar_partida()  # Llama a la función para reiniciar
                return  # Finaliza la ejecución actual de main
            elif opcion == 'salir':
                print("Gracias por jugar. ¡Hasta la próxima!")
                return  # Finaliza la ejecución actual de main
        else:
            primer_intento = False  # Cambiar a False después del primer intento

    if continuar_jugando == 'no':
        print("Gracias por jugar. ¡Hasta la próxima!")

# Inicia el juego
if __name__ == "__main__":
    main()
