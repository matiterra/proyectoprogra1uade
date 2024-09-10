#Importo librerias 
import random
import json

#Función encargada de leer json desde el archivo plano


def LeerJSON():
    lista_json = []
    with open("palabras.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        
        for clave in data.items():
            lista_json.append(list(clave))


    return lista_json

#Función encargada de cargar las dos listas principales: 1-Palabras 2-Definiciones
def cargarListas(lista):
    '''Función que se va a encargar de llenar las N listas principales: - palabras = [] - definiciones1 = ["definición1"] - definiciones2 = ["definición2"] - definicionesN = ["definiciónN"]. 
    En caso de solo llevar una definición, en su indice de la lista definiciones_2 se completará con un guión medio (-)'''
    
    

    palabras = []
    definiciones_1 = []
    definiciones_2 = []

    for i in range(len(lista)):
        palabras.append(list(lista[i][0]))
        if len(lista[i][1]) > 1:
            definiciones_1.append(lista[i][1][0])
            definiciones_2.append(lista[i][1][1])
        else:
            definiciones_1.append(lista[i][1][0])
            definiciones_2.append("-")

   

    return palabras,definiciones_1,definiciones_2
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
