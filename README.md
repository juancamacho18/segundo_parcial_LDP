# segundo_parcial_LDP

## Punto 1: Diseño de Gramática para Lenguaje CRUD

- Descripción del Lenguaje

Gramática formal para un lenguaje de programación que permite realizar operaciones CRUD (Create, Read, Update, Delete) en una base de datos.

- Especificación de la Gramátical

Símbolo Inicial

    S

Tipos de Sentencias

    SENTENCIA -> CREATE | READ | UPDATE | DELETE

Sentencia CREATE (Crear tabla)

    CREATE -> 'create' 'table' ID '(' CAMPOS ')'
    CAMPOS -> CAMPO CAMPOS_FINAL
    CAMPOS_FINAL -> ',' CAMPO CAMPOS_FINAL | ε
    CAMPO -> ID TIPO
    TIPO -> 'int' | 'string' | 'float'

Sentencia READ (Consultar datos)

    READ -> 'select' COLUMNAS 'from' ID CONDICION_WHERE
    COLUMNAS -> '*' | ID COLUMNAS_FINAL
    COLUMNAS_FINAL -> ',' ID COLUMNAS_FINAL | ε
    CONDICION_WHERE -> 'where' CONDICION | ε
    CONDICION -> ID OPER VALOR
    OPER -> '=' | '<' | '>' | '<=' | '>=' | '!='
    VALOR -> NUMERO | CADENA

Sentencia UPDATE (Actualizar datos)

    UPDATE -> 'update' ID 'set' ASIGNACIONES CONDICION_WHERE
    ASIGNACIONES -> ASIGNACION ASIGNACIONES_FINAL
    ASIGNACIONES_FINAL -> ',' ASIGNACION ASIGNACIONES_FINAL | ε
    ASIGNACION -> ID '=' VALOR

Sentencia DELETE (Eliminar datos)

    DELETE -> 'delete' 'from' ID CONDICION_WHERE

Terminales

    ID -> letra (letra | digito | '_')*
    NUMERO -> digito+
    CADENA -> '"' (caracter)* '"'

- Ejemplos de Sentencias Válidas

      create table empleados (id int, nombre string, salario float)
      create table productos (codigo int, descripcion string, precio float)

- Características del Lenguaje

1. Tipos de Datos Soportados

- int: Valores enteros

- string: Cadenas de texto entre comillas dobles

- float: Valores decimales

2. Operadores de Comparación

-  = : Igualdad

-  < : Menor que

-   > : Mayor que

-  <= : Menor o igual que

-   >= : Mayor o igual que

-  != : Diferente de

3. Estructuras Principales

CREATE TABLE

- Permite definir nuevas tablas

- Especificación de campos con tipos de datos

- Múltiples campos separados por comas

SELECT

- Consulta de datos con proyección de columnas

- Soporta * para todas las columnas

- Condiciones WHERE opcionales

- Múltiples condiciones posibles

UPDATE

- Actualización de registros

- Múltiples asignaciones en una sola sentencia

- Condición WHERE opcional

DELETE

- Eliminación de registros

- Condición WHERE opcional (si se omite, elimina todos los registros)

Definición Formal de la Gramática

- Terminales:

      { 'create', 'table', 'select', 'from', 'where', 'update', 'set', 'delete',
      'int', 'string', 'float', '*', '=', '<', '>', '<=', '>=', '!=',
      ID, NUMERO, CADENA }

- No Terminales:

        { S, SENTENCIA, CREATE, READ, UPDATE, DELETE, CAMPOS, CAMPOS_FINAL, CAMPO, TIPO,
          COLUMNAS, COLUMNAS_FINAL, CONDICION_WHERE, CONDICION, OPER, VALOR,
          ASIGNACIONES, ASIGNACIONES_FINAL, ASIGNACION }

## Punto 2: Proyecto Parser CRUD - ANTLR con Java

Descripción
Implementación de un analizador léxico y sintáctico para un lenguaje de operaciones CRUD (Create, Read, Update, Delete) usando ANTLR 4 con Java.

Requisitos:

- Java JDK 8 o superior

- ANTLR 4.9 o superior

- Sistema operativo: Windows, Linux o macOS

Estructura del proyecto:

    2/
    ├── CRUD.g4                 # Gramática ANTLR
    └── test.sql               # Archivo de pruebas

- Uso

1. Generar el lexer y parser

        antlr4 CRUD.g4

2. Compilar las clases Java

        javac CRUD*.java

3. Probar la gramática

- Modo consola (árbol textual):

        grun CRUD programa test.sql

- Modo árbol gráfico:

        grun CRUD programa test.sql -gui

- Modo tokens:

        grun CRUD programa test.sql -tokens

- Modo árbol en consola:

        grun CRUD programa test.sql -tree

Ejemplos de sentencias válidas

    create table empleados (id int, nombre string, salario float)
    select * from empleados where salario > 2000
    update empleados set salario = 3000 where id = 5
    delete from empleados where nombre = "Juan"
    select id, nombre from productos where precio <= 100

Gramática implementada
La gramática soporta:

- CREATE: Creación de tablas con campos tipados

- SELECT: Consultas con o sin condiciones WHERE

- UPDATE: Actualizaciones con múltiples asignaciones

- DELETE: Eliminaciones con condiciones opcionales

- Tipos de datos: int, string, float

- Operadores comparación: =, <, >, <=, >=, !=

## Punto 3: Analizador sintactico ascendente

Implementación de un analizador sintactico ascendente de una gramatica para expresiones aritmeticas simples además de calculadr conjuntos de primeros, siguientes y de predicciones. La gramatica a utilizar es la siguiente:


Las metas para completar el ejercicio fueron las sigueintes:

*Convertir gramatica LL(1)

La gramatica originalmente esta establecida de esta manera

E->E + T

E->T

T-> T * F

T-> F

F->( E )

F->id

Como se puede notar, hay recursividad hacia la izquierda en las producciones de E y T, por lo que hay que arreglar esto de tal manera de eliminar esa recursividad y de esa manera lograr que la gramatica sea LL(1), realizando esto, entonces la gramatica queda asi

E->T E'

E'-> + T E'

E'->ε

T->F T'

T'->* F T'

T'->ε

F-> ( E )

F-> id

logrando eliminar recursividad, y factores comunes a la izquierda



*calcular conjuntos de primeros, siguientes y de predicciones

Dentro del programa hay algoritmos para calcular todo los conjuntos, por lo que solo imprimiendolos es posible observar cuales son para la gramatica que se usa (esta obviamente ya trasnformada en LL(1)).

>Primeros:
>
>Primero(Term')= {'ε', '*', '/'}
>
>Primero(Expr')= {'+', 'ε', '-'}
>
>Primero(Expr)= {'id', '('}
>
>Primero(Term)= {'id', '('}
>
>Primero(Fact)= {'id', '('}
>
>
>Siguientes:
>
>Siguiente(Expr)= {'$', ')'}
>
>Siguiente(Expr')= {'$', ')'}
>
>Siguiente(Term)= {'$', '+', ')', '-'}
>
>Siguiente(Term')= {'$', '+', ')', '-'}
>
>Siguiente(Fact)= {'-', '$', ')', '+', '*', '/'}
>
>
>
>Conjuntos de prediccion:
>
>Expr -> Term Expr' {'id', '('}
>
>Expr' -> + Term Expr' {'+'}
>
>Expr' -> - Term Expr' {'-'}
>
>Expr' -> ε {'$', ')'}
>
>Term -> Fact Term' {'id', '('}
>
>Term' -> * Fact Term' {'*'}
>
>Term' -> / Fact Term' {'/'}
>
>Term' -> ε {'$', '+', ')', '-'}
>
>Fact -> ( Expr ) {'('}
>
>Fact -> id {'id'}


*el algoritmo ascendente

Se realiza el proceso de desplazamiento y reducción (shift-reduce), aplicando las reglas de producción hasta determinar si la expresión es válida.

*pruebas y resultados

realizando las pruebas para las cadenas de cadenas.txt:

id + id * id

( id + id ) * id

( id )

id + ( id / id )

id : id

El resultado que genera al ejecutar el programa, muestra lo siguiente:

    Analizando: id + id * id
    Pila                                    Entrada                       Acción
    ------------------------------------------------------------------------------------------
    id                                      + id * id $                   Desplazar
    Fact                                    + id * id $                   Reducir: F → id
    Term                                    + id * id $                   Reducir: T → F
    Expr                                    + id * id $                   Reducir: E → T
    Expr +                                  id * id $                     Desplazar
    Expr + id                               * id $                        Desplazar
    Expr + Fact                             * id $                        Reducir: F → id
    Expr + Term                             * id $                        Reducir: T → F
    Expr                                    * id $                        Reducir: E → E + T
    Expr *                                  id $                          Desplazar
    Expr * id                               $                             Desplazar
    Expr * Fact                             $                             Reducir: F → id
    Expr * Term                             $                             Reducir: T → F
    Expr * Expr                             $                             Reducir: E → T
    Expr * Expr                                                           no aceptado
    
    Analizando: ( id + id ) * id
    Pila                                    Entrada                       Acción
    ------------------------------------------------------------------------------------------
    (                                       id + id ) * id $              Desplazar
    ( id                                    + id ) * id $                 Desplazar
    ( Fact                                  + id ) * id $                 Reducir: F → id
    ( Term                                  + id ) * id $                 Reducir: T → F
    ( Expr                                  + id ) * id $                 Reducir: E → T
    ( Expr +                                id ) * id $                   Desplazar
    ( Expr + id                             ) * id $                      Desplazar
    ( Expr + Fact                           ) * id $                      Reducir: F → id
    ( Expr + Term                           ) * id $                      Reducir: T → F
    ( Expr                                  ) * id $                      Reducir: E → E + T
    ( Expr )                                * id $                        Desplazar
    Fact                                    * id $                        Reducir: F → ( E )
    Term                                    * id $                        Reducir: T → F
    Term *                                  id $                          Desplazar
    Term * id                               $                             Desplazar
    Term * Fact                             $                             Reducir: F → id
    Term                                    $                             Reducir: T → T * F
    Expr                                    $                             Reducir: E → T
    Expr                                    $                             aceptado
    
    Analizando: ( id )
    Pila                                    Entrada                       Acción
    ------------------------------------------------------------------------------------------
    (                                       id ) $                        Desplazar
    ( id                                    ) $                           Desplazar
    ( Fact                                  ) $                           Reducir: F → id
    ( Term                                  ) $                           Reducir: T → F
    ( Expr                                  ) $                           Reducir: E → T
    ( Expr )                                $                             Desplazar
    Fact                                    $                             Reducir: F → ( E )
    Term                                    $                             Reducir: T → F
    Expr                                    $                             Reducir: E → T
    Expr                                    $                             aceptado
    
    Analizando: id + ( id / id )
    Pila                                    Entrada                       Acción
    ------------------------------------------------------------------------------------------
    id                                      + ( id / id ) $               Desplazar
    Fact                                    + ( id / id ) $               Reducir: F → id
    Term                                    + ( id / id ) $               Reducir: T → F
    Expr                                    + ( id / id ) $               Reducir: E → T
    Expr +                                  ( id / id ) $                 Desplazar
    Expr + (                                id / id ) $                   Desplazar
    Expr + ( id                             / id ) $                      Desplazar
    Expr + ( Fact                           / id ) $                      Reducir: F → id
    Expr + ( Term                           / id ) $                      Reducir: T → F
    Expr + ( Term /                         id ) $                        Desplazar
    Expr + ( Term / id                      ) $                           Desplazar
    Expr + ( Term / Fact                    ) $                           Reducir: F → id
    Expr + ( Term                           ) $                           Reducir: T → T / F
    Expr + ( Expr                           ) $                           Reducir: E → T
    Expr + ( Expr )                         $                             Desplazar
    Expr + Fact                             $                             Reducir: F → ( E )
    Expr + Term                             $                             Reducir: T → F
    Expr                                    $                             Reducir: E → E + T
    Expr                                    $                             aceptado

    Analizando: id : id
    Pila                                    Entrada                       Acción
    ------------------------------------------------------------------------------------------
    id                                      : id $                        Desplazar
    Fact                                    : id $                        Reducir: F → id
    Term                                    : id $                        Reducir: T → F
    Expr                                    : id $                        Reducir: E → T
    Expr :                                  id $                          Desplazar
    Expr : id                               $                             Desplazar
    Expr : Fact                             $                             Reducir: F → id
    Expr : Term                             $                             Reducir: T → F
    Expr : Expr                             $                             Reducir: E → T
    Expr : Expr                                                           no aceptado


## Punto 4: Programa comparativo parser con algoritmo CYK y parser de tipo predictivo

Este programa en python permite comparar el rendimiento y funcionamiento de dos algoritmos de análisis sintáctico diferentes, uno CYK y un parser predictivo. El sistema mide el tiempo de ejecución de cada algoritmo al procesar una serie de cadenas con base en una gramática libre de contexto (GLC).

Explicacion:

El programa lee una gramática desde un archivo gramatica.txt y una lista de cadenas desde cadenas.txt, luego ejecuta ambos analizadores sintacticos sobre cada cadena para medir sus tiempos de ejecucion en milisegundos

Debe contener las reglas de producción en formato:

S -> A B

A -> a

B -> b


Si una producción es vacía, se escribe:

A -> vacio



Ejecución del Programa:


python comparador_parsers.py


ahi pedira ingresar el nombre del archivo con las cadenas,mostrando este resultado por ejemplo:

===Comparacion de parsers===

|cadena | tiempo CYK (ms)  |  tiempo predictivo (ms)|
|----|-----|-----|
| a b | 0.812 | 0.144 |
| a a b | 1.105 | 0.220 |
| b b a | 0.934 | 0.155 |
---------------------------------------------------------------------------


Explicación de los Parsers
*CYK

requiere que la gramatica este en Forma Normal de Chomsky (FNC). utiliza una tabla triangular para verificar si la cadena pertenece al lenguaje, además de tener una complejidad de O(n³).

*Predictivo

Utiliza una pila y un conjunto de reglas para expandir los no terminales y funcionando mejor con gramáticas LL(1).

Su complejidad es O(n) en el mejor caso.

--------------------------------------------------------------------------

Pruebas

para el desarrollo del programa se uso la siguiente gramatica que esta incluida en el ejercicio:

>S->A uno B C
>
>S->S dos
>
>A->B C D
>
>A->A tres
>
>A->vacio
>
>B->D cuatro C tres
>
>B->vacio
>
>C->cinco D B
>
>C->vacio
>
>D->seis
>
>D->vacio

y al ejecutar probando con el archivo de cadenas, estos son los resultados que muestran:

===Comparacion de parsers===
| cadena | tiempo CYK (ms) | tiempo predictivo (ms) |
|------|---------|----------|
| cuatro cinco seis | 0.075 | 0.025 |
| uno cuatro | 0.019 | 0.010 |
| uno | 0.007 | 0.007 |
| uno cuatro tres | 0.028 | 0.007 |
| cinco seis | 0.014 | 0.007 |
| seis | 0.005 | 0.009 |
| uno seis cuatro tres | 0.040 | 0.007 |
| cuatro dos | 0.011 | 0.006 |
| uno cuatro cinco seis tres | 0.064 | 0.006 |
| uno seis | 0.011 | 0.006 |
------------------------------------------------------------------------------------------
comparando entre los resultados se puede concluir que el algoritmo de CYK toma mas tiempo que un algoritmo predictivo cuando hay varios terminales o simbolos en una cadena, y que cuando solo hay un dato pueden llegar a tomar el mismo o menos tiempo .

## Punto 5: Parser Descendente Recursivo con Algoritmo de Emparejamiento

Implementación de un analizador descendente recursivo con algoritmo de emparejamiento (matching) para analizar expresiones aritméticas. El analizador procesa expresiones con operadores de suma (+) y multiplicación (*), respetando la precedencia de operadores y permitiendo el uso de paréntesis.

Características principales:

- Cálculo automático de conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN

- Validación basada en gramática LL(1)

- Algoritmo de emparejamiento centralizado

- Detección precisa de errores sintácticos

Objetivos

- Implementar un algoritmo de emparejamiento para análisis descendente recursivo

- Calcular conjuntos PRIMEROS, SIGUIENTES y PREDICCION

- Validar la sintaxis de expresiones aritméticas

- Generar un árbol de derivación paso a paso

- Detectar y reportar errores sintácticos con precisión

Gramática

- Gramática Original

        E → E + T | T
        T → T * F | F
        F → ( E ) | id

- Gramática Transformada (LL(1))

        E  → T E'
        E' → + T E' | ε
        T  → F T'
        T' → * F T' | ε
        F  → ( E ) | id

Se eliminó la recursión izquierda para hacer la gramática compatible con el análisis descendente recursivo.

Conjuntos Calculados:

- PRIMEROS

        PRIMERO(E)   = {(, id}
        PRIMERO(E')  = {+, ε}
        PRIMERO(F)   = {(, id}
        PRIMERO(T)   = {(, id}
        PRIMERO(T')  = {*, ε}

- SIGUIENTES

        SIGUIENTE(E)   = {$, )}
        SIGUIENTE(E')  = {$, )}
        SIGUIENTE(F)   = {$, ), *, +}
        SIGUIENTE(T)   = {$, ), +}
        SIGUIENTE(T')  = {$, ), +}

- PREDICCION

        E:
          E → T E'           | PRED = {(, id}
        
        E':
          E' → + T E'        | PRED = {+}
          E' → ε             | PRED = {$, )}
        
        T:
          T → F T'           | PRED = {(, id}
        
        T':
          T' → * F T'        | PRED = {*}
          T' → ε             | PRED = {$, ), +}
        
        F:
          F → ( E )          | PRED = {(}
          F → id             | PRED = {id}

Arquitectura:

- Componentes principales:

1. AnalizadorGramatica

- Calcula automáticamente los conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN

- Valida que la gramática sea LL(1)

- Imprime los conjuntos calculados de forma legible

Métodos principales:

- calcular_primero(simbolo): Calcula PRIMERO de un símbolo

- calcular_siguientes(): Calcula SIGUIENTES de todos los no-terminales

- calcular_prediccion(): Calcula PREDICCIÓN de cada producción

- imprimir_conjuntos(): Muestra todos los conjuntos

2. Lexer (Analizador Léxico)

- Convierte la cadena de entrada en tokens

- Tokens reconocidos: ID, PLUS (+), MULT (*), LPAREN ((), RPAREN ()), EOF

Métodos:

- tokenizar(): Procesa el texto de entrada y genera tokens

3. AnalizadorDescendenteRecursivo (Parser)

- Implementa el análisis descendente recursivo

- Una función por cada símbolo no-terminal de la gramática

- Usa conjuntos PREDICCIÓN para decidir qué producción aplicar

- Algoritmo de emparejamiento centralizado

Métodos principales:

- emparejar(tipo_esperado): 🔑 Algoritmo de emparejamiento

- analizar_E(): E → T E'

- analizar_E_prima(): E' → + T E' | ε

- analizar_T(): T → F T'

- analizar_T_prima(): T' → * F T' | ε

- analizar_F(): F → ( E ) | id

- analizar(): Función principal

- mostrar_resultados(): Muestra resultados y errores

4. Algoritmo de Emparejamiento

- Método emparejar(tipo_esperado): nucleo del algoritmo

- Valida tokens esperados vs tokens encontrados

- Consume tokens y avanza en la entrada

- Reporta errores de sintaxis

Requisitos

- Python 3.7 o superior

Uso:

- Ejecución Básica

        python descendente.py

Esto ejecutará automáticamente:

- Cálculo de conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN

- Casos de prueba predefinidos (11 expresiones)

- Resumen de resultados

Uso programación:

    from descendente import AnalizadorLexico, AnalizadorDescendenteRecursivo, AnalizadorGramatica

    # Calcular conjuntos
    analizador_gramatica = AnalizadorGramatica()
    analizador_gramatica.imprimir_conjuntos()
    
    # Crear el analizador léxico
    expresion = "a + b * c"
    lexico = AnalizadorLexico(expresion)
    
    # Crear el analizador sintáctico
    analizador = AnalizadorDescendenteRecursivo(lexico.tokens, analizador_gramatica)
    
    # Realizar el análisis
    exito = analizador.analizar()
    
    # Mostrar resultados
    analizador.mostrar_resultados()


- Estructura del Código

         descendente.py
        ├── Token                              # Clase para representar tokens
        ├── AnalizadorGramatica                # Calcula PRIMEROS, SIGUIENTES y PREDICCIÓN
        │   ├── calcular_primero()
        │   ├── calcular_primero_cadena()
        │   ├── calcular_siguientes()
        │   ├── calcular_prediccion()
        │   ├── calcular_todos()
        │   └── imprimir_conjuntos()
        ├── AnalizadorLexico                   # Analizador léxico
        │   └── tokenizar()
        ├── AnalizadorDescendenteRecursivo     # Analizador sintáctico
        │   ├── emparejar()                    # Algoritmo de emparejamiento
        │   ├── verificar_prediccion()         # Verifica conjuntos PREDICT
        │   ├── analizar_E()                   # E → T E'
        │   ├── analizar_E_prima()             # E' → + T E' | ε
        │   ├── analizar_T()                   # T → F T'
        │   ├── analizar_T_prima()             # T' → * F T' | ε
        │   ├── analizar_F()                   # F → ( E ) | id
        │   ├── analizar()                     # Función principal
        │   └── mostrar_resultados()           # Mostrar resultados
        └── probar_analizador()                # Función de prueba

Conceptos Implementados

- Análisis descendente recursivo

- Algoritmo de emparejamiento (matching)

- Eliminación de recursión izquierda

- Gramática LL(1)

- Cálculo de conjuntos PRIMEROS (FIRST)

- Cálculo de conjuntos SIGUIENTES (FOLLOW)

- Cálculo de conjuntos PREDICCIÓN (PREDICT)

- Manejo de producciones ε (épsilon)

- Precedencia de operadores

- Detección de errores sintácticos

- Generación de árbol de derivación


Juan Esteban Martinez Cantero y Juan Camilo Camacho Mejía 
