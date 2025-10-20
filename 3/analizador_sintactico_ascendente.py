import re

gramatica = {
    'Expr': [['Term', "Expr'"]],
    "Expr'": [['+', 'Term', "Expr'"], ['-', 'Term', "Expr'"], ['ε']],
    'Term': [['Fact', "Term'"]],
    "Term'": [['*', 'Fact', "Term'"], ['/', 'Fact', "Term'"], ['ε']],
    'Fact': [['(', 'Expr', ')'], ['id']]
}

simbolo_inicial=list(gramatica.keys())[0]
no_terminales=set(gramatica.keys())
terminales=set()
for producciones in gramatica.values():
    for prod in producciones:
        for simbolo in prod:
            if simbolo not in gramatica and simbolo!='ε':
                terminales.add(simbolo)

def Primeros(gramatica, terminales):
    primero={}
    todos_los_simbolos=set()
    for producciones in gramatica.values():
        for produccion in producciones:
            todos_los_simbolos.update(produccion)
    todos_los_simbolos.update(gramatica.keys())  

    def obtener_primero(simbolo):
        if simbolo in primero:
            return primero[simbolo]
        primero[simbolo]=set()
        if simbolo in terminales or simbolo=='ε':
            primero[simbolo].add(simbolo)
            return primero[simbolo]

        for produccion in gramatica.get(simbolo, []):
            for s in produccion:
                primeros_s=obtener_primero(s)
                primero[simbolo].update(primeros_s-{'ε'})
                if 'ε' not in primeros_s:
                    break
            else:
                primero[simbolo].add('ε')
        return primero[simbolo]
    
    for simbolo in todos_los_simbolos:
        obtener_primero(simbolo)
    return primero

def Siguientes(gramatica, primero, simbolo_inicial):
    siguiente={}
    for nt in gramatica:
        siguiente[nt]=set()
    siguiente[simbolo_inicial].add('$')

    cambiado=True
    while cambiado:
        cambiado=False
        for nt in gramatica:
            for produccion in gramatica[nt]:
                for i, simbolo in enumerate(produccion):
                    if simbolo in gramatica:  
                        rest=produccion[i+1:]
                        antes=len(siguiente[simbolo])

                        if rest:
                            primero_rest=set()
                            for s in rest:
                                primeros_s=primero[s]
                                primero_rest.update(primeros_s-{'ε'})
                                if 'ε' not in primeros_s:
                                    break
                            else:
                                primero_rest.add('ε')
                            siguiente[simbolo].update(primero_rest-{'ε'})
                            if 'ε' in primero_rest:
                                siguiente[simbolo].update(siguiente[nt])
                        else:
                            siguiente[simbolo].update(siguiente[nt])

                        if len(siguiente[simbolo])>antes:
                            cambiado=True
    return siguiente


def Predicciones(gramatica, primero, siguiente):
    conjunto_prediccion={}

    for nt in gramatica:
        for prod in gramatica[nt]:
            regla=f"{nt} -> {' '.join(prod)}"
            pred=set()

            for s in prod:
                primeros_s=primero[s]
                pred.update(primeros_s-{'ε'})
                if 'ε' not in primeros_s:
                    break
            else:
                pred.add('ε')

            conjunto_prediccion[regla]=pred-{'ε'}
            if 'ε' in pred:
                conjunto_prediccion[regla].update(siguiente[nt])

    return conjunto_prediccion

primero=Primeros(gramatica, terminales)
siguiente=Siguientes(gramatica, primero, simbolo_inicial)
prediccion=Predicciones(gramatica, primero, siguiente)

reglas = [
    (('T', '*', 'F'), 'T'),
    (('T', '/', 'F'), 'T'),
    (('E', '+', 'T'), 'E'),
    (('F',), 'T'),
    (('id',), 'F'),
    (('(', 'E', ')'), 'F'),
    (('T',), 'E'),
]

terminales={'id', '+', '-', '*', '/', '(', ')'}
simbolo_inicial='E'  
nombre_mostrar = {'E':'Expr', 'T':'Term', 'F':'Fact'}

def algoritmo_ascendente(cadena):
    tokens=[tok for tok in cadena.split() if tok]
    entrada=tokens + ['$']
    pila=[]
    i=0

    print(f"\nAnalizando: {cadena}")
    print(f"{'Pila':<40}{'Entrada':<30}{'Acción'}")
    print("-" * 90)

    while True:
        cadena_entrada=' '.join(entrada[i:])
        reduccion=True
        hecho_una_reduccion=False
        while reduccion:
            reduccion=False
            for derecha, izquierda in reglas:
                n=len(derecha)
                if n==0:
                    continue
                if len(pila)<n:
                    continue
                if tuple(pila[-n:])==derecha:
                    siguiente_token=entrada[i]
                    if derecha==('T',) and siguiente_token in ('*', '/'):
                        continue

                    pila=pila[:-n] + [izquierda]
                    accion=f"Reducir: {izquierda} → {' '.join(derecha)}"
  
                    pila_print=' '.join(nombre_mostrar.get(x, x) for x in pila)
                    print(f"{pila_print:<40}{cadena_entrada:<30}{accion}")
                    reduccion=True
                    hecho_una_reduccion=True
                    break  

        if pila==['E'] and entrada[i]=='$':
            print(f"{'Expr':<40}{cadena_entrada:<30}aceptado")
            return True
        
        if entrada[i]!='$':
            pila.append(entrada[i])
            i += 1
            accion="Desplazar"
            pila_print =' '.join(nombre_mostrar.get(x, x) for x in pila)
            print(f"{pila_print:<40}{' '.join(entrada[i:]):<30}{accion}")
            continue
        else:
            break

    for derecha, izquierda in reglas:
        n=len(derecha)
        if n==0:
            continue
        if len(pila)>=n and tuple(pila[-n:])==derecha:
            pila=pila[:-n]+[izquierda]

    pila_print=' '.join(nombre_mostrar.get(x, x) for x in pila)
    if pila==['E']:
        print(f"{pila_print:<40}{'':<30}aceptado")
        return True
    else:
        print(f"{pila_print:<40}{'':<30}no aceptado")
        return False

archivo=input("ingrese el nombre del archivo a analizar: ")

try:
    with open(archivo, "r", encoding="utf-8") as f:
        lineas=[linea.strip() for linea in f if linea.strip()]
except FileNotFoundError:
    print(f"No se encontro el archivo '{archivo}'.")
    lineas=[]

for linea in lineas:
    algoritmo_ascendente(linea)