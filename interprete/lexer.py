class Lexer:
    def __init__(self, expresion):
        self.expresion = expresion

    def tokenizar(self):
        tokens = []
        i = 0

        while i < len(self.expresion):
            caracter = self.expresion[i]

            # Ignorar espacios
            if caracter.isspace():
                i += 1
                continue

            # Paréntesis
            if caracter in "()":
                tokens.append(caracter)
                i += 1
                continue

            # Operadores
            if caracter in "∪∩−-△^":
                tokens.append(caracter)
                i += 1
                continue

            # Complemento
            if caracter == "ᶜ":
                tokens.append(caracter)
                i += 1
                continue

            # Nombre del conjunto
            if caracter.isalpha():
                nombre = caracter.upper()
                tokens.append(nombre)
                i += 1
                continue

            # Carácter no reconocido
            raise ValueError(
                f"Carácter no reconocido: '{caracter}'"
            )

        return tokens