def convertir_elemento(texto):
    texto = texto.strip()

    if not texto:
        raise ValueError("No se puede introducir un elemento vacío.")

    # Intentar convertir a entero
    try:
        return int(texto)
    except ValueError:
        pass

    # Intentar convertir a decimal
    try:
        return float(texto)
    except ValueError:
        pass

    # Si no es un número, se conserva como texto
    return texto