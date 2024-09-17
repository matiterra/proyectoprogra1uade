#Importo librerias 
import random
import json
from re import match

#Función encargada de leer json desde el archivo plano

#No presentar, función a futuro para el uso de archivos
def LeerJSON():
    lista_json = []
    with open("palabras.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        
        for clave in data.items():
            lista_json.append(list(clave))


    return lista_json

#Para la primer entrega, usaremos un diccionario y cargaremos los datos desde ahi de manera representativa

#Función encargada de reunir palabras y definiciones multiples (pueden variar por palabra) y las reune en una sublista de una lista
def LeerDict(diccionario):
    lista_extraida = []
    for clave,valor in diccionario.items():
        lista_extraida.append([clave,valor])
    return lista_extraida

'''Función encargada de cargar 4 listas: 1 de palabras y las siguientes para sus respectivas definiciones. 
En caso de no contar con tantas definiciones, su indice en la lista correspondiente se completa con un "-" '''
         
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
    
    print(palabras)
            
            
        
    return palabras,definiciones_1,definiciones_2,definiciones_3

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
    if len(palabra[:indice_coincidencia]) > len(palabra[indice_coincidencia + 1:]): 
        flag_direccion = "norte" 
    elif len(palabra[:indice_coincidencia]) == len(palabra[indice_coincidencia + 1:]): 
        
        random_flag = random.randint(1,2)
        if random_flag == 1:
            flag_direccion = "norte"
        else:
            flag_direccion = "sur"
            
    else: flag_direccion = "sur"
    return flag_direccion


def LogicaConstruccion(lista_palabras,diccionario_coincidencias):
    '''Esta función delimitará la lógica de construcción partida a partida a partir del primer 
    llamado a la función anterior: "BuscarPrimerPalabra" que devolverá una palabra que minimamente tenga 7 caracteres o más. La palabras irán de a pares: Horizontales y Verticales'''
    
    #La primer palabra siempre se utilizará de manera horizontal
    palabras_partida = BuscarPrimerPalabra(lista_palabras)
    lista_direcciones = ["-"]
    lista_coincidencias = []
    
    flag_direccion = ""
    while len(palabras_partida) != 5:
        if len(palabras_partida) == 1: #segunda palabra
            indice_letra_a_buscar = random.randint(0,2)
            letra_palabra = palabras_partida[0][indice_letra_a_buscar]
            siguiente_palabra = random.choice(diccionario_coincidencias.get((letra_palabra)))
            palabras_partida.append(siguiente_palabra)
            #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de coincidencias
            # flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia)
            #lista_direcciones.append("horizontal-"+flag_direccion)
            #lista_coincidencias.append([indice_letra_a_buscar, indicecoincidencia])
        if len(palabras_partida) == 2: #tercera palabra - depende de como se formó la primera
            if lista_direcciones[1].count("norte") > 0:
                flag_direccion = "sur"
                lista_direcciones.append("vertical-"+flag_direccion)
                indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra = random.choice(diccionario_coincidencias.get((letra_palabra)))#esto tendría que ser una palabra que empiece con la última letra de la primer palabra horizontal
                #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de coincidencias
                #lista_coincidencias.append([indice_letra_a_buscar, indicecoincidencia]) 
                palabras_partida.append(siguiente_palabra)
                
            else:
                flag_direccion = "norte"
                lista_direcciones.append("vertical-"+flag_direccion)
                indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra = random.choice(diccionario_coincidencias.get((letra_palabra))) #esto tendría que ser una palabra que termine con la última letra de la primer palabra horizontal
                #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de coincidencias
                #lista_coincidencias.append([indice_letra_a_buscar, indicecoincidencia]) 
                palabras_partida.append(siguiente_palabra)
                
                
        if len(palabras_partida) == 3:
            if lista_direcciones[1].count("norte") > 0: #cuarta palabra, depende de como se formó la segunda
                indice_letra_a_buscar = 0
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra = random.choice(diccionario_coincidencias.get((letra_palabra))) #se buscará un coincidencia con la primer letra de la palabra N° 2
                #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de coincidencias
                # flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia)
                
                #lista_direcciones.append("horizontal-"flag_direccion)
                palabras_partida.append(siguiente_palabra)
           
            else:
                indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra = random.choice(diccionario_coincidencias.get((letra_palabra))) #Se buscará una coincidencia con la última letra de la palabra N°2
                #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de coincidencias
                # flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia)
                #lista_direcciones.append("horizontal-"flag_direccion)
                palabras_partida.append(siguiente_palabra)
        if len(palabras_partida) == 4: #Quinta palabra, depende de la palabra 3
            if lista_direcciones[2] == "norte":
                indice_letra_a_buscar = 0
                letra_palabra = palabras_partida[2][indice_letra_a_buscar]
                siguiente_palabra = random.choice(diccionario_coincidencias.get(letra_palabra)) #se buscará una coincidencia con la primer letra
                #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de coincidencias
                # flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia)
                #lista_direcciones.append("horizontal-"flag_direccion)
                palabras_partida.append(siguiente_palabra)
            else:
                indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[2][indice_letra_a_buscar]
                siguiente_palabra = random.choice(diccionario_coincidencias.get(letra_palabra))  #se buscará coincidencia con la última letra
                #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de coincidencias
                # flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia)
                #lista_direcciones.append("horizontal-"flag_direccion)
                 palabras_partida.append(siguiente_palabra)

def calcularFila(fila_anterior,indice,direccion):
    if direccion == "vertical-norte": 
        fila_siguiente = fila_anterior - indice  

    elif direccion == "vertical-sur":
        fila_siguiente = fila_anterior + indice
    
    elif direccion == "horizontal-sur":
        fila_siguiente = fila_anterior + indice
    
    else:
        fila_siguiente = fila_anterior
    return fila_siguiente



def calcularColumna(columna_anterior,indice,direccion):
    if direccion == "vertical-norte" or "vertical-sur":
        columna_siguiente = columna_anterior + indice 

    elif direccion == "horizontal-norte":
        columna_siguiente = columna_anterior - indice


    else: 
        columna_siguiente = columna_anterior  + indice
    return columna_siguiente

#Aclaración: calcularFila y calcularColumna están bajo revisión

def ConstruirTablero(tablero,lista_palabras,lista_coincidencias,direccion):
    indice_fila_inicial = 9
    indice_columna_inicial = 5
    fila_anterior = indice_fila_inicial
    columna_anterior = indice_columna_inicial
    for i in range(len(lista_palabras)):
        
        for j in range(len(lista_palabras[i])):
        
            print(coordenadas)

            if i == 0:
                fila_anterior = indice_fila_inicial
                columna_anterior =indice_columna_inicial 
                
                tablero[fila_anterior][columna_anterior + j][0] = lista_palabras[i][j]

            elif i == 1:
                proxima_columna = calcularColumna(columna_anterior,coincidencias[i][0],direcciones[i])
                proxima_fila = calcularFila(fila_anterior,coincidencias[i][1],direcciones[i])
                if len(coordenadas) == 0: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                print(coordenadas)
                tablero[proxima_fila + j][proxima_columna][0] = lista_palabras[i][j]
                

            elif i == 2:
                
                proxima_columna = calcularColumna(columna_anterior,coincidencias[i][0],direcciones[i])
                proxima_fila = proxima_fila = calcularFila(fila_anterior,coincidencias[i][1],direcciones[i])
                if len(coordenadas) == 1:#Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                
                tablero[proxima_fila + j][proxima_columna][0] = lista_palabras[i][j]
            elif i == 3:
                proxima_fila = proxima_fila = calcularFila(coordenadas[0][0],coincidencias[i][1],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[0][1],coincidencias[i][0],direcciones[i])
                if len(coordenadas) == 2: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                
                tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]
            elif i == 4:
                proxima_fila = calcularFila(coordenadas[1][0],coincidencias[i][0],direcciones[i])
                proxima_columna = calcularColumna(coordenadas[1][1],coincidencias[i][1],direcciones[i])
                if len(coordenadas) == 3: #Guardo las coordenadas
                    coordenadas.append([proxima_fila,proxima_columna])
                
                tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]
def IngresarPalabraNumero():
    '''Función encargada del Ingreso de la palabra a adivinar siguiendo la lógica de número - palabra (1 - C A S A)
        Devuelve la palabra Ingresada, el número de la palabra a adivinar y si el usuario necesita una pista. '''
    bandera = True
    while bandera:
        try:
            SeleccionaNumero = int(input("Ingrese el número de la palabra que quiere adivinar: "))
            if 1 <= SeleccionaNumero <= 10:
                bandera = False
            else:
                print("El número ingresado debe corresponder a uno de los números que se muestran en el tablero.")
        except ValueError:
            print("Por favor ingrese un número. Vuelva a intentarlo.")

    bandera2 = True
    while bandera2:
        PedirPista = input("¿Desea pedir una pista extra? S = Sí / N = No: ").strip().upper()
        if PedirPista == "S" or PedirPista == "N":
            bandera2 = False
        else:
            print("Por favor, ingrese 'S' para Sí o 'N'  para No.")

    bandera3 = True
    while bandera3:
        IngresaPalabra = input("Ingrese la palabra que quiere adivinar: ")
        if IngresaPalabra.isalpha():
            bandera3= False
            return IngresaPalabra, SeleccionaNumero, PedirPista
        else: 
            print("Por favor ingrese una palabra. Vuelva a intentarlo.")
    
    ValidarPalabra(IngresaPalabra)

def ValidarPalabra(palabras_partida, IngresaPalabra, SeleccionaNumero):
    palabra_con_numero= f"{SeleccionaNumero}-{IngresaPalabra}"
    for palabra_con_numero in palabras_partida:
        if IngresaPalabra == palabras_partida:
            print("Correcto! La palabra adivinada es la correcta")
            ImpresionTablero()
    else: 
        print("Incorrecto! La palabra adivinada no es correcta")
        ImpresionTablero()


'''Función lambda que verifica si el primer carácter de una cadena es un dígito'''
IniciaConNumero = lambda palabra_a_analizar: palabra_a_analizar[0].isdigit()

def AgregoIndice(palabras_partida):
    '''Función encargada de colocar el prefijo utilizando una palabra a analizar. (1 - C A S A)
       Esta función llama a la función lambda IniciaConNumero que devuelve True
        o False que verifica si la palabra a analizar tiene un dígito en el indice 0 o no.'''

    devolucion_palabras = []

    for i, palabra in enumerate(palabras_partida):
        if IniciaConNumero(palabra) == True:
            devolucion_palabras.append(palabra)
        else:
            devolucion_palabras.append(f"{i+1}"- + palabra)
    return devolucion_palabras

def ConstruccionTableroVacio():
    '''Función encargada de generar un tablero vacio con el centro marcado con un *'''

    filas = 20
    columnas = 20
    tablero_vacio = [[list(" ") for i in range(columnas)] for i in range(filas)]

    tablero_vacio[9][9] = list("*")

    for fila in tablero_vacio:
        print(fila)


def ImpresionTablero():
    pass

def BuscoCoincidencias(palabras):
    #Función que se encarga de buscar letras dentro de las palabras de forma que guarde el Indice
    coincidencias = {}

    for palabra in palabras:
        palabra_str = ''.join(palabra)
        index = 0  # Contador para el índice de la letra
        
        while index < len(palabra):
            letra = palabra[index]
            if letra not in coincidencias:
                coincidencias[letra] = []
            coincidencias[letra].append({
                'palabra': palabra_str,
                'indice': index
            })
            index += 1  #incrementa el indice
    return coincidencias


#MAIN
def main(lista):
    diccionario_maqueta = {
    "perro": [
        "Mamífero doméstico de la familia de los cánidos, de tamaño, forma y pelaje muy diversos, según las razas, que tiene olfato muy fino y es inteligente y muy leal a su dueño. Usado en masculino referido a la especie.",
        "El mejor amigo del hombre",
        "Un capo sinceramente"
    ],
    "gato": [
        "Mamífero de la familia de los félidos, digitígrado, doméstico, de unos 50 centímetro(s) de largo desde la cabeza hasta el arranque de la cola, que por sí sola mide unos 20 centímetro(s), de cabeza redonda, lengua muy áspera, patas cortas y generalmente pelaje suave y espeso, de color blanco, gris, pardo, rojizo o negro, empleado en algunos lugares para cazar ratones. Usado en masculino referido a la especie.",
        "Minino"
    ],
    "banana": [
        "Fruta tropical procedente de la planta herbácea que recibe el mismo nombre o banano, perteneciente a la familia de las musáceas. Tiene forma alargada o ligeramente curvada"
    ],
    "pelota": [
        "Bola hecha de una materia que le permita botar, usada en diversos juegos y deportes.",
        "esférico"
    ]
    }

    ista = LeerDict(diccionario_maqueta)
    palabras,def_01,def_02,def_03 = cargarListas(lista)
    AgregoIndice(palabras)
    ConstruccionTableroVacio()


main()
