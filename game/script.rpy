## script.rpy — flujo de Alcalde Digital (Entrega 1).
## La logica no vive aqui: este archivo solo encadena pantallas.

define narrador = Character(None, what_color="#e8eef7")
define civitas = Character("Civitas", color="#38bdf8")

default partida = None
default mapa_nova = MapaCiudad()


label start:

    scene bg red with fade

    narrador "Ciudad Nova esta a pocos dias de elegir alcalde."

    narrador "Cuatro candidatos compiten por el cargo y toda la campana pasa por {b}Civitas{/b}, la red social de la ciudad."

    civitas "Aqui circulan noticias verdaderas, opiniones... y tambien rumores y mentiras que se propagan mas rapido que los hechos."

    narrador "Cada publicacion que llega a tu feed trae un {b}nivel de riesgo{/b}: cuanto dano puede causar si se difunde sin comprobar."

    narrador "Tu decides que hacer con cada una. La ciudad recordara todas tus decisiones el dia de la eleccion."

    call screen seleccion_rol

    $ partida = Partida("Tu", _return)

    scene bg ciudad with dissolve

    $ viaje_ciudad = Viaje(mapa_nova, "centro")
    call screen mapa_ciudad(viaje_ciudad)

    narrador "Juegas como {b}[partida.jugador.nombre_rol]{/b}. [partida.jugador.perfil['habilidad']]"

    narrador "El feed esta ordenado en un arbol AVL por nivel de riesgo. Siempre enfrentaras primero lo mas peligroso que circula ahora mismo."

    jump turno


label turno:

    if not partida.hay_turnos():
        jump eleccion

    $ _pub = partida.siguiente_publicacion()

    if _pub is None:
        jump eleccion

    call screen pantalla_juego(_pub)

    $ _resultado = partida.decidir(_return)

    if _resultado is None:
        jump turno

    call screen panel_resultado(_resultado)

    jump turno


label eleccion:

    $ _final = partida.resultado_final()

    scene bg ciudad with fade

    narrador "Llega el dia de la eleccion. Ciudad Nova acude a las urnas con la conversacion publica que ustedes dejaron."

    call screen pantalla_final(_final)

    return
