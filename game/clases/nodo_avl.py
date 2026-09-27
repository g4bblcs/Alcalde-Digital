# -*- coding: utf-8 -*-
"""Nodo del arbol AVL que indexa el feed de Civitas."""


class NodoAVL(object):

    def __init__(self, clave, publicacion):
        self.clave = clave
        self.publicacion = publicacion
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None

    def __repr__(self):
        return "NodoAVL({0})".format(self.clave)
