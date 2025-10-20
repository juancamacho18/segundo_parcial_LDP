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
