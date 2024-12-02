import pytest
import json
import os
from implementacion import registrar_usuario, iniciar_sesion

#Obtener la ruta del directorio actual del archivo de prueba
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
CREDENCIALES_PATH = os.path.join(DIRECTORIO_ACTUAL, 'credenciales.json')

@pytest.fixture(autouse=True)
def setup_and_teardown():
    #Configuración: crear un archivo de credenciales vacío antes de cada prueba
    with open(CREDENCIALES_PATH, 'w', encoding='utf-8') as f:
        json.dump({}, f)
    yield
    #Limpieza: eliminar el archivo de credenciales después de cada prueba
    os.remove(CREDENCIALES_PATH)

def test_registrar_usuario_nuevo():
    assert registrar_usuario("usuario_nuevo", "contrasenia123") == True
    with open(CREDENCIALES_PATH, 'r', encoding='utf-8') as f:
        credenciales = json.load(f)
    assert "usuario_nuevo" in credenciales

def test_registrar_usuario_existente():
    registrar_usuario("usuario_existente", "contrasenia123")
    assert registrar_usuario("usuario_existente", "otra_contrasenia") == False

def test_iniciar_sesion_exitoso():
    registrar_usuario("usuario_login", "contrasenia123")
    assert iniciar_sesion("usuario_login", "contrasenia123") == True

def test_iniciar_sesion_contrasenia_incorrecta():
    registrar_usuario("usuario_login", "contrasenia123")
    assert iniciar_sesion("usuario_login", "contrasenia_incorrecta") == False

def test_iniciar_sesion_usuario_no_existente():
    assert iniciar_sesion("usuario_no_existente", "contrasenia123") == False