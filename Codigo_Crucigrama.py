#Importo librerias 
import random
import json

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
            
            
        
    return palabras,definiciones_1,definiciones_2,definiciones_3
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
IngresarPalabraNumero()
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

lista = LeerDict(diccionario)
palabras,def_01,def_02,def_03 = cargarListas(lista)


