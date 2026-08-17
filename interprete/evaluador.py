from operaciones.operaciones import (
    union,
    interseccion,
    diferencia,
    diferencia_simetrica,
    complemento
)


class Evaluador:

    def __init__(self, conjuntos, universal=None):

        self.conjuntos = conjuntos
        self.universal = universal
        self.pasos = []

    # ==========================================================
    # EVALUAR
    # ==========================================================

    def evaluar(self, nodo):

        # ======================================================
        # CONJUNTO
        # ======================================================

        if nodo.tipo == "CONJUNTO":

            nombre = nodo.valor.upper()

            if nombre not in self.conjuntos:

                raise ValueError(
                    f"El conjunto '{nombre}' no está definido."
                )

            return self.conjuntos[nombre]

        # ======================================================
        # COMPLEMENTO
        # ======================================================

        if nodo.tipo == "COMPLEMENTO":

            conjunto = self.evaluar(
                nodo.izquierda
            )

            # El complemento necesita U.
            if self.universal is None:

                raise ValueError(
                    "No se puede calcular el complemento "
                    "porque no se ha definido el conjunto universo U."
                )

            resultado = complemento(
                conjunto,
                self.universal
            )

            self.pasos.append(
                f"{conjunto.nombre}ᶜ = {resultado.elementos}"
            )

            return resultado

        # ======================================================
        # OPERACIÓN
        # ======================================================

        if nodo.tipo == "OPERACION":

            izquierda = self.evaluar(
                nodo.izquierda
            )

            derecha = self.evaluar(
                nodo.derecha
            )

            operador = nodo.valor

            # --------------------------------------------------
            # UNIÓN
            # --------------------------------------------------

            if operador == "∪":

                resultado = union(
                    izquierda,
                    derecha
                )

            # --------------------------------------------------
            # INTERSECCIÓN
            # --------------------------------------------------

            elif operador == "∩":

                resultado = interseccion(
                    izquierda,
                    derecha
                )

            # --------------------------------------------------
            # DIFERENCIA
            # --------------------------------------------------

            elif operador in ("-", "−"):

                resultado = diferencia(
                    izquierda,
                    derecha
                )

            # --------------------------------------------------
            # DIFERENCIA SIMÉTRICA
            # --------------------------------------------------

            elif operador in ("△", "^"):

                resultado = diferencia_simetrica(
                    izquierda,
                    derecha
                )

            else:

                raise ValueError(
                    f"Operador no soportado: '{operador}'"
                )

            self.pasos.append(
                f"{izquierda.elementos} "
                f"{operador} "
                f"{derecha.elementos} "
                f"= {resultado.elementos}"
            )

            return resultado

        # ======================================================
        # ERROR
        # ======================================================

        raise ValueError(
            f"Tipo de nodo desconocido: '{nodo.tipo}'"
        )