import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

class AnalizadorGramatica:
    #Calcula conjuntos PRIMEROS, SIGUIENTES y PREDICCION
    
    def __init__(self):
        # Definicion de la gramatica
        self.gramatica = {
            'E': [['T', "E'"]],
            "E'": [['+', 'T', "E'"], ['ε']],
            'T': [['F', "T'"]],
            "T'": [['*', 'F', "T'"], ['ε']],
            'F': [['(', 'E', ')'], ['id']]
        }
        
        self.terminales = {'+', '*', '(', ')', 'id', 'ε', '$'}
        self.no_terminales = {'E', "E'", 'T', "T'", 'F'}
        
        self.conjuntos_primeros = {}
        self.conjuntos_siguientes = {}
        self.conjuntos_prediccion = {}
        
        self.calcular_todos()
    
    def calcular_primero(self, simbolo):
        #Calcula el conjunto PRIMERO de un simbolo
        if simbolo in self.conjuntos_primeros:
            return self.conjuntos_primeros[simbolo]
        
        primero = set()
        
        # Si es terminal, PRIMERO(terminal) = {terminal}
        if simbolo in self.terminales or simbolo == 'ε':
            primero.add(simbolo)
            return primero
        
        # Si es no-terminal
        if simbolo in self.no_terminales:
            for produccion in self.gramatica[simbolo]:
                # Para cada produccion X -> Y1 Y2 ... Yn
                todos_tienen_epsilon = True
                for elemento in produccion:
                    primero_elemento = self.calcular_primero(elemento)
                    primero.update(primero_elemento - {'ε'})
                    
                    if 'ε' not in primero_elemento:
                        todos_tienen_epsilon = False
                        break
                
                # Si todos tienen ε, agregar ε a PRIMERO(X)
                if todos_tienen_epsilon:
                    primero.add('ε')
        
        self.conjuntos_primeros[simbolo] = primero
        return primero
    
    def calcular_primero_cadena(self, simbolos):
        #Calcula PRIMERO de una cadena de símbolos
        primero = set()
        todos_tienen_epsilon = True
        
        for simbolo in simbolos:
            primero_simbolo = self.calcular_primero(simbolo)
            primero.update(primero_simbolo - {'ε'})
            
            if 'ε' not in primero_simbolo:
                todos_tienen_epsilon = False
                break
        
        if todos_tienen_epsilon:
            primero.add('ε')
        
        return primero
    
    def calcular_siguientes(self):
        #Calcula el conjunto SIGUIENTE para todos los no-terminales
        # Inicializar conjuntos vacios
        for nt in self.no_terminales:
            self.conjuntos_siguientes[nt] = set()
        
        # SIGUIENTE(E) contiene $
        self.conjuntos_siguientes['E'].add('$')
        
        # Iterar hasta que no haya cambios
        cambio = True
        iteraciones = 0
        while cambio and iteraciones < 10:
            cambio = False
            iteraciones += 1
            
            for nt in self.no_terminales:
                for produccion in self.gramatica[nt]:
                    for i, simbolo in enumerate(produccion):
                        if simbolo in self.no_terminales:
                            # Caso 1: A -> αBβ, agregar PRIMERO(β) - {ε} a SIGUIENTE(B)
                            beta = produccion[i+1:]
                            if beta:
                                primero_beta = self.calcular_primero_cadena(beta)
                                tamano_anterior = len(self.conjuntos_siguientes[simbolo])
                                self.conjuntos_siguientes[simbolo].update(primero_beta - {'ε'})
                                if len(self.conjuntos_siguientes[simbolo]) > tamano_anterior:
                                    cambio = True
                                
                                # Caso 2: Si ε ∈ PRIMERO(β), agregar SIGUIENTE(A) a SIGUIENTE(B)
                                if 'ε' in primero_beta:
                                    tamano_anterior = len(self.conjuntos_siguientes[simbolo])
                                    self.conjuntos_siguientes[simbolo].update(self.conjuntos_siguientes[nt])
                                    if len(self.conjuntos_siguientes[simbolo]) > tamano_anterior:
                                        cambio = True
                            else:
                                # Caso 3: A -> αB, agregar SIGUIENTE(A) a SIGUIENTE(B)
                                tamano_anterior = len(self.conjuntos_siguientes[simbolo])
                                self.conjuntos_siguientes[simbolo].update(self.conjuntos_siguientes[nt])
                                if len(self.conjuntos_siguientes[simbolo]) > tamano_anterior:
                                    cambio = True
    
    def calcular_prediccion(self):
        #Calcula el conjunto PREDICCION para cada produccion
        for nt in self.no_terminales:
            self.conjuntos_prediccion[nt] = {}
            
            for idx, produccion in enumerate(self.gramatica[nt]):
                pred = set()
                primero_produccion = self.calcular_primero_cadena(produccion)
                
                # PRED(A -> α) = (PRIMERO(α) - {ε}) ∪ (SIGUIENTE(A) si ε ∈ PRIMERO(α))
                pred.update(primero_produccion - {'ε'})
                
                if 'ε' in primero_produccion:
                    pred.update(self.conjuntos_siguientes[nt])
                
                cadena_produccion = ' '.join(produccion)
                self.conjuntos_prediccion[nt][cadena_produccion] = pred
    
    def calcular_todos(self):
        #Calcula todos los conjuntos
        # Calcular PRIMEROS
        for simbolo in self.no_terminales | self.terminales:
            self.calcular_primero(simbolo)
        
        # Calcular SIGUIENTES
        self.calcular_siguientes()
        
        # Calcular PREDICCIÓN
        self.calcular_prediccion()
    
    def imprimir_conjuntos(self):
        #Imprime todos los conjuntos calculados
        print("\n" + "="*70)
        print("CONJUNTOS PRIMEROS")
        print("="*70)
        for simbolo in sorted(self.no_terminales):
            primero = sorted(self.conjuntos_primeros.get(simbolo, set()))
            print(f"PRIMERO({simbolo:3}) = {{{', '.join(primero)}}}")
        
        print("\n" + "="*70)
        print("CONJUNTOS SIGUIENTES")
        print("="*70)
        for simbolo in sorted(self.no_terminales):
            siguiente = sorted(self.conjuntos_siguientes.get(simbolo, set()))
            print(f"SIGUIENTE({simbolo:3}) = {{{', '.join(siguiente)}}}")
        
        print("\n" + "="*70)
        print("CONJUNTOS PREDICCION")
        print("="*70)
        for nt in sorted(self.no_terminales):
            print(f"\n{nt}:")
            for produccion, pred in self.conjuntos_prediccion[nt].items():
                pred_str = ', '.join(sorted(pred))
                print(f"  {nt} → {produccion:15} | PRED = {{{pred_str}}}")

class AnalizadorLexico:
    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0
        self.tokens = []
        self.tokenizar()
    
    def tokenizar(self):
        patrones_tokens = [
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('MAS', r'\+'),
            ('POR', r'\*'),
            ('PAREN_IZQ', r'\('),
            ('PAREN_DER', r'\)'),
            ('ESPACIO', r'\s+'),
        ]
        
        texto = self.texto
        while texto:
            emparejado = False
            for tipo_token, patron in patrones_tokens:
                regex = re.match(patron, texto)
                if regex:
                    valor = regex.group(0)
                    if tipo_token != 'ESPACIO':
                        self.tokens.append(Token(tipo_token, valor))
                    texto = texto[len(valor):]
                    emparejado = True
                    break
            
            if not emparejado:
                raise Exception(f"Carácter inválido: {texto[0]}")
        
        self.tokens.append(Token('EOF', ''))

class AnalizadorDescendenteRecursivo:
    # con emparejamiento
    
    def __init__(self, tokens, analizador_gramatica):
        self.tokens = tokens
        self.posicion = 0
        self.token_actual = self.tokens[0] if tokens else Token('EOF', '')
        self.errores = []
        self.arbol_derivacion = []
        self.gramatica = analizador_gramatica
        
        # Mapeo de tokens a simbolos de la gramatica
        self.token_a_gramatica = {
            'MAS': '+',
            'POR': '*',
            'PAREN_IZQ': '(',
            'PAREN_DER': ')',
            'ID': 'id',
            'EOF': '$'
        }
    
    def avanzar(self):
        if self.posicion < len(self.tokens) - 1:
            self.posicion += 1
            self.token_actual = self.tokens[self.posicion]
    
    def emparejar(self, tipo_esperado):
        # Verifica si el token actual coincide con el tipo esperado.
        # Si coincide, consume el token y avanza.
        # Si no coincide, reporta un error.
        
        if self.token_actual.tipo == tipo_esperado:
            token_emparejado = self.token_actual
            self.registrar_emparejamiento(tipo_esperado, token_emparejado.valor)
            self.avanzar()
            return token_emparejado
        else:
            self.error(f"Error de sintaxis: se esperaba '{tipo_esperado}', "
                      f"pero se encontro '{self.token_actual.tipo}' "
                      f"(valor: '{self.token_actual.valor}')")
            return None
    
    def registrar_emparejamiento(self, esperado, valor):
        self.arbol_derivacion.append(f" Emparejamiento: {esperado} = '{valor}'")
    
    def error(self, mensaje):
        self.errores.append(f"[Posicion {self.posicion}] {mensaje}")
    
    def obtener_simbolo_gramatica_actual(self):
        return self.token_a_gramatica.get(self.token_actual.tipo, self.token_actual.tipo)
    
    def verificar_prediccion(self, no_terminal, produccion):
        simbolo_actual = self.obtener_simbolo_gramatica_actual()
        cadena_produccion = ' '.join(produccion)
        conjunto_pred = self.gramatica.conjuntos_prediccion[no_terminal].get(cadena_produccion, set())
        return simbolo_actual in conjunto_pred
    
    # Funciones para cada produccion de la gramatica
    
    def analizar_E(self):
        # E -> T E'
        print(f"Entrando a E (token actual: {self.token_actual})")
        self.arbol_derivacion.append("E → T E'")
        self.analizar_T()
        self.analizar_E_prima()
        print("Saliendo de E")
    
    def analizar_E_prima(self):
        # E' → + T E' | ε
        print(f"Entrando a E' (token actual: {self.token_actual})")
        simbolo_actual = self.obtener_simbolo_gramatica_actual()
        
        # Usar conjunto PREDICCION para decidir que produccion aplicar
        if self.verificar_prediccion("E'", ['+', 'T', "E'"]):
            self.arbol_derivacion.append("E' → + T E' (por PRED)")
            self.emparejar('MAS')
            self.analizar_T()
            self.analizar_E_prima()
        elif self.verificar_prediccion("E'", ['ε']):
            self.arbol_derivacion.append("E' → ε (por PRED)")
        else:
            self.error(f"Token inesperado en E': {simbolo_actual}")
        print("Saliendo de E'")
    
    def analizar_T(self):
        # T → F T'
        print(f"Entrando a T (token actual: {self.token_actual})")
        self.arbol_derivacion.append("T → F T'")
        self.analizar_F()
        self.analizar_T_prima()
        print("Saliendo de T")
    
    def analizar_T_prima(self):
        # T' -> * F T' | ε
        print(f"Entrando a T' (token actual: {self.token_actual})")
        simbolo_actual = self.obtener_simbolo_gramatica_actual()
        
        # Usar conjunto PREDICCIoN para decidir que produccion aplicar
        if self.verificar_prediccion("T'", ['*', 'F', "T'"]):
            self.arbol_derivacion.append("T' → * F T' (por PRED)")
            self.emparejar('POR')
            self.analizar_F()
            self.analizar_T_prima()
        elif self.verificar_prediccion("T'", ['ε']):
            self.arbol_derivacion.append("T' → ε (por PRED)")
        else:
            self.error(f"Token inesperado en T': {simbolo_actual}")
        print("Saliendo de T'")
    
    def analizar_F(self):
        """F → ( E ) | id"""
        print(f"Entrando a F (token actual: {self.token_actual})")
        
        if self.verificar_prediccion('F', ['(', 'E', ')']):
            self.arbol_derivacion.append("F → ( E ) (por PRED)")
            self.emparejar('PAREN_IZQ')
            self.analizar_E()
            self.emparejar('PAREN_DER')
        elif self.verificar_prediccion('F', ['id']):
            self.arbol_derivacion.append("F → id (por PRED)")
            self.emparejar('ID')
        else:
            self.error(f"Error: se esperaba '(' o 'id', pero se encontro '{self.token_actual.tipo}'")
        print("Saliendo de F")
    
    def analizar(self):
        print("\n" + "="*60)
        print("INICIANDO ANALISIS DESCENDENTE RECURSIVO")
        print("="*60 + "\n")
        
        self.analizar_E()
        
        if self.token_actual.tipo != 'EOF':
            self.error(f"Entrada no completamente consumida. Token restante: {self.token_actual}")
        
        print("\n" + "="*60)
        print("ANALISIS COMPLETADO")
        print("="*60)
        
        return len(self.errores) == 0
    
    def mostrar_resultados(self):
        """Muestra los resultados del analisis"""
        print("\n" + "="*60)
        print("ARBOL DE DERIVACION:")
        print("="*60)
        for paso in self.arbol_derivacion:
            print(paso)
        
        if self.errores:
            print("\n" + "="*60)
            print("ERRORES ENCONTRADOS:")
            print("="*60)
            for error in self.errores:
                print(error)
            print(f"\n Analisis FALLIDO - {len(self.errores)} error(es)")
        else:
            print("\n✅ Analisis EXITOSO - Entrada valida")

def probar_analizador(expresion, analizador_gramatica):
    print("\n" + "="*60)
    print(f"PROBANDO EXPRESION: {expresion}")
    print("="*60)
    
    try:
        lexico = AnalizadorLexico(expresion)
        print("\nTokens generados:")
        for token in lexico.tokens:
            print(f"  {token}")
        
        analizador = AnalizadorDescendenteRecursivo(lexico.tokens, analizador_gramatica)
        exito = analizador.analizar()
        analizador.mostrar_resultados()
        
        return exito
    except Exception as e:
        print(f"\n Error: {e}")
        return False

if __name__ == "__main__":
    print("="*70)
    print("ANALIZADOR DESCENDENTE RECURSIVO LL(1) CON EMPAREJAMIENTO")
    print("="*70)
    
    # Calcular conjuntos PRIMEROS, SIGUIENTES y PREDICCION
    analizador_gramatica = AnalizadorGramatica()
    analizador_gramatica.imprimir_conjuntos()
    
    print("\n" + "="*70)
    print("PRUEBAS DEL ANALIZADOR")
    print("="*70)
    
    # Casos de prueba
    casos_prueba = [
        ("a", True),
        ("a + b", True),
        ("a * b", True),
        ("a + b * c", True),
        ("(a + b) * c", True),
        ("a * (b + c)", True),
        ("((a))", True),
        ("a + b + c * d", True),
        ("a + ", False),
        ("+ a", False),
        ("(a + b", False),
    ]
    
    resultados = []
    for expr, esperado in casos_prueba:
        exito = probar_analizador(expr, analizador_gramatica)
        resultados.append({
            'expresion': expr,
            'esperado': 'Valida' if esperado else 'Invalida',
            'resultado': 'PASS' if exito == esperado else 'FAIL'
        })
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS")
    print("="*70)
    for r in resultados:
        estado = "Bien" if r['resultado'] == 'PASS' else "Mal"
        print(f"{estado} {r['expresion']:20} | Esperado: {r['esperado']:10} | {r['resultado']}")
