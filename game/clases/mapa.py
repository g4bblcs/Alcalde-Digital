# -*- coding: utf-8 -*-
"""Mapa navegable de Ciudad Nova, independiente de Ren'Py."""

import heapq
import math


IDLE = "IDLE"
VIAJANDO = "VIAJANDO"
LLEGADA = "LLEGADA"
CANCELADO = "CANCELADO"


class Ubicacion(object):

    def __init__(self, identificador, nombre, posicion, descripcion=""):
        self.id = identificador
        self.nombre = nombre
        self.posicion = posicion
        self.descripcion = descripcion


class MapaCiudad(object):
    """Catalogo de destinos y grafo de calles expresado en coordenadas 0..1."""

    UBICACIONES = (
        ("universidad", "Universidad", (0.39, 0.145)),
        ("prensa", "Prensa", (0.70, 0.19)),
        ("barrio_norte", "Barrio Norte", (0.19, 0.30)),
        ("centro", "Centro", (0.48, 0.34)),
        ("alcaldia", "Alcaldia", (0.60, 0.53)),
        ("parque_central", "Parque Central", (0.22, 0.63)),
        ("barrio_sur", "Barrio Sur", (0.49, 0.79)),
        ("transporte", "Transporte Publico", (0.75, 0.73)),
    )

    CONEXIONES = (
        ("universidad", "centro"),
        ("universidad", "barrio_norte"),
        ("barrio_norte", "centro"),
        ("centro", "prensa"),
        ("centro", "alcaldia"),
        ("centro", "parque_central"),
        ("alcaldia", "prensa"),
        ("alcaldia", "barrio_sur"),
        ("alcaldia", "transporte"),
        ("parque_central", "barrio_sur"),
        ("barrio_sur", "transporte"),
    )

    def __init__(self):
        self.ubicaciones = {
            identificador: Ubicacion(identificador, nombre, posicion)
            for identificador, nombre, posicion in self.UBICACIONES
        }
        self.conexiones = {identificador: [] for identificador in self.ubicaciones}
        for origen, destino in self.CONEXIONES:
            peso = self._distancia(origen, destino)
            self.conexiones[origen].append((destino, peso))
            self.conexiones[destino].append((origen, peso))

    def _distancia(self, origen, destino):
        a = self.ubicaciones[origen].posicion
        b = self.ubicaciones[destino].posicion
        return math.hypot(b[0] - a[0], b[1] - a[1])

    def obtener(self, identificador):
        return self.ubicaciones.get(identificador)

    def ruta(self, origen, destino):
        """Devuelve ids de ubicaciones en la ruta minima, incluido origen y destino."""
        if origen not in self.ubicaciones or destino not in self.ubicaciones:
            return []
        if origen == destino:
            return [origen]

        distancias = {origen: 0.0}
        anteriores = {}
        cola = [(0.0, origen)]
        while cola:
            distancia, actual = heapq.heappop(cola)
            if actual == destino:
                break
            if distancia != distancias.get(actual):
                continue
            for vecino, peso in self.conexiones[actual]:
                nueva_distancia = distancia + peso
                if nueva_distancia < distancias.get(vecino, float("inf")):
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

        if destino not in anteriores:
            return []
        camino = [destino]
        while camino[-1] != origen:
            camino.append(anteriores[camino[-1]])
        camino.reverse()
        return camino


class Viaje(object):
    """Avance temporal de un carro sobre una ruta de ubicaciones."""

    DIRECCIONES = {
        "arriba": "arriba",
        "abajo": "abajo",
        "izquierda": "izq",
        "derecha": "der",
        "arriba_izquierda": "arriba_diag_izq",
        "arriba_derecha": "arriba_diag_der",
        "abajo_izquierda": "abajo_diag_izq",
        "abajo_derecha": "abajo_diag_der",
    }
    FRAMES = {"arriba": 3}

    def __init__(self, mapa, origen):
        self.mapa = mapa
        self.origen = origen
        self.destino = origen
        self.ruta = [origen]
        self.segmento = 0
        self.progreso = 0.0
        self.tiempo = 0.0
        self.estado = IDLE
        self.posicion = mapa.obtener(origen).posicion
        self.direccion = "abajo"

    def iniciar(self, destino):
        ruta = self.mapa.ruta(self.ubicacion_actual, destino)
        if not ruta:
            return False
        self.destino = destino
        self.ruta = ruta
        self.segmento = 0
        self.progreso = 0.0
        self.tiempo = 0.0
        self.estado = IDLE if len(ruta) == 1 else VIAJANDO
        self.posicion = self.mapa.obtener(ruta[0]).posicion
        if self.estado == IDLE:
            self.estado = LLEGADA
        return True

    @property
    def ubicacion_actual(self):
        if self.estado == LLEGADA:
            return self.destino
        return self.ruta[self.segmento]

    @property
    def terminado(self):
        return self.estado == LLEGADA

    def cancelar(self):
        if self.estado == VIAJANDO:
            self.estado = CANCELADO

    def avanzar(self, segundos):
        if self.estado != VIAJANDO:
            return False
        self.tiempo += max(0.0, segundos)
        restante = max(0.0, segundos)
        while restante > 0 and self.segmento < len(self.ruta) - 1:
            origen = self.mapa.obtener(self.ruta[self.segmento]).posicion
            destino = self.mapa.obtener(self.ruta[self.segmento + 1]).posicion
            longitud = max(self.mapa._distancia(self.ruta[self.segmento], self.ruta[self.segmento + 1]), 0.001)
            velocidad = 0.22
            disponible = (1.0 - self.progreso) * longitud / velocidad
            paso = min(restante, disponible)
            self.progreso += paso * velocidad / longitud
            self.posicion = (
                origen[0] + (destino[0] - origen[0]) * self.progreso,
                origen[1] + (destino[1] - origen[1]) * self.progreso,
            )
            self.direccion = self._direccion(origen, destino)
            restante -= paso
            if self.progreso >= 0.999999:
                self.segmento += 1
                self.progreso = 0.0
                self.posicion = destino
        if self.segmento >= len(self.ruta) - 1:
            self.posicion = self.mapa.obtener(self.destino).posicion
            self.estado = LLEGADA
        return True

    def _direccion(self, origen, destino):
        dx = destino[0] - origen[0]
        dy = destino[1] - origen[1]
        horizontal = "derecha" if dx >= 0 else "izquierda"
        vertical = "abajo" if dy >= 0 else "arriba"
        if abs(dx) < 0.35 * abs(dy):
            return vertical
        if abs(dy) < 0.35 * abs(dx):
            return horizontal
        return vertical + "_" + horizontal

    def sprite_path(self):
        return "images/carro/Carro_{0}/{1}.png".format(
            self.DIRECCIONES[self.direccion], self.frame())

    def frame(self):
        cantidad = self.FRAMES.get(self.DIRECCIONES[self.direccion], 4)
        return int(self.tiempo * 8.0) % cantidad