from modelos.conjunto import Conjunto
from interprete.parser import Parser
from interprete.evaluador import Evaluador
from interprete.lexer import Lexer
from modelos.gestor_conjuntos import GestorConjuntos
from utils.entrada import crear_conjunto_desde_entrada
from app.sesion import SesionCalculadora
from operaciones.operaciones import (
    union,
    interseccion,
    diferencia,
    diferencia_simetrica,
    complemento
)


A = Conjunto("A", [1, 2, 3, 4])
B = Conjunto("B", [3, 4, 5, 6])
U = Conjunto("U", [1, 2, 3, 4, 5, 6, 7, 8])

print("CONJUNTOS")
print(A)
print(B)
print(U)

print("\nOPERACIONES")

print("Unión:")
print(union(A, B))

print("\nIntersección:")
print(interseccion(A, B))

print("\nDiferencia A - B:")
print(diferencia(A, B))

print("\nDiferencia simétrica:")
print(diferencia_simetrica(A, B))

print("\nComplemento de A:")
print(complemento(A, U))

print("\nPRUEBA DEL LEXER")

expresion = "(A ∪ B) ∩ (C - A)"

lexer = Lexer(expresion)
tokens = lexer.tokenizar()

print("Expresión:")
print(expresion)

print("\nTokens:")
print(tokens)

print("\nPRUEBA DEL PARSER")

expresion = "(A ∪ B) ∩ (C - A)"

lexer = Lexer(expresion)
tokens = lexer.tokenizar()

parser = Parser(tokens)
arbol = parser.analizar()

print("Expresión:")
print(expresion)

print("\nÁrbol:")
print(arbol)

print("\nPRUEBA DEL EVALUADOR")

conjuntos = {
    "A": A,
    "B": B,
}

expresion = "(A ∪ B) ∩ A"

lexer = Lexer(expresion)
tokens = lexer.tokenizar()

parser = Parser(tokens)
arbol = parser.analizar()

evaluador = Evaluador(conjuntos)

resultado = evaluador.evaluar(arbol)

print("Expresión:")
print(expresion)

print("\nPasos:")

for numero, paso in enumerate(evaluador.pasos, start=1):
    print(f"{numero}. {paso}")

print("\nResultado:")
print(resultado)


print("\nPRUEBA DE ELEMENTOS MIXTOS")

X = Conjunto(
    "X",
    [
        1,
        2,
        2,
        "a",
        "b",
        "rojo",
        "azul",
        "α",
        "β",
        "+"
    ]
)

print(X)

print("Cantidad:", X.cantidad())


from utils.elementos import convertir_elemento


print("\nPRUEBA DEL CONVERSOR")

elementos = [
    "10",
    "3.14",
    "rojo",
    "x",
    "α",
    "+"
]

for texto in elementos:
    elemento = convertir_elemento(texto)

    print(
        f"{texto!r} → {elemento!r} "
        f"({type(elemento).__name__})"
    )


print("\nPRUEBA DE CREACIÓN DESDE ENTRADA")

A_prueba = crear_conjunto_desde_entrada(
    "A",
    "1, 2, 3, rojo, azul, α, +"
)

print(A_prueba)

print("\nPRUEBA DEL GESTOR DE CONJUNTOS")

gestor = GestorConjuntos()

A = crear_conjunto_desde_entrada(
    "A",
    "1, 2, 3, rojo, azul"
)

B = crear_conjunto_desde_entrada(
    "B",
    "3, 4, verde, azul"
)

gestor.agregar(A)
gestor.agregar(B)

print("\nConjuntos registrados:")

for conjunto in gestor.obtener_todos().values():
    print(conjunto)

print("\nPRUEBA DE SESIÓN")

sesion = SesionCalculadora()

A = crear_conjunto_desde_entrada(
    "A",
    "1, 2, 3, 4"
)

B = crear_conjunto_desde_entrada(
    "B",
    "3, 4, 5, 6"
)

sesion.gestor.agregar(A)
sesion.gestor.agregar(B)

expresion = "(A ∪ B) ∩ A"

resultado, pasos = sesion.resolver(expresion)

print("\nExpresión:")
print(expresion)

print("\nPasos:")

for numero, paso in enumerate(pasos, start=1):
    print(f"{numero}. {paso}")

print("\nResultado:")
print(resultado)

print("\nHistorial:")
print(sesion.obtener_historial())