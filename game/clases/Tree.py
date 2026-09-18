class ArbolDecisiones:
    def __init__(self):
        self.raiz = None

    def insertar(self, texto, ruta, consecuencia=None):
        """
        ruta: lista de 'izq'/'der' que indica dónde insertar
        ej: ['izq', 'der'] -> raíz -> izquierda -> derecha
        """
        if self.raiz is None:
            self.raiz = NodoDecision(texto, consecuencia)
            return

        actual = self.raiz
        for paso in ruta[:-1]:
            actual = actual.izquierda if paso == 'izq' else actual.derecha

        nuevo_nodo = NodoDecision(texto, consecuencia)
        if ruta[-1] == 'izq':
            actual.izquierda = nuevo_nodo
        else:
            actual.derecha = nuevo_nodo

    def avanzar(self, nodo_actual, eleccion):
        """eleccion: 'izq' o 'der'"""
        if eleccion == 'izq':
            return nodo_actual.izquierda
        return nodo_actual.derecha