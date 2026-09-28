## Mapa independiente de Ciudad Nova.

init python:
    def mapa_actualizar(viaje):
        viaje.avanzar(0.05)
        renpy.restart_interaction()

    def mapa_iniciar(viaje, destino):
        viaje.iniciar(destino)


screen mapa_ciudad(viaje):
    modal True
    tag mapa

    add "images/mapa/mapa_1.png" xysize (1920, 1080)

    for identificador, ubicacion in viaje.mapa.ubicaciones.items():
        $ px = int(ubicacion.posicion[0] * 1920)
        $ py = int(ubicacion.posicion[1] * 1080)
        button:
            xpos px
            ypos py
            xanchor 0.5
            yanchor 0.5
            xpadding 12
            ypadding 8
            action Function(mapa_iniciar, viaje, identificador)
            sensitive viaje.estado != "VIAJANDO"
            background Frame(Solid("#101b2ddd"), 8, 8)
            hover_background Frame(Solid("#38bdf0ee"), 8, 8)
            text ubicacion.nombre size 20 color "#ffffff"

    add viaje.sprite_path():
        xpos int(viaje.posicion[0] * 1920)
        ypos int(viaje.posicion[1] * 1080)
        xanchor 0.5
        yanchor 0.5
        zoom 0.30

    frame:
        xpos 36
        ypos 30
        xsize 420
        padding (20, 16)
        background Frame(Solid("#07111ddd"), 12, 12)
        vbox:
            spacing 6
            text "CIUDAD NOVA" size 30 color "#ffffff" bold True
            if viaje.estado == "VIAJANDO":
                text "En ruta hacia [viaje.mapa.obtener(viaje.destino).nombre]" size 22 color "#9de7ff"
            elif viaje.estado == "LLEGADA":
                text "Llegaste a [viaje.mapa.obtener(viaje.destino).nombre]" size 22 color "#8ff0b0"
            else:
                text "Selecciona un destino" size 22 color "#d6deea"

    if viaje.estado == "VIAJANDO":
        textbutton "Cancelar viaje":
            xpos 36
            ypos 180
            action Function(viaje.cancelar)
    elif viaje.estado == "LLEGADA":
        textbutton "Continuar":
            xpos 36
            ypos 180
            action Return(viaje.destino)

    if viaje.estado == "VIAJANDO":
        timer 0.05 action Function(mapa_actualizar, viaje) repeat True