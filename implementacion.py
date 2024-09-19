
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
            
def calcularFila(fila_anterior,indice,direccion):
    

    if direccion in ["horizontal-sur" ,"horizontal-norte"]:
        fila_siguiente = fila_anterior + indice
    
    else: 
        fila_siguiente = fila_anterior - indice  
    
   
    return fila_siguiente


def ConstruccionTableroVacio():
    '''Función encargada de generar un tablero vacio con el centro marcado con un *'''

    filas = 30
    columnas = 30
    tablero_vacio = [[list(" ") for i in range(columnas)] for i in range(filas)]

    tablero_vacio[9][9] = list("*")

    # for fila in tablero_vacio:
    #     print(fila)

    return tablero_vacio

def calcularColumna(columna_anterior,indice,direccion):
    if direccion in ["vertical-norte","vertical-sur"]:
        columna_siguiente = columna_anterior + indice 

    else:
        columna_siguiente = columna_anterior - indice


   
    return columna_siguiente

def LogicaConstruccion(lista_palabras,diccionario):
    '''Esta función delimitará la lógica de construcción partida a partida a partir del primer 
    llamado a la función anterior: "BuscarPrimerPalabra" que devolverá una palabra que minimamente tenga 7 caracteres o más. La palabras irán de a pares: Horizontales y Verticales'''
    
    #La primer palabra siempre se utilizará de manera horizontal
    palabras_partida = BuscarPrimerPalabra(lista_palabras)
    lista_direcciones = ["-"]
    lista_coincidencias = ["-"]
    
    flag_direccion = ""
    while len(palabras_partida) != 4:
        if len(palabras_partida) == 1: #segunda palabra
            indice_letra_a_buscar = random.randint(0,2)
            letra_palabra = palabras_partida[0][indice_letra_a_buscar]
            siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
            palabras_partida.append(siguiente_palabra)
            # if len(indice_coincidencia) == 1:
            lista_coincidencias.append([palabras_partida[0].index(letra_palabra),indice_coincidencia[0]])
            # else:
            #     lista_coincidencias.append([indice_letra_a_buscar,indice_coincidencia[0][0]])
            flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
            lista_direcciones.append("vertical-"+flag_direccion)
            
        if len(palabras_partida) == 2: #tercera palabra - depende de como se formó la primera
            if lista_direcciones[1].count("norte") > 0:
                flag_direccion = "sur"
                indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while siguiente_palabra[0] != letra_palabra and siguiente_palabra not in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))#esto tendría que ser una palabra que empiece con la última letra de la primer palabra horizontal
                 #índice que tiene la letra de la palabra que voy a traer del diccionario de lista_coincidencias
                # if len(indice_coincidencia) == 1:
                lista_coincidencias.append([palabras_partida[0].index(letra_palabra),indice_coincidencia[0]])
                # else:
                #     lista_coincidencias.append([indice_letra_a_buscar,indice_coincidencia[0][0]])
                palabras_partida.append(siguiente_palabra)
                lista_direcciones.append("vertical-"+flag_direccion)
                
            else:
                flag_direccion = "norte"
                lista_direcciones.append("vertical-"+flag_direccion)
                indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[0][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                while siguiente_palabra[-1] != letra_palabra and siguiente_palabra not in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) #esto tendría que ser una palabra que termine con la última letra de la primer palabra horizontal
                # if len(indice_coincidencia) == 1:
                lista_coincidencias.append([palabras_partida[0].index(letra_palabra),indice_coincidencia[0]])
                # else:
                #     lista_coincidencias.append([indice_letra_a_buscar,indice_coincidencia[0][0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)

                
                palabras_partida.append(siguiente_palabra)
                
                
        if len(palabras_partida) == 3:
            if lista_direcciones[1].count("norte") > 0: #cuarta palabra, depende de como se formó la segunda
                indice_letra_a_buscar = 0
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items())) #se buscará un coincidencia con la primer letra de la palabra N° 2
                while siguiente_palabra[0] != letra_palabra and siguiente_palabra not in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                # if len(indice_coincidencia) == 1:
                lista_coincidencias.append([palabras_partida[1].index(letra_palabra),indice_coincidencia[0]])
                # else:
                #     lista_coincidencias.append([indice_letra_a_buscar,indice_coincidencia[0][0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+ flag_direccion)
                
                palabras_partida.append(siguiente_palabra)
           
            else:
                indice_letra_a_buscar = -1
                letra_palabra = palabras_partida[1][indice_letra_a_buscar]
                siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))#Se buscará una coincidencia con la última letra de la palabra N°2
                while siguiente_palabra[-1] != letra_palabra and siguiente_palabra not in palabras_partida:
                    siguiente_palabra, indice_coincidencia = random.choice(list(diccionario.get(letra_palabra).items()))
                # if len(indice_coincidencia) == 1:
                lista_coincidencias.append([palabras_partida[1].index(letra_palabra),indice_coincidencia[0]])
                # else:
                #     lista_coincidencias.append([indice_letra_a_buscar,indice_coincidencia[0][0]])
                flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia[0])
                lista_direcciones.append("horizontal-"+flag_direccion)
                palabras_partida.append(siguiente_palabra)
        # if len(palabras_partida) == 4: #Quinta palabra, depende de la palabra 3
        #     if lista_direcciones[2] == "norte":
        #         indice_letra_a_buscar = 0
        #         letra_palabra = palabras_partida[2][indice_letra_a_buscar]
        #         siguiente_palabra = random.choice(diccionario_lista_coincidencias.get(letra_palabra)) #se buscará una coincidencia con la primer letra
        #         #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de lista_coincidencias
        #         # flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia)
        #         #lista_direcciones.append("horizontal-"flag_direccion)
        #         palabras_partida.append(siguiente_palabra)
        #     else:
        #         indice_letra_a_buscar = -1
        #         letra_palabra = palabras_partida[2][indice_letra_a_buscar]
        #         siguiente_palabra = random.choice(diccionario_lista_coincidencias.get(letra_palabra))  #se buscará coincidencia con la última letra
        #         #indice_coincidencia = #índice que tiene la letra de la palabra que voy a traer del diccionario de lista_coincidencias
        #         # flag_direccion = definir_direccion(siguiente_palabra,indice_coincidencia)
        #         #lista_direcciones.append("horizontal-"flag_direccion)
        #         palabras_partida.append(siguiente_palabra)
    return palabras_partida,lista_direcciones,lista_coincidencias

def ConstruirTablero(tablero,lista_palabras,lista_coincidencias,direcciones):
    indice_fila_inicial = 9
    indice_columna_inicial = 9
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
                

            # elif i == 3: #Cuarta Palabra - Horizontal - Depende de la Palabra N° 2
            #     proxima_fila = calcularFila(coordenadas[1][0],lista_coincidencias[i][0],direcciones[i])
            #     proxima_columna = calcularColumna(coordenadas[1][1],lista_coincidencias[i][1],direcciones[i])
            #     if len(coordenadas) == 3: #Guardo las coordenadas
            #         coordenadas.append([proxima_fila,proxima_columna])
            #     tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]
                
            # elif i == 4: #Quinta Palabra - Horizontal - Depende de la plabra N 3
            #     proxima_fila = calcularFila(coordenadas[2][0],lista_coincidencias[i][0],direcciones[i])
            #     proxima_columna = calcularColumna(coordenadas[2][1],lista_coincidencias[i][1],direcciones[i])
            #     if len(coordenadas) == 4: #Guardo las coordenadas
            #         coordenadas.append([proxima_fila,proxima_columna])
            #     tablero[proxima_fila][proxima_columna + j][0] = lista_palabras[i][j]
            #     print(coordenadas)
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
                
          


                

          
                



    return tablero







#MAIN
lista = [
    "abaco", "abandonar", "abierto", "abogado", "abundante", "acuerdo", "acusar", "adelante",
    "admirar", "adverso", "afecto", "agregar", "ahora", "alcance", "alegría", "alivio",
    "alumno", "amar", "análisis", "anhelo", "anotar", "ansioso", "aprender", "aprecio",
    "aroma", "arte", "asistente", "asociar", "atender", "atrasar", "atún", "avanzar",
    "bailar", "banco", "barco", "bello", "beso", "bicho", "brillante", "brindar",
    "cabeza", "cambiar", "camino", "cantar", "capacidad", "caracter", "cargar", "carta",
    "causar", "celebrar", "cielo", "ciudad", "claridad", "cohesión", "comunicar", "compañero",
    "comprender", "conectar", "consentir", "contar", "correr", "crear", "crédito", "cultivar",
    "curiosidad", "dar", "decidir", "dedicar", "defender", "delicado", "demostrar", "deporte",
    "desafío", "descubrir", "deseo", "destino", "detener", "difundir", "diligente", "disfrutar",
    "divertido", "doctor", "dolar", "educar", "efectivo", "efecto", "elegir", "emocionar",
    "empresa", "encontrar", "enviar", "entender", "enviar", "escribir", "esperanza", "espejo",
    "estudiante", "estilo", "eterno", "evidente", "exitoso", "felicidad", "feliz", "futuro",
    "ganar", "generar", "gente", "globo", "gusto", "hablar", "herencia", "historia",
    "honor", "hospital", "humano", "idea", "iluminar", "imaginación", "impulso", "importante",
    "inclusión", "iniciar", "innovar", "intención", "intentar", "interesante", "inversión",
    "jardín", "juego", "juntar", "lápiz", "lavar", "libertad", "libro", "luz", "magia",
    "maravilla", "medida", "mientras", "misterio", "modificar", "motivo", "mover", "música",
    "navegar", "naturaleza", "nube", "ocurrir", "ofrecer", "opción", "optimismo", "organizar",
    "paz", "pedir", "pensar", "pequeño", "placer", "plena", "pluma", "poder", "preguntar",
    "probar", "promesa", "propósito", "pueblo", "razón", "recibir", "reconocer", "reflejar",
    "regresar", "relación", "reparar", "requerir", "resolver", "respeto", "resultar", "reunir",
    "saber", "salud", "salir", "satisfacción", "seguir", "semilla", "sentido", "sueño",
    "sorpresa", "sostenible", "sumar", "superar", "sustento", "suerte", "tarea", "tiempo",
    "trabajo", "tranquilidad", "tratar", "unir", "valer", "valor", "variar", "viajar",
    "vida", "vivir", "volver", "voto", "yacer", "zanahoria", "zapato", "zona"
]


diccionario = Buscolista_coincidencias(lista)
tablero = ConstruccionTableroVacio()

palabras_para_juga,lista_direcciones,lista_coincidencias = LogicaConstruccion(lista,diccionario)

palabras_separadas = []

for palabra in palabras_para_juga:
    palabras_separadas.append(list(palabra))


producto_final = ConstruirTablero(tablero,palabras_separadas,lista_coincidencias,lista_direcciones)
print(palabras_separadas,lista_direcciones,lista_coincidencias)


for fila in producto_final:
    print(fila)
