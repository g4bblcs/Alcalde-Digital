from collections import deque
from clases.Node import NodoDecision

class ArbolDecisiones:
    def __init__(self):
        self.raiz = None

    def insertar(self, texto, ruta, consecuencia=None, etiqueta=None):
        if self.raiz is None:
            self.raiz = NodoDecision(texto, consecuencia, etiqueta)
            return

        actual = self.raiz
        for paso in ruta[:-1]:
            if actual is None:
                raise ValueError("La ruta especificada no existe en el árbol.")
            actual = actual.izquierda if paso == 'izq' else actual.derecha

        nuevo_nodo = NodoDecision(texto, consecuencia, etiqueta)
        if ruta[-1] == 'izq':
            actual.izquierda = nuevo_nodo
        else:
            actual.derecha = nuevo_nodo

    def recorrido_por_niveles(self):
        #recorrido bfs :)
        if not self.raiz:
            return []
        
        resultado = []
        cola = deque([self.raiz])
        
        while cola:
            nodo_actual = cola.popleft()
            resultado.append(nodo_actual.texto)
            
            if nodo_actual.izquierda:
                cola.append(nodo_actual.izquierda)
            if nodo_actual.derecha:
                cola.append(nodo_actual.derecha)
                
        return resultado

    def avanzar(self, nodo_actual, eleccion):
        """eleccion: 'izq' o 'der'"""
        if eleccion == 'izq':
            return nodo_actual.izquierda
        return nodo_actual.derecha