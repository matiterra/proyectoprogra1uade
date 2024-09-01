# proyectoprogra1uade

Repositorio de la materia de Programación I de la carrera Licenciatura en Gestión de Proyectos de Sistemas de la Información - UADE

Primeras ideas:

1-Poder importar un archivo JSON con palabras y sus pistas correspondientes para poder utilizar y elegirlas de manera random para que cada partida sea distinta. El archivo podría contener 50 palabras o más - Al ser un JSON el archivo plano debe contar con la siguiente estructura: {"word":"DOG","definition1":"Un mejor amigo de los humanos", "definition2":"Animal Canino"}. Expansible ✔

2-Poder entrelazar palabras en vertical y horizontal por letras en común sin que se solapen. Podríamos agregar reglas como: que solamente se creen con mínimo una casilla de distancia, que tome en primer lugar la palabra mas larga elegida al azar y que construya a partir de ahí y que por cada palabra recien se tome en cuenta a partir del segundo elemento para construir el resto del crucigrama ya que los primero dos elementos siempre serán el número asociado y el guión. Ejemplo: ["1-Palabra"] solo se empezará a tener en cuenta a partir de la "P" en adelante ✔

3-Crear función para que al traer las palabras, que podrían ser 10 para empezar a probar, les añada un número y guión para que despues podamos ingresar el número de la palabra por teclado para poder adivinarla. Ejemplo: ["1-Palabra"] - Esta función debería traer todas las palabras y guardarlas en una lista, luego a través de un random.sample se crea una lista nueva y se utilizan las primeras diez palabras. ✔

4-Crear función para que separe todos los elementos de la palabra para poder imprimirlo luego con guiones. Ejemplo: ["1,-,P,A,L,A,B,R,A"]
Imprimir la primer letra de la primer palabra para poder empezar ✔

5-Crear función para poder indicar por consola cual palabra se desea elegir, una vez que se indica el número de la palabra printear en consola la primer definición asignada. Ofrecer la opción: "Intentar adivinar, solicitar otra definición o cambiar de palabra a elegir". Las definiciones que se vayan pidiendo tendrán que printearse de acuerdo a lo solicitado previamente. ✔

6-Poder ingresar por consola las letras correspondientes y manejo de excepciones. Podemos crear un diccionario y la función lambda para que solamente acepte esos caracteres y transformalos en mayusculas para que coincida graficamente con como se imprime. ✔

7-Informar correctamente el error del usuario. Ejemplo: "La palabra ingresada no es la correcta, vuelva a intentarlo.", "Los valores númericos y caracteres especiales no son válidos, vuelva a intentarlo." ✔

8-Crear función de repregunta y confirmación para volver a jugar al final o en caso de que quiera reiniciarse la partida. Para reiniciar el programa el usuario deberá ingresar por consola la palabra "reset". En el caso de que el usuario gane, se le preguntará si quiere volver a jugar o finalizar el programa. ✔

9-Crear un Sistema de Temáticas a elegir al empezar a jugar y que haya un modo en dónde las listas se Temáticas se mezclen entre sí.
Ejemplo: Jugadores de Fútbol, Vegetales o Informática. ✔

10-Si el usuario se queda trabado o necesita una pista, tendrá un comodin por partida (Se completará una palabra random mientras no sea la ultima que quede sin completar.) ✔

---

Primeras ideas sobre funciones a incluir en el programa:

def LeerJson(): ✔
#Función que se va a utilizar para leer los datos del archivo plano.

def CargarListas(): ✔
#Función que se va a encargar de llenar las N listas principales: - palabras = [] - definiciones1 = ["definición1"] - definiciones2 = ["definición2"] - definicionesN = ["definiciónN"]
En este caso, en la lista de palabras, se podría utilizar algo cómo:

for i in palabras_data:
palabras.append(list(i['word'])) --> Esto realizaría una lista de listas para tener las palabras separadas por letras: [["D","O","G"], ["C","A","T"]]
definiciones.append(i['definition'])

def BuscoCoincidencias(palabras):
#Función que se encarga de buscar letras dentro de las palabras de forma que guarde el Indice

def AgregoIndice(palabras):
#Función para agregar un Indice a cada palabra (Ejemplo: ["1,-,P,A,L,A,B,R,A"]), esto se haría agregando un elemento númerico que comience por uno y se vaya incrementando cada vez que se inserta con indice [0] dentro los elementos del arreglo de palabras. Una vez insertado se elimina del array esa palabra para continuar con la siguiente.

def ConstrucciónTablero(palabras):
#La idea de esta función es elegir que palabras van a ir en Vertical y cuales van a ir en Horizontal eligiendo desde las listas correspondientes.

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

---

1/9/2024

Planning Poker y estimación de esfuerzos para futura división de labores.

1- función LeerJson(parámetros E/S a revisar) ---> Puntos: 1 ---> Designación pendiente

2- función CargarListas(parámetros E/S a revisar) ---> Puntos: 1.5 ---> Rework y designación pendiente

3- función BuscoCoincidencias(parámetros E/S a revisar) ---> Puntos: 3.5 ---> Designación pendiente

4- función AgregoIndice(parámetros E/S a revisar) ---> Puntos: 2 ---> Designación pendiente

5- función ConstrucciónTablero(parámetros E/S a revisar) ---> Puntos: 8 ---> Es necesario modularizarla (pendiente)

6- función ImprimirTablero(parámetros E/S a revisar) ---> Puntos: 4 ---> Designación pendiente --- ¿Rework pendiente?

7- función IngresarPalabra(parámetros E/S a revisar) ---> Puntos: 2.5 ---> Designación Pendiente --- Permite que el usuario indique el indice de palabra que desea adivinar y revisa que la palabra pertenezca al conjunto de palabras del crucigrama

8- función ManejarErrores(parámetros E/S a revisar) ---> Puntos: 3.5 ---> Designación pendiente

9- función ReiniciarJuego(parámetros E/S a revisar) ---> Puntos: 1.5 ---> Designación pendiente

10- función SeleccionarModo(parámetros E/S a revisar) ---> Puntos: 1 ---> Designación pendiente

11- función SolicitarPista(parámetros E/S a revisar) ---> Puntos: 1 ---> Designación pendiente

Puntos totales: 29, 5 a dividir entre los 3 integrantes sin tener en cuenta que la función N° 5 todavia tiene que ser modularizada

---

Funciones necesarias para la primer entrega:

-Listas avanzadas y métodos de caracteres: 1 y 2 (maquetas, sin uso de archivos externos)

-Funciones lambda, math, filter y reduce: 5(a modularizar)

-Expresiones regulares: 7 y 5 (a modularizar)

-Manipulación avanzada de diccionarios: 3

-Tuplas y conjuntos: 4

-Excepciones: 8

---

Integrantes:

- Martin Schauvinhold
- Matias Terranova
- Luciano Perrella
