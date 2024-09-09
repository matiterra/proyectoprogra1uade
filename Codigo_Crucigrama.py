#Importo librerias 
import random
import json

#Función encargada de leer json desde el archivo plano
def LeerJson():
    with open('palabras.json', 'r') as file:
        palabras_data = json.load(file)
    return palabras_data

#Función encargada de cargar las dos listas principales: 1-Palabras 2-Definiciones
def CargarListas(palabras_data):
    palabras = []
    definiciones = []

    for _ in palabras_data:
        palabras.append(list(_['word']))
        definiciones.append(_['definition'])

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


#MAIN
IngresarPalabraNumero()
