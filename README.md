# proyectoprogra1uade

Repositorio de la materia de Programación I de la carrera Licenciatura en Gestión de Proyectos de Sistemas de la Información - UADE

Primeras ideas:

1-Poder importar un archivo JSON con palabras y su pista correspondiente para poder utilizar y elegirlas de manera random para que cada partida sea distinta. El archivo podría contener 50 palabras o más - Al ser un JSON el archivo plano debe contar con la siguiente estructura: {"word":"DOG","definition":"Un mejor amigo de los humanos"}. Expansible

2-Poder entrelazar palabras en vertical y horizontal por letras en común sin que se solapen. Podríamos agregar reglas como: que solamente se creen con mínimo una casilla de distancia , que tome en primer lugar la palabra mas larga elegida al azar y que construya a partir de ahí y que por cada palabra recien se tome en cuenta a partir del segundo elemento para construir el resto del crucigrama ya que los primero dos elementos siempre serán el número asociado y el guión. Ejemplo: ["1-Palabra"] solo se empezará a tener en cuenta a partir de la "P" en adelante

3-Crear función para que al traer las palabras, que podrían ser 10 para empezar a probar, les añada un número y guión para que despues podamos ingresar el número de la palabra por teclado para poder adivinarla. Ejemplo: ["1-Palabra"] - Esta función debería traer todas las palabras y guardarlas en una lista, luego a través de un random.sample se crea una lista nueva y se utilizan las primeras diez palabras.

4-Crear función para que separe todos los elementos de la palabra para poder imprimirlo luego con guiones. Ejemplo: ["1,-,P,A,L,A,B,R,A"]

¿Imprimir la primer letra de la primer palabra para poder empezar? - Puede ser según la dificultad elegida.

5-Crear función para poder indicar por consola cual palabra se desea adivinar

6-Poder ingresar por consola las letras correspondiente y manejo de excepciones. Podemos crear un diccionario y la función lambda para que solamente acepte esos caracteres y transformalos en mayusculas para que coincida graficamente con como se imprime (¿ingresar la palabra en una sola interacción?)

7-Informar correctamente el error del usuario. Ejemplo: "La palabra ingresada no es la correcta, vuelva a intentar.", "Los valores númericos y caracteres especiales no son válidos, vuelva a intentar"

8-Crear función de re pregunta y confirmación para volver a jugar al final o en caso de que quiera reiniciarse la partida

9-¿Dificultades distintas?

10-¿Incluír varias pistas en caso de que el jugador solicite ayuda?


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Primeras ideas sobre funciones a incluir en el programa:

def LeerJson():
#Función que se va a utilizar para leer los datos del archivo plano.

def CargarListas():
#Función que se va a encargar de llenar las dos listas principales: 
                                                                    - palabras = []
                                                                    - definiciones = []
En este caso, en la lista de palabras, se podría utilizar algo cómo: 

for _ in palabras_data:
    palabras.append(list(_['word']))  --> Esto realizaría una lista de listas para tener las palabras separadas por letras: [["D","O","G"], ["C","A","T"]]
    definiciones.append(_['definition'])

def AgregoIndice(palabras):
#Función para agregar un Indice a cada palabra (Ejemplo: ["1,-,P,A,L,A,B,R,A"]), esto se haría agregando un elemento númerico que comience por uno y se vaya incrementando cada vez que se inserta con indice [0] dentro los elementos del arreglo de palabras. Una vez insertado se elimina del array esa palabra para continuar con la siguiente.

def PalabrasVerticales(palabras):
#¿Funcion para crear un listado de palabras que van a ir en forma vertical?

def ImprimirTablero(tablero):
#Función para imprimir el tablero en la consola, mostrando las palabras y guiones.

def IngresarPalabra(numero_palabra, palabra, tablero):
#Función para que el usuario ingrese una palabra por consola y verificar si es correcta.

def ManejarErrores(entrada):
#Función para manejar errores en la entrada de datos del usuario.

def ReiniciarJuego():
#Función para reiniciar el juego o iniciar una nueva partida.

def SeleccionarDificultad():
#Función para que el usuario seleccione el nivel de dificultad.

def SolicitarPista():
#Función para que el usuario solicite una pista.

------------------------------------------------------------------------------------------------------------------------------------------------

Integrantes:
- Martin Schauvinhold 
- Matias Terranova
- Luciano Perrella
