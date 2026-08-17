from modelos.conjunto import Conjunto


def union(conjunto_a, conjunto_b):
    elementos = conjunto_a.elementos | conjunto_b.elementos
    return Conjunto("Resultado", elementos)


def interseccion(conjunto_a, conjunto_b):
    elementos = conjunto_a.elementos & conjunto_b.elementos
    return Conjunto("Resultado", elementos)


def diferencia(conjunto_a, conjunto_b):
    elementos = conjunto_a.elementos - conjunto_b.elementos
    return Conjunto("Resultado", elementos)


def diferencia_simetrica(conjunto_a, conjunto_b):
    elementos = conjunto_a.elementos ^ conjunto_b.elementos
    return Conjunto("Resultado", elementos)


def complemento(conjunto, universal):
    elementos = universal.elementos - conjunto.elementos
    return Conjunto("Resultado", elementos)