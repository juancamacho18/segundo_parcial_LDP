grammar CRUD;

programa
    : sentencia+ EOF
    ;

sentencia
    : createStmt
    | readStmt
    | updateStmt
    | deleteStmt
    ;

createStmt
    : CREATE TABLE ID '(' campos ')'
    ;

campos
    : campo (',' campo)*
    ;

campo
    : ID tipo
    ;

tipo
    : INT
    | STRING
    | FLOAT
    ;

readStmt
    : SELECT columnas FROM ID condicionWhere
    ;

columnas
    : STAR
    | ID (',' ID)*
    ;

condicionWhere
    : WHERE condicion
    | /* vacío */
    ;

condicion
    : ID oper valor
    ;

oper
    : EQ
    | LT
    | GT
    | LE
    | GE
    | NEQ
    ;

valor
    : NUMERO
    | CADENA
    ;

updateStmt
    : UPDATE ID SET asignaciones condicionWhere
    ;

asignaciones
    : asignacion (',' asignacion)*
    ;

asignacion
    : ID EQ valor
    ;

deleteStmt
    : DELETE FROM ID condicionWhere
    ;

CREATE  : 'create';
TABLE   : 'table';
SELECT  : 'select';
FROM    : 'from';
WHERE   : 'where';
UPDATE  : 'update';
SET     : 'set';
DELETE  : 'delete';

INT     : 'int';
STRING  : 'string';
FLOAT   : 'float';

STAR    : '*';
EQ      : '=';
LT      : '<';
GT      : '>';
LE      : '<=';
GE      : '>=';
NEQ     : '!=';

ID      : [a-zA-Z_][a-zA-Z0-9_]*;
NUMERO  : [0-9]+;
CADENA  : '"' (~["\r\n])* '"';

WS      : [ \t\r\n]+ -> skip;