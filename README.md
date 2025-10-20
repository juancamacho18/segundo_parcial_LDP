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
        │   ├── emparejar()                    # ⭐ Algoritmo de emparejamiento
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
