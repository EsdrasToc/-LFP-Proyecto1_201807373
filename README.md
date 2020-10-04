BIENVENIDO!
A continuacion encontraras todo lo que necesitas saber para el uso de SimpleQL CLI.

Para comenzar, debes saber que SimpleQL CLI está hecho con el fin de manejar de forma
rapida y sencilla la informacion de archivos con extension .aon, debes tener en
cuenta que no se podra leer ningun otro tipo de archivo.

Antes de utilizar SimpleQL CLI debes tener la version 3.8.5 de python para que
SimpleQL CLI pueda funcionar de la mejor forma.

Recuerda que SimpleQL CLI es una herramienta que se utiliza en modo consola asi que
tendras que aprender los comandos existentes en SimpleQL CLI y presionar ENTER para 
hacer que funcionen. No te preocupes, a continuacion encontraras cada comando 
con su funcion y su forma de uso.

Ahora si, comencemos!

================================= Creacion de Sets =================================

SimpleQL CLI te ofrece la opcion de crear distintos sets para poder manejar tu in-
formacion de una manera mas eficiente y ordenada. ¿Que es un set? Imagina una carpeta
en donde podras guardar muchas paginas de informacion, eso es un set, un grupo al que
podras colocarle el nombre que desees con el fin de guardar ahi cierta informacion.

Cabe resaltar que siempre deberas crear un set para poder cargar la informacion, no
hay un set general.

Ejemplo:

    CREATE SET _Nombre_de_tu_set

*NOTA: el nombre de tu set no puede llevar espacios en blanco y no puede iniciar
con numeros, solo con un guion bajo o con letras. El resto del nombre puede llevar
numeros, guiones bajos o letras.

=============================== Carga de informacion ===============================

Para poder utilizar tu informacion, primero tendras que cargarla dentro del programa.
Para ello utilizaremos el comando LOAD INTO seguido de el nombre del set en el que
deseas guardar la informacion, luego continuaremos con la palabra FILES y por ultimo
colocaremos la direccion de los archivos que deseamos cargar. (Estos deben tener la
extension AON)

Ejemplo:

    LOAD INTO _Nombre_de_tu_set_ FILES archivo1.aon, archivo2.aon, archivo3.aon

Cabe resaltar que no es necesario cargar archivo por archivo, podemos ingresar
muchos archivos de golpe.

================================= Seleccion de Sets ================================

Para este momento ya hemos creado nuestros sets y cargado informacion dentro de 
ellos. Ademas, para los proximos 7 comandos, es un pre-requisito seleccionar un set.

Ya que la intecion es hacer consultas de nuestra informacion y ya la hemos ordenado
en sets, es necesario antes elegir el set que queremos consultar. Para ello utiliza-
remos el comando USE SET, seguido de el nombre de nuestro set.

Ejemplo:

    USE SET _Nombre_de_tu_set_

Tienes que tener en cuenta que el nombre debe ser identico a como fue guardado en
su creacion.

================================= Consulta de datos ================================

Podemos hacer distintos tipos de consultas con distintas condiciones, esto a travez
del comando SELECT.

CONSULTA GENERAL:
Para poder realizar una consulta general de un set, luego de SELECT haremos uso de un
asterisco (*), esto representa que nos mostrara todos los atributos de cada registro
dentro de el set que hayamos elegido.

Ejemplo:

    SELECT *

CONSULTA DE CIERTOS ATRIBUTOS:
Podemos hacer consultas omitiendo algunos atributos que no sean de nuestro interes.
En lugar de utilizar el asterisco (*), escribiremos una lista de los atributos que
deseamos ver separados por comas (,).

Ejemplo:

    SELECT _atributo

    SELECT _atributo1, _atributo2, _atributo3

CONSULTA CON CONDICIONES:
A las consultas generales y por atributos, podemos añadirle condiciones para filtrar
la informacion a nuestra conveniencia. Para ello añadiremos el comando WHERE seguido
de el atributo que deseamos comparar, un comparador y el contenido con el que desea-
mos comparar.

Los comparadores disponibles son menor que (<), mayor que (>), menor o igual (<=),
mayor o igual (>=), igual (=) y NO igual (!=).

Si el atributo que deseamos comparar es un numero, basta con colocar el numero luego
de el comparador; si es un booleano (verdadero o falso) tendremos que colocar True
para verdadero y False para falso; por ultimo, si el atributo guarda cadenas de texto
tendremos que encerrar las cadenas dentro de comillas dobles (").

Cabe resaltar que tenemos acceso a 3 operadores logicos con los cuales podremos fil-
trar con 2 condiciones. Estos operadores se utilizan añadiendo los comandos OR, AND
o XOR. El operador OR evaluara que por lo menos una de las 2 condiciones se cumpla;
el operador AND evaluara que ambas condiciones se cumplan; el operador XOR evaluara
que por lo menos una de las 2 condiciones se cumpla.

Ejemplos:

    SELECT * WHERE _atributo = 5

    SELECT _atributo1, _atributo2 WHERE _atributo1 > False AND _atributo3 != "asdf"

    SELECT _atributo1 WHERE _atributo1 >= False XOR _atributo2 <= 10

CONSULTAS CON REGEX:
SimpleQL CLI nos permite realizar busquedas con expresiones regulares, esto por medio
del comando REGEX y encapsular una expresion regular dentro de corchetes ([]).

¿Que es una expresion regular? La respuesta es simple, es una forma de "describir"
o "representar" el texto que deseamos buscar. Esto por medio de ciertas simbologias.
Suena complejo, ¿verdad?. No te preocupes, ahora te daremos ejemplos de como se
utilizan. Primero, conozcamos la simbologia y sus significados.

\+ : Define que el elemento anterior puede venir entre una y muchas veces.

\* : Define que el elemento anterior puede venir desde cero a muchas veces.

? : Define que el elemento anterior puede venir una vez o no venir.

() : Se utilizan para agrupar elementos, al estar agrupados se toman como uno solo al
aplicar cualquier otro de los operadores.

| : Se utiliza para separar opciones, es decir que en una cadena pueda venir el 
elemento a la izquierda o el elemento a la derecha.

^ : Se utiliza para definir cuál será el primer elemento en la cadena

\. : Denota cualquier caracter.

Ahora que ya conocemos cada simbolo y su uso, vamos con algunos ejemplos de REGEX
para aclarar las dudas.

Ejemplos de REGEX:

    [a+.] - esto quiere decir que puede venir una o muchas veces la letra a, seguida
    de cualquier caracter -> "aaaaaaaaaab", "ax", "a@"

    [^(ab)|..a] - significa que el texto puede iniciar con "ab" O pueden haber 2
    caracteres seguidos de una a -> "abcdefg", "kda", "@oa"

Ejemplo:

    SELECT * WHERE REGEX [a+.]

    SELECT _atributo1, _atributo2 WHERE REGEX [^(ab)|..a]

================================= Listar atributos =================================

Luego de seleccionar un set, podemos ver cuales son los attributos almacenados den-
tro de este set. Esto lo haremos con el comando LIST.

Ejemplo:

    LIST ATTRIBUTES

============================== Buscar el valor maximo ==============================

Si deseamos buscar el valor maximo en un atributo podemos utilizar el comando MAX
seguido de el atributo que deseamos evaluar. En los valores booleanos el valor True
siempre sera mayor que el valor False, y si intentamos encontrar el maximo de una
cadena de texto, se hara de forma lexicografica.

Ejemplo:

    MAX _atributo

============================== Buscar el valor minimo ==============================

Si deseamos buscar el valor minimo en un atributo podemos utilizar el comando MIN
seguido de el atributo que deseamos evaluar. En los valores booleanos el valor True
siempre sera mayor que el valor False, y si intentamos encontrar el minimo de una
cadena de texto, se hara de forma lexicografica.

Ejemplo:

    MIN _atributo

============================== Sumatoria de atributos ==============================

Podemos realizar sumatorias de los valores de ciertos atributos, es necesario que
tengamos en cuenta que esta opcion solamente sera funcional con atributos que alma-
cenen valores numericos. Este comando acepta el uso de asterisco (*)

Ejemplo:

    SUM *

    SUM _atributo1, _atributo2

============================ Conteo basado en atributos ============================

Si deseamos verificar cuantas veces aparece un atributo dentro de un set, podemos
utilizar el comando COUNT, este permite el uso de asterisco *

Ejemplo:

    COUNT *

    COUNT _atributo1, _atributo2

=========================== Reporte de consultas en HTML ===========================

Con la finalidad de que usted pueda guardar las consultas que necesite, SimpleQL CLI
le proporciona un comando que le permitira observar la informacion obtenida basandose
en una consulta dentro de un HTML, de una forma ordenada dentro de una tabla.
Para esto utilizara el comando REPORT TO, seguido de el nombre con el que quiere
guardar su archivo (debe colocar la extension .html) y la consulta que quiere guardar.

Ejemplo:

    REPORT TO archivo.html SELECT _atributo1 WHERE _atributo3 <= 9999

    REPORT TO archivo.html COUNT *

============================ Cambio de color en consola ============================

Si usted desea que el texto que aparece en pantalla cambie de color, puede utilizar
el comando PRINT IN seguido de alguno de los siguientes colores...

BLUE : azul
RED, : rojo
GREEN : verde
YELLOW : amarillo
ORANGE : anaranjado
PINK: rosado

Ejemplo:

    PRINT IN ORANGE

============================= Reporte de tokens en HTML ============================

El programa puede reportar los tokens encontrados dentro de cada instruccion ingre-
sada en el programa. El reporte se guardara con el nombre de REPORTE_TOKENS.html

Ejemplo:

    REPORT TOKENS

========================= Ingreso de instrucciones externas ========================

Para evitar ingresar solamente una instruccion a la vez, podemos ingresar muchas por
medio de el comando SCRIPT, seguido de la direccion de un archivo con extension
.siql

Ejemplo:

    SCRIPT instrucciones.siql

    SCRIPT instrucciones1.siql, instrucciones2.siql

=================================== Archivos .AON ==================================

Los archivos en donde esté guardada la informacion deben tener la extensio .aon
y cumplir con la notacion del mismo.

() : Los paréntesis definen un arreglo, todo lo que se encuentra adentro es un 
elemento del mismo.

<> : Estos símbolos definen un objeto, los atributos de un objeto están separados 
por comas.

[] : Se utilizan para definir identificadores, o en otras palabra el nombre de un 
atributo.

Ejemplo:

    (
        <
            [atributo_numerico] = 45.09,
            [atributo_cadena] = "hola mundo",
            [atributo_booleano] = true
        >,
        <
            [atributo_numerico] = 4,
            [atributo_cadena] = "adios mundo",
            [atributo_booleano] = false
        >,
        <
            [atributo_numerico] = -56.4,
            [atributo_cadena] = "este es otro ejemplo, las cadenas pueden ser 
            muy largas",
            [atributo_booleano] = false
        >
    )

================================== Archivos .SIQL ==================================

Para el comando SCRIPT los archivos que carguemos deben tener la extension .siql,
es muy sencillo de utilizar, simplemente escribimos las instrucciones en orden de
como deseamos que se ejecuten separadas por punto y coma (;).

Ejemplo:

    create hola;
    load into hola files prueba.aon, prueba2.aon, prueba3.aon;
    use set hola;
    print in color blue;
    select lala, atributo_booleano where lala = 4;
    print in color green;
    min *;
    print in color pink;
    max *;
    print in color orange;
    sum lala, atributo_booleano;
    print in color yellow;
    Count *;
    report to reportePrueba.html min *;
    print in color green;
    select *;
    print in color yellow;
    select * where atributo_cadena regex [^(ad)];
    print in red;
    select * where atributo_cadena regex [^j];
    report tokens;
    exit