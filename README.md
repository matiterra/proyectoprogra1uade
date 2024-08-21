# proyectoprogra1uade

Repositorio de la materia de Programación I de la carrera Licenciatura en Gestión de Proyectos de Sistemas de la Información - UADE

Primeras ideas:

1-Poder importar un archivo JSON con palabras y su pista correspondiente para poder utilizar y elegirlas de manera random para que cada partida sea distinta. El archivo podría contener 50 palabras o más. Expansible

2-Poder entrelazar palabras en vertical y horizontal por letras en común sin que se solapen. Podríamos agregar reglas como: que solamente se creen con mínimo una casilla de distancia , que tome en primer lugar la palabra mas larga elegida al azar y que construya a partir de ahí y que por cada palabra recien se tome en cuenta a partir del segundo elemento para construir el resto del crucigrama ya que los primero dos elementos siempre serán el número asociado y el guión. Ejemplo: ["1-Palabra"] solo se empezará a tener en cuenta a partir de la "P" en adelante

3-Crear función para que al traer las palabras, que podrían ser 10 para empezar a probar, les añada un número y guión para que despues podamos ingresar el número de la palabra por teclado para poder adivinarla. Ejemplo: ["1-Palabra"]

4-Crear función para que separe todos los elementos de la palabra para poder imprimirlo luego con guiones. Ejemplo: ["1,-,P,A,L,A,B,R,A"]

¿Imprimir la primer letra de la primer palabra para poder empezar?

5-Crear función para poder indicar por consola cual palabra se desea adivinar

6-Poder ingresar por consola las letras correspondiente y manejo de excepciones. Podemos crear un diccionario y la función lambda para que solamente acepte esos caracteres y transformalos en mayusculas para que coincida graficamente con como se imprime (¿ingresar la palabra en una sola interacción?)

7-Informar correctamente el error del usuario. Ejemplo: "La palabra ingresada no es la correcta, vuelva a intentar.", "Los valores númericos y caracteres especiales no son válidos, vuelva a intentar"

8-Crear función de re pregunta y confirmación para volver a jugar al final o en caso de que quiera reiniciarse la partida

9-¿Dificultades distintas?

10-¿Incluír varias pistas en caso de que el jugador solicite ayuda?
