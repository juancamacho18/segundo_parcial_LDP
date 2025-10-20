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

