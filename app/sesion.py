from modelos.gestor_conjuntos import GestorConjuntos
from interprete.lexer import Lexer
from interprete.parser import Parser
from interprete.evaluador import Evaluador


class SesionCalculadora:

    def __init__(self):
        self.gestor = GestorConjuntos()
        self.historial = []

    # ==========================================================
    # RESOLVER EXPRESIÓN
    # ==========================================================

    def resolver(self, expresion):

        lexer = Lexer(expresion)
        tokens = lexer.tokenizar()

        parser = Parser(tokens)
        arbol = parser.analizar()

        # Obtenemos los conjuntos disponibles.
        conjuntos = self.gestor.obtener_todos()

        # Obtenemos U solamente si está definido.
        universo = self.gestor.universo

        evaluador = Evaluador(
            conjuntos,
            universo
        )

        resultado = evaluador.evaluar(arbol)

        self.historial.append({
            "expresion": expresion,
            "resultado": resultado,
            "pasos": evaluador.pasos.copy()
        })

        return resultado, evaluador.pasos

    # ==========================================================
    # HISTORIAL
    # ==========================================================

    def obtener_historial(self):

        return self.historial