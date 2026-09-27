## pantallas_juego.rpy — interfaz propia de Alcalde Digital.
## Estas pantallas solo dibujan: toda la logica vive en game/clases/*.py

################################################################
## Seleccion de rol
################################################################

screen seleccion_rol():
    tag menu
    add "bg red"

    vbox:
        align (0.5, 0.06)
        spacing 6
        text "ALCALDE DIGITAL" size 72 color COL_CIAN bold True xalign 0.5
        text "Ciudad Nova esta en campana. Elige tu rol en Civitas." style "texto_tenue" xalign 0.5

    hbox:
        align (0.5, 0.52)
        spacing 34
        for clave in ("CIUDADANO", "PERIODISTA", "INFLUENCER", "CANDIDATO"):
            $ perfil = ROLES[clave]
            button:
                action Return(clave)
                xysize (380, 560)
                background Frame(Solid("#13203acc"), 12, 12)
                hover_background Frame(Solid(COLOR_ROL[clave] + "cc"), 12, 12)
                vbox:
                    align (0.5, 0.5)
                    spacing 14
                    add AVATARES[clave] zoom 0.42 xalign 0.5
                    fixed:
                        xysize (340, 92)
                        text perfil["nombre"] size 34 color COL_TEXTO bold True align (0.5, 0.0) text_align 0.5 xsize 330
                    text perfil["descripcion"] style "texto_tenue" xalign 0.5 text_align 0.5 size 20
                    null height 6
                    text perfil["habilidad"] size 19 color COL_CIAN xalign 0.5 text_align 0.5
                    null height 4
                    text "Verificaciones: [perfil['verificaciones']]" size 20 color COL_AMBAR xalign 0.5

    text "Cada rol cambia el efecto de tus decisiones y cuantas veces puedes verificar" style "texto_tenue" align (0.5, 0.94) size 20


################################################################
## Indicadores de la ciudad (seccion 10 del enunciado)
################################################################

screen hud_indicadores():
    frame:
        style "panel_juego"
        align (0.5, 0.0)
        xsize 1860
        hbox:
            spacing 18
            vbox:
                yalign 0.5
                text "CIUDAD NOVA" style "titulo_seccion"
                text "Salud publica: [partida.ciudad.salud()]" size 30 color COL_TEXTO bold True
            null width 10
            for clave, nombre, valor in partida.ciudad.indicadores():
                vbox:
                    spacing 5
                    yalign 0.5
                    text nombre size 17 color COL_TENUE
                    hbox:
                        spacing 8
                        frame:
                            xysize (162, 16)
                            background Solid("#00000066")
                            padding (0, 0)
                            add Solid(color_indicador(clave)) xysize (max(2, int(162 * valor / 100.0)), 16)
                        text "[valor]" size 20 color COL_TEXTO bold True


################################################################
## Panel del jugador (personaje, puntuacion, estado)
################################################################

screen panel_jugador():
    frame:
        style "panel_juego"
        xpos 30
        ypos 150
        xsize 380
        vbox:
            spacing 10
            add AVATARES[partida.jugador.rol] zoom 0.36 xalign 0.5
            text partida.jugador.nombre size 34 color COL_TEXTO bold True xalign 0.5
            text partida.jugador.nombre_rol size 24 color COL_CIAN xalign 0.5
            null height 8
            add Solid(COL_BORDE) xysize (324, 2)
            null height 8
            hbox:
                text "Puntos" style "texto_tenue"
                null width 1 xfill True
                text "[partida.jugador.puntos]" style "texto_base" bold True
            hbox:
                text "Reputacion" style "texto_tenue"
                null width 1 xfill True
                text "[partida.jugador.reputacion]" style "texto_base" bold True
            hbox:
                text "Precision" style "texto_tenue"
                null width 1 xfill True
                text "[partida.jugador.precision()]%" style "texto_base" bold True
            null height 6
            hbox:
                text "Verificaciones" style "texto_tenue"
                null width 1 xfill True
                text "[partida.jugador.verificaciones]" size 28 color COL_AMBAR bold True
            null height 10
            add Solid(COL_BORDE) xysize (324, 2)
            null height 8
            text "Turno [partida.turno] de 8" style "texto_tenue" xalign 0.5
            text "Publicaciones vivas: [len(partida.arbol)]" style "texto_tenue" xalign 0.5


################################################################
## Tarjeta de la publicacion actual
################################################################

screen tarjeta_publicacion(pub):
    frame:
        style "panel_juego"
        xpos 450
        ypos 150
        xsize 1440
        vbox:
            spacing 14
            hbox:
                spacing 14
                text "CIVITAS" style "titulo_seccion" yalign 0.5
                null width 1 xfill True
                frame:
                    background Solid(color_riesgo(pub.nivel_riesgo) + "33")
                    padding (14, 6)
                    text "Riesgo [pub.nivel_riesgo] · [pub.etiqueta_riesgo()]" size 22 color color_riesgo(pub.nivel_riesgo) bold True
            add Solid(COL_BORDE) xysize (1384, 2)
            text "@[pub.autor]" size 24 color COL_VIOLETA
            text pub.texto size 40 color COL_TEXTO
            null height 4
            if pub.verificada:
                text "Verificada: esta publicacion es [pub.tipo]" size 26 color COL_VERDE bold True
            else:
                text "Sin verificar: no sabes si es verdadera, falsa, un rumor o una opinion." style "texto_tenue"


################################################################
## Pantalla principal de juego. Devuelve la accion elegida.
################################################################

screen pantalla_juego(pub):
    use hud_indicadores
    use panel_jugador
    use tarjeta_publicacion(pub)

    hbox:
        xpos 450
        ypos 500
        spacing 18
        for etiqueta in partida.opciones():
            button:
                action Return(etiqueta)
                xysize (340, 150)
                background Frame(Solid("#1b2d4de6"), 10, 10)
                hover_background Frame(Solid(COL_CIAN + "40"), 10, 10)
                vbox:
                    align (0.5, 0.5)
                    spacing 6
                    text ETIQUETA_ACCION[etiqueta] size 32 color COL_TEXTO bold True xalign 0.5
                    text AYUDA_ACCION[etiqueta] size 16 color COL_TENUE xalign 0.5 text_align 0.5 xsize 300

    if "VERIFICAR" not in partida.opciones():
        text "Te quedaste sin verificaciones: ahora decides a ciegas." size 22 color COL_AMBAR xpos 450 ypos 670

    hbox:
        xpos 450
        ypos 706
        spacing 16
        for _txt, _acc in (("Ver el arbol AVL", Show("visor_arbol")),
                           ("Ayuda", Show("pantalla_ayuda"))):
            button:
                action _acc
                xysize (260, 60)
                background Frame(Solid("#13203ae6"), 8, 8)
                hover_background Frame(Solid(COL_CIAN + "40"), 8, 8)
                text _txt size 24 color COL_TEXTO align (0.5, 0.5)


################################################################
## Consecuencias de la accion (retroalimentacion, seccion 11)
################################################################

screen panel_resultado(res):
    modal True
    add Solid("#040810f2")
    frame:
        style "panel_juego"
        align (0.5, 0.5)
        xsize 1200
        vbox:
            spacing 16
            hbox:
                spacing 14
                if res["acierto"]:
                    text "DECISION RESPONSABLE" size 34 color COL_VERDE bold True
                else:
                    text "DECISION CON COSTE" size 34 color COL_ROJO bold True
                null width 1 xfill True
                text "[res['puntos']] pts" size 34 color (COL_VERDE if res["puntos"] >= 0 else COL_ROJO) bold True
            add Solid(COL_BORDE) xysize (1144, 2)
            text "Camino en el arbol de decisiones: [' -> '.join(res['camino'])]" size 22 color COL_CIAN
            text "La publicacion era: [res['tipo_real']]" size 26 color COL_TEXTO
            null height 6
            text res["titulo"] size 32 color COL_TEXTO bold True
            text res["mensaje"] style "texto_tenue" size 24
            null height 10
            text "Efecto sobre Ciudad Nova" style "titulo_seccion"
            if res["cambios"]:
                hbox:
                    spacing 26
                    for clave, delta in res["cambios"].items():
                        vbox:
                            text NOMBRES_IND[clave] size 18 color COL_TENUE
                            text ("+" if delta > 0 else "") + str(delta) size 30 bold True color (COL_VERDE if (delta > 0) == (clave not in ("desinformacion", "conflictos")) else COL_ROJO)
            else:
                text "Sin cambios medibles en los indicadores." style "texto_tenue"
            null height 14
            textbutton "Continuar" action Return(True) xalign 1.0


################################################################
## Visor del arbol AVL (operaciones y recorridos)
################################################################

screen visor_arbol():
    modal True
    add Solid("#050a14")

    $ nodos, aristas = partida.arbol.disposicion()
    $ ESP_X = 104
    $ ESP_Y = 108
    $ OY = 150
    $ _ancho = (max([n["x"] for n in nodos]) if nodos else 0) * ESP_X
    $ OX = max(80, (1920 - _ancho) // 2)
    $ R = 34

    text "ARBOL AVL — clasificacion del feed por nivel de riesgo" style "titulo_seccion" xpos 60 ypos 40 size 32
    text "Clave: (riesgo, id). Recorrer en inorden da el feed de menor a mayor peligro." style "texto_tenue" xpos 60 ypos 84

    ## aristas: conectores ortogonales (vertical, horizontal, vertical)
    for padre, hijo in aristas:
        $ px = OX + nodos[padre]["x"] * ESP_X
        $ py = OY + nodos[padre]["y"] * ESP_Y
        $ hx = OX + nodos[hijo]["x"] * ESP_X
        $ hy = OY + nodos[hijo]["y"] * ESP_Y
        $ medio = py + (ESP_Y // 2)
        add Solid(COL_BORDE) xysize (3, medio - py) xpos px ypos py
        add Solid(COL_BORDE) xysize (abs(hx - px) + 3, 3) xpos min(px, hx) ypos medio
        add Solid(COL_BORDE) xysize (3, hy - medio) xpos hx ypos medio

    ## nodos
    for n in nodos:
        $ nx = OX + n["x"] * ESP_X
        $ ny = OY + n["y"] * ESP_Y
        frame:
            xpos nx - R
            ypos ny - R + 6
            xysize (R * 2, R * 2)
            padding (0, 0)
            background Frame(Solid(color_riesgo(n["riesgo"])), 4, 4)
            vbox:
                align (0.5, 0.5)
                text str(n["riesgo"]) size 26 color "#08111f" bold True xalign 0.5
                text "FE {:+d}".format(n["fe"]) size 14 color "#08111f" xalign 0.5

    frame:
        style "panel_juego"
        xpos 60
        ypos 640
        xsize 1800
        vbox:
            spacing 8
            hbox:
                spacing 40
                text "Nodos: [partida.arbol.contar_nodos()]" style "texto_base"
                text "Altura: [partida.arbol.altura(partida.arbol.raiz)]" style "texto_base"
                text "FE raiz: [partida.arbol.factor_equilibrio(partida.arbol.raiz)]" style "texto_base"
                text ("Balanceado: SI" if partida.arbol.esta_balanceado() else "Balanceado: NO") style "texto_base" color (COL_VERDE if partida.arbol.esta_balanceado() else COL_ROJO)
            add Solid(COL_BORDE) xysize (1744, 2)
            text "Preorden   [' · '.join(str(p.nivel_riesgo) for p in partida.arbol.preorden())]" size 22 color COL_TENUE
            text "Inorden    [' · '.join(str(p.nivel_riesgo) for p in partida.arbol.inorden())]" size 22 color COL_CIAN
            text "Posorden   [' · '.join(str(p.nivel_riesgo) for p in partida.arbol.posorden())]" size 22 color COL_TENUE
            text "Niveles    [' | '.join(' '.join(str(x.clave[0]) for x in fila) for fila in partida.arbol.por_niveles())]" size 22 color COL_TENUE

    textbutton "Cerrar" action Hide("visor_arbol") align (0.97, 0.96)


################################################################
## Ayuda (seccion 16 del enunciado)
################################################################

screen pantalla_ayuda():
    modal True
    add Solid("#050a14")
    frame:
        style "panel_juego"
        align (0.5, 0.5)
        xsize 1500
        ysize 900
        viewport:
            scrollbars "vertical"
            mousewheel True
            vbox:
                spacing 12
                xsize 1400
                text "AYUDA" style "titulo_seccion" size 40
                text "Objetivo" style "titulo_seccion"
                text "Ciudad Nova elige alcalde. Tu trabajo no es ganar votos, sino que la ciudad llegue a las urnas con informacion verificada, confianza y convivencia altas, y con desinformacion y conflictos bajos." style "texto_base"
                text "Como se gana" style "titulo_seccion"
                text "Al terminar los 8 turnos se calcula la salud de la conversacion publica. Cuanto mas alta, mejor el alcalde que sale electo. Verificar antes de actuar es la via mas fiable, pero tus verificaciones son limitadas: gastalas en lo que mas riesgo tiene." style "texto_base"
                text "Los botones" style "titulo_seccion"
                for k in ("VERIFICAR", "COMPARTIR", "REPORTAR", "IGNORAR"):
                    text "[ETIQUETA_ACCION[k]]: [AYUDA_ACCION[k]]" style "texto_base" size 24
                text "Los indicadores" style "titulo_seccion"
                text "Informacion verificada, Confianza, Convivencia y Bienestar suman a la salud de la ciudad. Desinformacion y Conflictos restan. Cada accion los mueve segun el impacto de la publicacion y la habilidad de tu rol." style "texto_base"
                text "Los roles" style "titulo_seccion"
                for k in ("CIUDADANO", "PERIODISTA", "INFLUENCER", "CANDIDATO"):
                    text "[ROLES[k]['nombre']]: [ROLES[k]['habilidad']]" style "texto_base" size 24
                text "Accesibilidad" style "titulo_seccion"
                text "El nivel de riesgo nunca se comunica solo con color: cada publicacion muestra siempre el numero y la etiqueta ALTO, MEDIO o BAJO, de modo que el juego es legible sin distinguir rojo de verde." style "texto_base"
        textbutton "Cerrar" action Hide("pantalla_ayuda") align (0.98, 0.99)


################################################################
## Cierre de partida: eleccion del alcalde (seccion 12)
################################################################

screen pantalla_final(final):
    modal True
    add "bg ciudad"
    add Solid("#050a14cc")

    vbox:
        align (0.5, 0.5)
        spacing 18
        xsize 1300

        text "RESULTADO DE LA ELECCION" style "titulo_seccion" size 34 xalign 0.5
        text final["alcalde"] size 76 color COL_CIAN bold True xalign 0.5
        text "alcalde electo de Ciudad Nova" style "texto_tenue" xalign 0.5
        null height 10
        text final["relato"] style "texto_base" size 28 xalign 0.5 text_align 0.5 xsize 1200
        null height 20

        frame:
            style "panel_juego"
            xalign 0.5
            hbox:
                spacing 70
                for etiqueta, valor, sufijo in (
                        ("Salud de la ciudad", final["salud"], ""),
                        ("Puntos", final["puntos"], ""),
                        ("Reputacion", final["reputacion"], ""),
                        ("Precision", final["precision"], "%")):
                    vbox:
                        text etiqueta size 20 color COL_TENUE xalign 0.5
                        text "[valor][sufijo]" size 44 color COL_TEXTO bold True xalign 0.5

        null height 16
        hbox:
            xalign 0.5
            spacing 20
            textbutton "Ver el arbol final" action Show("visor_arbol")
            textbutton "Volver al menu" action Return(True)
