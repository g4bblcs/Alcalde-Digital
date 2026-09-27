# -*- coding: utf-8 -*-
"""Modelo de una publicacion de la red social Civitas."""

VERDADERA = "VERDADERA"
FALSA = "FALSA"
RUMOR = "RUMOR"
OPINION = "OPINION"

ACTIVA = "ACTIVA"
VERIFICADA = "VERIFICADA"
REPORTADA = "REPORTADA"
PROPAGADA = "PROPAGADA"


class Publicacion(object):
    """Contenido que circula en Civitas.

    El nivel de riesgo (0-100) mide cuanto dano puede causar si se difunde
    sin verificar. Es la clave con la que el AVL ordena el feed.
    """

    def __init__(self, id, texto, autor, tipo, nivel_riesgo, impacto):
        self.id = id
        self.texto = texto
        self.autor = autor
        self.tipo = tipo
        self.nivel_riesgo = nivel_riesgo
        self.impacto = impacto
        self.verificada = False
        self.estado = ACTIVA

    @property
    def clave(self):
        """Clave de ordenamiento del AVL.

        Se usa la tupla (riesgo, id) en lugar del riesgo solo para garantizar
        unicidad: si dos publicaciones tuvieran el mismo riesgo, una clave
        simple obligaria a descartar la segunda y se perderia informacion.
        """
        return (self.nivel_riesgo, self.id)

    @property
    def es_confiable(self):
        return self.tipo == VERDADERA

    def etiqueta_riesgo(self):
        if self.nivel_riesgo >= 70:
            return "ALTO"
        if self.nivel_riesgo >= 40:
            return "MEDIO"
        return "BAJO"

    def __str__(self):
        return "[{0}] riesgo {1} ({2}) - {3}".format(
            self.id, self.nivel_riesgo, self.etiqueta_riesgo(), self.texto)

    def __repr__(self):
        return "Publicacion(id={0}, riesgo={1})".format(self.id, self.nivel_riesgo)
