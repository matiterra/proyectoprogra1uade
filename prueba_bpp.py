# test_implementacion.py
import random
import pytest
from implementacion import BuscarPrimerPalabra

def test_buscar_primer_palabra():
    #Establecer una semilla para que el comportamiento aleatorio sea predecible
    random.seed(0)
    
    #Lista de palabras de prueba
    lista_palabras = [
        "casa", "gato", "elefante", "hipopotamo", "rinoceronte", "jirafa", "cocodrilo", "dinosaurio", "murcielago"
    ]
    
    #Ejecutar la función
    resultado = BuscarPrimerPalabra(lista_palabras)
    
    #Verificar que el resultado sea una lista con una palabra de 9 o más letras
    assert len(resultado) == 1
    assert len(resultado[0]) >= 9
    assert resultado[0] in lista_palabras

