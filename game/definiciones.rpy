## definiciones.rpy — imagenes, paleta y estilos propios de Alcalde Digital.

image bg ciudad = "images/bg_ciudad.png"
image bg red = "images/bg_red.png"

image avatar ciudadano = "images/rol_ciudadano.png"
image avatar periodista = "images/rol_periodista.png"
image avatar influencer = "images/rol_influencer.png"
image avatar candidato = "images/rol_candidato.png"

init python:
    ## La logica vive en Python puro (game/clases/). Aqui solo se importa
    ## lo que las pantallas necesitan para dibujar.
    from clases.jugador import ROLES, CIUDADANO, PERIODISTA, INFLUENCER, CANDIDATO
    from clases.ciudad import NOMBRES as NOMBRES_IND
    from clases.partida import Partida, TURNOS
    from clases.mapa import MapaCiudad, Viaje

    # Paleta unica del juego; se usa desde las pantallas.
    COL_FONDO   = "#0b1424"
    COL_PANEL   = "#13203acc"
    COL_BORDE   = "#27405f"
    COL_TEXTO   = "#e8eef7"
    COL_TENUE   = "#93a7c4"
    COL_CIAN    = "#38bdf8"
    COL_VERDE   = "#34d399"
    COL_AMBAR   = "#f59e0b"
    COL_ROJO    = "#ef4444"
    COL_VIOLETA = "#a78bfa"

    AVATARES = {
        "CIUDADANO": "avatar ciudadano",
        "PERIODISTA": "avatar periodista",
        "INFLUENCER": "avatar influencer",
        "CANDIDATO": "avatar candidato",
    }

    COLOR_ROL = {
        "CIUDADANO": "#2563a0",
        "PERIODISTA": "#107a6e",
        "INFLUENCER": "#9240ac",
        "CANDIDATO": "#b06212",
    }

    ETIQUETA_ACCION = {
        "VERIFICAR": "Verificar",
        "COMPARTIR": "Compartir",
        "REPORTAR": "Reportar",
        "IGNORAR": "Ignorar",
    }

    AYUDA_ACCION = {
        "VERIFICAR": "Contrasta la fuente antes de actuar. Revela si es verdadera o falsa. Tienes un numero limitado.",
        "COMPARTIR": "La difundes tal cual. Rapido, pero si era falsa multiplicas el dano.",
        "REPORTAR": "La marcas como problematica. Baja conflictos, pero reportar a ciegas tambien silencia.",
        "IGNORAR": "Sigues de largo. No es neutral: el contenido sigue circulando.",
    }

    def color_riesgo(valor):
        if valor >= 70:
            return COL_ROJO
        if valor >= 40:
            return COL_AMBAR
        return COL_VERDE

    def color_indicador(clave):
        return COL_ROJO if clave in ("desinformacion", "conflictos") else COL_CIAN


style panel_juego is frame:
    background Solid("#13203ae6")
    padding (28, 22)

style titulo_seccion is text:
    color "#38bdf8"
    size 26
    bold True

style texto_base is text:
    color "#e8eef7"
    size 28

style texto_tenue is text:
    color "#93a7c4"
    size 22

