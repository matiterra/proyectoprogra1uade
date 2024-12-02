import pytest

from implementacion import ImpresionTablero

def test_tablero_con_numeros():
    """Prueba con un tablero que contiene solo números."""
    tablero = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"]
    ]
    resultado_esperado = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"]
    ]
    assert ImpresionTablero(tablero) == resultado_esperado

def test_tablero_con_letras():
    """Prueba con un tablero que contiene solo letras."""
    tablero = [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"]
    ]
    resultado_esperado = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
    ]
    assert ImpresionTablero(tablero) == resultado_esperado

def test_tablero_con_guiones():
    """Prueba con un tablero que contiene solo guiones."""
    tablero = [
        ["-", "-", "-"],
        ["-", "-", "-"],
        ["-", "-", "-"]
    ]
    resultado_esperado = [
        ["-", "-", "-"],
        ["-", "-", "-"],
        ["-", "-", "-"]
    ]
    assert ImpresionTablero(tablero) == resultado_esperado

def test_tablero_con_espacios():
    """Prueba con un tablero que contiene solo espacios."""
    tablero = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    resultado_esperado = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    assert ImpresionTablero(tablero) == resultado_esperado

def test_tablero_mixto():
    """Prueba con un tablero que contiene una mezcla de números, letras, guiones y espacios."""
    tablero = [
        ["1", "A", "-"],
        [" ", "B", "2"],
        ["C", "3", " "]
    ]
    resultado_esperado = [
        ["1", "_", "-"],
        [" ", "_", "2"],
        ["_", "3", " "]
    ]
    assert ImpresionTablero(tablero) == resultado_esperado

def test_tablero_vacio():
    """Prueba con un tablero vacío."""
    tablero = []
    resultado_esperado = []
    assert ImpresionTablero(tablero) == resultado_esperado

def test_tablero_con_filas_vacias():
    """Prueba con un tablero que contiene filas vacías."""
    tablero = [
        [],
        [],
        []
    ]
    resultado_esperado = [
        [],
        [],
        []
    ]
    assert ImpresionTablero(tablero) == resultado_esperado
