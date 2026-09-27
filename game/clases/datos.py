# -*- coding: utf-8 -*-
"""Contenido inicial de Civitas y publicaciones de eventos aleatorios."""

from clases.publicacion import Publicacion, VERDADERA, FALSA, RUMOR, OPINION

# (id, texto, autor, tipo, riesgo, impacto)
_INICIALES = [
    (1, "Manana se realizara una campana de reciclaje en el parque central.",
     "CanalNovaNoticias", VERDADERA, 10, 3),
    (2, "Se confirmo la apertura de un nuevo hospital en el sector sur.",
     "AlcaldiaOficial", VERDADERA, 15, 5),
    (3, "La candidata Sofia propone mas zonas verdes para la ciudad.",
     "CampaniaSofia2026", OPINION, 22, 4),
    (4, "Los vecinos del barrio este piden mas iluminacion en las calles.",
     "VecinosBarrioEste", OPINION, 30, 4),
    (5, "Se detecto un brote de gripe en las escuelas de Ciudad Nova.",
     "SaludNovaOficial", VERDADERA, 42, 6),
    (6, "El candidato Lucas planea privatizar el acueducto municipal.",
     "CuentaAnonima55", RUMOR, 55, 7),
    (7, "Manana cerraran todos los parques de Ciudad Nova.",
     "UsuarioDesconocido", RUMOR, 62, 7),
    (8, "El candidato Marco quiere cerrar el colegio del barrio norte.",
     "UsuarioCivitas1", RUMOR, 75, 8),
    (9, "El candidato Tomas tiene vinculos con organizaciones criminales.",
     "BlogPolitico", FALSA, 86, 9),
    (10, "El alcalde actual esta robando dinero del presupuesto municipal.",
     "CuentaAnonima99", FALSA, 92, 10),
]

# Publicaciones que entran en plena partida por eventos aleatorios.
_EVENTOS = [
    (101, "URGENTE: se cae el sistema de votacion de Ciudad Nova.",
     "AlertaNova", FALSA, 88, 9),
    (102, "Un video muestra a un candidato agrediendo a un periodista.",
     "ViralCivitas", FALSA, 79, 8),
    (103, "La alcaldia habilita puntos de informacion electoral verificada.",
     "AlcaldiaOficial", VERDADERA, 12, 4),
    (104, "Dicen que van a subir el pasaje del bus despues de elecciones.",
     "VecinoPreocupado", RUMOR, 48, 5),
    (105, "Campana ciudadana por una conversacion digital mas sana.",
     "ColectivoNova", VERDADERA, 8, 3),
    (106, "Aseguran que los votos del barrio sur no seran contados.",
     "CuentaAnonima77", FALSA, 94, 10),
]


def _construir(filas):
    return [Publicacion(*fila) for fila in filas]


def publicaciones_iniciales():
    return _construir(_INICIALES)


def publicaciones_evento():
    return _construir(_EVENTOS)
