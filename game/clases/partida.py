# -*- coding: utf-8 -*-
"""Orquestador de la partida: une el AVL, el arbol de decisiones,
la ciudad y el jugador. Toda la logica vive aqui, en Python puro;
los archivos .rpy solo dibujan.
"""

import random

from clases.arbol_avl import ArbolAVL
from clases.arbol_decisiones import construir_arbol_acciones, RESULTADO
from clases.ciudad import Ciudad
from clases.jugador import Jugador
from clases import datos

TURNOS = 8


class Partida(object):

    def __init__(self, nombre_jugador, rol, semilla=None):
        self.rng = random.Random(semilla)
        self.arbol = ArbolAVL()
        self.decisiones = construir_arbol_acciones()
        self.ciudad = Ciudad()
        self.jugador = Jugador(nombre_jugador, rol)

        for p in datos.publicaciones_iniciales():
            self.arbol.insertar(p)

        self.pendientes = datos.publicaciones_evento()
        self.rng.shuffle(self.pendientes)

        self.turno = 0
        self.actual = None
        self.ultimo_resultado = None
        self.registro = []

    # ----- flujo de turnos -----------------------------------------------

    def hay_turnos(self):
        return self.turno < TURNOS and not self.arbol.vacio()

    def siguiente_publicacion(self):
        """Toma la de mayor riesgo viva en el feed.

        Se usa el inorden del AVL: su ultimo elemento es el maximo. Asi el
        jugador siempre enfrenta lo mas peligroso que circula ahora mismo.
        """
        feed = self.arbol.inorden()
        if not feed:
            self.actual = None
            return None
        self.actual = feed[-1]
        return self.actual

    def opciones(self):
        """Etiquetas disponibles del primer nivel del arbol de decisiones.

        VERIFICAR desaparece cuando el jugador agota su presupuesto: esa
        escasez es lo que convierte el turno en una decision real y no en
        un tramite (enunciado, seccion 9).
        """
        etiquetas = self.decisiones.raiz.etiquetas()
        if not self.jugador.puede_verificar():
            etiquetas = [e for e in etiquetas if e != "VERIFICAR"]
        return etiquetas

    def decidir(self, etiqueta):
        """Baja por el arbol de decisiones y aplica las consecuencias.

        Si la accion es VERIFICAR, el camino siguiente no lo elige el jugador:
        lo determina el dato real de la publicacion. Eso es exactamente lo que
        significa verificar, y hace que el recorrido del arbol dependa a la vez
        de la decision y de la informacion.
        """
        pub = self.actual
        if etiqueta == "VERIFICAR" and not self.jugador.gastar_verificacion():
            return None
        nodo = self.decisiones.avanzar(self.decisiones.raiz, etiqueta)
        camino = [etiqueta]

        if nodo is not None and nodo.tipo != RESULTADO:
            rama = "ES_VERDADERA" if pub.es_confiable else "ES_FALSA"
            nodo = self.decisiones.avanzar(nodo, rama)
            camino.append(rama)
            pub.verificada = True

        multiplicador = self.jugador.multiplicador(etiqueta)
        escala = 1.0 + (pub.impacto - 5) * 0.06
        cambios = self.ciudad.aplicar(nodo.efecto, multiplicador * escala)

        acierto = self._fue_responsable(etiqueta, pub)
        puntos = self._puntos(etiqueta, pub, acierto)
        self.jugador.registrar(puntos, acierto)

        self.arbol.eliminar(pub.clave)
        self.turno += 1

        self.ultimo_resultado = {
            "camino": camino,
            "titulo": nodo.texto,
            "mensaje": nodo.mensaje,
            "cambios": cambios,
            "acierto": acierto,
            "puntos": puntos,
            "tipo_real": pub.tipo,
            "verificaciones": self.jugador.verificaciones,
        }
        self.registro.append(self.ultimo_resultado)

        self._evento_aleatorio()
        return self.ultimo_resultado

    # ----- reglas ---------------------------------------------------------

    def _fue_responsable(self, etiqueta, pub):
        if etiqueta == "VERIFICAR":
            return True
        if etiqueta == "COMPARTIR":
            return pub.es_confiable
        if etiqueta == "REPORTAR":
            return not pub.es_confiable
        return pub.nivel_riesgo < 40      # ignorar algo inofensivo no hace dano

    def _puntos(self, etiqueta, pub, acierto):
        base = 10 + pub.nivel_riesgo // 10
        if etiqueta == "VERIFICAR":
            base += 5
        return base if acierto else -base

    def _evento_aleatorio(self):
        """Seccion 8: en plena partida puede entrar contenido nuevo al feed.

        Esto es lo que obliga a que el arbol sea AVL y no una lista ordenada:
        el feed cambia de tamano y de forma mientras se juega.
        """
        if not self.pendientes or self.rng.random() > 0.55:
            return None
        nueva = self.pendientes.pop()
        self.arbol.insertar(nueva)
        return nueva

    # ----- cierre ----------------------------------------------------------

    def resultado_final(self):
        alcalde, relato = self.ciudad.resultado_eleccion()
        return {
            "alcalde": alcalde,
            "relato": relato,
            "salud": self.ciudad.salud(),
            "puntos": self.jugador.puntos,
            "reputacion": self.jugador.reputacion,
            "precision": self.jugador.precision(),
        }
