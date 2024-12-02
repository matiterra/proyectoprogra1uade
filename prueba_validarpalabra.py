import pytest
from implementacion import ValidarPalabra

def test_validar_palabra_correcta():
    palabras_con_indice = ["0-casa", "1-gato", "2-perro"]
    assert ValidarPalabra(palabras_con_indice, "casa", 0) == True
    assert ValidarPalabra(palabras_con_indice, "gato", 1) == True
    assert ValidarPalabra(palabras_con_indice, "perro", 2) == True

def test_validar_palabra_incorrecta():
    palabras_con_indice = ["0-casa", "1-gato", "2-perro"]
    assert ValidarPalabra(palabras_con_indice, "perro", 0) == False
    assert ValidarPalabra(palabras_con_indice, "casa", 1) == False
    assert ValidarPalabra(palabras_con_indice, "gato", 2) == False

def test_validar_palabra_numero_invalido():
    palabras_con_indice = ["0-casa", "1-gato", "2-perro"]
    assert ValidarPalabra(palabras_con_indice, "casa", -1) == False
    assert ValidarPalabra(palabras_con_indice, "gato", 2) == False

def test_validar_palabra_vacia():
    palabras_con_indice = ["0-casa", "1-gato", "2-perro"]
    assert ValidarPalabra(palabras_con_indice, "", 0) == False
    assert ValidarPalabra(palabras_con_indice, "", 1) == False
    assert ValidarPalabra(palabras_con_indice, "", 2) == False