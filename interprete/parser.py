class Nodo:
    def __init__(self, tipo, valor=None, izquierda=None, derecha=None):
        self.tipo = tipo
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha

    def __repr__(self):

        if self.tipo == "CONJUNTO":
            return self.valor

        if self.tipo == "COMPLEMENTO":
            return f"({self.izquierda}ᶜ)"

        return f"({self.izquierda} {self.valor} {self.derecha})"


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    # ==========================================================
    # TOKEN ACTUAL
    # ==========================================================

    def token_actual(self):

        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]

        return None

    # ==========================================================
    # AVANZAR
    # ==========================================================

    def avanzar(self):
        self.posicion += 1

    # ==========================================================
    # ANALIZAR
    # ==========================================================

    def analizar(self):

        if not self.tokens:
            raise ValueError(
                "La expresión está vacía."
            )

        arbol = self.expresion()

        if self.token_actual() is not None:
            raise ValueError(
                f"Token inesperado: '{self.token_actual()}'"
            )

        return arbol

    # ==========================================================
    # EXPRESIÓN
    #
    # Unión, diferencia y diferencia simétrica
    # tienen menor precedencia que la intersección.
    # ==========================================================

    def expresion(self):

        nodo = self.termino()

        while self.token_actual() in (
            "∪",
            "-",
            "−",
            "△",
            "^"
        ):

            operador = self.token_actual()

            self.avanzar()

            derecha = self.termino()

            nodo = Nodo(
                "OPERACION",
                operador,
                nodo,
                derecha
            )

        return nodo

    # ==========================================================
    # TÉRMINO
    #
    # La intersección tiene mayor precedencia.
    # ==========================================================

    def termino(self):

        nodo = self.factor()

        while self.token_actual() == "∩":

            operador = self.token_actual()

            self.avanzar()

            derecha = self.factor()

            nodo = Nodo(
                "OPERACION",
                operador,
                nodo,
                derecha
            )

        return nodo

    # ==========================================================
    # FACTOR
    #
    # Maneja:
    #
    # A
    # Aᶜ
    # (A ∪ B)
    # (A ∪ B)ᶜ
    # ==========================================================

    def factor(self):

        token = self.token_actual()

        if token is None:
            raise ValueError(
                "Se esperaba un conjunto o un paréntesis."
            )

        # ======================================================
        # CONJUNTO
        # ======================================================

        if token.isalpha():

            self.avanzar()

            nodo = Nodo(
                "CONJUNTO",
                token
            )

            # Complemento posterior:
            #
            # Aᶜ
            #
            # En lugar de:
            #
            # ᶜA
            #
            if self.token_actual() == "ᶜ":

                self.avanzar()

                nodo = Nodo(
                    "COMPLEMENTO",
                    "ᶜ",
                    nodo
                )

            return nodo

        # ======================================================
        # PARÉNTESIS
        # ======================================================

        if token == "(":

            self.avanzar()

            nodo = self.expresion()

            if self.token_actual() != ")":
                raise ValueError(
                    "Falta un paréntesis de cierre ')'."
                )

            self.avanzar()

            # Complemento de una expresión completa:
            #
            # (A ∪ B)ᶜ
            #
            if self.token_actual() == "ᶜ":

                self.avanzar()

                nodo = Nodo(
                    "COMPLEMENTO",
                    "ᶜ",
                    nodo
                )

            return nodo

        # ======================================================
        # TOKEN NO RECONOCIDO
        # ======================================================

        raise ValueError(
            f"Token inesperado: '{token}'"
        )