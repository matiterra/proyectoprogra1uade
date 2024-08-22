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
