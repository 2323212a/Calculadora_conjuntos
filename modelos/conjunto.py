class Conjunto:
    def __init__(self, nombre, elementos=None):
        self.nombre = nombre.upper()
        self.elementos = set(elementos) if elementos is not None else set()

    # ==========================================================
    # AGREGAR ELEMENTO
    # ==========================================================

    def agregar(self, elemento):
        self.elementos.add(elemento)

    # ==========================================================
    # ELIMINAR ELEMENTO
    # ==========================================================

    def eliminar(self, elemento):
        self.elementos.discard(elemento)

    # ==========================================================
    # COMPROBAR PERTENENCIA
    # ==========================================================

    def contiene(self, elemento):
        return elemento in self.elementos

    # ==========================================================
    # CANTIDAD
    # ==========================================================

    def cantidad(self):
        return len(self.elementos)

    # ==========================================================
    # CONJUNTO VACÍO
    # ==========================================================

    def esta_vacio(self):
        return len(self.elementos) == 0

    # ==========================================================
    # ELEMENTOS ORDENADOS
    # ==========================================================

    def obtener_elementos_ordenados(self):
        return sorted(
            self.elementos,
            key=lambda elemento: str(elemento)
        )

    # ==========================================================
    # REPRESENTACIÓN
    # ==========================================================

    def __str__(self):

        if self.esta_vacio():
            return f"{self.nombre} = ∅"

        elementos_ordenados = self.obtener_elementos_ordenados()

        contenido = ", ".join(
            map(str, elementos_ordenados)
        )

        return f"{self.nombre} = {{{contenido}}}"