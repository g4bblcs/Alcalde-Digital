# -*- coding: utf-8 -*-
"""Arbol AVL: clasifica las publicaciones de Civitas por nivel de riesgo.

JUSTIFICACION (preguntas exigidas por el enunciado, seccion 5)

1. Que problema resuelve?
   El feed de Civitas debe recorrerse siempre de menor a mayor riesgo para que
   el jugador enfrente primero el contenido inofensivo y despues el peligroso.
   Ademas el feed es dinamico: los eventos virales insertan publicaciones nuevas
   en plena partida y reportar una la elimina. Se necesita una estructura que
   mantenga el orden y siga siendo rapida tras esas altas y bajas.

2. Por que esta estructura?
   Una lista ordenada costaria O(n) por insercion. Un BST simple degenera a
   lista enlazada si las publicaciones llegan casi ordenadas por riesgo (que es
   justo lo que pasa cuando una racha de rumores entra de menor a mayor), y ahi
   las operaciones caen a O(n).

3. Que variante se utiliza?
   AVL: BST con autobalanceo por altura. Tras cada alta o baja se recalcula el
   factor de equilibrio y se rota si |FE| > 1, garantizando altura O(log n).

4. Como se insertan y eliminan elementos?
   Insercion recursiva + rebalanceo (4 casos: II, DD, ID, DI).
   Eliminacion con los 3 casos clasicos; con dos hijos se sustituye por el
   sucesor inorden y se rebalancea al regresar de la recursion.

5. Como se recorre?
   Preorden, inorden, posorden (recursivos e iterativos con pila) y por niveles
   (BFS con cola). El inorden es el que alimenta el orden real del feed.
"""

from clases.nodo_avl import NodoAVL


class ArbolAVL(object):

    def __init__(self):
        self.raiz = None
        self._tamano = 0

    # ----- consultas basicas -------------------------------------------

    def __len__(self):
        return self._tamano

    def vacio(self):
        return self.raiz is None

    def altura(self, nodo):
        return 0 if nodo is None else nodo.altura

    def factor_equilibrio(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self.altura(nodo.izquierdo),
                              self.altura(nodo.derecho))

    # ----- rotaciones ---------------------------------------------------

    def _rotar_derecha(self, y):
        x = y.izquierdo
        y.izquierdo = x.derecho
        x.derecho = y
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x):
        y = x.derecho
        x.derecho = y.izquierdo
        y.izquierdo = x
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _rebalancear(self, nodo):
        self._actualizar_altura(nodo)
        fe = self.factor_equilibrio(nodo)

        if fe > 1:
            if self.factor_equilibrio(nodo.izquierdo) < 0:   # caso ID
                nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)                 # caso II

        if fe < -1:
            if self.factor_equilibrio(nodo.derecho) > 0:     # caso DI
                nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)               # caso DD

        return nodo

    # ----- insercion ----------------------------------------------------

    def insertar(self, publicacion):
        self.raiz = self._insertar(self.raiz, publicacion.clave, publicacion)
        self._tamano += 1

    def _insertar(self, nodo, clave, publicacion):
        if nodo is None:
            return NodoAVL(clave, publicacion)
        if clave < nodo.clave:
            nodo.izquierdo = self._insertar(nodo.izquierdo, clave, publicacion)
        else:
            nodo.derecho = self._insertar(nodo.derecho, clave, publicacion)
        return self._rebalancear(nodo)

    # ----- eliminacion --------------------------------------------------

    def eliminar(self, clave):
        antes = self._tamano
        self.raiz = self._eliminar(self.raiz, clave)
        return self._tamano < antes

    def _eliminar(self, nodo, clave):
        if nodo is None:
            return None

        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar(nodo.derecho, clave)
        else:
            self._tamano -= 1
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            sucesor = self._minimo(nodo.derecho)
            nodo.clave = sucesor.clave
            nodo.publicacion = sucesor.publicacion
            # el sucesor ya fue copiado: al borrarlo no debe contar dos veces
            self._tamano += 1
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.clave)

        return self._rebalancear(nodo)

    def _minimo(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    # ----- busqueda -----------------------------------------------------

    def buscar(self, clave):
        nodo = self.raiz
        while nodo is not None:
            if clave == nodo.clave:
                return nodo
            nodo = nodo.izquierdo if clave < nodo.clave else nodo.derecho
        return None

    def buscar_por_riesgo(self, riesgo_min, riesgo_max):
        """Publicaciones dentro de un rango de riesgo (poda de ramas)."""
        encontradas = []
        self._rango(self.raiz, riesgo_min, riesgo_max, encontradas)
        return encontradas

    def _rango(self, nodo, minimo, maximo, acc):
        if nodo is None:
            return
        riesgo = nodo.clave[0]
        if riesgo > minimo:
            self._rango(nodo.izquierdo, minimo, maximo, acc)
        if minimo <= riesgo <= maximo:
            acc.append(nodo.publicacion)
        if riesgo < maximo:
            self._rango(nodo.derecho, minimo, maximo, acc)

    # ----- recorridos recursivos ----------------------------------------

    def preorden(self):
        acc = []
        self._preorden(self.raiz, acc)
        return acc

    def _preorden(self, nodo, acc):
        if nodo is None:
            return
        acc.append(nodo.publicacion)
        self._preorden(nodo.izquierdo, acc)
        self._preorden(nodo.derecho, acc)

    def inorden(self):
        acc = []
        self._inorden(self.raiz, acc)
        return acc

    def _inorden(self, nodo, acc):
        if nodo is None:
            return
        self._inorden(nodo.izquierdo, acc)
        acc.append(nodo.publicacion)
        self._inorden(nodo.derecho, acc)

    def posorden(self):
        acc = []
        self._posorden(self.raiz, acc)
        return acc

    def _posorden(self, nodo, acc):
        if nodo is None:
            return
        self._posorden(nodo.izquierdo, acc)
        self._posorden(nodo.derecho, acc)
        acc.append(nodo.publicacion)

    # ----- recorridos iterativos ----------------------------------------

    def inorden_iterativo(self):
        acc, pila, actual = [], [], self.raiz
        while actual is not None or pila:
            while actual is not None:
                pila.append(actual)
                actual = actual.izquierdo
            actual = pila.pop()
            acc.append(actual.publicacion)
            actual = actual.derecho
        return acc

    def por_niveles(self):
        """BFS con cola: devuelve lista de listas, una por nivel."""
        if self.raiz is None:
            return []
        niveles, cola = [], [self.raiz]
        while cola:
            siguiente, fila = [], []
            for nodo in cola:
                fila.append(nodo)
                if nodo.izquierdo:
                    siguiente.append(nodo.izquierdo)
                if nodo.derecho:
                    siguiente.append(nodo.derecho)
            niveles.append(fila)
            cola = siguiente
        return niveles

    # ----- utilidades para la interfaz ----------------------------------

    def contar_nodos(self):
        return self._contar(self.raiz)

    def _contar(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar(nodo.izquierdo) + self._contar(nodo.derecho)

    def esta_balanceado(self):
        """Verifica la invariante AVL en todos los nodos."""
        return self._balanceado(self.raiz)

    def _balanceado(self, nodo):
        if nodo is None:
            return True
        if abs(self.factor_equilibrio(nodo)) > 1:
            return False
        return self._balanceado(nodo.izquierdo) and self._balanceado(nodo.derecho)

    def lineas_ascii(self):
        """Arbol horizontal como lista de strings, para dibujarlo en pantalla."""
        acc = []
        self._ascii(self.raiz, 0, acc)
        return acc

    def _ascii(self, nodo, nivel, acc):
        if nodo is None:
            return
        self._ascii(nodo.derecho, nivel + 1, acc)
        acc.append("    " * nivel + "{0} (FE {1:+d})".format(
            nodo.clave[0], self.factor_equilibrio(nodo)))
        self._ascii(nodo.izquierdo, nivel + 1, acc)

    def disposicion(self):
        """Posiciones para dibujar el arbol en pantalla.

        x = indice inorden (garantiza que ningun nodo se solape),
        y = profundidad. Devuelve (nodos, aristas) con coordenadas relativas.
        """
        nodos, aristas = [], []
        contador = [0]

        def recorrer(nodo, profundidad, padre_idx):
            if nodo is None:
                return None
            recorrer_izq = recorrer(nodo.izquierdo, profundidad + 1, None)
            x = contador[0]
            contador[0] += 1
            idx = len(nodos)
            nodos.append({
                "x": x,
                "y": profundidad,
                "riesgo": nodo.clave[0],
                "fe": self.factor_equilibrio(nodo),
                "publicacion": nodo.publicacion,
            })
            if recorrer_izq is not None:
                aristas.append((idx, recorrer_izq))
            der = recorrer(nodo.derecho, profundidad + 1, None)
            if der is not None:
                aristas.append((idx, der))
            return idx

        recorrer(self.raiz, 0, None)
        return nodos, aristas
