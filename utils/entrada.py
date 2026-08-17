from modelos.conjunto import Conjunto
from utils.elementos import convertir_elemento


def crear_conjunto_desde_entrada(nombre, entrada):
    if not nombre:
        raise ValueError(
            "El nombre del conjunto no puede estar vacío."
        )

    entrada = entrada.strip()

    # Conjunto vacío
    if entrada == "" or entrada == "∅" or entrada == "{}":
        return Conjunto(nombre)

    partes = entrada.split(",")

    elementos = []

    for posicion, parte in enumerate(partes, start=1):
        parte = parte.strip()

        if not parte:
            raise ValueError(
                f"El elemento número {posicion} está vacío."
            )

        # Evitar confundir ∅ con un elemento
        if parte == "∅":
            raise ValueError(
                "El símbolo ∅ representa el conjunto vacío. "
                "No puede utilizarse como elemento individual."
            )

        elemento = convertir_elemento(parte)
        elementos.append(elemento)

    return Conjunto(nombre, elementos)