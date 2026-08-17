from modelos.conjunto import Conjunto


class GestorConjuntos:

    def __init__(self):

        self.conjuntos = {}

        # ======================================================
        # CONJUNTO UNIVERSO
        # ======================================================
        #
        # U no se administra manualmente.
        # Siempre se obtiene a partir de los elementos
        # existentes en los demás conjuntos.
        #

        self.universo = Conjunto("U")

    # ==========================================================
    # ACTUALIZAR UNIVERSO
    # ==========================================================

    def actualizar_universo(self):

        elementos = set()

        for conjunto in self.conjuntos.values():

            elementos.update(
                conjunto.elementos
            )

        self.universo.elementos = elementos

    # ==========================================================
    # AGREGAR CONJUNTO
    # ==========================================================

    def agregar(self, conjunto):

        nombre = conjunto.nombre.upper()

        # ------------------------------------------------------
        # U ESTÁ RESERVADO
        # ------------------------------------------------------

        if nombre == "U":

            raise ValueError(
                "La letra U está reservada para el conjunto universo."
            )

        # ------------------------------------------------------
        # EVITAR DUPLICADOS
        # ------------------------------------------------------

        if nombre in self.conjuntos:

            raise ValueError(
                f"El conjunto {nombre} ya existe."
            )

        # ------------------------------------------------------
        # GUARDAR
        # ------------------------------------------------------

        conjunto.nombre = nombre

        self.conjuntos[nombre] = conjunto

        # ------------------------------------------------------
        # ACTUALIZAR U
        # ------------------------------------------------------

        self.actualizar_universo()

    # ==========================================================
    # OBTENER CONJUNTO
    # ==========================================================

    def obtener(self, nombre):

        nombre = nombre.upper()

        # ------------------------------------------------------
        # U
        # ------------------------------------------------------

        if nombre == "U":

            return self.universo

        # ------------------------------------------------------
        # CONJUNTO NORMAL
        # ------------------------------------------------------

        if nombre not in self.conjuntos:

            raise ValueError(
                f"El conjunto {nombre} no existe."
            )

        return self.conjuntos[nombre]

    # ==========================================================
    # OBTENER TODOS
    # ==========================================================

    def obtener_todos(self):

        resultado = dict(
            self.conjuntos
        )

        # U siempre aparece al final
        resultado["U"] = self.universo

        return resultado

    # ==========================================================
    # MODIFICAR
    # ==========================================================

    def modificar(
        self,
        nombre,
        elementos
    ):

        nombre = nombre.upper()

        # ------------------------------------------------------
        # U NO SE MODIFICA
        # ------------------------------------------------------

        if nombre == "U":

            raise ValueError(
                "El conjunto universo se genera automáticamente "
                "y no puede modificarse directamente."
            )

        # ------------------------------------------------------
        # VERIFICAR EXISTENCIA
        # ------------------------------------------------------

        if nombre not in self.conjuntos:

            raise ValueError(
                f"El conjunto {nombre} no existe."
            )

        # ------------------------------------------------------
        # ACTUALIZAR ELEMENTOS
        # ------------------------------------------------------
        #
        # La interfaz se encarga de garantizar que los elementos
        # existentes se conserven.
        #

        self.conjuntos[nombre].elementos = set(
            elementos
        )

        # ------------------------------------------------------
        # ACTUALIZAR U
        # ------------------------------------------------------

        self.actualizar_universo()

    # ==========================================================
    # ELIMINAR
    # ==========================================================

    def eliminar(
        self,
        nombre
    ):

        nombre = nombre.upper()

        # ------------------------------------------------------
        # U NO SE ELIMINA
        # ------------------------------------------------------

        if nombre == "U":

            raise ValueError(
                "El conjunto universo no puede eliminarse."
            )

        # ------------------------------------------------------
        # VERIFICAR EXISTENCIA
        # ------------------------------------------------------

        if nombre not in self.conjuntos:

            raise ValueError(
                f"El conjunto {nombre} no existe."
            )

        # ------------------------------------------------------
        # ELIMINAR
        # ------------------------------------------------------

        del self.conjuntos[nombre]

        # ------------------------------------------------------
        # RECONSTRUIR U
        # ------------------------------------------------------

        self.actualizar_universo()

    # ==========================================================
    # OBTENER UNIVERSO
    # ==========================================================

    def obtener_universo(self):

        return self.universo

    # ==========================================================
    # COMPATIBILIDAD
    # ==========================================================

    def obtener_universal(self):

        return self.universo