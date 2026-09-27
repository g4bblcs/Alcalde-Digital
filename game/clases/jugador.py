# -*- coding: utf-8 -*-
"""Jugador y roles de Civitas (seccion 4 del enunciado).

Cada rol tiene habilidades distintas, de modo que la misma decision no
produce el mismo efecto para todos.
"""

CIUDADANO = "CIUDADANO"
PERIODISTA = "PERIODISTA"
INFLUENCER = "INFLUENCER"
CANDIDATO = "CANDIDATO"

ROLES = {
    CIUDADANO: {
        "nombre": "Ciudadano",
        "descripcion": "Interactua de forma responsable con lo que recibe.",
        "habilidad": "Equilibrado: sin penalizaciones ni bonos.",
        "mult_verificar": 1.0,
        "mult_compartir": 1.0,
        "ve_tipo_real": False,
        "verificaciones": 3,
    },
    PERIODISTA: {
        "nombre": "Periodista",
        "descripcion": "Investiga y detecta noticias falsas.",
        "habilidad": "Al verificar descubre el tipo real de la publicacion "
                     "y su verificacion rinde un 50% mas.",
        "mult_verificar": 1.5,
        "mult_compartir": 1.0,
        "ve_tipo_real": True,
        "verificaciones": 5,
    },
    INFLUENCER: {
        "nombre": "Influencer",
        "descripcion": "Su alcance multiplica el efecto de lo que difunde.",
        "habilidad": "Compartir tiene el doble de impacto, para bien y para mal.",
        "mult_verificar": 1.0,
        "mult_compartir": 2.0,
        "ve_tipo_real": False,
        "verificaciones": 2,
    },
    CANDIDATO: {
        "nombre": "Candidato a alcalde",
        "descripcion": "Construye confianza y enfrenta los rumores.",
        "habilidad": "Gana mas reputacion al verificar, pero los rumores sin "
                     "responder le cuestan el doble.",
        "mult_verificar": 1.3,
        "mult_compartir": 1.2,
        "ve_tipo_real": False,
        "verificaciones": 3,
    },
}


class Jugador(object):

    def __init__(self, nombre, rol=CIUDADANO):
        self.nombre = nombre
        self.rol = rol
        self.puntos = 0
        self.reputacion = 50
        self.decisiones = 0
        self.aciertos = 0
        self.verificaciones = ROLES[rol]["verificaciones"]

    # ----- datos del rol -------------------------------------------------

    @property
    def perfil(self):
        return ROLES[self.rol]

    @property
    def nombre_rol(self):
        return self.perfil["nombre"]

    def multiplicador(self, accion):
        if accion == "VERIFICAR":
            return self.perfil["mult_verificar"]
        if accion == "COMPARTIR":
            return self.perfil["mult_compartir"]
        return 1.0

    def ve_tipo_real(self):
        return self.perfil["ve_tipo_real"]

    # ----- puntuacion ----------------------------------------------------

    def registrar(self, puntos, acierto):
        self.decisiones += 1
        if acierto:
            self.aciertos += 1
            self.reputacion = min(100, self.reputacion + 3)
        else:
            self.reputacion = max(0, self.reputacion - 4)
        self.puntos = max(0, self.puntos + puntos)

    def puede_verificar(self):
        return self.verificaciones > 0

    def gastar_verificacion(self):
        if self.verificaciones > 0:
            self.verificaciones -= 1
            return True
        return False

    def precision(self):
        if self.decisiones == 0:
            return 0
        return int(round(100.0 * self.aciertos / self.decisiones))
