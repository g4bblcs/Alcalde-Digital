import random
from Tree import ArbolDecisiones


class Publicacion:
    def __init__(self, autor, contenido, es_falsa, arbol):
        self.autor = autor
        self.contenido = contenido
        self.es_falsa = es_falsa
        self.arbol = arbol


class SesionPublicacion:

    def __init__(self, publicacion):
        self.publicacion = publicacion
        self.actual = publicacion.arbol.raiz

    def opciones(self):
        ops = []
        if self.actual.izquierda:
            ops.append((self.actual.izquierda.etiqueta, 'izq'))
        if self.actual.derecha:
            ops.append((self.actual.derecha.etiqueta, 'der'))
        return ops

    def elegir(self, eleccion):
        self.actual = self.publicacion.arbol.avanzar(self.actual, eleccion)
        return self.actual

    def terminada(self):
        return self.actual.es_hoja()


class BancoPublicaciones:

    def __init__(self, publicaciones):
        self.pendientes = list(publicaciones)

    def hay_mas(self):
        return len(self.pendientes) > 0

    def siguiente(self):
        pub = random.choice(self.pendientes)
        self.pendientes.remove(pub)
        return pub


def armar_publicacion(autor, contenido, es_falsa, pregunta, izq, der):
    arbol = ArbolDecisiones()
    arbol.insertar(pregunta, [])
    arbol.insertar(izq["texto"], ['izq'], izq["efecto"], izq["etiqueta"])
    arbol.insertar(der["texto"], ['der'], der["efecto"], der["etiqueta"])
    return Publicacion(autor, contenido, es_falsa, arbol)