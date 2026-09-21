init python:
    from clases.Publicacion import SesionPublicacion, BancoPublicaciones, armar_publicacion

label nueva_publicacion:
    if not banco.hay_mas():
        return

    $ sesion = SesionPublicacion(banco.siguiente())

    "📱 Recibiste una publicación nueva en Civitas."
    "[sesion.publicacion.autor]: [sesion.publicacion.contenido]"
    "[sesion.actual.texto]"

    while not sesion.terminada():
        $ eleccion = renpy.display_menu(sesion.opciones())
        $ sesion.elegir(eleccion)
        "[sesion.actual.texto]"

    $ aplicar_consecuencia(sesion.actual.consecuencia)
    return
init python:
    def aplicar_consecuencia(consecuencia):
            if not consecuencia:
                return
            for clave, valor in consecuencia.items():
                store.stats[clave] = store.stats.get(clave, 0) + valor

# personajes

define inf = Character("Influencer")
define  may = Character("Candidato a Alcalde")
define inv = Character("Investigador")
define ci = Character("Civil")

# Publicaciones

default banco = BancoPublicaciones([
    armar_publicacion(
        "@sol.y.limon", "Escuché que el alcalde robó fondos publicos para comprar su casa", True,
        "¿Cómo respondes?",
        {"etiqueta": "Desmentir con datos", "texto": "La gente te cree.","efecto": {"reputacion": 10}},
        {"etiqueta": "Ignorarlo", "texto": "El rumor crece.","efecto": {"reputacion": -10}},
    ), 
    armar_publicacion(
        "@ciudadano", "El candidato a alcalde ha sido acusado de corrupción.", True, "¿Qué haces?",
        {"etiqueta": "Investigar y publicar evidencia", "texto": "La gente te respalda.","efecto": {"reputacion": 15}},
        {"etiqueta": "Difundir el rumor sin verificar", "texto": "El rumor se propaga.","efecto": {"reputacion": -15}},
    ),
    
])

#stats iniciales

default stats = {"reputacion": 50, "desinformacion": 0}

