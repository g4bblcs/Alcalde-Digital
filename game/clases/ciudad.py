# -*- coding: utf-8 -*-
"""Estado de Ciudad Nova: los seis indicadores del enunciado (seccion 10)."""

POSITIVOS = ("info_verificada", "confianza", "convivencia", "bienestar")
NEGATIVOS = ("desinformacion", "conflictos")

NOMBRES = {
    "info_verificada": "Informacion verificada",
    "confianza": "Confianza ciudadana",
    "convivencia": "Convivencia",
    "bienestar": "Bienestar digital",
    "desinformacion": "Desinformacion",
    "conflictos": "Conflictos",
}


class Ciudad(object):

    def __init__(self):
        self.info_verificada = 50
        self.confianza = 60
        self.convivencia = 70
        self.bienestar = 65
        self.desinformacion = 30
        self.conflictos = 20
        self.historial = []

    # ----- mutacion -----------------------------------------------------

    def aplicar(self, efecto, multiplicador=1.0):
        """Aplica un diccionario de deltas, saturando siempre en [0, 100]."""
        cambios = {}
        for indicador, delta in efecto.items():
            if not hasattr(self, indicador):
                continue
            real = int(round(delta * multiplicador))
            antes = getattr(self, indicador)
            despues = max(0, min(100, antes + real))
            setattr(self, indicador, despues)
            if despues != antes:
                cambios[indicador] = despues - antes
        self.historial.append(cambios)
        return cambios

    # ----- consultas ----------------------------------------------------

    def indicadores(self):
        return [(k, NOMBRES[k], getattr(self, k)) for k in POSITIVOS + NEGATIVOS]

    def salud(self):
        """Indice global 0-100 de la conversacion publica.

        Media ponderada de los indicadores positivos y de los negativos
        invertidos. El estado inicial da ~67: un punto de partida neutro,
        de modo que mantenerlo ya cuesta y empeorarlo es facil.
        """
        buenos = sum(getattr(self, k) for k in POSITIVOS) / float(len(POSITIVOS))
        malos = sum(getattr(self, k) for k in NEGATIVOS) / float(len(NEGATIVOS))
        return max(0, min(100, int(round(0.6 * buenos + 0.4 * (100 - malos)))))

    def en_crisis(self):
        return self.desinformacion >= 85 or self.convivencia <= 15

    def resultado_eleccion(self):
        """Seccion 12: el alcalde electo depende del estado final de la ciudad."""
        s = self.salud()
        if s >= 80:
            return ("Sofia Restrepo",
                    "Ciudad Nova voto informada. Gana la candidata que sostuvo "
                    "sus propuestas con datos verificables.")
        if s >= 62:
            return ("Marco Duarte",
                    "Una eleccion reñida. La ciudad llego dividida pero sin "
                    "que la desinformacion definiera el resultado.")
        if s >= 42:
            return ("Tomas Iriarte",
                    "El ruido pudo mas que las propuestas. Gana quien mejor "
                    "aprovecho la confusion.")
        return ("Lucas Vergara",
                "Ciudad Nova voto en medio del rumor y la desconfianza. "
                "El resultado refleja una conversacion publica rota.")
