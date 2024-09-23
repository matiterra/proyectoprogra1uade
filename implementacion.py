
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
    '''Función encargada de colocar el prefijo utilizando una palabra a analizar. (1 - C A S A)
       Esta función llama a la función lambda IniciaConNumero que devuelve True
        o False que verifica si la palabra a analizar tiene un dígito en el indice 0 o no.'''

    devolucion_palabras = []

    for i, palabra in enumerate(palabras_partida):
       
        devolucion_palabras.append(list(f"{i+1}"+ "-" + palabra))
    return devolucion_palabras

def ImpresionTablero(tablero):
    tablero_actualizado = []

    for fila in tablero:
        nueva_fila = []
        for elemento in fila:
            if elemento[0].isdigit() or elemento[0] == "-":
                nueva_fila.append(elemento[0])

            elif elemento[0].isalpha():
                nueva_fila.append("_")
            else:
                nueva_fila.append(" ")

        tablero_actualizado.append(nueva_fila)

    for fila in tablero_actualizado:
        print(" ".join(fila))

    return tablero_actualizado

def ImprimirTableroActualizado(tablero_actualizado, flag_palabra, palabras_con_indice, coordenadas, lista_direcciones, SeleccionaNumero):
    numero_indice = SeleccionaNumero - 1

    if flag_palabra == True:
        palabra = palabras_con_indice[numero_indice]
        coordenadas = coordenadas[numero_indice]
        direccion = lista_direcciones[numero_indice]

        if direccion in ["vertical-norte", "vertical-sur"]:
            direccion = "flag-vertical"
        elif direccion in ["horizontal-norte", "horizontal-sur"]:
            direccion = "flag-horizontal"

        print(direccion, coordenadas, palabra)

        if SeleccionaNumero == 1:
            coordenadas = [12, 12]
            direccion = "flag-horizontal"

        x, y = coordenadas
        
        for letra in palabra:
            tablero_actualizado [x][y] = str(letra)

            if direccion == "flag-horizontal":
                y = y + 1

            elif direccion == "flag-vertical":
                x = x + 1
                
        for fila in tablero_actualizado:
            nueva_fila = [celda[0] if isinstance(celda, list) else celda for celda in fila]
            print(" ".join(nueva_fila))

        return tablero_actualizado
    


def IngresarPalabraNumero(numero_palabra_encontrada):
    '''Función encargada del Ingreso de la palabra a adivinar siguiendo la lógica de número - palabra (1 - C A S A)
        Devuelve la palabra Ingresada, el número de la palabra a adivinar y si el usuario necesita una pista. '''
    bandera = True
    while bandera:
        try:
            SeleccionaNumero = int(input("Ingrese el número de la palabra que quiere adivinar ó de la que quiere consultar una Pista: "))
            if 1 <= SeleccionaNumero <= 5 and SeleccionaNumero not in numero_palabra_encontrada:
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
            bandera3 = False
            return IngresaPalabra, SeleccionaNumero, PedirPista
        else: 
            print("Por favor ingrese una palabra. Vuelva a intentarlo.")


def ValidarPalabra(palabras_con_indice, IngresaPalabra, SeleccionaNumero):
    numero_palabra_encontrada = []
    numero_indice = SeleccionaNumero - 1
    flag_palabra = False
    palabra_con_numero= f"{SeleccionaNumero}-{IngresaPalabra}"

    palabrita = "".join(palabras_con_indice[numero_indice])

    if palabra_con_numero == palabrita:
        print("Correcto! La palabra adivinada es correcta")
        flag_palabra = True

        numero_palabra_encontrada.append(SeleccionaNumero)
    else: 
        print("Incorrecto! La palabra adivinada no es correcta")
        
    return flag_palabra, numero_palabra_encontrada

def reiniciar_partida():
    print("\nReiniciando la partida...\n")
    main()
    
def main():
    lista =[
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
        "empresa", "encontrar", "enviar", "entender", "escribir", "esperanza", "espejo",
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
        "vida", "vivir", "volver", "voto", "yacer", "zanahoria", "zapato", "zona",
        "acertar", "alegrar", "apasionar", "cautivar", "claro", "compromiso", "construir",
        "dar", "destacar", "educación", "entusiasmo", "equilibrio", "esfuerzo", "experiencia",
        "fuerza", "generosidad", "gesto", "honestidad", "imaginación", "inspirar", "inteligencia",
        "liberación", "magnífico", "metas", "optimista", "pasión", "perseverancia", "recuerdo",
        "reflejo", "renacer", "sincero", "sorpresa", "temprano", "tranquilidad", "transformar",
        "valentía", "vigor", "visión", "vital", "zénit"
    ]


    
    diccionario = Buscolista_coincidencias(lista)
    tablero = ConstruccionTableroVacio()
    palabras_para_jugar, lista_direcciones, lista_coincidencias = LogicaConstruccion(lista, diccionario)
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
