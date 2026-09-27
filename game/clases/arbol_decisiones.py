# -*- coding: utf-8 -*-
"""Arbol de decisiones: modela el flujo de accion sobre una publicacion.

Es la segunda estructura de arbol del proyecto y resuelve un problema
distinto al del AVL.

1. Que problema resuelve?
   Las consecuencias de una decision no son planas: dependen del camino
   recorrido. Verificar y despues compartir algo falso no es lo mismo que
   compartirlo de entrada. Este arbol guarda ese encadenamiento.

2. Por que esta estructura?
   El flujo es jerarquico y finito: cada decision abre un subconjunto de
   decisiones posibles y ningun camino vuelve atras. Eso es exactamente un
   arbol. Con condicionales sueltos el codigo seria inmantenible y no se
   podria recorrer ni mostrar graficamente.

3. Que variante se utiliza?
   Arbol n-ario de decision (cada nodo tiene de 0 a 3 hijos etiquetados).
   No requiere balanceo porque su forma la define el diseno del juego, no
   el orden de llegada de los datos.

4. Como se insertan y eliminan elementos?
   Insercion por ruta de etiquetas desde la raiz; eliminacion por poda de
   la rama completa que cuelga de una etiqueta.

5. Como se recorre?
   En preorden y por niveles para mostrarlo en pantalla, y descendiendo
   etiqueta a etiqueta durante la partida (metodo avanzar).
"""

PREGUNTA = "PREGUNTA"
RESULTADO = "RESULTADO"


class NodoDecision(object):

    def __init__(self, texto, tipo=PREGUNTA, efecto=None, mensaje=""):
        self.texto = texto
        self.tipo = tipo
        self.efecto = efecto or {}
        self.mensaje = mensaje
        self.hijos = []          # lista de (etiqueta, NodoDecision)

    def agregar(self, etiqueta, nodo):
        self.hijos.append((etiqueta, nodo))
        return nodo

    def hijo(self, etiqueta):
        for et, nodo in self.hijos:
            if et == etiqueta:
                return nodo
        return None

    def etiquetas(self):
        return [et for et, _ in self.hijos]

    def es_hoja(self):
        return len(self.hijos) == 0


class ArbolDecisiones(object):

    def __init__(self, raiz=None):
        self.raiz = raiz

    # ----- construccion -------------------------------------------------

    def insertar(self, ruta, etiqueta, nodo):
        """Cuelga `nodo` bajo `etiqueta` en el nodo alcanzado por `ruta`."""
        destino = self.nodo_en(ruta)
        if destino is None:
            return None
        return destino.agregar(etiqueta, nodo)

    def eliminar(self, ruta, etiqueta):
        """Poda la rama que cuelga de `etiqueta`. Devuelve si elimino algo."""
        destino = self.nodo_en(ruta)
        if destino is None:
            return False
        antes = len(destino.hijos)
        destino.hijos = [(e, n) for e, n in destino.hijos if e != etiqueta]
        return len(destino.hijos) < antes

    def nodo_en(self, ruta):
        actual = self.raiz
        for etiqueta in ruta:
            if actual is None:
                return None
            actual = actual.hijo(etiqueta)
        return actual

    # ----- navegacion en partida ----------------------------------------

    def avanzar(self, nodo, etiqueta):
        return nodo.hijo(etiqueta) if nodo else None

    # ----- recorridos ---------------------------------------------------

    def preorden(self):
        acc = []
        self._preorden(self.raiz, 0, acc)
        return acc

    def _preorden(self, nodo, nivel, acc):
        if nodo is None:
            return
        acc.append((nivel, nodo))
        for _, hijo in nodo.hijos:
            self._preorden(hijo, nivel + 1, acc)

    def posorden(self):
        acc = []
        self._posorden(self.raiz, 0, acc)
        return acc

    def _posorden(self, nodo, nivel, acc):
        if nodo is None:
            return
        for _, hijo in nodo.hijos:
            self._posorden(hijo, nivel + 1, acc)
        acc.append((nivel, nodo))

    def por_niveles(self):
        if self.raiz is None:
            return []
        niveles, cola = [], [self.raiz]
        while cola:
            siguiente, fila = [], []
            for nodo in cola:
                fila.append(nodo)
                siguiente.extend(h for _, h in nodo.hijos)
            niveles.append(fila)
            cola = siguiente
        return niveles

    def altura(self):
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        if nodo.es_hoja():
            return 1
        return 1 + max(self._altura(h) for _, h in nodo.hijos)

    def contar_nodos(self):
        return self._contar(self.raiz)

    def _contar(self, nodo):
        if nodo is None:
            return 0
        return 1 + sum(self._contar(h) for _, h in nodo.hijos)

    def lineas_ascii(self):
        acc = []
        for nivel, nodo in self.preorden():
            marca = "*" if nodo.tipo == RESULTADO else "?"
            acc.append("   " * nivel + marca + " " + nodo.texto)
        return acc


def construir_arbol_acciones():
    """Arbol de decisiones del enunciado (seccion 5), con consecuencias.

    Los efectos son diccionarios de deltas sobre los indicadores de la ciudad.
    """
    raiz = NodoDecision("Llega una publicacion a tu feed. Que haces?")

    # --- VERIFICAR: abre una segunda decision informada ---------------
    verificar = raiz.agregar("VERIFICAR", NodoDecision(
        "Contrastaste la fuente. Resulta ser..."))

    verificar.agregar("ES_VERDADERA", NodoDecision(
        "La compartes ya verificada", RESULTADO,
        {"info_verificada": 6, "confianza": 4, "bienestar": 2, "desinformacion": -3},
        "Verificaste antes de difundir: la ciudad gana informacion confiable."))

    verificar.agregar("ES_FALSA", NodoDecision(
        "La reportas como desinformacion", RESULTADO,
        {"info_verificada": 5, "confianza": 3, "desinformacion": -7, "conflictos": -2},
        "Detectaste la mentira y cortaste su propagacion."))

    # --- COMPARTIR sin verificar --------------------------------------
    raiz.agregar("COMPARTIR", NodoDecision(
        "La compartes sin comprobar nada", RESULTADO,
        {"confianza": -4, "desinformacion": 8, "conflictos": 5, "convivencia": -4},
        "Difundiste sin verificar. Si era falsa, el dano ya esta hecho."))

    # --- REPORTAR de entrada ------------------------------------------
    raiz.agregar("REPORTAR", NodoDecision(
        "La reportas de inmediato", RESULTADO,
        {"conflictos": -3, "info_verificada": 2, "convivencia": 1},
        "Reportar ayuda, pero reportar sin leer tambien silencia voces legitimas."))

    # --- IGNORAR -------------------------------------------------------
    raiz.agregar("IGNORAR", NodoDecision(
        "Sigues de largo", RESULTADO,
        {"desinformacion": 3, "conflictos": 1},
        "Ignorar no es neutral: el contenido sigue circulando sin contrapeso."))

    return ArbolDecisiones(raiz)
