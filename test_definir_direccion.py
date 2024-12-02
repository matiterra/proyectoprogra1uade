import pytest
from unittest.mock import patch
from implementacion import definir_direccion

def test_direccion_norte():
    """Prueba cuando hay más letras antes del punto de intersección"""
    palabra = "ABCDEFGH"
    indice = 6
    assert definir_direccion(palabra, indice) == "norte"

def test_direccion_sur():
    """Prueba cuando hay más letras después del punto de intersección"""
    palabra = "ABCDEFGH"
    indice = 1
    assert definir_direccion(palabra, indice) == "sur"

@patch('random.randint')
def test_direccion_igual_norte(mock_randint):
    """Prueba caso de igual cantidad de letras, simulando random=1 (norte)"""
    # Configurar el mock para que retorne 1
    mock_randint.return_value = 1
    
    palabra = "ABCDE"
    indice = 2
    assert definir_direccion(palabra, indice) == "norte"

@patch('random.randint')
def test_direccion_igual_sur(mock_randint):
    """Prueba caso de igual cantidad de letras, simulando random=2 (sur)"""
    # Configurar el mock para que retorne 2
    mock_randint.return_value = 2
    
    palabra = "ABCDE"
    indice = 2
    assert definir_direccion(palabra, indice) == "sur"

