import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []
        self.tokenize()
    
    def tokenize(self):
        token_patterns = [
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('PLUS', r'\+'),
            ('MULT', r'\*'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('WHITESPACE', r'\s+'),
        ]
        
        text = self.text
        while text:
            matched = False
            for token_type, pattern in token_patterns:
                regex = re.match(pattern, text)
                if regex:
                    value = regex.group(0)
                    if token_type != 'WHITESPACE':
                        self.tokens.append(Token(token_type, value))
                    text = text[len(value):]
                    matched = True
                    break
            
            if not matched:
                raise Exception(f"Carácter inválido: {text[0]}")
        
        # Añadir token de fin de entrada
        self.tokens.append(Token('EOF', ''))

class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else Token('EOF', '')
        self.errors = []
        self.parse_tree = []
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
    
    def match(self, expected_type):
        #Verifica si el token actual coincide con el tipo esperado.
        #Si coincide, consume el token y avanza.
        #Si no coincide, reporta un error.
        if self.current_token.type == expected_type:
            matched_token = self.current_token
            self.log_match(expected_type, matched_token.value)
            self.advance()
            return matched_token
        else:
            self.error(f"Error de sintaxis: se esperaba '{expected_type}', "
                      f"pero se encontró '{self.current_token.type}' "
                      f"(valor: '{self.current_token.value}')")
            return None
    
    def log_match(self, expected, value):
        """Registra los emparejamientos exitosos"""
        self.parse_tree.append(f"✓ Match: {expected} = '{value}'")
    
    def error(self, message):
        """Registra errores de parsing"""
        self.errors.append(f"[Posición {self.pos}] {message}")
    
    # Funciones para cada producción de la gramática
    
    def parse_E(self):
        # E → T E'
        print("Entrando a E")
        self.parse_tree.append("E → T E'")
        self.parse_T()
        self.parse_E_prime()
        print("Saliendo de E")
    
    def parse_E_prime(self):
        # E' → + T E' | ε
        print("Entrando a E'")
        if self.current_token.type == 'PLUS':
            self.parse_tree.append("E' → + T E'")
            self.match('PLUS')
            self.parse_T()
            self.parse_E_prime()
        else:
            self.parse_tree.append("E' → ε")
        print("Saliendo de E'")
    
    def parse_T(self):
        # T → F T'
        print("Entrando a T")
        self.parse_tree.append("T → F T'")
        self.parse_F()
        self.parse_T_prime()
        print("Saliendo de T")
    
    def parse_T_prime(self):
        # T' → * F T' | ε
        print("Entrando a T'")
        if self.current_token.type == 'MULT':
            self.parse_tree.append("T' → * F T'")
            self.match('MULT')
            self.parse_F()
            self.parse_T_prime()
        else:
            self.parse_tree.append("T' → ε")
        print("Saliendo de T'")
    
    def parse_F(self):
        # F → ( E ) | id
        print("Entrando a F")
        if self.current_token.type == 'LPAREN':
            self.parse_tree.append("F → ( E )")
            self.match('LPAREN')
            self.parse_E()
            self.match('RPAREN')
        elif self.current_token.type == 'ID':
            self.parse_tree.append("F → id")
            self.match('ID')
        else:
            self.error(f"Error: se esperaba '(' o 'id', pero se encontró '{self.current_token.type}'")
        print("Saliendo de F")
    
    def parse(self):
        """Inicia el análisis sintáctico"""
        print("\n" + "="*60)
        print("INICIANDO ANÁLISIS DESCENDENTE RECURSIVO")
        print("="*60 + "\n")
        
        self.parse_E()
        
        # Verificar que se consumió toda la entrada
        if self.current_token.type != 'EOF':
            self.error(f"Entrada no completamente consumida. Token restante: {self.current_token}")
        
        print("\n" + "="*60)
        print("ANÁLISIS COMPLETADO")
        print("="*60)
        
        return len(self.errors) == 0
    
    def show_results(self):
        """Muestra los resultados del análisis"""
        print("\n" + "="*60)
        print("ÁRBOL DE DERIVACIÓN:")
        print("="*60)
        for step in self.parse_tree:
            print(step)
        
        if self.errors:
            print("\n" + "="*60)
            print("ERRORES ENCONTRADOS:")
            print("="*60)
            for error in self.errors:
                print(error)
            print(f"\n Análisis FALLIDO - {len(self.errors)} error(es)")
        else:
            print("\n Análisis EXITOSO - Entrada válida")

def test_parser(expression):
    """Función para probar el parser"""
    print("\n" + "="*60)
    print(f"PROBANDO EXPRESIÓN: {expression}")
    print("="*60)
    
    try:
        # Análisis léxico
        lexer = Lexer(expression)
        print("\nTokens generados:")
        for token in lexer.tokens:
            print(f"  {token}")
        
        # Análisis sintáctico
        parser = RecursiveDescentParser(lexer.tokens)
        success = parser.parse()
        parser.show_results()
        
        return success
    except Exception as e:
        print(f"\n Error: {e}")
        return False

if __name__ == "__main__":
    print("PARSER DESCENDENTE RECURSIVO CON EMPAREJAMIENTO")
    print("Gramática: E → T E', E' → + T E' | ε, T → F T', T' → * F T' | ε, F → ( E ) | id")
    
    # Casos de prueba
    test_cases = [
        ("a", True),
        ("a + b", True),
        ("a * b", True),
        ("a + b * c", True),
        ("(a + b) * c", True),
        ("a * (b + c)", True),
        ("((a))", True),
        ("a + b + c * d", True),
        ("a + ", False),  # Error: expresión incompleta
        ("+ a", False),   # Error: inicia con operador
        ("(a + b", False), # Error: paréntesis sin cerrar
    ]
    
    results = []
    for expr, expected in test_cases:
        success = test_parser(expr)
        results.append({
            'expresion': expr,
            'esperado': 'Válida' if expected else 'Inválida',
            'resultado': 'PASS' if success == expected else 'FAIL'
        })
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    for r in results:
        status = "PASA" if r['resultado'] == 'PASS' else "No PASA"
        print(f"{status} {r['expresion']:20} | Esperado: {r['esperado']:10} | {r['resultado']}")