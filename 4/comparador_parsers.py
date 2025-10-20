import time
import re

def leer_gramatica(nombre_archivo):
    gramatica={}
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            linea=linea.strip()
            if not linea or '->' not in linea:
                continue
            izquierda, derecha=linea.split('->')
            izquierda=izquierda.strip()
            derecha=derecha.strip()

            if izquierda not in gramatica:
                gramatica[izquierda]=[]
            if derecha.lower()=='vacio':
                gramatica[izquierda].append(['ε'])
            else:
                gramatica[izquierda].append(derecha.split())
    return gramatica

def cyk_parse(palabras, reglas):
    n=len(palabras)
    if n==0:
        return False

    T=[[set() for _ in range(n)] for _ in range(n)]
    for j in range(n):
        for lhs, rhs_list in reglas.items():
            for rhs in rhs_list:
                if len(rhs)==1 and rhs[0]==palabras[j]:
                    T[j][j].add(lhs)

        for i in range(j, -1, -1):
            for k in range(i, j):
                for lhs, rhs_list in reglas.items():
                    for rhs in rhs_list:
                        if len(rhs)==2:
                            B, C=rhs
                            if B in T[i][k] and C in T[k+1][j]:
                                T[i][j].add(lhs)
    return "S" in T[0][n-1]

def predictivo_parse(palabras, reglas):
    pila=["$", "S"]
    entrada=palabras+["$"]
    i=0

    while pila:
        tope=pila.pop()
        actual=entrada[i]

        if tope==actual:
            i+=1
        elif tope in reglas:
            encontrado=False
            for rhs in reglas[tope]:
                if len(rhs)==1 and rhs[0]==actual:
                    pila.extend(reversed(rhs))
                    encontrado=True
                    break
                elif len(rhs)>1 and rhs[0]==actual or rhs[0].isupper():
                    pila.extend(reversed(rhs))
                    encontrado=True
                    break
            if not encontrado:
                return False
        elif tope=="$":
            return actual=="$"
        else:
            return False

    return True

if __name__=="__main__":
    gramatica=leer_gramatica("gramatica.txt")

    cadenas=input("ingrese las cadenas a comparar: ")
    with open("cadenas.txt", "r") as f:
        cadenas=[re.sub(r"\s+", " ", linea.strip()) for linea in f if linea.strip()]

    print("\n===Comparacion de parsers===\n")
    print(f"{'cadena':<25}{'tiempo CYK (ms)':<18}{'tiempo predictivo (ms)':<22}")
    print("-" * 90)

    for cadena in cadenas:
        tokens=re.findall(r"\w+", cadena)

        t1=time.perf_counter()
        resultado_cyk=cyk_parse(tokens, gramatica)
        t2=time.perf_counter()
        tiempo_cyk=(t2-t1)*1000

        t3=time.perf_counter()
        resultado_pred=predictivo_parse(tokens, gramatica)
        t4=time.perf_counter()
        tiempo_pred=(t4-t3)*1000

        print(f"{cadena:<25}"
              f"{tiempo_cyk:<18.3f}"
              f"{tiempo_pred:<.3f}")

    print("-"*90)

