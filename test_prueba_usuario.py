import pytest
import json
import os
from implementacion import registrar_usuario, iniciar_sesion

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
CREDENCIALES_PATH = os.path.join(DIRECTORIO_ACTUAL, 'credenciales_test.json')

@pytest.fixture(autouse=True)
def setup_and_teardown():
    with open(CREDENCIALES_PATH, 'w', encoding='utf-8') as f:
        json.dump({}, f)
    yield
    if os.path.exists(CREDENCIALES_PATH):
        os.remove(CREDENCIALES_PATH)

def test_registrar_usuario_nuevo():
    assert registrar_usuario("abcde12", "clave123", archivo_credenciales=CREDENCIALES_PATH) is True
    with open(CREDENCIALES_PATH, 'r', encoding='utf-8') as f:
        credenciales = json.load(f)
    assert "abcde12" in credenciales

def test_iniciar_sesion_exitoso():
    registrar_usuario("abcde12", "clave123", archivo_credenciales=CREDENCIALES_PATH)
    assert iniciar_sesion("abcde12", "clave123", archivo_credenciales=CREDENCIALES_PATH) is True


def test_registrar_usuario_existente():
    registrar_usuario("usuario_existente", "clave123", archivo_credenciales=CREDENCIALES_PATH)
    assert registrar_usuario("usuario_existente", "claveNueva", archivo_credenciales=CREDENCIALES_PATH) is False

def test_iniciar_sesion_contrasenia_incorrecta():
    registrar_usuario("usuario_login", "clave123", archivo_credenciales=CREDENCIALES_PATH)
    assert iniciar_sesion("usuario_login", "claveIncorrecta", archivo_credenciales=CREDENCIALES_PATH) is False

def test_iniciar_sesion_usuario_no_existente():
    assert iniciar_sesion("usuario_no_existe", "clave123", archivo_credenciales=CREDENCIALES_PATH) is False
